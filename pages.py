import random

from util import (
    get_values_alchemy, delete_character_alchemy, delete_data_alchemy, insert_character_alchemy,
    on_submit_click, insert_data_alchemy, insert_stat_alchemy, get_stat_by_name_alchemy,
    update_stat_by_name, get_id, get_item_from_id, show_image, insert_stat_item_relation_alchemy,
    get_stat_id, get_stats_for_item, upsert_stat_for_item, delete_item_stat_relation,
    insert_trait_alchemy, get_trait_from_id, get_trait_by_name_alchemy, update_trait_by_name,
    get_stats_for_trait, delete_trait_stat_relation, upsert_stat_for_trait, get_trait_id, delete_trait_alchemy,
    fetch_all_from_table, get_character_by_name_alchemy, get_traits_for_character, delete_trait_character_relation,
    upsert_trait_for_character, get_trait_id, get_race_by_name_alchemy, get_traits_for_race, delete_trait_race_relation,
    upsert_trait_for_race, get_stats_for_race, delete_stat_race_relation, upsert_stat_for_race,
    get_class_by_name_alchemy, delete_trait_class_relation, get_traits_for_class, upsert_trait_for_class,
    get_stats_for_class, upsert_stat_for_class, delete_stat_class_relation, get_all_usernames, check_user_admin,
    modify_user_admin_status, update_data_alchemy, update_item_by_name,
    )
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
    names_from_primary_info = [d["name"] for d in names_from_primary_info]
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
    class_names = get_values_alchemy('classes', 'name')
    class_names = [d["name"] for d in class_names]
    st.session_state.delete = st.selectbox("Select class to delete", class_names)
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
    stat_names = get_values_alchemy('stats', 'stat_name')
    stat_names = [d["stat_name"] for d in stat_names]
    st.session_state.delete = st.selectbox("Select stat to delete", stat_names)
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
    item_names = get_values_alchemy('items', 'name')
    item_names = [d["name"] for d in item_names]
    st.session_state.delete = st.selectbox("Select item to delete", item_names)
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
    race_names = get_values_alchemy('race', 'name')
    race_names = [d["name"] for d in race_names]
    st.session_state.delete = st.selectbox("Select race to delete", race_names)
    if st.button('Delete race'):
        delete_data_alchemy('race', st.session_state.delete)
        st.success(f"Race {st.session_state.delete} was successfully removed.")
        st.toast("Race successfully deleted", icon="✅")
        time.sleep(2)
        st.experimental_rerun()
    return


def delete_trait():
    """

    :return:
    """
    st.title("Delete Trait")
    trait_names = get_values_alchemy('traits', 'trait_name')
    trait_names = [d["trait_name"] for d in trait_names]
    st.session_state.delete = st.selectbox("Select trait to delete", trait_names)
    if st.button('Delete Trait'):
        delete_trait_alchemy('traits', st.session_state.delete)
        st.success(f"Trait {st.session_state.delete} was successfully removed.")
        st.toast("Trait successfully deleted", icon="✅")
        time.sleep(2)
        st.experimental_rerun()
    return


