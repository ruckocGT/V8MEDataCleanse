import streamlit as st
import pandas as pd
from io import BytesIO

def data_cleanse(df):
    # Define the column indices to check (0-based index, so 0 to 9 corresponds to columns A to K, excluding index 3)
    cols_to_check = [0, 1, 2, 4, 5, 6, 7, 8, 9]  # Exclude index 3 (column D)
    
    # Iterate over the rows and columns
    for col in cols_to_check:
        for i in range(1, len(df)):
            if pd.isna(df.iat[i, col]):
                # Fill the blank cell with the value from the cell above
                df.iat[i, col] = df.iat[i-1, col]
    return df

def main():
    st.title("Valid8ME Data Cleanse")
    
    # File uploader widget
    uploaded_file = st.file_uploader("Upload Valid8Me Output", type=['xlsx'])
    
    if uploaded_file is not None:
        # Load the data from the uploaded Excel file
        df = pd.read_excel(uploaded_file)
        
        st.write("Before cleaning:")
        st.write(df.head(20))  # Displaying the first 20 rows for inspection
        
        # "Clean Data" button
        if st.button("Clean Data"):
            # Clean the data
            cleaned_df = data_cleanse(df)
            
            st.write("After cleaning:")
            st.write(cleaned_df.head(20))  # Displaying the first 20 rows for inspection
            
            # Save the cleaned data to a BytesIO object as Excel
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                cleaned_df.to_excel(writer, index=False, sheet_name='Sheet1')
                writer.save()
            output.seek(0)
            
            # Provide a downloadable link for the cleaned Excel file
            st.download_button(label="Download Cleaned Excel", data=output, file_name="Valid8MeOutput-clean.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

if __name__ == "__main__":
    main()
