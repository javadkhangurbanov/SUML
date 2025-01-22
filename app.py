import streamlit as st

# page title
st.set_page_config(page_title="Time Series Forecasting Tool", layout="wide")

# main page layout
st.title("📊 Time Series Forecasting Tool")

# css styling
st.markdown("""
    <style>
        div[data-testid="stButton"] {
            display: flex;
            justify-content: center;
            align-items: center;
        }
        div[data-testid="column"] > div {
            width: 100%;
        }
        button[data-testid="stBaseButton-secondary"] {
            padding: 5rem 5rem;
        }
        button[data-testid="stBaseButton-secondary"] p {
            font-size: 1.5rem;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# column containers for buttons
col1, col2 = st.columns(2)

# list of pages
pages = {
    "Data Upload": "pages/data_upload.py",
    "Display": "pages/display.py",
    "Export Data": "pages/export_data.py",
    "Forecast Results": "pages/forecast_results.py"
}

# column 1 buttons
with col1:
    if st.button("📤 Data Upload"):
        st.switch_page(pages["Data Upload"])

    if st.button("🔍 Forecast Results"):
        st.switch_page(pages["Forecast Results"])

# column 2 buttons
with col2:
    if st.button("📊 Display"):
        st.switch_page(pages["Display"])

    if st.button("📤 Export Data"):
        st.switch_page(pages["Export Data"])

# show success message if data exists in session state
if 'uploaded_data' in st.session_state:
    st.success("Data has been uploaded and is accessible across pages.")

# footer
st.write("---")
st.write("Navigate to any page by clicking the buttons above.")
