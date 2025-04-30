from aiogram.dispatcher.filters.state import State,StatesGroup

class Kinodata(StatesGroup):
    kino=State()
    number=State()

class Deletekino(StatesGroup):
    kinokod=State()

class Reklmayoz(StatesGroup):
    reklamayoz=State()

class Updatakino(StatesGroup):
    kinokod=State()
    updatakino=State()


class CaptionC(StatesGroup):
    captionsearch=State()
