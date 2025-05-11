import pandas as pd
import streamlit as st
import io

def process_csv_data(csv_file):
    """
    Process CSV data containing soil characteristics by address.
    
    Args:
        csv_file: Uploaded CSV file object
        
    Returns:
        pandas.DataFrame: Processed CSV data
    """
    try:
        # Read CSV file
        df = pd.read_csv(csv_file)
        
        # Basic data cleaning
        df = clean_csv_data(df)
        
        return df
    except Exception as e:
        st.error(f"Error processing CSV file: {str(e)}")
        return None

def clean_csv_data(df):
    """
    Clean the CSV data.
    
    Args:
        df (pandas.DataFrame): Original dataframe
        
    Returns:
        pandas.DataFrame: Cleaned dataframe
    """
    # Make a copy to avoid modifying the original
    cleaned_df = df.copy()
    
    # Convert column names to lowercase and replace spaces with underscores
    cleaned_df.columns = [col.lower().replace(' ', '_') for col in cleaned_df.columns]
    
    # Handle missing values
    for col in cleaned_df.columns:
        # For numeric columns, fill NaN with median
        if pd.api.types.is_numeric_dtype(cleaned_df[col]):
            cleaned_df[col] = cleaned_df[col].fillna(cleaned_df[col].median())
        # For string columns, fill NaN with "Unknown"
        else:
            cleaned_df[col] = cleaned_df[col].fillna("Unknown")
    
    return cleaned_df

def get_soil_data_by_address(df, address_query):
    """
    Search for soil data by address in the CSV data.
    
    Args:
        df (pandas.DataFrame): The CSV data
        address_query (str): Address query string
        
    Returns:
        pandas.DataFrame: Filtered dataframe containing matching rows
    """
    if df is None:
        return None
    
    # Identify address columns
    address_cols = [col for col in df.columns if 
                    any(term in col for term in ['address', 'location', 'site', 'place'])]
    
    # If no specific address columns found, search all string columns
    if not address_cols:
        address_cols = [col for col in df.columns if pd.api.types.is_string_dtype(df[col])]
    
    # Create a mask for matching rows
    mask = pd.Series(False, index=df.index)
    
    # Search for the address query in each address column
    for col in address_cols:
        mask = mask | df[col].astype(str).str.contains(address_query, case=False, na=False)
    
    # Return the filtered dataframe
    return df[mask]

def summarize_csv_data(df):
    """
    Generate a summary of the CSV data.
    
    Args:
        df (pandas.DataFrame): The CSV data
        
    Returns:
        str: Text summary of the CSV data
    """
    if df is None:
        return "No CSV data available."
    
    # Create a summary text
    summary = f"CSV Data Summary:\n"
    summary += f"Total records: {len(df)}\n"
    summary += f"Columns: {', '.join(df.columns)}\n\n"
    
    # Add basic statistics for numeric columns
    numeric_cols = df.select_dtypes(include=['number']).columns
    if len(numeric_cols) > 0:
        summary += "Numeric Column Statistics:\n"
        for col in numeric_cols:
            summary += f"  {col}:\n"
            summary += f"    Mean: {df[col].mean():.2f}\n"
            summary += f"    Min: {df[col].min():.2f}\n"
            summary += f"    Max: {df[col].max():.2f}\n"
    
    # Add value counts for categorical columns (top 5 values)
    categorical_cols = df.select_dtypes(include=['object']).columns
    if len(categorical_cols) > 0:
        summary += "\nCategorical Column Top Values:\n"
        for col in categorical_cols:
            summary += f"  {col}:\n"
            for value, count in df[col].value_counts().head(5).items():
                summary += f"    {value}: {count}\n"
    
    return summary
