import logging,asyncio
import os

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import FSInputFile
from sqlalchemy.exc import SQLAlchemyError
from bot_instance import bot
from aiogram import F, types, Router
from aiogram.filters import CommandStart, Command, or_f, StateFilter
from aiogram.utils.formatting import (
    as_list,
    as_marked_section,
    Bold,
)
from dotenv import load_dotenv, find_dotenv
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Product
from database.orm_query import orm_add_product, orm_get_products
from filters.chat_types import ChatTypeFilter
from kbds.inline import get_inlineMix_btns
from kbds.reply import get_keyboard

load_dotenv(find_dotenv())
user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(["private"]))


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    print(message.from_user.id)
    await message.answer(
        f"<b>{message.from_user.first_name}</b>\nДобро пожаловать в наш VPN бот!\nВыберите действие:",parse_mode='HTML',
        reply_markup=get_keyboard(
            "Варианты подписки",
            "Способы оплаты",
            "О сервере",
            "Инструкции",
            placeholder="Что вас интересует?",
            sizes=(2, 2)
        ),
    )

@user_private_router.message(or_f(Command("subscription_plans"), (F.text.lower() == "варианты подписки")))
async def menu_cmd(message: types.Message,session: AsyncSession):
    for product in await orm_get_products(session):
        await message.answer(
            f'<strong>{product.name}</strong>\n'
            f'Цена: {product.price} руб.',
        reply_markup=get_inlineMix_btns(btns={
            'Купить': f'pay_{product.id}',
            'Подробнее': f'change_{product.id}'
        })
        )


@user_private_router.message(F.text.lower() == "о сервере")
@user_private_router.message(Command("about"))
async def about_cmd(message: types.Message):
    await message.answer("<b>Сервер</b>, расположенный в Нидерландах, "
                         "предлагает высокую скорость соединения и "
                         "минимальные задержки для пользователей", parse_mode="HTML")

@user_private_router.message(F.text.lower() == "способы оплаты")
@user_private_router.message(Command("payment"))
async def payment_cmd(message: types.Message):
    text = as_marked_section(
        Bold("Способы оплаты:"),
        "Картой в боте",
        "При получении карта/кеш",
        "В заведении",
        marker="✅ ",
    )
    await message.answer(text.as_html())


@user_private_router.message(F.text.lower() == "инструкции")
@user_private_router.message(Command("inst"))
async def about_cmd(message: types.Message):
    await message.answer("<b>Здесь будет описание:</b>", parse_mode="HTML")


"""-----------------------------------------------------------------"""


class PaymentStates(StatesGroup):
    waiting_for_payment = State()        # Начало оплаты
    waiting_for_payment_2 = State()      # Ожидание подтверждения оплаты
    payment_successful = State()         # Состояние успешной оплаты
    generating_qr_and_config = State()   # Создание конфиг клиента
    sending_qr_and_config = State()      # Отправка конфиг и QR
    saving_client_info = State()         # Сохранение клиента в БД
    error_handling = State()             # Непредвиденная ошибка

# Обработчик для кнопки оплаты FSM
@user_private_router.callback_query(F.data.startswith('pay_'))
async def pay(callback: types.CallbackQuery, session: AsyncSession, state: FSMContext):
    # Проверка состояния для правильного начала процесса оплаты
    current_state = await state.get_state()
    if current_state not in [None, PaymentStates.payment_successful]:
        await callback.answer("Вы уже находитесь в процессе оплаты.", show_alert=True)
        return
    try:
        # Извлекаем ID продукта из данных коллбэка
        product_id = int(callback.data.split('_')[1])

        # Получаем продукт из базы данных по его ID
        query = select(Product).where(Product.id == product_id)
        result = await session.execute(query)
        product = result.scalar()

        if product:
            # Устанавливаем состояние ожидания оплаты
            await state.set_state(PaymentStates.waiting_for_payment)
            # Отправляем счет на оплату
            await bot.send_invoice(
                chat_id=callback.from_user.id,
                title="Оплата подписки",
                description=f"Тариф {product.name}",
                payload=f"wtf_{product_id}",
                provider_token=os.getenv('TOKEN_CASH'),
                currency='RUB',
                prices=[types.LabeledPrice(label=product.name, amount=int(product.price * 100))]
            )
        else:
            await callback.answer("Продукт не найден", show_alert=True)
    except SQLAlchemyError as e:
        logging.error(f"Ошибка при запросе к базе данных: {str(e)}")
        await callback.answer("Ошибка базы данных", show_alert=True)
        await session.rollback()
    except Exception as e:
        logging.error(f"Неизвестная ошибка: {str(e)}")
        await callback.answer(f"Ошибка: {str(e)}", show_alert=True)
        await session.rollback()
    else:
        await session.commit()

