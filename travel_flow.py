import streamlit as st


def start_screen():

    st.subheader("Start Planning Your Trip")

    choice = st.radio(
        "Choose an option",
        [
            "I already know my destination",
            "Get travel suggestions"
        ]
    )

    if st.button("Continue"):

        if choice == "I already know my destination":
            st.session_state.step = "destination"
        else:
            st.session_state.step = "scope"

        st.rerun()
        