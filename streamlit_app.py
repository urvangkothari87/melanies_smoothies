# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie!"""
)
# option = st.selectbox('How would you like to be contacted?',
#                      ('Email', 'Home Phone', 'Mobile Phone')
#                      )
# option = st.selectbox('What is your favorite fruit?',
#                      ('Banana', 'Strawberries', 'Peaches')
#                      )
# st.write('Your favorite fruit is', option)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your smoothie will be', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect('Choose up to 5 ingredients:', my_dataframe, max_selections=5)

if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)
    
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
    
    st.write(ingredients_string)

    insert_stmt = f"Insert Into smoothies.public.orders (ingredients, NAME_ON_ORDER) values ('{ingredients_string}', '{name_on_order}')"

    # st.write(insert_stmt)

    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(insert_stmt).collect()

        st.success('Your Smoothie is ordered!', icon='✅')


fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
st.text(fruityvice_response)
    

