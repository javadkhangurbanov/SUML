import streamlit as st
import pandas as pd

# page title
st.set_page_config(page_title="Export Data", layout="wide")

st.title("📤 Export Data")

# check if forecasted data exists in session state
if 'forecasted_data' in st.session_state:
    forecasted_data = st.session_state['forecasted_data']

    st.write("### Forecasted Data Preview")
    st.dataframe(forecasted_data.head())

    # provide download link for the forecasted data
    csv_data = forecasted_data.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Forecasted Data as CSV",
        data=csv_data,
        file_name="forecasted_results.csv",
        mime="text/csv"
    )

    # option to combine original and forecasted data
    if 'uploaded_data' in st.session_state:
        original_data = st.session_state['uploaded_data'].copy()
        original_data.columns = original_data.columns.str.strip().str.lower()
        original_data['date'] = pd.to_datetime(original_data['date'], errors='coerce')

        # merge original and forecasted data
        combined_data = pd.concat([original_data, forecasted_data.set_index('date')], axis=1).reset_index()

        st.write("### Combined Original + Forecasted Data Preview")
        st.dataframe(combined_data.head())

        # provide download link for combined data
        combined_csv_data = combined_data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Combined Data as CSV",
            data=combined_csv_data,
            file_name="combined_forecasted_data.csv",
            mime="text/csv"
        )
else:
    st.warning("No forecasted data available. Please go to the 'Forecast Results' page to generate predictions.")
