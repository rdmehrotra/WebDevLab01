import streamlit as st
import pandas as pd
import json
import os

st.title("welcome to the jungle 🌴🌴🌴")

with open("data/data.json") as file:
    data = json.load(file)

tab1, tab2, tab3 = st.tabs(["NYT Mini Crossword", "Baking Ratings", "Book Ratings"])

with tab1:
    st.subheader("Rohan's Mini Crossword Speed Over Time")

    with st.expander("CLICK ME to learn more about this graph!!"):
        st.write("""
        What started out as a New Year's resolution to do the New York Times Mini Crossword every day, even if that meant in class 🙃, eventually turned into a personal challenge where I aim to speedrun it as fast as I can.

        As of June 2025, my average that I calculated is **50 seconds**. Not bad, but I can do even better!
        """)

    df = pd.DataFrame(data["crossword_times"], columns=["month", "seconds"])
    df["month"] = pd.to_datetime(df["month"])
    df = df.sort_values("month")

    st.subheader("How many months do you want to see?")
    count = st.slider("Months to display:", 1, len(df), len(df))
    chart_data = df.tail(count)

    st.subheader("📉 Time Taken to Complete NYT Mini Crossword")
    st.line_chart(chart_data.set_index("month")["seconds"])


with tab2:
    st.subheader("My Family’s Ratings of My Baking")

    with st.expander("CLICK ME to learn more about this graph!!"):
        st.write(
            "Ever since I was a little kid I **LOVED** baking. My family however, not so much. "
            "Over the years I've gotten them to enjoy more and more of my creations, even when both my parents are diabetic..."
        )
        st.image("images/baby_me.jpeg", width=250)

    bake_df = pd.DataFrame(data["baking_ratings"]).sort_values("year")
    bake_df["year"] = bake_df["year"].astype(str)

    st.subheader("How many years do you want to see?")
    count_years = st.slider("Years to display in graph:", 1, len(bake_df), len(bake_df))
    chart_data = bake_df.tail(count_years)
    st.line_chart(chart_data.set_index("year")["rating"])

    st.subheader("Pick a year to see that bake:")
    year_choices = list(bake_df["year"])
    selected_year = st.select_slider("Choose year for photo:", options=year_choices, value="2015")

    row = bake_df[bake_df["year"] == selected_year].iloc[0]
    st.markdown(f"**{row['caption']}**")
    st.image(os.path.join("images", row["image"]), width=300)
    st.markdown(f"### ⭐ Family Rating for {selected_year}: **{row['rating']} / 10**")


    st.subheader("Mark your favorite bake based on the year")
    fav = st.selectbox("Pick your favorite year:", year_choices)

    if st.button("Save Favorite"):
        st.session_state["favorite_bake_year"] = fav

    if "favorite_bake_year" in st.session_state:
        st.success(f"Your favorite bake year is **{st.session_state.favorite_bake_year}**")



with tab3:
    st.subheader("Books I've Read in 2025 and My Ratings")

    book_df = pd.DataFrame(data["book_ratings_2025"])
    st.bar_chart(book_df.set_index("title")["rating"])

    st.subheader("Have you heard of these books before?")

    heard_yes = st.checkbox("Yes", key="heard_yes")
    heard_no = st.checkbox("No", key="heard_no")

    if st.button("Save Response"):
        if heard_yes and not heard_no:
            st.session_state["heard_response"] = "yes"
        elif heard_no and not heard_yes:
            st.session_state["heard_response"] = "no"
        elif heard_yes and heard_no:
            st.session_state["heard_response"] = "both"
        else:
            st.session_state["heard_response"] = "none"

    if "heard_response" in st.session_state:
        if st.session_state["heard_response"] == "yes":
            st.success("Awesome, happy to hear that :)")
        elif st.session_state["heard_response"] == "no":
            st.info("No worries, I reccomend all of them!")
        elif st.session_state["heard_response"] == "both":
            st.warning("Hmm...did you mean to say both? lol")
        elif st.session_state["heard_response"] == "none":
            st.error("Hold up...u didn't select anything")
