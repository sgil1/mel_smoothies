# Import python packages
import streamlit as st
import time
import requests

# Write directly to the app
st.title("Customize your Smoothie! :cup_with_straw:")
st.write("""Choose the fruits you want in your custom Smoothie!""")

name_on_order = st.text_input('Name on Smoothie:')

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options")

ingredients_list = st.multiselect('Choose up to 5 ingredients:', 
                                  my_dataframe, 
                                  max_selections=5)

if ingredients_list:    
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    my_insert_stmt = """ insert into smoothies.public.orders(name_on_order, ingredients)
            values ('""" + name_on_order + '\',\'' + ingredients_string + """')"""

    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")