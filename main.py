import streamlit as st
import pandas as pd

# Set the page title and icon
st.set_page_config(page_title="Time Series Forecasting Tool")

# Title and description for the Data Upload page
st.title("📤 Data Upload")
st.write("You can click the 'Browse files...' button below to select a .CSV file to upload and work on.")

# File upload widget
uploaded_file = st.file_uploader("Browse files...", type=["csv"])

# Submit button
if uploaded_file is not None:
    try:
        # Read the uploaded CSV file
        data = pd.read_csv(uploaded_file)

        # Check if there is a column named 'date'
        if not any(col.lower() == "date" for col in data.columns):
            st.error("No 'date' column found! Please ensure your file contains a 'date' column.")
        else:
            # Check if there is at least one numerical column
            numeric_cols = data.select_dtypes(include=["int64", "float64"]).columns
            if numeric_cols.empty:
                st.error("No numeric columns found! Please ensure your file contains at least one numerical column.")
            else:
                st.success("Found a \"date\" column")
                st.success(f"Found numerical columns: {list(numeric_cols)}")

                # Display the uploaded data
                st.write("### Uploaded Data")
                st.dataframe(data)

    except Exception as e:
        st.error(f"Error reading file: {e}")
else:
    st.warning("No data uploaded yet. Your data table will appear here after submission.")
