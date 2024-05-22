import streamlit as st
import pandas as pd
from io import BytesIO

def data_cleanse(df):
    # Convert empty strings to NaN for easier handling
    df.replace("", pd.NA, inplace=True)
    
    # Define the columns to check based on their actual names
    cols_to_check = ['Form template', 'Form_instance_ID', 'Form template version']
    
    # Iterate over the rows and columns
    for col in cols_to_check:
        for i in range(1, len(df)):
            if pd.isna(df.at[i, col]):
                # Check if the corresponding cell in column 'Client name' is not empty
                if not pd.isna(df.at[i, 'Client name']):
                    # Fill the blank cell with the value from the cell above
                    df.at[i, col] = df.at[i-1, col]

    return df

def main():
    st.title("Valid8ME Data Cleanse")
    
    # File uploader widget
    uploaded_file = st.file_uploader("Upload Valid8Me Output", type=['xlsx'])
    
    if uploaded_file is not None:
        # Load the data from the uploaded Excel file
        df = pd.read_excel(uploaded_file)
        
        st.write("Before cleaning:")
        st.write(df)
        
        # "Clean Data" button
        if st.button("Clean Data"):
            # Clean the data
            cleaned_df = data_cleanse(df)
            
            st.write("After cleaning:")
            st.write(cleaned_df)
            
            # Save the cleaned data to a CSV file
            cleaned_file = "Valid8MeOutPut-clean.csv"
            cleaned_df.to_csv(cleaned_file, index=False)
            
            # Provide a downloadable link for the cleaned CSV file
            csv_data = cleaned_df.to_csv(index=False).encode('utf-8')
            st.download_button(label="Download Cleaned CSV", data=csv_data, file_name=cleaned_file, mime="text/csv")

if __name__ == "__main__":
    main()
