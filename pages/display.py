import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# page title
st.set_page_config(page_title="Display Data", layout="wide")

st.title("📊 Display Data")

# check if data exists in session state
if 'uploaded_data' in st.session_state:
    data = st.session_state['uploaded_data'].copy()

    # standardize column names
    data.columns = data.columns.str.strip().str.lower()

    # check if 'date' column exists
    if 'date' not in data.columns:
        st.error("No 'date' column found in the uploaded file. Please upload a valid file with a 'date' column.")
        st.stop()

    # convert date column to datetime
    data['date'] = pd.to_datetime(data['date'], errors='coerce')
    data.dropna(subset=['date'], inplace=True)

    # set date column as index for visualization
    if data.index.name != 'date':
        data.set_index('date', inplace=True)

    # select numerical columns for display
    numeric_cols = data.select_dtypes(include=["number"]).columns

    if numeric_cols.empty:
        st.error("No valid numerical columns found in the uploaded file.")
        st.stop()

    # user selection for columns to display
    selected_cols = st.multiselect("Select columns to visualize", numeric_cols, default=numeric_cols[:1])

    if not selected_cols:
        st.warning("Please select at least one column to display.")
    else:
        # display the selected data
        st.write("### Selected Data Preview")
        st.dataframe(data[selected_cols].head())

        # plot the selected data
        st.write("### Data Visualization")

        fig, ax = plt.subplots(figsize=(12, 6))
        data[selected_cols].plot(ax=ax)
        plt.xlabel("Date")
        plt.ylabel("Values")
        plt.title("Time Series Data Visualization")
        plt.grid(True)

        st.pyplot(fig)

else:
    st.warning("No data uploaded yet! Please go to the 'Data Upload' page to upload a file.")