# Обработчик для предварительной проверки платежа
@user_private_router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state == PaymentStates.waiting_for_payment:
        await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
        # Переключаемся на следующее состояние ожидания подтверждения платежа
        await state.set_state(PaymentStates.waiting_for_payment_2)
    else:
        await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=False,error_message="Ошибка: платеж не может быть обработан в текущем состоянии."
        )

# Обработчик успешной оплаты
@user_private_router.message(F.successful_payment)
async def process_pay(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == PaymentStates.waiting_for_payment_2 and message.successful_payment:
        if message.successful_payment.invoice_payload.startswith('wtf'):
            # Выводим сообщение после успешной оплаты
            await bot.send_message(message.from_user.id, 'Оплата прошла успешно! Спасибо.')
            # Устанавливаем состояние как успешная оплата
            await state.set_state(PaymentStates.payment_successful) # Состояние оплата успешна
            await generate_and_send_qr(message, state)
"""Закончил тут"""

async def generate_and_send_qr(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == PaymentStates.payment_successful:
        user_id = message.from_user.id
        username = f"user_{user_id}"
        qr_path = f"/home/jacksmile/PycharmProjects/vpn_bot_v1.1/users_configs/qr_png/qr_{user_id}.png"
        config_path = f"/home/jacksmile/configs/{username}.conf"

        try:
            # Асинхронное добавление нового пользователя с помощью команды pivpn
            process = await asyncio.create_subprocess_exec(
                "sudo", "-S", "/usr/local/bin/pivpn", "-a", "-n", username,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate(input=b'\n')
            if process.returncode != 0:
                await message.answer(f"Ошибка при добавлении пользователя: {stderr.decode()}")
                return

            # Асинхронное создание QR-кода из конфигурационного файла
            process = await asyncio.create_subprocess_exec(
                "sudo", "-S", "qrencode", "-o", qr_path, "-r", config_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            if process.returncode != 0:
                await message.answer(f"Ошибка при создании QR-кода: {stderr.decode()}")
                return

            # Отправка QR-кода пользователю


            # photo = FSInputFile(qr_path)
            # await bot.send_photo(chat_id=message.chat.id, photo=photo)
            document = FSInputFile(config_path)
            await bot.send_document(chat_id=message.chat.id,document=document)
            await message.answer(
                f"<strong>{message.from_user.first_name}</strong>, ваш конфиг файл успешно сгенерирован.",
                reply_markup=get_inlineMix_btns(btns={"Показать QR": f"qr_{user_id}"})
            )
            await state.clear()


        except Exception as e:
            await message.answer(f"Произошла неизвестная ошибка: {e}")
            await state.clear()


@user_private_router.callback_query(F.data.startswith('qr_'))
async def send_qr(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    qr_path = f"/home/jacksmile/PycharmProjects/vpn_bot_v1.1/users_configs/qr_png/qr_{user_id}.png"

    try:
        # Отправка QR-кода
        photo = FSInputFile(qr_path)
        await callback.message.answer_photo(photo=photo)
    except Exception as e:
        await callback.message.answer(f"Ошибка при отправке QR-кода: {e}")






#     # Извлекаем ID продукта из данных коллбэка, например: 'pay_123' -> product_id = 123
#     product_id = int(callback.data.split('_')[1])
#
#     # Запрашиваем продукт из базы данных по ID
#     query = select(Product).where(Product.id == product_id)
#     result = await session.execute(query)
#     product = result.scalar()
#     if product:
#         price = int(product.price*100)
#         print(price)