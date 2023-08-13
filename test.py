from streamlit_elements import elements, dashboard, mui, editor, media, lazy, sync, nivo
from util import *

layout = [
    # Editor item is positioned in coordinates x=0 and y=0, and takes 6/12 columns and has a height of 3.
    dashboard.Item("editor", 0, 0, 3, 4),
    # Chart item is positioned in coordinates x=6 and y=0, and takes 6/12 columns and has a height of 3.
    dashboard.Item("chart", 6, 0, 6, 3),
    # Media item is positioned in coordinates x=0 and y=3, and takes 6/12 columns and has a height of 4.
    dashboard.Item("media", 0, 2, 12, 4),
]

print("1 ", type(layout))
print("2 ", type(dashboard.Item("editor", 0, 0, 3, 4),))
print(layout)
dict_add = dashboard.Item("someItem", 1,2,3,4)
layout.append(dict_add)
print(layout)
print(get_items_for_character(24))