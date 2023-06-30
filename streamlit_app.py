import streamlit as sl

sl.title('My Parents New Healthy Diner - by Astrid :)')

sl.header('Breakfast Favorites')
sl.text(' 🥣 Omega 3 & Blueberry Oatmeal')
sl.text(' 🥗 Kale, Spinach & Rocket Smoothie')
sl.text(' 🐔 Hard-Boiled Free-Range Egg')
sl.text(' 🥑🍞 Avocado Toast')

sl.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

import pandas as p
my_fruit_list = p.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include. Examples are case sensitive, be careful how you spell the fruits in the example
fruits_selected = sl.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
sl.dataframe(fruits_to_show) # sl.dataframe(my_fruit_list)

# New Section to display fruityvice api response
sl.header('Fruityvice Fruit Advice!')
fruit_choice = sl.text_input('What fruit would you like information about?', 'Kiwi')
sl.write('The user entered', fruit_choice)

import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
# sl.text(fruityvice_response.json())

# Take the json version of the response and normalize it
fruityvice_normalized = p.json_normalize(fruityvice_response.json())
# Shows the list as a table in the screen
sl.dataframe(fruityvice_normalized)

import snowflake.connector
