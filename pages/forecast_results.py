import streamlit as st
import pandas as pd
from darts import TimeSeries
from darts.models import NBEATSModel
from darts.utils.timeseries_generation import datetime_attribute_timeseries
from darts.utils.missing_values import fill_missing_values

# page title
st.set_page_config(page_title="Forecast Results", layout="wide")

# title and description
st.title("🔍 Forecast Results")
st.write("Upload your time-series data to generate simple forecast results.")

# file submission
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        # read file
        data = pd.read_csv(uploaded_file)

        # check if file has a column named "date"
        if any(col.lower() == "date" for col in data.columns):
            date_col = 'date'
            numeric_cols = data.select_dtypes(include=["int64", "float64"]).columns

            if len(numeric_cols) > 0:
                selected_col = st.selectbox("Select a column to forecast", numeric_cols)

                # convert the date column to datetime
                data[date_col] = pd.to_datetime(data[date_col])

                # set the date column as the index
                data.set_index(date_col, inplace=True)

                # prepare the time-series data
                series = TimeSeries.from_dataframe(data, value_cols=selected_col)
                series = fill_missing_values(series)

                # the hugging face modwl from darts
                model = NBEATSModel(input_chunk_length=12, output_chunk_length=12, n_epochs=50)
                model.fit(series)

                # forecasting the next 12 periods
                forecast = model.predict(n=12)

                # combine actual data with forecasted data
                combined_series = series.append(forecast)

                # plot the forecasted data
                st.write("### Forecast Results")
                st.line_chart(combined_series.pd_dataframe())

            else:
                st.error("No numerical columns found in the uploaded file.")
        else:
            for col in data.columns:
                print(col.lower())
            st.error("No 'date' column found in the uploaded file.")

    except Exception as e:
        st.error(f"Error processing the file: {e}")
else:
    st.info("Please upload a CSV file to start forecasting.")
