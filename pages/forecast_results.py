import streamlit as st
import pandas as pd
from darts import TimeSeries
from darts.models import NBEATSModel

# page title
st.set_page_config(page_title="Forecast Results", layout="wide")

st.title("🔍 Forecast Results")

# check if data exists in session state
if 'uploaded_data' in st.session_state:
    data = st.session_state['uploaded_data'].copy()  # Work with a copy to avoid modifying session state directly

    # debugging output
    st.write("Session state columns BEFORE processing:", data.columns.tolist())

    # standardize column names
    data.columns = data.columns.str.strip().str.lower()

    # check if 'date' column exists
    if 'date' not in data.columns:
        st.error("No 'date' column found in the uploaded file. Please upload a valid file with a 'date' column.")
        st.stop()

    # convert date column to datetime to ensure proper handling
    data['date'] = pd.to_datetime(data['date'], errors='coerce')
    data.dropna(subset=['date'], inplace=True)

    # convert all columns except 'date' to numeric and handle errors
    for col in data.columns:
        if col != 'date':
            data[col] = pd.to_numeric(data[col], errors='coerce')

    # drop rows where numerical values could not be converted
    data.dropna(inplace=True)

    # debugging output
    st.write("Session state columns AFTER processing:", data.columns.tolist())
    st.write("Data types after conversion:")
    st.write(data.dtypes)

    # select a numerical column for forecasting
    numeric_cols = data.select_dtypes(include=["number"]).columns

    if numeric_cols.empty:
        st.error("No valid numerical columns found in the uploaded file.")
        st.stop()

    selected_col = st.selectbox("Select a column to forecast", numeric_cols)

    # debugging output
    st.write(f"Forecasting selected column: {selected_col}")
    st.write("Data before forecasting:")
    st.dataframe(data[['date', selected_col]].head())

    # set 'date' column as index without modifying original dataframe
    if data.index.name != 'date':
        data.set_index('date', inplace=True)

    data = data.asfreq('D').fillna(method='ffill')

    # prepare the time-series data
    try:
        series = TimeSeries.from_dataframe(data, value_cols=selected_col, fill_missing_dates=True, freq="D")

        # forecasting model
        if 'model' not in st.session_state or st.session_state['selected_column'] != selected_col:
            st.session_state['selected_column'] = selected_col
            st.session_state['model'] = NBEATSModel(input_chunk_length=12, output_chunk_length=12, n_epochs=50)
            st.session_state['model'].fit(series)

        # forecast the next 12 periods
        forecast = st.session_state['model'].predict(n=12)

        # combine actuals and forecast
        combined_series = series.append(forecast)

        # convert forecast to DataFrame and store in session state
        forecast_df = combined_series.pd_dataframe().reset_index()
        forecast_df.rename(columns={'index': 'date'}, inplace=True)
        forecast_df['date'] = forecast_df['date'].dt.strftime('%Y-%m-%d')

        st.session_state['forecasted_data'] = forecast_df

        # plot the forecast
        st.write("### Forecast Results")
        st.line_chart(forecast_df.set_index('date'))

        st.success("Forecasted data is now available for export.")

    except Exception as e:
        st.error(f"Error during forecasting: {e}")

else:
    st.warning("No data uploaded yet! Please go to the 'Data Upload' page to upload a file.")
