import streamlit as st


def apply_custom_style():
    """
    Apply light CSS polish to the app without overriding Streamlit's built-in themes.

    All colors here use rgba() with low opacity so the styles work correctly in
    both Streamlit light mode and dark mode. No hardcoded background or text colors
    are set — this keeps the theme switcher working as expected.
    """
    st.markdown(
        """
        <style>
        /* Page spacing */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1400px;
        }

        /* Headings */
        h1 {
            font-weight: 800 !important;
            letter-spacing: -0.04em;
            margin-bottom: 0.4rem;
        }

        h2, h3 {
            font-weight: 700 !important;
            letter-spacing: -0.03em;
        }

        /* Metric cards: use theme variables instead of fixed colors */
        [data-testid="stMetric"] {
            padding: 1rem;
            border-radius: 16px;
            border: 1px solid rgba(128, 128, 128, 0.25);
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
        }

        [data-testid="stMetricLabel"] {
            font-size: 0.85rem;
        }

        [data-testid="stMetricValue"] {
            font-weight: 750;
        }

        /* Dataframes */
        div[data-testid="stDataFrame"] {
            border-radius: 14px;
            overflow: hidden;
            border: 1px solid rgba(128, 128, 128, 0.22);
        }

        /* Buttons */
        .stButton > button {
            border-radius: 12px;
            border: 1px solid rgba(128, 128, 128, 0.35);
            font-weight: 600;
        }

        .stButton > button:hover {
            border-color: rgba(59, 130, 246, 0.9);
        }

        /* Inputs */
        .stTextInput input,
        .stNumberInput input,
        .stTextArea textarea,
        .stDateInput input {
            border-radius: 12px;
        }

        /* Expanders */
        [data-testid="stExpander"] {
            border-radius: 14px;
            border: 1px solid rgba(128, 128, 128, 0.25);
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            border-right: 1px solid rgba(128, 128, 128, 0.18);
        }
        </style>
        """,
        unsafe_allow_html=True
    )
