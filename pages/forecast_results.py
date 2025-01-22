import streamlit as st
import pandas as pd
from darts import TimeSeries
from darts.models import NBEATSModel

# Set the page title and icon
st.set_page_config(page_title="Forecast Results", page_icon="🔍", layout="wide")

st.title("🔍 Forecast Results")

# Check if data exists in session state
if 'uploaded_data' in st.session_state:
    data = st.session_state['uploaded_data'].copy()  # Work with a copy to avoid modifying session state directly

    # Debugging output
    st.write("Session state columns BEFORE processing:", data.columns.tolist())

    # Standardize column names
    data.columns = data.columns.str.strip().str.lower()

    # Check if 'date' column exists
    if 'date' not in data.columns:
        st.error("No 'date' column found in the uploaded file. Please upload a valid file with a 'date' column.")
        st.stop()

    # Convert date column to datetime to ensure proper handling
    data['date'] = pd.to_datetime(data['date'], errors='coerce')
    data.dropna(subset=['date'], inplace=True)

    # Convert all columns except 'date' to numeric and handle errors
    for col in data.columns:
        if col != 'date':
            data[col] = pd.to_numeric(data[col], errors='coerce')

    # Drop rows where numerical values could not be converted
    data.dropna(inplace=True)

    # Debugging output
    st.write("Session state columns AFTER processing:", data.columns.tolist())
    st.write("Data types after conversion:")
    st.write(data.dtypes)

    # Select a numerical column for forecasting
    numeric_cols = data.select_dtypes(include=["number"]).columns

    if numeric_cols.empty:
        st.error("No valid numerical columns found in the uploaded file.")
        st.stop()

    selected_col = st.selectbox("Select a column to forecast", numeric_cols)

    # Debugging output
    st.write(f"Forecasting selected column: {selected_col}")
    st.write("Data before forecasting:")
    st.dataframe(data[[selected_col]].head())

    # Set 'date' column as index without modifying original dataframe
    if data.index.name != 'date':
        data.set_index('date', inplace=True)

    data = data.asfreq('D').fillna(method='ffill')

    # Prepare the time-series data
    try:
        series = TimeSeries.from_dataframe(data, value_cols=selected_col, fill_missing_dates=True, freq="D")

        # Forecasting model
        if 'model' not in st.session_state or st.session_state['selected_column'] != selected_col:
            st.session_state['selected_column'] = selected_col
            st.session_state['model'] = NBEATSModel(input_chunk_length=12, output_chunk_length=12, n_epochs=50)
            st.session_state['model'].fit(series)

        # Forecast the next 12 periods
        forecast = st.session_state['model'].predict(n=12)

        # Combine actuals and forecast
        combined_series = series.append(forecast)

        # Plot the forecast
        st.write("### Forecast Results")
        st.line_chart(combined_series.pd_dataframe())

    except Exception as e:
        st.error(f"Error during forecasting: {e}")

else:
    st.warning("No data uploaded yet! Please go to the 'Data Upload' page to upload a file.")