def insert_character():
    """
    Depreciated since 24.09.23
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
                    'c': c,
                    'created_by': st.session_state.USERNAME
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
            elif name in get_values_alchemy('items', 'name'):
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
            elif name in get_values_alchemy('stats', 'stat_name'):
                st.warning('Name already taken. Please try something else')
            else:
                stats = {
                    'stat_name': name,
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


def insert_trait():
    """

    :return:
    """
    st.title("Insert trait")
    with st.form(key='trait_form', clear_on_submit=True):
        name = st.text_input('Trait Name')
        description = st.text_input('Description')
        type_in = st.selectbox('Type', options=['numerical', 'functional'])
        cost = st.number_input('Cost', step=1)
        category = st.selectbox('Type', options=['all', 'character', 'item', 'race', 'class'], index=0)
        # category = st.selectbox('Type', options=[1, 2, 3, 4], index=1)
        # Create the submit button
        st.form_submit_button("Submit", on_click=on_submit_click)

        # If the submit button is clicked, insert the new character into the SQLite database
        if st.session_state.get('submitted', False):
            if name == '':
                st.warning('Please enter a name before submitting.')
            elif name in get_values_alchemy('traits', 'trait_name'):
                st.warning('Name already taken. Please try something else')
            else:
                trait = {
                    'trait_name': name,
                    'description': description,
                    'type': type_in,
                    'cost': cost,
                    'category': category
                    }
                insert_trait_alchemy(trait)
                st.success('Trait added!')
                st.session_state.submitted = False
                st.session_state.show_form = False
                st.toast("Trait added!", icon="✅")
                time.sleep(2)
                st.experimental_rerun()
    return


def update_stat():
    """

    :return:
    """
    st.title("Update stat")
    names_from_stat = get_values_alchemy('stats', 'stat_name')
    names_from_stat = [d["stat_name"] for d in names_from_stat]
    update_value = st.selectbox("Select stat to update", names_from_stat)
    from_stats = get_stat_by_name_alchemy(update_value)
    with st.form(key='stat_form', clear_on_submit=True):
        name = st.text_input('Name', from_stats[1])
        description = st.text_input('Description', from_stats[3])
        new_type = st.selectbox('Type', options=['numerical', 'functional'],
                                index=0 if from_stats[2] == 'numerical' else 1)
        # Create the submit button
        st.form_submit_button("Submit", on_click=on_submit_click)

        # If the submit button is clicked, insert the new character into the SQLite database
        if st.session_state.get('submitted', False):
            if name == '':
                st.warning('Please enter a name before submitting.')
            elif name in get_values_alchemy('stats', 'stat_name') and update_value != name:
                st.warning('Name already taken. Please try something else')
            else:
                stats = {
                    'stat_name': name,
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


def update_trait():
    """

    :return:
    """
    st.title("Update trait")
    names_from_stat = fetch_all_from_table('traits')
    desired_categories = ['all', 'character', 'item', 'race', 'class']
    c_trait_select, c_cat_filter = st.columns([15, 5])

    with c_cat_filter:
        filtered_cat = st.multiselect('Category', options=['all', 'character', 'item', 'race', 'class'],
                                      default='all')
        if 'all' in filtered_cat:
            desired_categories_ = desired_categories
        else:
            desired_categories_ = filtered_cat
        filtered_list = [d for d in names_from_stat if d['category'] in desired_categories_]
        traits_list = [d['trait_name'] for d in filtered_list]
    with c_trait_select:
        update_value = st.selectbox("Select trait to update", traits_list)
    from_stats = get_trait_by_name_alchemy(update_value)
    if from_stats == None:
        st.write("Select Trait to update..")
    else:
        with st.form(key='trait_form', clear_on_submit=True):
            name = st.text_input('Name', from_stats[1])
            description = st.text_input('Description', from_stats[2])
            new_type = st.selectbox('Type', options=['numerical', 'functional'],
                                    index=0 if from_stats[3] == 'numerical' else 1)
            cost_ = st.number_input('Cost', value=from_stats[4], step=1)
            if from_stats[5] == 'character':
                index = 1
            elif from_stats[5] == 'item':
                index = 2
            elif from_stats[5] == 'race':
                index = 3
            elif from_stats[5] == 'class':
                index = 4
            elif from_stats[5] == "all":
                index = 0
            new_cat = st.selectbox('Type', options=['all', 'character', 'item', 'race', 'class'], index=index)

            # Create the submit button
            st.form_submit_button("Submit", on_click=on_submit_click)

            # If the submit button is clicked, insert the new character into the SQLite database
            if st.session_state.get('submitted', False):
                if name == '':
                    st.warning('Please enter a name before submitting.')
                elif name in get_values_alchemy('traits', 'trait_name') and update_value != name:
                    st.warning('Name already taken. Please try something else')
                else:
                    trait = {
                        'trait_name': name,
                        'description': description,
                        'type': new_type,
                        'cost': cost_,
                        'category': new_cat
                        }
                    update_trait_by_name(from_stats[1], trait)

                    st.success('Trait updated!')
                    st.session_state.submitted = False
                    st.session_state.show_form = False
                    st.toast("Trait updated!", icon="✅")
                    time.sleep(2)
                    st.experimental_rerun()
    return


def edit_item():
    st.title("Edit Item")
    item_from_dropdown = get_values_alchemy('items', 'name')
    item_from_dropdown = [d["name"] for d in item_from_dropdown]
    show_item = st.selectbox("Select item to edit", item_from_dropdown)
    item_id = get_id('items', show_item)
    item = get_item_from_id(item_id)
    with st.form(key="edit-item"):
        st.subheader(item[0][0])
        name = st.text_input('Name', item[0][0])
        image = st.text_input('Image URL', item[0][1])
        st.session_state.show_image = image
        # st.button("Show picture..")
        if 'show_image' in st.session_state:
            st.image(st.session_state.show_image)
        description = st.text_input('Description', item[0][2])

        st.form_submit_button("Submit", on_click=on_submit_click)

        # If the submit button is clicked, insert the new character into the SQLite database
        if st.session_state.get('submitted', False):
            # print(get_values_alchemy('items', ['name']))
            # print(name in get_values_alchemy('items', ['name']))
            # print()
            if st.session_state.get('submitted', False):
                if name == '':
                    st.warning('Please enter a name before submitting.')
                elif any(item['name'] == name for item in get_values_alchemy('items', ['name'])):
                    st.warning('Name already taken. Please try something else')
                else:
                    items = {
                        'name': name,
                        'description': description,
                        'image_url': image
                        }
                    result_ = update_item_by_name(show_item, items)
                    # update_data_alchemy(table_name="items",table_column="id", value=item_id, updated_values=items)
                    st.success('Item updated!')
                    st.session_state.submitted = False
                    st.session_state.show_form = False
                    st.toast("Item updated!", icon="✅")
                    time.sleep(2)
                    st.experimental_rerun()


    st.divider()
    st.session_state.item_stats = get_stats_for_item(item_id)
    # print(st.session_state.item_stats)
    c_stat_value, c_button, c_fill = st.columns([5, 2, 25])
    # print("st.session_state.item_stats: ", st.session_state.item_stats)
    for active_stat in st.session_state.item_stats:
        # print('active_stat: ', active_stat)
        with c_stat_value:
            annotated_text(
                annotation(str(active_stat['value']), active_stat['name'], font_size='25px', padding_top="16px",
                           padding_bottom="16px")
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
            # uni_key = str(item_id) + str(active_stat['stat_id']) + "_button_" + str(uuid.uuid4())
            # print(uni_key)
            # print(f"Before button creation with key: {uni_key}")
            st.button(":wastebasket:", type="secondary", key=active_stat['name'], on_click=delete_item_stat_relation,
                      args=(item_id,
                            active_stat['stat_id']))
            # print(f"After button creation with key: {uni_key}")
        with c_fill:
            st.text("")
    st.divider()
    col_stat, col_value, col_button = st.columns(3)
    stat_names = get_values_alchemy('stats', 'stat_name')
    stat_names = [d["stat_name"] for d in stat_names]
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
            {'item_id': item_id, 'stat_id': stat_id, 'value': in_value},), key="add_stat_button"
                  )
    return


def edit_trait():
    st.title("Edit Trait")
    trait_from_dropdown = fetch_all_from_table('traits')
    desired_categories = ['all','character', 'item', 'race', 'class']
    c_trait_select, c_cat_filter = st.columns([15, 5])

    with c_cat_filter:
        filtered_cat = st.multiselect('Category', options=['all', 'character', 'item', 'race', 'class'],
                                      default='all')
        if 'all' in filtered_cat:
            desired_categories_ = desired_categories
        else:
            desired_categories_ = filtered_cat
        filtered_list = [d for d in trait_from_dropdown if d['category'] in desired_categories_]
        traits_list = [d['trait_name'] for d in filtered_list]
    with c_trait_select:
        update_value = st.selectbox("Select trait to update", traits_list)
    trait_id = get_trait_id('traits', update_value)
    trait = get_trait_from_id(trait_id)
    if trait == {}:
        st.write("Select Trait to edit..")
    else:
        st.subheader(trait[0][0])
        if trait[0][1] == 'functional':
            text_ = "a functional use."
            desc_ = "Function: "
        elif trait[0][1] == 'numerical':
            text_ = "only numerical use."
            desc_ = "Description: "
        else:
            text_ = "no use."
            desc_ = "Des: "
        st.text("This trait has " + text_)
        st.text(desc_ + trait[0][2])
        st.text("Trait costs: " + str(trait[0][3]))

        st.divider()
        st.session_state.trait_stats = get_stats_for_trait(trait_id)
        c_trait_value, c_trait_button, c_trait_fill = st.columns([5, 2, 25])
        for active_trait in st.session_state.trait_stats:
            with c_trait_value:
                filler = active_trait['value']
                annotated_text(
                    annotation(str(filler), active_trait['stat_name'], font_size='25px', padding_top="16px",
                               padding_bottom="16px")
                    )
            with c_trait_button:
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
                # uni_key = str(item_id) + str(active_stat['stat_id']) + "_button_" + str(uuid.uuid4())
                # print(uni_key)
                # print(f"Before button creation with key: {uni_key}")
                st.button(":wastebasket:", type="secondary", key=active_trait['stat_name'],
                          on_click=delete_trait_stat_relation, args=(trait_id,
                                                                     active_trait['stat_id']))
                # print(f"After button creation with key: {uni_key}")
            with c_trait_fill:
                st.text("")
        st.divider()
        col_trait, col_trait_value, col_trait_button = st.columns(3)
        stat_names = get_values_alchemy('stats', 'stat_name')
        stat_names = [d["stat_name"] for d in stat_names]
        with col_trait:
            in_stat_name = st.selectbox("Trait", stat_names)
            stat_id = get_stat_id('stats', in_stat_name)
        with col_trait_value:
            in_value = st.number_input("Value", step=1)

        with col_trait_button:
            st.markdown("""
            <style>
            .blocker {
                font-size:0px;
                opacity:0;
            }
            </style>
            """, unsafe_allow_html=True)

            st.markdown(f'<p class="blocker">hhuhu<p>', unsafe_allow_html=True)
            st.button(":heavy_plus_sign:", type="primary", on_click=upsert_stat_for_trait, args=(
                {'trait_id': trait_id, 'stat_id': stat_id, 'value': in_value},), key="add_trait_button"
                      )
    return


def link_stat_trait_to_race():
    names_from_primary_info = get_values_alchemy('race', 'name')
    race_ = [d["name"] for d in names_from_primary_info]
    st.session_state.key = st.selectbox("Select Race", race_)
    race_ = get_race_by_name_alchemy(st.session_state.key)
    # race_ = get_values_alchemy('race', column_names= ['name','id'])
    st.session_state.race_traits = get_traits_for_race(race_['id'])
    # print("char traits " + str(st.session_state.race_traits))
    st.divider()

    st.subheader("Traits")
    c_trait_info, c_trait_button_delete, c_trait_fill = st.columns([10, 2, 15])
    if st.session_state.race_traits is not None:
        for race_trait in st.session_state.race_traits:
            with c_trait_info:
                # print("race_trait   " + str(race_trait))
                filler = str(race_trait['value'])
                annotated_text(
                    annotation(str(filler), race_trait['trait_name'], font_size='25px', padding_top="16px",
                               padding_bottom="16px")
                    )
            with c_trait_button_delete:
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
                # uni_key = str(item_id) + str(active_stat['stat_id']) + "_button_" + str(uuid.uuid4())
                # print(uni_key)
                # print(f"Before button creation with key: {uni_key}")
                st.button(":wastebasket:", type="secondary", key=race_trait['trait_name'],
                          on_click=delete_trait_race_relation,
                          args=(race_trait['id'],
                                race_['id']))
                # print(f"After button creation with key: {uni_key}")
            with c_trait_fill:
                st.text("")
    # --------------------------------------Stat Input----------------------------------------------
    col_trait, col_trait_value, col_trait_button = st.columns(3)
    trait_names = get_values_alchemy('traits', 'trait_name')
    trait_names = [d["trait_name"] for d in trait_names]
    with col_trait:
        in_trait_name = st.selectbox("Trait", trait_names)
        trait_id = get_trait_id('traits', in_trait_name)
    with col_trait_value:
        in_value = st.number_input("Value", step=1, key=in_trait_name+"-1")

    with col_trait_button:
        st.markdown("""
                <style>
                .blocker {
                    font-size:0px;
                    opacity:0;
                }
                </style>
                """, unsafe_allow_html=True)

        st.markdown(f'<p class="blocker">hhuhu<p>', unsafe_allow_html=True)
        st.button(":heavy_plus_sign:", type="primary", on_click=upsert_trait_for_race, args=(
            {'trait_id': trait_id, 'race_id': race_['id'], 'value': in_value},), key=uuid.uuid4()
                  )
    st.divider()
    # --------------------------------------Stat Input----------------------------------------------

    st.session_state.race_stats = get_stats_for_race(race_['id'])
    # print("st.session_state.race_stats   ", str(st.session_state.race_stats))
    st.subheader("Stats")
    c_stat_info, c_stat_button_delete, c_stat_fill = st.columns([10, 2, 15])
    if st.session_state.race_stats is not None:
        for race_stat in st.session_state.race_stats:
            with c_stat_info:
                # print("race_stat   ", str(race_stat))
                # print(race_stat)
                filler = str(race_stat['value'])
                annotated_text(
                    annotation(str(filler), race_stat['name'], font_size='25px', padding_top="16px",
                               padding_bottom="16px")
                    )
            with c_stat_button_delete:
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
                # uni_key = str(item_id) + str(active_stat['stat_id']) + "_button_" + str(uuid.uuid4())
                # print(uni_key)
                # print(f"Before button creation with key: {uni_key}")
                st.button(":wastebasket:", type="secondary", key=race_stat['name'],
                          on_click=delete_stat_race_relation,
                          args=(race_stat['stat_id'],
                                race_['id']))
                # print(f"After button creation with key: {uni_key}")
            with c_stat_fill:
                st.text("")

    # --------------------------------------Trait Input----------------------------------------------
    col_trait, col_trait_value, col_trait_button = st.columns(3)
    stat_names = get_values_alchemy('stats', 'stat_name')
    with col_trait:
        in_stat_name = st.selectbox("Stat", stat_names)
        stat_id = get_stat_id('stats', in_stat_name)
    with col_trait_value:
        in_value = st.number_input("Value", step=1, key=in_stat_name+"-1")

    with col_trait_button:
        st.markdown("""
                <style>
                .blocker {
                    font-size:0px;
                    opacity:0;
                }
                </style>
                """, unsafe_allow_html=True)

        st.markdown(f'<p class="blocker">hhuhu<p>', unsafe_allow_html=True)
        st.button(":heavy_plus_sign:", type="primary", on_click=upsert_stat_for_race, args=(
            {'stat_id': stat_id, 'race_id': race_['id'], 'value': in_value},), key="add_trait_button"
                  )
    st.divider()
    # --------------------------------------Trait Input----------------------------------------------
    return


def link_stat_trait_to_class():
    names_from_primary_info = get_values_alchemy('classes', 'name')
    class_ = [d["name"] for d in names_from_primary_info]
    st.session_state.key = st.selectbox("Select Class", class_)
    class_ = get_class_by_name_alchemy(st.session_state.key)
    st.session_state.class_traits = get_traits_for_class(class_['id'])
    # print("char traits " + str(st.session_state.class_traits))
    st.divider()

    st.subheader("Traits")
    c_trait_info, c_trait_button_delete, c_trait_fill = st.columns([10, 2, 15])
    if st.session_state.class_traits is not None:
        for class_trait in st.session_state.class_traits:
            with c_trait_info:
                # print("race_trait   " + str(class_trait))
                filler = str(class_trait['value'])
                annotated_text(
                    annotation(str(filler), class_trait['trait_name'], font_size='25px', padding_top="16px",
                               padding_bottom="16px")
                    )
            with c_trait_button_delete:
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
                # uni_key = str(item_id) + str(active_stat['stat_id']) + "_button_" + str(uuid.uuid4())
                # print(uni_key)
                # print(f"Before button creation with key: {uni_key}")
                st.button(":wastebasket:", type="secondary", key=class_trait['trait_name'],
                          on_click=delete_trait_class_relation,
                          args=(class_trait['id'],
                                class_['id']))
                # print(f"After button creation with key: {uni_key}")
            with c_trait_fill:
                st.text("")
    # --------------------------------------Stat Input----------------------------------------------
    col_trait, col_trait_value, col_trait_button = st.columns(3)
    trait_names = get_values_alchemy('traits', 'trait_name')
    with col_trait:
        in_trait_name = st.selectbox("Trait", trait_names)
        trait_id = get_trait_id('traits', in_trait_name)
    with col_trait_value:
        in_value = st.number_input("Value", step=1, key=in_trait_name+"-2")

    with col_trait_button:
        st.markdown("""
                <style>
                .blocker {
                    font-size:0px;
                    opacity:0;
                }
                </style>
                """, unsafe_allow_html=True)

        st.markdown(f'<p class="blocker">hhuhu<p>', unsafe_allow_html=True)
        st.button(":heavy_plus_sign:", type="primary", on_click=upsert_trait_for_class, args=(
            {'trait_id': trait_id, 'class_id': class_['id'], 'value': in_value},), key=uuid.uuid4()
                  )
    st.divider()
    # --------------------------------------Stat Input----------------------------------------------
    st.session_state.class_stats = get_stats_for_class(class_['id'])
    # print("st.session_state.race_stats   ", str(st.session_state.class_stats))
    st.subheader("Stats")
    c_stat_info, c_stat_button_delete, c_stat_fill = st.columns([10, 2, 15])
    if st.session_state.class_stats is not None:
        for class_stat in st.session_state.class_stats:
            with c_stat_info:
                # print("race_stat   ", str(class_stat))
                # print(class_stat)
                filler = str(class_stat['value'])
                annotated_text(
                    annotation(str(filler), class_stat['name'], font_size='25px', padding_top="16px",
                               padding_bottom="16px")
                    )
            with c_stat_button_delete:
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
                # uni_key = str(item_id) + str(active_stat['stat_id']) + "_button_" + str(uuid.uuid4())
                # print(uni_key)
                # print(f"Before button creation with key: {uni_key}")
                st.button(":wastebasket:", type="secondary", key=class_stat['name'],
                          on_click=delete_stat_class_relation,
                          args=(class_stat['stat_id'],
                                class_['id']))
                # print(f"After button creation with key: {uni_key}")
            with c_stat_fill:
                st.text("")

    # --------------------------------------Trait Input----------------------------------------------
    col_trait, col_trait_value, col_trait_button = st.columns(3)
    stat_names = get_values_alchemy('stats', 'name')
    with col_trait:
        in_stat_name = st.selectbox("Stat", stat_names)
        stat_id = get_stat_id('stats', in_stat_name)
    with col_trait_value:
        in_value = st.number_input("Value", step=1, key=in_stat_name+"-2")

    with col_trait_button:
        st.markdown("""
                <style>
                .blocker {
                    font-size:0px;
                    opacity:0;
                }
                </style>
                """, unsafe_allow_html=True)

        st.markdown(f'<p class="blocker">hhuhu<p>', unsafe_allow_html=True)
        st.button(":heavy_plus_sign:", type="primary", on_click=upsert_stat_for_class, args=(
            {'stat_id': stat_id, 'class_id': class_['id'], 'value': in_value},), key="add_trait_button"
                  )
    st.divider()
    # --------------------------------------Trait Input----------------------------------------------
    return


def add_trait_to_character():
    names_from_primary_info = get_values_alchemy('primary_info', 'name')
    character_ = [d["name"] for d in names_from_primary_info]
    st.session_state.key = st.selectbox("Select your character", character_)
    character = get_character_by_name_alchemy(st.session_state.key)
    st.session_state.character_traits = get_traits_for_character(character['id'])
    # print("char traits " + str(st.session_state.character_traits))
    st.divider()

    c_trait_info, c_trait_button_delete, c_trait_fill = st.columns([10, 2, 15])
    if st.session_state.character_traits is not None:
        for character_trait in st.session_state.character_traits:
            with c_trait_info:
                # print(character_trait)
                filler = str(character_trait['value'])
                annotated_text(
                    annotation(str(filler), character_trait['trait_name'], font_size='25px', padding_top="16px",
                               padding_bottom="16px")
                    )
            with c_trait_button_delete:
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
                # uni_key = str(item_id) + str(active_stat['stat_id']) + "_button_" + str(uuid.uuid4())
                # print(uni_key)
                # print(f"Before button creation with key: {uni_key}")
                st.button(":wastebasket:", type="secondary", key=character_trait['trait_name'],
                          on_click=delete_trait_class_relation,
                          args=(character_trait['id'],
                                character['id']))
                # print(f"After button creation with key: {uni_key}")
            with c_trait_fill:
                st.text("")
    st.divider()
    col_trait, col_trait_value, col_trait_button = st.columns(3)
    trait_names = get_values_alchemy('traits', 'trait_name')
    trait_names = [d["trait_name"] for d in trait_names]
    with col_trait:
        in_trait_name = st.selectbox("Trait", trait_names)
        trait_id = get_trait_id('traits', in_trait_name)
    with col_trait_value:
        in_value = st.number_input("Value", step=1)

    with col_trait_button:
        st.markdown("""
        <style>
        .blocker {
            font-size:0px;
            opacity:0;
        }
        </style>
        """, unsafe_allow_html=True)

        st.markdown(f'<p class="blocker">hhuhu<p>', unsafe_allow_html=True)
        st.button(":heavy_plus_sign:", type="primary", on_click=upsert_trait_for_character, args=(
            {'trait_id': trait_id, 'character_id': character['id'], 'value': in_value},), key="add_trait_button"
                  )

def manage_user_rights():
    usernames = get_all_usernames()
    username = st.selectbox("Select user", usernames)

    is_admin = st.toggle("User/Admin", value = check_user_admin(username))
    if is_admin:
        st.write("{username} is Admin".format(username=username))
    if not is_admin:
        st.write("{username} is User.".format(username=username))
    if st.button("Set rights"):
        modify_user_admin_status(username, is_admin)


def create_timeline():
    st.title("Create Timeline")
    with st.form(key='timeline-form', clear_on_submit=True):
        media_url = st.text_input('URL to a media file')
        media_caption = st.text_input('Caption for the media file')
        media_credit = st.text_input('Credit of the media file')
        start_date_year =st.number_input("Start Year",step=1)
        text_headline = st.text_input("Headline")
        text_description = st.text_area('Description', placeholder="Enter story here...", height=250)
        is_visible = st.toggle("Should the timeline be visible?",value= True)
        # Create the submit button
        st.form_submit_button("Submit", on_click=on_submit_click)

        # If the submit button is clicked, insert the new character into the SQLite database
        if st.session_state.get('submitted', False):
            if text_headline in get_values_alchemy('Timeline', 'title_text_headline'):
                st.warning('Timeline headline already in use.')
            else:
                timeline_data = {
                    'title_media_url': media_url,
                    'title_media_caption': media_caption,
                    'title_media_credit': media_credit,
                    'title_start_date_year': start_date_year,
                    'title_text_headline': text_headline,
                    'title_text_description': text_description,
                    'created_by': st.session_state.USERNAME,
                    'visible': is_visible
                    }
                insert_data_alchemy('Timeline', timeline_data)
                st.success('Timeline created successfully!')
                st.session_state.submitted = False
                st.session_state.show_form = False
                st.toast("Timeline created successfully!", icon="✅")
                time.sleep(2)
                st.experimental_rerun()
    return


def create_event():
    st.title("Create Event")
    with st.form(key='event-form', clear_on_submit=True):
        media_url = st.text_input('URL to a media file')
        media_caption = st.text_input('Caption for the media file')
        start_date_year = st.number_input("Start Year", step=1)
        text_headline = st.text_input("Headline")
        text_description = st.text_area('Description', placeholder="Enter story here...", height=250)
        is_visible = st.toggle("Should the Event be visible for other users to add?", value=True)
        # Create the submit button
        st.form_submit_button("Submit", on_click=on_submit_click)

        # If the submit button is clicked, insert the new character into the SQLite database
        if st.session_state.get('submitted', False):
            if text_headline in get_values_alchemy('Timeline', 'title_text_headline'):
                st.warning('Timeline headline already in use.')
            else:
                event_data = {
                    'media_url': media_url,
                    'media_caption': media_caption,
                    'start_date_year': start_date_year,
                    'text_headline': text_headline,
                    'text_description': text_description,
                    'created_by': st.session_state.USERNAME,
                    'visible': is_visible
                    }
                insert_data_alchemy('Event', event_data)
                st.success('Event created successfully!')
                st.session_state.submitted = False
                st.session_state.show_form = False
                st.toast("Event created successfully!", icon="✅")
                time.sleep(2)
                st.experimental_rerun()
    return


def connect_event_timeline():
    st.title("Link Events to a Timeline")
    timelines = get_values_alchemy("Timeline", ["title_text_headline", "timeline_id"])
    st.selectbox("To which timeline do you want to add an event?", timelines)
    return

def empty_page():
    return
