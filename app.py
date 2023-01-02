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


def add_new(new_name=None, new_recipe_link=None) -> None:
    """add new entry to dataframe"""

    if new_name is None:
        new_name = st.session_state.new_meal_name
        st.session_state.new_meal_name = ""

    if new_recipe_link is None:
        new_recipe_link = st.session_state.new_meal_recipe
        st.session_state.new_meal_recipe = ""

    new_time = pd.Timestamp(datetime.datetime.now())

    new_row = pd.DataFrame(
        dict(
            thing=new_name,
            last_done=new_time,
            recipe_link=new_recipe_link,
        ),
        index=[0],
    )
    df = pd.concat((load_df(), new_row))

    df.to_parquet("data.pq")


# figure out when each item was last cooked
df = load_df().groupby("thing", as_index=False).max()
df = df.sort_values("last_done", ascending=True)

st.write("------------")

# make buttons for each item
for thing, recipe_link in zip(df["thing"], df["recipe_link"]):
    with st.container():
        st.write("## " + thing)
        left, right = st.columns(2)
        with left:
            if len(recipe_link) > 0:
                st.markdown(f"[Recipe]({recipe_link})")
        with right:
            st.button("cooked ✅", on_click=add_new, args=(thing,), key=thing)
        st.write("------------")


# make some UI elements to add new items
left, center, right = st.columns([0.4, 0.4, 0.2])

with left:
    new_meal = st.text_input(
        "Add new meal", key="new_meal_name", placeholder="Meal name"
    )

with center:
    new_meal_recipe = st.text_input(
        "", key="new_meal_recipe", placeholder="Link to recipe"
    )

with right:
    st.write("")
    st.write("")
    st.button("Add", type="primary", on_click=add_new)
