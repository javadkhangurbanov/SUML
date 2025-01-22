import streamlit as st
import pandas as pd

# Page title
st.set_page_config(page_title="Time Series Forecasting Tool")

# Title and description
st.title("📤 Data Upload")
st.write("You can click the 'Browse files...' button below to select a .CSV file to upload and work on.")

# File upload
uploaded_file = st.file_uploader("Browse files...", type=["csv"])

# File submission
if uploaded_file is not None:
    try:
        # Read file and clean column names
        data = pd.read_csv(uploaded_file)
        data.columns = data.columns.str.strip().str.lower()  # Standardize column names

        # Check if 'date' column exists
        if 'date' not in data.columns:
            st.error("No 'date' column found! Please ensure your file contains a 'date' column.")
        else:
            # Convert date column and drop invalid entries
            data['date'] = pd.to_datetime(data['date'], format='%d/%m/%Y', errors='coerce')
            data.dropna(subset=['date'], inplace=True)

            # Check for numerical columns
            numeric_cols = data.select_dtypes(include=["int64", "float64"]).columns
            if numeric_cols.empty:
                st.error("No numeric columns found! Please ensure your file contains at least one numerical column.")
            else:
                st.success("Found a \"date\" column")
                st.success(f"Found numerical columns: {list(numeric_cols)}")

                # Store the cleaned data in session state
                st.session_state['uploaded_data'] = data

                # Display the cleaned uploaded data
                st.write("### Uploaded Data")
                st.dataframe(data)

    except Exception as e:
        st.error(f"Error reading file: {e}")

# If data already exists in session state, show it
elif 'uploaded_data' in st.session_state:
    st.success("Data has been previously uploaded and is available.")
    st.write("### Uploaded Data")
    st.dataframe(st.session_state['uploaded_data'])

else:
    st.warning("No data uploaded yet. Your data table will appear here after submission.")
