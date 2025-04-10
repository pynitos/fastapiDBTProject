from aiogram.fsm.state import State, StatesGroup


class TargetListSG(StatesGroup):
    view = State()


class TargetViewSG(StatesGroup):
    view = State()
    confirm_delete = State()


class TargetCreateSG(StatesGroup):
    urge = State()
    action = State()
    effectiveness = State()
    confirm = State()


class TargetUpdateSG(StatesGroup):
    select = State()
    urge = State()
    action = State()
    effectiveness = State()
    confirm = State()


class TargetDeleteSG(StatesGroup):
    confirm = State()
