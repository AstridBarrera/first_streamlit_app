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

# Let's put a pick list here so they can pick the fruit they want to include 
sl.multiselect("Pick some fruits ✔:", list(my_fruit_list.Index), ['Avocado', 'Strawberries', 'Coconout'])

# Display the table on the page.
sl.dataframe(my_fruit_list)
