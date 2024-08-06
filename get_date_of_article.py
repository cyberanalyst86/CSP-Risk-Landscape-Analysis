import requests
from bs4 import BeautifulSoup
import dateparser
import pandas as pd
import datetime
import re

def extract_date(date_string):

    date_pattern = r'\d{4}-\d{2}-\d{2}'
    match = re.search(date_pattern, date_string)
    if match:

        date_object = datetime.datetime.strptime(str(match.group(0)), "%Y-%m-%d")
        formatted_date = date_object.strftime("%d/%m/%Y")

        return formatted_date
    else:
        return None

def extract_date_from_url(url):
    """Extracts the date from an internet article given a URL.

    Args:
        url (str): The URL of the article.

    Returns:
        datetime.datetime or None: The extracted date as a datetime object or None if not found.
    """

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for error HTTP statuses
        soup = BeautifulSoup(response.content, 'html.parser')

        # Potential date elements (adjust based on website structure)
        date_elements = [
            soup.find('meta', {'property': 'article:published_time'}),
            soup.find('time'),
            soup.find('meta', {'name': 'publish_date'}),
            # Add more elements as needed
        ]

        for element in date_elements:
            if element:
                date_str = element.get('content') or element.text.strip()
                try:
                    return dateparser.parse(date_str)
                except ValueError:
                    pass

        # If no date found, you can try more complex logic or heuristics
        # For example, searching for specific text patterns or using NLP techniques

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
    except ValueError as e:
        print(f"Error parsing date: {e}")

    return None

def get_date_of_article(df):

    url_list = df["url"].to_list()

    query_date_list = []

    for url in url_list:

        #print(url)
        date = extract_date_from_url(url)
        if date:

            processed_date = extract_date(str(date))

            query_date_list.append(processed_date)
        else:
            query_date_list.append("Error")

    df["article date"] = query_date_list

    return df