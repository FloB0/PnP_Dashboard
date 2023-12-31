from uuid import uuid4
from abc import ABC, abstractmethod
import streamlit as st
from streamlit_elements import dashboard, mui
from contextlib import contextmanager
from util import get_layout_items_character_item
from util import init_connection_alchemy
from sqlalchemy import MetaData, Table, text ,delete, update, select
from streamlit import session_state as state
from streamlit_elements import elements, sync, event
from types import SimpleNamespace


def change_equipped (character_id, item_id, equipped):
    engine = init_connection_alchemy()
    metadata = MetaData()
    data = {
        "charID": character_id,
        "itemID": item_id
        }

    # Define the table based on metadata
    character_items = Table('character_items', metadata, autoload_with=engine)

    with engine.connect() as connection:
        # Ensure equipped count does not exceed quantity
        sel_stmt = select(character_items.c.quantity, character_items.c.equipped).where(
            (character_items.c.character_id == character_id) &
            (character_items.c.item_id == item_id)
            )
        result = connection.execute(sel_stmt).fetchone()

        if not result:
            # Item not found for the character
            return

        quantity, current_equipped = result

        if equipped and current_equipped > 0:
            # Decrement equipped count
            stmt = update(character_items).where(
                (character_items.c.character_id == character_id) &
                (character_items.c.item_id == item_id)
                ).values(equipped=current_equipped - 1)
        elif not equipped and current_equipped < quantity:
            # Increment equipped count
            stmt = update(character_items).where(
                (character_items.c.character_id == character_id) &
                (character_items.c.item_id == item_id)
                ).values(equipped=current_equipped + 1)
        else:
            # Either trying to equip more than available quantity or trying to unequip when nothing is equipped
            return

        connection.execute(stmt)
        st.session_state.item_added = True
        connection.commit()

def decrement_or_delete_character_item (character_id, item_id, equipped):
    engine = init_connection_alchemy()
    metadata = MetaData()
    print("charID: ", character_id, " itemID: ", item_id, " equipped: ", equipped)
    # Define the table based on metadata
    character_items = Table('character_items', metadata, autoload_with=engine)

    # Use the connection
    with engine.connect() as connection:
        # Create an update statement
        if equipped:
            stmt = (
                update(character_items)
                .where(
                    (character_items.c.character_id == character_id) &
                    (character_items.c.item_id == item_id)
                    )
                .values(
                    quantity=character_items.c.quantity - 1,
                    equipped=character_items.c.equipped - 1
                    )
            )
        else:
            stmt = (
                update(character_items)
                .where(
                    (character_items.c.character_id == character_id) &
                    (character_items.c.item_id == item_id)
                    )
                .values(
                    quantity=character_items.c.quantity - 1
                    )
            )
        print("stmt ", stmt)
        result = connection.execute(stmt)
        print("Rows affected by update:", result.rowcount)
        # Delete rows with quantity 0
        del_stmt = (
            delete(character_items)
            .where(
                (character_items.c.character_id == character_id) &
                (character_items.c.item_id == item_id) &
                (character_items.c.quantity == 0)
                )
        )
        print("del_stmt ", del_stmt)
        del_result = connection.execute(del_stmt)
        print("Rows deleted:", del_result.rowcount)
        st.session_state.item_added = True
        connection.commit()


