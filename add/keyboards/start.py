from vkbottle.bot import Message, BotLabeler
from vkbottle import Keyboard, Text

bl = BotLabeler()

# Кнопка "Каталог"
def get_catalog_button():
    keyboard = Keyboard(inline=True)
    keyboard.add(Text("Каталог"))
    return keyboard

def get_company_button():
    keyboard = Keyboard(inline=True)
    keyboard.add(Text("PrimeKraft"))
    keyboard.row()
    # keyboard.add(Text("Mutant"))
    # keyboard.add(Text("Maxler"))
    # keyboard.add(Text("Dr.Hoffman"))
    keyboard.add(Text("В начало"))
    return keyboard

def get_food_button():
    keyboard = Keyboard(inline=True)
    keyboard.add(Text("Гейнер"))
    keyboard.row()
    keyboard.add(Text("Протеин"))
    keyboard.row()
    keyboard.add(Text("BCAA"))
    keyboard.row()
    keyboard.add(Text("🔙 Назад"))
    keyboard.row()
    return keyboard

# Обработчик команды "привет"
@bl.message(text=["привет", "Привет", "Начать",  "/start"])
async def hello_handler(message: Message):
    keyboard = get_catalog_button()
    await message.answer("Добро пожаловать в SportMarketBot!\n"
           "Этот бот позволяет приобрести товары\n"
           "из каталога с доставкой по всей Росии.\n", keyboard=keyboard)

# Обработчик нажатия на "Каталог"
@bl.message(text="Каталог")
async def catalog_handler(message: Message):
    await message.answer("Выберете компанию из каталога", keyboard=get_company_button())

@bl.message(text="В начало")
async def back_to_start_handler(message: Message):
    keyboard = get_catalog_button()
    await message.answer("Добро пожаловать в SportMarketBot!\n"
           "Этот бот позволяет приобрести товары\n"
           "из каталога с доставкой по всей Росии.\n", keyboard=keyboard)
    
@bl.message(text="PrimeKraft")
async def primekraft_handler(message: Message):
    await message.answer("Что вы хотите от этой компании?", keyboard=get_food_button())

@bl.message(text="🔙 Назад")
async def back_to_company_handler(message: Message):
    keyboard = get_food_button()
    await message.answer("Выберете компанию из каталога", keyboard=get_company_button())

@bl.message(text="Гейнер")
async def gainer_handler(message: Message):
    await message.answer("тебе не поможет, ты не спортсмен")

@bl.message(text="Протеин")
async def protein_handler(message: Message):
    await message.answer("тебе не поможет, ты не спортсмен")

@bl.message(text="BCAA")
async def bcaa_handler(message: Message):
    await message.answer("тебе не поможет, ты не спортсмен")