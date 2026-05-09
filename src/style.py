import streamlit as st

def apply_custom_style():
    """
    Apply custom CSS to make the app feel more polished and dashboard-like.
    """
    st.markdown(
        """
        <style>
            /* Custom CSS styles */
            .stApp {
                background-color: #f0f2f5;
            }
            .stButton {
                background-color: #007bff;
                color: white;
            }
            .stButton:hover {
                background-color: #0056b3;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
