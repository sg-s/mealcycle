"""core app to run mealcycle"""

import datetime
import os

import pandas as pd

import streamlit as st

st.write("# Mealcycle")


if "new_meal_name" not in st.session_state:
    st.session_state.new_meal_name = ""


def load_df() -> pd.DataFrame:
    """read data from disk"""
    if os.path.exists("data.pq"):
        df = pd.read_parquet("data.pq")
    else:
        df = pd.DataFrame(dict(thing=[], last_done=[]))
    return df


def add_new(new_name=None) -> None:
    """add new entry to dataframe"""

    if new_name is None:
        print("new_name is None, reading from session state")
        new_name = st.session_state.new_meal_name
        st.session_state.new_meal_name = ""

    new_time = pd.Timestamp(datetime.datetime.now())

    new_row = pd.DataFrame(dict(thing=new_name, last_done=new_time), index=[0])
    df = pd.concat((load_df(), new_row))

    df.to_parquet("data.pq")


# figure out when each item was last cooked
df = load_df().groupby("thing", as_index=False).max()
df = df.sort_values("last_done", ascending=True)

st.write("------------")


# make buttons for each item
for thing in df["thing"]:
    st.button(thing, on_click=add_new, args=(thing,))


st.write("------------")


# make some UI elements to add new items
left, right = st.columns([0.8, 0.2])

with left:
    new_meal = st.text_input("Add new meal", key="new_meal_name")

with right:
    st.write("")
    st.write("")
    st.button("Add", type="primary", on_click=add_new)
