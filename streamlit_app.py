import streamlit as sl
import pandas as p
import requests
import snowflake.connector
from urllib.error import URLError 

sl.title('My Parents New Healthy Diner - by Astrid :)')
sl.header('Breakfast Favorites')
sl.text(' 🥣 Omega 3 & Blueberry Oatmeal')
sl.text(' 🥗 Kale, Spinach & Rocket Smoothie')
sl.text(' 🐔 Hard-Boiled Free-Range Egg')
sl.text(' 🥑🍞 Avocado Toast')

sl.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# import pandas as p
my_fruit_list = p.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include. Examples are case sensitive, be careful how you spell the fruits in the example
fruits_selected = sl.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
sl.dataframe(fruits_to_show) # sl.dataframe(my_fruit_list)

#Create the repeatable code block (called a function)
def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
  fruityvice_normalized = p.json_normalize(fruityvice_response.json())
  return fruityvice_normalized
  
# New Section to display fruityvice api response
sl.header('Fruityvice Fruit Advice!')
try:
  fruit_choice = sl.text_input('What fruit would you like information about?')
  if not fruit_choice:
    sl.error("Please select a fruit to get information")
  else:
     back_from_function = get_fruityvice_data(fruit_choice)
     sl.dataframe(back_from_function)
    
except URLError as e:
  sl.error()
  
#Don't run anything past here while we troubleshoot
sl.stop()

# Make a connection with the internal
# import snowflake.connector
my_cnx = snowflake.connector.connect(**sl.secrets["snowflake"])
my_cur = my_cnx.cursor()
# my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_cur.execute("Select * From fruit_load_list")
# my_data_row = my_cur.fetchone() #It only fetchs one record
my_data_rows = my_cur.fetchall()
# sl.text("The fruit load list contains:")
# sl.text(my_data_row)
sl.header("The fruit load list contains:")
# sl.dataframe(my_data_row) # when there are more records than one we have to add a S to tell it there are plural records.
sl.dataframe(my_data_rows)

# Adding a second text entry box
add_my_fruit = sl.text_input('What fruit would you like to add?')
sl.write('Thanks for adding:', add_my_fruit)

#This will not work correctly, but just go with it for now
my_cur.execute("Insert Into fruit_load_list values ('From Streamlit')")
