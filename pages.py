import random

from util import (get_values_alchemy, delete_character_alchemy, delete_data_alchemy, insert_character_alchemy,
                  on_submit_click, insert_data_alchemy, insert_stat_alchemy, get_stat_by_name_alchemy,
                  update_stat_by_name, get_id, get_item_from_id, show_image, insert_stat_item_relation_alchemy,
                  get_stat_id, get_stats_for_item, upsert_stat_for_item, delete_item_stat_relation)
import streamlit as st
import time
import uuid
from annotated_text import annotated_text, annotation


def delete_character():
    """

    :return:
    """
    st.title("Delete Character")
    names_from_primary_info = get_values_alchemy('primary_info', 'name')
    st.session_state.delete = st.selectbox("Select your character", names_from_primary_info)
    if st.button('Delete Character'):
        delete_character_alchemy(st.session_state.delete)
        st.success(f"Character {st.session_state.delete} was successfully removed.")
        st.toast("Character successfully deleted", icon="✅")
        time.sleep(2)
        st.experimental_rerun()

    return


def delete_class():
    """

    :return:
    """
    st.title("Delete Class")
    names_from_primary_info = get_values_alchemy('classes', 'name')
    st.session_state.delete = st.selectbox("Select class to delete", names_from_primary_info)
    if st.button('Delete class'):
        delete_data_alchemy('classes', st.session_state.delete)
        st.success(f"Class {st.session_state.delete} was successfully removed.")
        st.toast("Class successfully deleted", icon="✅")
        time.sleep(2)
        st.experimental_rerun()
    return


def delete_stat():
    """

    :return:
    """
    st.title("Delete Stat")
    names_from_stat = get_values_alchemy('stats', 'name')
    st.session_state.delete = st.selectbox("Select stat to delete", names_from_stat)
    if st.button('Delete stat'):
        delete_data_alchemy('stats', st.session_state.delete)
        st.success(f"Stat {st.session_state.delete} was successfully removed.")
        st.toast("Stat successfully deleted", icon="✅")
        time.sleep(2)
        st.experimental_rerun()
    return


def delete_item():
    """

    :return:
    """
    st.title("Delete Item")
    names_from_primary_info = get_values_alchemy('items', 'name')
    st.session_state.delete = st.selectbox("Select item to delete", names_from_primary_info)
    if st.button('Delete item'):
        delete_data_alchemy('items', st.session_state.delete)
        st.success(f"Item {st.session_state.delete} was successfully removed.")
        st.toast("Item successfully deleted", icon="✅")
        time.sleep(2)
        st.experimental_rerun()
    return


def delete_race():
    """

    :return:
    """
    st.title("Delete Race")
    names_from_primary_info = get_values_alchemy('race', 'name')
    st.session_state.delete = st.selectbox("Select race to delete", names_from_primary_info)
    if st.button('Delete race'):
        delete_data_alchemy('race', st.session_state.delete)
        st.success(f"Race {st.session_state.delete} was successfully removed.")
        st.toast("Race successfully deleted", icon="✅")
        time.sleep(2)
        st.experimental_rerun()
    return


def insert_character():
    """

    :return:
    """
    st.title("Create Character")

    with st.form(key='character_form', clear_on_submit=True):
        # fetch dropdown data
        races = get_values_alchemy('race', 'name')
        classes = get_values_alchemy('classes', 'name')

        st.write('Character Details')
        name = st.text_input('Name')
        race = st.selectbox('Rasse', races)
        class_ = st.selectbox('Klasse', classes)

        c1, c2, c3 = st.columns(3)
        with c1:
            st.write('Physis')
            kk = st.number_input('Körperkraft', value=0, step=1)
            a = st.number_input('Ausdauer', value=0, step=1)
            p = st.number_input('Präzision', value=0, step=1)
            pb = st.number_input('Physische Belastbarkeit', value=0, step=1)
            v = st.number_input('Verhindern', value=0, step=1)
        with c2:
            st.write('Psyche')
            intel = st.number_input('Intelligenz', value=0, step=1)
            wk = st.number_input('Willenskraft', value=0, step=1)
            wa = st.number_input('Wahrnehmung', value=0, step=1)
            mb = st.number_input('Mentale Belastbarkeit', value=0, step=1)
            ins = st.number_input('Inspiration', value=0, step=1)
        with c3:
            st.write('Talente')
            ini = st.number_input('Initiative', value=0, step=1)
            tv = st.number_input('Technisches Verständnis', value=0, step=1)
            g = st.number_input('Glück', value=0, step=1)
            wi = st.number_input('Wissen', value=0, step=1)
            c = st.number_input('Charisma', value=0, step=1)

        # Create the submit button
        st.form_submit_button("Submit", on_click=on_submit_click)

        # If the submit button is clicked, insert the new character into the SQLite database
        if st.session_state.get('submitted', False):
            if name == '':
                st.warning('Please enter a name before submitting.')
            elif name in get_values_alchemy('primary_info', 'name'):
                st.warning('Name already taken. Please try something else')
            else:
                character = {
                    'name': name,
                    'race': race,
                    'class': class_,
                    'kk': kk,
                    'a': a,
                    'p': p,
                    'pb': pb,
                    'v': v,
                    'intel': intel,
                    'wk': wk,
                    'wa': wa,
                    'mb': mb,
                    'ins': ins,
                    'ini': ini,
                    'tv': tv,
                    'g': g,
                    'wi': wi,
                    'c': c
                }
                insert_character_alchemy(character)
                st.success('Character created successfully!')
                st.session_state.submitted = False
                st.session_state.show_form = False
                st.toast("Character successfully addded", icon="✅")
                time.sleep(2)
                st.experimental_rerun()
    return


