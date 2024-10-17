from aiogram.dispatcher.filters.state import StatesGroup, State


class User(StatesGroup):
    Lang = State()
    Phone = State()


class Flat(StatesGroup):
    Sub1 = State()
    Sub2 = State()
    Urls = State()


class Flat_rent(StatesGroup):
    Sub1 = State()
    Sub2 = State()
    Urls = State()


class Del_Flat(StatesGroup):
    Categ = State()
    Sub1 = State()
    Sub2 = State()


class Edit_flat(StatesGroup):
    Categ = State()
    Sub1 = State()
    Sub2 = State()

    Cont_Sub1 = State()
    Cont2_Sub1 = State()
    Cont2uz_Sub1 = State()

    Cont_Sub2 = State()
    Cont2_Sub2 = State()
    Cont2uz_Sub2 = State()

    Cont_Sub3 = State()
    Contuz_Sub3 = State()


class Add_Flat(StatesGroup):
    Categ = State()
    Sub1 = State()
    Sub2 = State()
    Url = State()
    Url_uz = State()
    Confirm = State()

    New_sub1 = State()
    New_sub1_uz = State()
    New_sub2 = State()
    New_sub2_uz = State()
    New_url = State()
    New_url_uz = State()
    New_Confirm = State()


class Add_Room(StatesGroup):
    New_sub2 = State()
    New_sub2_uz = State()
    New_url = State()
    New_url_uz = State()
    Confirm = State()


class Admin(StatesGroup):
    Delete_admin = State()
    Add_admin = State()
    Add_level = State()


class Custom(StatesGroup):
    Lang = State()





