import streamlit as st

def apply_custom_style():
    """
    Apply custom CSS to make the app feel more polished and dashboard-like.
    """
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(135deg, #0f1117 0%, #111827 50%, #0b1120 100%);
            color: #f9fafb;
        }

        h1 {
            font-size: 3rem !important;
            font-weight: 800 !important;
            letter-spacing: -0.04em;
        }

        h2, h3 {
            letter-spacing: -0.03em;
        }

        [data-testid="stSidebar"] {
            background-color: #0b1120;
            border-right: 1px solid #1f2937;
        }

        [data-testid="stMetric"] {
            background-color: rgba(17, 24, 39, 0.85);
            border: 1px solid #273244;
            padding: 1rem;
            border-radius: 18px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.25);
        }

        div[data-testid="stDataFrame"] {
            border-radius: 16px;
            overflow: hidden;
            border: 1px solid #273244;
        }

        

        
        """
    )