def insert_class():
    """

    :return:
    """
    st.title("Insert Class")
    with st.form(key='class_form', clear_on_submit=True):
        name = st.text_input('Name')
        # Create the submit button
        st.form_submit_button("Submit", on_click=on_submit_click)

        # If the submit button is clicked, insert the new character into the SQLite database
        if st.session_state.get('submitted', False):
            if name == '':
                st.warning('Please enter a name before submitting.')
            elif name in get_values_alchemy('classes', 'name'):
                st.warning('Name already taken. Please try something else')
            else:
                classes = {
                    'name': name,
                }
                insert_data_alchemy('classes', classes)
                st.success('Class created successfully!')
                st.session_state.submitted = False
                st.session_state.show_form = False
                st.toast("Class successfully addded", icon="✅")
                time.sleep(2)
                st.experimental_rerun()
    return


def insert_item():
    """

    :return:
    """
    st.title("Insert Item")
    with st.form(key='item_form', clear_on_submit=True):
        name = st.text_input('Name')
        description = st.text_input('Description')
        image_url = st.text_input('Image-URL', value="https://res.cloudinary.com/dlzncrunt/image/upload/f_auto,q_auto/")
        # Create the submit button
        st.form_submit_button("Submit", on_click=on_submit_click)

        # If the submit button is clicked, insert the new character into the SQLite database
        if st.session_state.get('submitted', False):
            if name == '':
                st.warning('Please enter a name before submitting.')
            elif name in get_values_alchemy('classes', 'name'):
                st.warning('Name already taken. Please try something else')
            else:
                items = {
                    'name': name,
                    'description': description,
                    'image_url': image_url
                }
                insert_data_alchemy('items', items)
                st.success('Item created successfully!')
                st.session_state.submitted = False
                st.session_state.show_form = False
                st.toast("Item successfully addded", icon="✅")
                time.sleep(2)
                st.experimental_rerun()
    return


def insert_race():
    """

    :return:
    """
    st.title("Insert Race")
    with st.form(key='race_form', clear_on_submit=True):
        name = st.text_input('Name')
        # Create the submit button
        st.form_submit_button("Submit", on_click=on_submit_click)

        # If the submit button is clicked, insert the new character into the SQLite database
        if st.session_state.get('submitted', False):
            if name == '':
                st.warning('Please enter a name before submitting.')
            elif name in get_values_alchemy('race', 'name'):
                st.warning('Name already taken. Please try something else')
            else:
                race = {
                    'name': name,
                }
                insert_data_alchemy('race', race)
                st.success('Race created successfully!')
                st.session_state.submitted = False
                st.session_state.show_form = False
                st.toast("Race successfully addded", icon="✅")
                time.sleep(2)
                st.experimental_rerun()
    return


def insert_stat():
    """

    :return:
    """
    st.title("Insert stat")
    with st.form(key='race_form', clear_on_submit=True):
        name = st.text_input('Name')
        description = st.text_input('Description')
        type_in = st.selectbox('Type', options=['numerical', 'functional'])
        # Create the submit button
        st.form_submit_button("Submit", on_click=on_submit_click)

        # If the submit button is clicked, insert the new character into the SQLite database
        if st.session_state.get('submitted', False):
            if name == '':
                st.warning('Please enter a name before submitting.')
            elif name in get_values_alchemy('stats', 'name'):
                st.warning('Name already taken. Please try something else')
            else:
                stats = {
                    'name': name,
                    'description': description,
                    'type': type_in
                }
                insert_stat_alchemy(stats)
                st.success('Stat added!')
                st.session_state.submitted = False
                st.session_state.show_form = False
                st.toast("Stat added!", icon="✅")
                time.sleep(2)
                st.experimental_rerun()
    return


