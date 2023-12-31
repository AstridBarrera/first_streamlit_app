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
#sl.stop() --For testing

# Make a connection with the internal
# import snowflake.connector

# sl.text("The fruit load list contains:")
sl.header("View Our Fruit List - Add Your Favorites!")
#Snowflake-related functions
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    # my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
    my_cur.execute("Select * From fruit_load_list")
    # my_data_row = my_cur.fetchone() #It only fetchs one record
    return my_cur.fetchall()
    my_cnx.close()

# Adding a second text entry box - Allow the end user to add a fruit to the list
def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("Insert Into fruit_load_list values ('" + add_my_fruit +"')")
    return "Thanks for adding:" + new_fruit
    
add_my_fruit = sl.text_input('What fruit would you like to add?')
#Add a button to load the fruit
if sl.button('Get the Fruit list'):
  my_cnx = snowflake.connector.connect(**sl.secrets["snowflake"])
  # sl.dataframe(my_data_row) # when there are more records than one we have to add a S to tell it there are plural records.
  # sl.text(my_data_row)
  back_from_function = insert_row_snowflake(add_my_fruit)
  my_cnx.close()
  sl.text(back_from_function)




