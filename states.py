from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from service import *
from keybords import *
from aiogram.types import CallbackQuery


router = Router()





class AddBook(StatesGroup):
    get_title = State()
    get_caption = State()
    get_author_id = State()
    get_category_id = State()
    get_pablisher = State()
    
   

class AddCategory(StatesGroup):
    get_title = State()

    

class AddAuthor(StatesGroup):
    get_name = State()
    get_country = State()

    
    
@router.message(F.text == "Добавить книгу")
@router.message(Command("add_book"))
async def add_book_title(message: Message, state: FSMContext):
    if await check_admin(message.from_user.id):
        await message.answer("Введите имя книги:")
        await state.set_state(AddBook.get_title)
    else:
        await message.answer("Только админ может создавать книги!")
        await state.clear()


    
@router.message(AddBook.get_title)
async def add_book_caption(message: Message, state: FSMContext):
    await state.update_data(title = message.text)
    await message.answer("Введите описания книги:")
    await state.set_state(AddBook.get_caption)
    
@router.message(AddBook.get_caption)
async def add_book_author(message: Message, state: FSMContext):
    await state.update_data(caption = message.text)
    buttons = await get_author_button()
    await message.answer("Выберите автора", reply_markup=buttons)
    await state.set_state(AddBook.get_author_id)
    
@router.callback_query(AddBook.get_author_id, F.data.startswith("author_"))
async def add_book_author(callback: CallbackQuery, state: FSMContext):
    author_id = callback.data.split("_")[1]
    await state.update_data(author_id = author_id)
    await callback.message.answer("Введдете категорию:")
    await callback.answer("Автор выбран")
    await state.set_state(AddBook.get_category_id)
    
    
@router.message(AddBook.get_category_id)
async def add_book_categroy(message: Message, state: FSMContext):
    await state.update_data(category_id = message.text)
    await message.answer("Введите Издател книги:")
    await state.set_state(AddBook.get_pablisher)



@router.message(AddBook.get_pablisher)
async def add_book_categroy(message: Message, state: FSMContext):
    await state.update_data(pablisher = message.text)
    data = await state.get_data()
    status = await create_book_db(data['title'], data['caption'], data['author_id'], data['category_id'], data['pablisher'])
    if status:
        await message.answer("Ваша книга создана")
        
    else:
        await message.answer("Ошибка при создании книги!")
    await state.clear()

        
    

@router.message(F.text == "Добавить категорию")
@router.message(Command("add_category"))
async def add_category(message: Message, state: FSMContext):
    if await check_admin(message.from_user.id):
        await message.answer("Введите имя категории:")
        await state.set_state(AddCategory.get_title)
    else:
        await message.answer("Только админ может создавать книги!")
        await state.clear()


@router.message(AddCategory.get_title)
async def add_category_title(message: Message, state: FSMContext):
    await state.update_data(title = message.text)
    data = await state.get_data()
    status = await create_category_db(data['title'])
    if status:
        await message.answer("Ваша категория создана")
        
    else:
        await message.answer("Ошибка при создании категория!")
    await state.clear()



@router.message(F.text == "Добавить автора")
@router.message(Command("add_author"))
async def add_author(message: Message, state: FSMContext):
    if await check_admin(message.from_user.id):
        await message.answer("Введите имя автора:")
        await state.set_state(AddAuthor.get_name)
    else:
        await message.answer("Только админ может создавать автор!")
        await state.clear()


    
@router.message(AddAuthor.get_name)
async def add_author_name(message: Message, state: FSMContext):
    await state.update_data(full_name = message.text)
    await message.answer("Введите страну автора:")
    await state.set_state(AddAuthor.get_country)



@router.message(AddAuthor.get_country)
async def add_author_country(message: Message, state: FSMContext):
    await state.update_data(country = message.text)
    data = await state.get_data()
    status = await create_author_db(data['full_name'], data['country'])
    if status:
        await message.answer("Ваша автор создана")
        
    else:
        await message.answer("Ошибка при создании автор!")
    await state.clear()
