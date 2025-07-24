import pandas as pd
import re

def create_timeline(scraped_data):
    """
    Creates a timeline from scraped data.

    Args:
        scraped_data (list): A list of text paragraphs.

    Returns:
        pd.DataFrame: A DataFrame with "timestamp" and "text" columns,
                      sorted by timestamp.
    """
    df = pd.DataFrame(scraped_data, columns=["text"])
    df["timestamp"] = df["text"].apply(extract_date)
    df = df[df["timestamp"].notna()]
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values(by="timestamp").reset_index(drop=True)
    return df

def extract_date(text):
    """
    Extracts a date from a string using various regex patterns.

    Args:
        text (str): The string to extract the date from.

    Returns:
        str: The extracted date in YYYY-MM-DD format, or None if no date is found.
    """
    # YYYY-MM-DD
    match = re.search(r'\b\d{4}-\d{2}-\d{2}\b', text)
    if match:
        return match.group(0)
    # MM/DD/YYYY
    match = re.search(r'\b\d{1,2}/\d{1,2}/\d{4}\b', text)
    if match:
        return pd.to_datetime(match.group(0)).strftime('%Y-%m-%d')
    # Month Day, Year
    match = re.search(r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2}, \d{4}\b', text, re.IGNORECASE)
    if match:
        return pd.to_datetime(match.group(0)).strftime('%Y-%m-%d')
    return None
