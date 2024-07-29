from aiogram import Router, F
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.filters import CommandStart, Command
from data.info import get_role
from keyboards import builder, inline
from data import book
from aiogram.enums.parse_mode import ParseMode
from middlewares.messages import DbLogMiddleware
from data.db import stat
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove


router = Router()
router.message.middleware(DbLogMiddleware())


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(text='Здравствуйте👋 Выберите действие⬇',
                         reply_markup=builder.reply_builder(
                             book.layers['menu']))

@router.callback_query(F.data == 'Меню')
async def btn_start(call: CallbackQuery):
    await call.answer()
    await call.message.answer(text='Выберите действие⬇',
                         reply_markup=builder.reply_builder(
                             book.layers['menu']))


@router.message(Command('secretinfo'))
async def cmd_getadminfo(message: Message):
    result = stat('./data/messages.db')
    await message.answer(str(result))
    '''await message.answer(f'<b>Пользователи</b>\n'
                         f'Всего: {result[0]}\n'
                         f'Сегодня: {result[2]}\n'
                         f'Неделя: {result[4]}\n\n'
                         f'<b>Сообщения</b>\n'
                         f'Сегодня: {result[1]}\n')'''


@router.message(F.text.in_(book.layers['menu']))
async def menu(message: Message):
    txt = message.text
    lst = book.layers['menu']
    if txt == lst[0]:
        await message.answer(text='Наш канал📣',
                             reply_markup=inline.create_inline(
                                 text='Перейти↗', url=book.menu[txt]))
    elif txt == lst[1]:
        await message.answer(text='Чат с техподдержкой📲',
                             reply_markup=inline.create_inline(
                                 text='Перейти↗', url=book.menu[txt]))
    elif txt == lst[2]:
        await message.answer(
            text=
            "Компания <i>elmex</i> является ведущим производителем клеммных колодок и интерфейсных модулей для управления и автоматизации в Индии.\n\nНаша история началась в 1963 году, когда мы начали производство клеммных колодок для промышленных распределительных устройств.С тех пор мы смогли достичь устойчивого и систематического роста благодаря инновациям, качеству обслуживания клиентов и повышению производительности производства.\n\nМы также гордимся своей технической и экономической конкурентоспособностью и международными сертификатами соответсвия на свою продукцию.\n\nКлючевые компании, как ABB, Alstom, Schneider Electric, Siemens, Honeywell, GE, L&T, BHEL и NTPC, выбирают нас в качестве глобального партнера по аутсорсингу.\n\nЧтобы расширить ассортимент продукции и обслуживать более широкий рынок, в 1993 году была создана компания <i>Elmex Electric Pvt. Ltd.</i>, которая впервые представила концепцию интерфейсных модулей для управления и автоматизации, монтируемых на DIN-рейку.\n\n#бот_о_компании",
            parse_mode=ParseMode.HTML)

    elif txt == lst[3]:
        for mes in book.menu[txt]:
            await message.answer(text=mes, parse_mode=ParseMode.HTML, disable_web_page_preview=True)

    elif txt == lst[4]:
        await message.answer(
            text='Выберите товар⬇️',
            reply_markup=builder.reply_builder(book.layers['Номенклатура'] +
                                               ['Меню']))

    elif txt == lst[5]:
        await message.answer(text='Введите артикул', reply_markup=ReplyKeyboardRemove())
        
@router.message(F.text.isdigit())
async def inf(message: Message):
    iou = get_role(int(message.text))
    await message.answer(iou, parse_mode=ParseMode.HTML)
    await message.answer(text='Введите артикул или нажмите на кнопку для выхода', reply_markup=builder.inline(["Меню"]))

@router.message(F.text.in_(book.nomen.keys()))
async def select_product(message: Message):
    txt = message.text
    thing = book.nomen[txt]
    if txt in book.nomen.keys():
        file = FSInputFile(f'data/{thing["photo"][0]}.PNG')
        if thing['url']:
            await message.answer_photo(photo=file,
                                       caption=thing['Описание'],
                                       reply_markup=inline.create_inline(
                                           text='Скачать каталог📥',
                                           url=thing['url']))
        else:
            await message.answer_photo(photo=file, caption=thing['Описание'])


@router.message(F.text.in_(list(book.layers.keys())[2:]))
async def send_layer2(message: Message):
    await message.answer(
        text='Какие именно?',
        reply_markup=builder.reply_builder(book.layers[message.text] +
                                           ['Назад']))


@router.message(F.text.in_(['Назад', 'Меню']))
async def back(message: Message):
    if message.text == 'Назад':
        await message.answer(
            text='Выберите товар⬇️',
            reply_markup=builder.reply_builder(book.layers['Номенклатура'] +
                                               ['Меню']))
    else:
        await message.answer(text='Выберите действие⬇',
                             reply_markup=builder.reply_builder(
                                 book.layers['menu']))


@router.message()
async def main_error(message: Message):
    await message.answer(text='Что-то пошло не так...😬\nВоспользуйся /start')



