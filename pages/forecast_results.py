import streamlit as st
import pandas as pd
from darts import TimeSeries
from darts.models import NBEATSModel
from darts.utils.missing_values import fill_missing_values

# Set the page title and icon
st.set_page_config(page_title="Forecast Results", page_icon="🔍", layout="wide")

st.title("🔍 Forecast Results")

# Check if data is available in session state
if 'uploaded_data' in st.session_state:
    data = st.session_state['uploaded_data']

    # Ensure correct date format and parse dates
    if 'date' in data.columns:
        data['date'] = pd.to_datetime(data['date'], format='%d/%m/%Y', errors='coerce')
        data.dropna(subset=['date'], inplace=True)

        numeric_cols = data.select_dtypes(include=["int64", "float64"]).columns
        if len(numeric_cols) > 0:
            selected_col = st.selectbox("Select a column to forecast", numeric_cols)

            # Set date column as index and infer frequency
            data.set_index('date', inplace=True)
            data = data.asfreq('D').fillna(method='ffill')

            # Prepare the time-series data
            series = TimeSeries.from_dataframe(data, value_cols=selected_col, fill_missing_dates=True, freq="D")

            # Hugging Face model via Darts
            model = NBEATSModel(input_chunk_length=12, output_chunk_length=12, n_epochs=50)
            model.fit(series)

            # Forecast the next 12 periods
            forecast = model.predict(n=12)

            # Combine actuals and forecast
            combined_series = series.append(forecast)

            # Plot the forecast
            st.write("### Forecast Results")
            st.line_chart(combined_series.pd_dataframe())

        else:
            st.error("No numerical columns found in the uploaded file.")
    else:
        st.error("No 'date' column found in the uploaded file.")

else:
    st.warning("No data uploaded yet! Please go to the 'Data Upload' page to upload a file.")