def update_stat():
    """

    :return:
    """
    st.title("Update stat")
    names_from_stat = get_values_alchemy('stats', 'name')
    update_value = st.selectbox("Select stat to update", names_from_stat)
    from_stats = get_stat_by_name_alchemy(update_value)
    with st.form(key='stat_form', clear_on_submit=True):
        name = st.text_input('Name', from_stats[1])
        description = st.text_input('Description', from_stats[2])
        new_type = st.selectbox('Type', options=['numerical', 'functional'],
                                index=0 if from_stats[3] == 'numerical' else 1)
        # Create the submit button
        st.form_submit_button("Submit", on_click=on_submit_click)

        # If the submit button is clicked, insert the new character into the SQLite database
        if st.session_state.get('submitted', False):
            if name == '':
                st.warning('Please enter a name before submitting.')
            elif name in get_values_alchemy('stats', 'name'):
                st.warning('Name already taken. Please try something else')
            else:
                stats = {
                    'name': name,
                    'description': description,
                    'type': new_type
                }
                update_stat_by_name(from_stats[1], stats)

                st.success('Stat updated!')
                st.session_state.submitted = False
                st.session_state.show_form = False
                st.toast("Stat updated!", icon="✅")
                time.sleep(2)
                st.experimental_rerun()
    return


def edit_item():
    st.title("Edit Item")
    item_from_dropdown = get_values_alchemy('items', 'name')
    show_item = st.selectbox("Select item to edit", item_from_dropdown)
    item_id = get_id('items', show_item)
    item = get_item_from_id(item_id)
    st.subheader(item[0][0])
    name = st.text_input('Name', item[0][0])
    image = st.text_input('Image URL', item[0][1])
    st.session_state.show_image = image
    # st.button("Show picture..")
    if 'show_image' in st.session_state:
        st.image(st.session_state.show_image)
    description = st.text_input('Description', item[0][2])

    st.divider()
    st.session_state.item_stats = get_stats_for_item(item_id)
    print(st.session_state.item_stats)
    c_stat_value, c_button, c_fill = st.columns([5,2,25])
    print("st.session_state.item_stats: ", st.session_state.item_stats)
    for active_stat in st.session_state.item_stats:
        print('active_stat: ', active_stat)
        with c_stat_value:
            annotated_text(
                annotation(str(active_stat['value']), active_stat['name'], font_size='25px', padding_top="16px", padding_bottom="16px")
            )
        with c_button:
            st.markdown(
                """
            <style>
            button {
                height: 5px;
                padding-top: 5px !important;
                padding-bottom: 5px !important;
                padding-right: 5px !important;
                padding-left: 5px !important;
            }
            </style>
            """,
                unsafe_allow_html=True,
            )
            uni_key = str(item_id) + str(active_stat['stat_id']) + "_button_" + str(uuid.uuid4())
            print(uni_key)
            print(f"Before button creation with key: {uni_key}")
            st.button(":wastebasket:", type="secondary", key=uni_key, on_click=delete_item_stat_relation, args=(item_id,
                                                                                                     active_stat['stat_id']))
            print(f"After button creation with key: {uni_key}")
        with c_fill:
            st.text("")
    st.divider()
    col_stat, col_value, col_button = st.columns(3)
    stat_names = get_values_alchemy('stats', 'name')
    with col_stat:
        in_stat_name = st.selectbox("Stat", stat_names)
        stat_id = get_stat_id('stats', in_stat_name)
    with col_value:
        in_value = st.number_input("Value", step=1)

    with col_button:
        st.markdown("""
        <style>
        .blocker {
            font-size:0px;
            opacity:0;
        }
        </style>
        """, unsafe_allow_html=True)

        st.markdown(f'<p class="blocker">hhuhu<p>', unsafe_allow_html=True)
        st.button(":heavy_plus_sign:", type="primary", on_click=upsert_stat_for_item, args=(
            {'item_id': item_id, 'stat_id': stat_id, 'value': in_value},), key=uni_key
                  )

    # Create the submit button
    # st.form_submit_button("Submit", on_click=on_submit_click)

    # If the submit button is clicked, insert the new character into the SQLite database
    # if st.session_state.get('submitted', False):
    #     if name == '':
    #         st.warning('Please enter a name before submitting.')
    #     elif name in get_values_alchemy('stats', 'name'):
    #         st.warning('Name already taken. Please try something else')
    #     else:
    #         stats = {
    #             'name': name,
    #             'description': description,
    #             'type': new_type
    #         }
    #         update_stat_by_name(from_stats[1], stats)
    #
    #         st.success('Stat updated!')
    #         st.session_state.submitted = False
    #         st.session_state.show_form = False
    #         st.toast("Stat updated!", icon="✅")
    #         time.sleep(2)
    #         st.experimental_rerun()
    return


def empty_page():
    return
