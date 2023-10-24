from uuid import uuid4
from abc import ABC, abstractmethod
import streamlit as st
from streamlit_elements import dashboard, mui
from contextlib import contextmanager
from util import get_layout_items_character_item
from util import init_connection_alchemy
from sqlalchemy import MetaData, Table, text ,delete
from streamlit import session_state as state
from streamlit_elements import elements, sync, event
from types import SimpleNamespace



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
                mui.IconButton(mui.icon.Backpack, color=self._color)
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


def decrement_or_delete_character_item(character_id, item_id, equipped):
    engine = init_connection_alchemy()
    metadata = MetaData()
    data = {
        "charID": character_id,
        "itemID": item_id,
        "equipped": equipped
        }

    # Define the table based on metadata
    character_items = Table('character_items', metadata, autoload_with=engine)

    # Use the connection
    with engine.connect() as connection:
        # Decrement Quantity
        if equipped:
            sql = text(f"""
                UPDATE character_items 
                SET quantity = quantity - 1, 
                    equipped = equipped - 1
                WHERE character_id = :charID AND item_id = :itemID;
            """)
        else:
            sql = text(f"""
                UPDATE character_items
                SET quantity = quantity - 1
                WHERE character_id = :charID AND item_id = :itemID;
            """)
        print(sql)
        connection.execute(sql, **data)

        # Delete rows with quantity 0
        del_stmt = delete(character_items).where(
            (character_items.c.character_id == character_id) &
            (character_items.c.item_id == item_id) &
            (character_items.c.quantity == 0)
        )
        connection.execute(del_stmt)