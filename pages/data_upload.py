import streamlit as st
import pandas as pd

# page title
st.set_page_config(page_title="Time Series Forecasting Tool")

# title and description
st.title("📤 Data Upload")
st.write("You can click the 'Browse files...' button below to select a .CSV file to upload and work on.")

# file upload
uploaded_file = st.file_uploader("Browse files...", type=["csv"])

# file submission
if uploaded_file is not None:
    try:
        # read file
        data = pd.read_csv(uploaded_file)

        # standardize column names
        data.columns = data.columns.str.strip().str.lower()

        # check if 'date' column exists
        if 'date' not in data.columns:
            st.error("No 'date' column found! Please ensure your file contains a 'date' column.")
        else:
            # convert date column and drop invalid entries
            data['date'] = pd.to_datetime(data['date'], format='%d/%m/%Y', errors='coerce')
            data.dropna(subset=['date'], inplace=True)

            # at least one column with numerical values
            numeric_cols = data.select_dtypes(include=["int64", "float64"]).columns
            if numeric_cols.empty:
                st.error("No numeric columns found! Please ensure your file contains at least one numerical column.")
            else:
                st.success("Found a \"date\" column")
                st.success(f"Found numerical columns: {list(numeric_cols)}")

                # store the cleaned data in session state
                st.session_state['uploaded_data'] = data

                # display the cleaned uploaded data
                st.write("### Uploaded Data")
                st.dataframe(data)

    except Exception as e:
        st.error(f"Error reading file: {e}")

# if data already exists in session state, show it
elif 'uploaded_data' in st.session_state:
    st.success("Data has been previously uploaded and is available.")
    st.write("### Uploaded Data")
    st.dataframe(st.session_state['uploaded_data'])

else:
    st.warning("No data uploaded yet. Your data table will appear here after submission.")
