from uuid import uuid4
from abc import ABC, abstractmethod
from streamlit_elements import dashboard, mui
from contextlib import contextmanager
from streamlit import session_state as state
from streamlit_elements import elements, sync, event


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
    def __init__(self, board, x, y, w , h, title, subheader, image, alt, content, item_id, character_id, width, height, **item_props):
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


    def delete(self):
        print("self._key | ", "Item ", self._item_id, "will be deleted from Character id: ", self._character_id)
        pass

    def __call__(self, content = None):
        with mui.Card(key=self._key, sx={"display": "flex", "flexDirection": "column", "borderRadius": 3, "overflow": "hidden"}, elevation=1):
            mui.CardHeader(
                title=self._title,
                subheader=self._subheader,
                avatar=mui.Avatar(self._title[0], sx={"bgcolor": "red"}),  # Assuming first letter of title as avatar
                action=mui.IconButton(mui.icon.MoreVert),
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
                mui.IconButton(mui.icon.Favorite)
                mui.IconButton(mui.icon.Share)
                mui.IconButton(mui.icon.Delete, onClick=self.delete)


board = Dashboard()
card=Card(board, x=0, y=0, w=3, h=4, title="Example", subheader="Subheader", image="https://cdn.discordapp.com/attachments/945077390839787570/1164314661538242670/earlnod_unholy_priest_rpg_character_casting_illumino_kinetica_u_f8d0c77f-3c43-4dd6-847a-8d40eb3c946c.png?ex=6542c387&is=65304e87&hm=0ce0da5b706b2701ee34e98049f4e499a340aa696721d72358402bc8a3113e75&", alt="Alt Text", content="Content here", item_id = 12, character_id= 53, width=300, height=400)

with elements("some key"):
    with board():  # using the board instance's __call__ method
        card()