class Dashboard:

    DRAGGABLE_CLASS = "draggable"

    def __init__(self):
        self._layout = []

    def _register(self, item):
        self._layout.append(item)

    @contextmanager
    def __call__(self, **props):
        # Draggable classname query selector.
        props["draggableHandle"] = f".{Dashboard.DRAGGABLE_CLASS}"

        with dashboard.Grid(self._layout, **props):
            yield

    class Item(ABC):

        def __init__(self, board, x, y, w, h, **item_props):
            self._key = str(uuid4())
            self._draggable_class = Dashboard.DRAGGABLE_CLASS
            self._dark_mode = True
            board._register(dashboard.Item(self._key, x, y, w, h, **item_props))

        def _switch_theme(self):
            self._dark_mode = not self._dark_mode

        @contextmanager
        def title_bar(self, padding="5px 15px 5px 15px", dark_switcher=True):
            with mui.Stack(
                className=self._draggable_class,
                alignItems="center",
                direction="row",
                spacing=1,
                sx={
                    "padding": padding,
                    "borderBottom": 1,
                    "borderColor": "divider",
                },
            ):
                yield

                if dark_switcher:
                    if self._dark_mode:
                        mui.IconButton(mui.icon.DarkMode, onClick=self._switch_theme)
                    else:
                        mui.IconButton(mui.icon.LightMode, sx={"color": "#ffc107"}, onClick=self._switch_theme)

        @abstractmethod
        def __call__(self):
            """Show elements."""
            raise NotImplementedError


class Card(Dashboard.Item):
    def __init__(self, board, x, y, w , h, title, subheader, image, alt, content, item_id, character_id, width, height,
                 equipped, **item_props):
        super().__init__(board, x, y, w, h, **item_props)
        self._title = title
        self._subheader = subheader
        self._image = image
        self._alt = alt
        self._content = content
        self._width = width
        self._height = height
        self._item_id = item_id
        self._character_id = character_id
        self._equipped = equipped
        if self._equipped:
            self._color = "success"
        else:
            self._color = "primary"

    def change_equipped(self):
        change_equipped(character_id=self._character_id,item_id=self._item_id,equipped=self._equipped)
    def delete(self):
        decrement_or_delete_character_item(character_id=self._character_id,item_id=self._item_id,equipped=self._equipped)

    def __call__(self, content = None):
        with mui.Card(key=self._key, sx={"display": "flex", "flexDirection": "column", "borderRadius": 3, "overflow": "hidden"}, elevation=1):
            mui.CardHeader(
                title=self._title,
                subheader=self._subheader,
                avatar=mui.Avatar(self._title[0], sx={"bgcolor": "red"}),  # Assuming first letter of title as avatar
                # action=mui.IconButton(mui.icon.MoreVert),
                # action=mui.IconButton(mui.icon.Delete, onClick=self.delete),
                className=self._draggable_class,
            )
            mui.CardMedia(
                component="img",
                height=self._height,
                width=self._width,
                image=self._image,
                alt=self._alt,
            )

            with mui.CardContent(sx={"flex": 1}):
                mui.Typography(self._content)

            with mui.CardActions(disableSpacing=True):
                mui.IconButton(mui.icon.Backpack, onClick=self.change_equipped, color=self._color)
                mui.IconButton(mui.icon.Share)
                mui.IconButton(mui.icon.Delete, onClick=self.delete)


def create_item_elements_for_character_id(characterID):
    # layout = get_layout_character_item(characterID)
    layout = get_layout_items_character_item(characterID)
    # print(layout)
    if "item_board" not in st.session_state:
        st.session_state.item_board = Dashboard()
    if "w" not in st.session_state or st.session_state.item_added:
        w = SimpleNamespace()
        board = st.session_state.item_board
        for card in layout:
            card_name = "card{}".format(card["i"])
            card_obj = Card(board,
                            x=card["x"], y=card["y"], w=card["w"], h=card["h"],
                            title=card["name"], subheader="Subheader",
                            image=card["image_url"], alt=card["name"],
                            content=card["description"], item_id=card["item_id"], equipped=card["equipped"],
                            character_id=characterID, width=300, height=400)
            setattr(w, card_name, card_obj)
        st.session_state.w = w
        st.session_state.item_added = False
        st.experimental_rerun()
    else:
        w = st.session_state.w
        board = st.session_state.item_board
        with elements("demo"):
            with board():
                for card_attr in vars(w):
                    card = getattr(w, card_attr)
                    card()


