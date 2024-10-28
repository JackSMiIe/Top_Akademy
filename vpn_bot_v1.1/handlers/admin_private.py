from aiogram import Router,types,F
from aiogram.filters import Command, or_f, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup,State

from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import orm_add_product, orm_get_products, orm_delete_product
from filters.chat_types import ChatTypeFilter, IsAdmin
from kbds.inline import get_inlineMix_btns
from kbds.reply import get_keyboard
ADMIN_KB = get_keyboard(
    "Добавить товар",
    "Ассортимент",
    placeholder="Выберите действие",
    sizes=(2,),
)

admin_router = Router()
admin_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())


@admin_router.message(Command("admin"))
async def admin_features(message: types.Message):
    await message.answer("Что хотите сделать?", reply_markup=ADMIN_KB)

@admin_router.message(F.text.lower() == 'ассортимент')
async def menu_cmd(message: types.Message,session: AsyncSession):
    for product in await orm_get_products(session):
        await message.answer(
            f'<strong>{product.name}</strong>\n'
            f'Цена: {product.price} руб.',
        reply_markup=get_inlineMix_btns(btns={
            'Удалить': f'delete_{product.id}',
            'Изменить': f'change_{product.id}'
        })
        )
    await message.answer('Ок, актуальный прайс ⬆️')

@admin_router.callback_query(F.data.startswith('delete_'))
async def delete_product(callback: types.CallbackQuery,session: AsyncSession):
    product_id = callback.data.split('_')[-1]
    await orm_delete_product(session,int(product_id))
    await callback.answer('Товар удален')
    await callback.message.answer('Товар удален')


@admin_router.message(or_f(Command("change"), (F.text.lower() == 'изменить товар')))
async def change_price(message: types.Message):
    await message.answer('Что будем менять?')
# FSM

class AddProduct(StatesGroup):
    name = State()
    #days_count = State()
    price = State()

    texts = {
        "AddProduct:name": "Введите название заново:",
        "AddProduct:price": "Этот стейт последний, поэтому...",
    }

@admin_router.message(StateFilter(None),F.text.lower() == 'добавить товар')
async def admin_add(message: types.Message,state: FSMContext):
    await message.answer('Введите название:', reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(AddProduct.name)

# Команда отмена
@admin_router.message(StateFilter('*'),Command('отмена')) # * любое состояние
@admin_router.message(StateFilter('*'),F.text.casefold() == 'отмена')
async def cancel_handler(message: types.Message,state: FSMContext):
    current_state = await state.get_state() # Проверка текущего состояние, если нет активного диалога-завешаем
    if current_state is None:
        return
    await state.clear() # Убираем все состояния
    await message.answer('Действия отменены', reply_markup=ADMIN_KB)

# Команда назад
# Вернутся на шаг назад (на прошлое состояние)
@admin_router.message(StateFilter("*"), Command("назад"))
@admin_router.message(StateFilter("*"), F.text.casefold() == "назад")
async def back_step_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()

    if current_state == AddProduct.name:
        await message.answer(
            'Предидущего шага нет, или введите название товара или напишите "отмена"'
        )
        return
# Смена состояния
    previous = None
    for step in AddProduct.__all_states__: # Все стейты
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(
                f"Ок, вы вернулись к прошлому шагу \n {AddProduct.texts[previous.state]}"
            )
            return
        previous = step

@admin_router.message(AddProduct.name,F.text)
async def add_name(message: types.Message,state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Введите стоимость:')
    await state.set_state(AddProduct.price)

@admin_router.message(AddProduct.name)
async def add_name(message: types.Message,state: FSMContext):
    await message.answer('Вы ввели недопустимые данные, введите текст!')


@admin_router.message(AddProduct.price,F.text)
async def ann_description(message: types.Message,state: FSMContext,session: AsyncSession):
    await state.update_data(price=message.text)
    data = await state.get_data()
    try:
        await orm_add_product(session,data)
        await message.answer('Товар добавлен', reply_markup=ADMIN_KB)
        await state.clear()
    except Exception as e:
        await message.answer(f'Ошибка {e} обратитесь в поддержку')
        await state.clear()

@admin_router.message(AddProduct.price)
async def ann_description(message: types.Message,state: FSMContext):
    await message.answer('Вы ввели недопустимые данные, цену!')

@admin_router.message(or_f(Command('dell'), (F.text.lower() == 'удалить товар')))
async def change_price(message: types.Message,state: FSMContext):
    await message.answer('Что удалить?')

@admin_router.message(F.text.lower() == 'отмена')
async def admin_features(message: types.Message,state: FSMContext):
    await message.answer('отмена')

@admin_router.message(F.text.lower() == 'выход')
async def admin_features(message: types.Message,state: FSMContext):
    await message.answer('выход')