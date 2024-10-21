from aiogram import F, types, Router
from aiogram.filters import CommandStart, Command, or_f
from aiogram.utils.formatting import (
    as_list,
    as_marked_section,
    Bold,
)
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import orm_add_product, orm_get_products
from filters.chat_types import ChatTypeFilter
from handlers.admin_private import admin_router
from kbds.inline import get_inlineMix_btns

from kbds.reply import get_keyboard

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(["private"]))


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
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