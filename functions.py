import os
from groq import Groq

import os
from groq import Groq
import pandas as pd
api_key="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"
# Initialize the Groq client
client = Groq(
    api_key=api_key,  # Replace with your actual API key
)

# Function to format the event name
def format_event_name(event_name):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "Your task is to format event names in proper title case, ensuring correct spelling and punctuation. Only return the formatted name without any extra explanation."
            },
            {
                "role": "user",
                "content": f"Format the event name: {event_name}"
            }
        ],
        model="llama3-70b-8192",
    )
    return chat_completion.choices[0].message.content.strip()

def format_date_and_time(date_str):
    # Call the Groq API to generate a response
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": """
                    Your task is to convert date and time in any format into a standardized format: 
                    YYYY-MM-DD HH:MM:SS. If a range of time or date is provided, format both the start and end dates and times accordingly.
                    - If there is a time range (e.g., 6:30 p.m. - 8:00 p.m.), format it as 'YYYY-MM-DD HH:MM:SS-HH:MM:SS'.
                    - If no time is given but only a date, output the date in the format 'YYYY-MM-DD'.
                    - Handle ambiguous formats, e.g., date ranges or times with time zones, and standardize them.
                    Do not include extra explanations. Only return the formatted date and time.
                """
            },
            {
                "role": "user",
                "content": f"Format the date and time: {date_str}"
            }
        ],
        model="llama3-70b-8192",  # or any other model you are using
    )
    
    # Adjust based on Groq's response structure
    # Assuming Groq's response is structured like OpenAI's, this should work:
    try:
        print("Done")
        return chat_completion['choices'][0]['message']['content'].strip()
    except (KeyError, IndexError):
        # If there's an error with the structure, print the full response for inspection
        print("Error with response format:")
        print(chat_completion)
        return None

# Function to format the event description
def format_description(description):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "Your task is to ensure the event description is concise, well-structured, and free from grammatical errors. Only return the formatted description, no extra details."
            },
            {
                "role": "user",
                "content": f"Format the event description: {description}"
            }
        ],
        model="llama3-70b-8192",
    )
    return chat_completion.choices[0].message.content.strip()

# Function to format the event location
def format_location(location):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "Your task is to standardize event locations, ensuring city, state, and country (if available) are correctly formatted. Only return the formatted location."
            },
            {
                "role": "user",
                "content": f"Format the event location: {location}"
            }
        ],
        model="llama3-70b-8192",
    )
    return chat_completion.choices[0].message.content.strip()

def format_cost(cost_str):
    # Call the Groq API to format the cost
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": """
                    Your task is to format event costs in a consistent manner:
                    - If the cost is a range (e.g., 'From $10 to $20'), pick the higher value and return it as '$20'.
                    - If there are multiple costs provided (e.g., '$10 and $15'), pick the higher value and return it as '$15'.
                    - If the cost is 'Free', return 'Free'.
                    - If the cost is 'Not Available', return 'Not Available'.
                    - In all cases, return the formatted cost as a number with a dollar sign (e.g., '$50').
                    Do not include any extra explanation. Only return the formatted cost.
                """
            },
            {
                "role": "user",
                "content": f"Format the event cost: {cost_str}"
            }
        ],
        model="llama3-70b-8192",  # Make sure to use the correct model
    )
    
    # Extract and return the formatted cost
    return chat_completion['choices'][0]['message']['content'].strip()
# Function to validate and format the event URL
def format_url(url):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "Your task is to ensure the event URL is valid, starting with 'https://' and correctly formatted. If invalid, return 'URL not available'. Only return the formatted URL."
            },
            {
                "role": "user",
                "content": f"Validate and format the event URL: {url}"
            }
        ],
        model="llama3-70b-8192",
    )
    return chat_completion.choices[0].message.content.strip()






import threading


def format_columns_parallel(data, columns):
    print("Formatting data...") 
    formatted_data = []

    def format_column(index, func):
        formatted_data.append(func(data[index]))

    threads = []
    for i, column in enumerate(columns):
        if column == "event_name":
            thread = threading.Thread(target=format_column, args=(i, format_event_name))
        elif column == "date_and_time":
            thread = threading.Thread(target=format_column, args=(i, format_date_and_time))
        elif column == "description":
            thread = threading.Thread(target=format_column, args=(i, format_description))
        elif column == "location":
            thread = threading.Thread(target=format_column, args=(i, format_location))
        elif column == "cost":
            thread = threading.Thread(target=format_column, args=(i, format_cost))
        elif column == "event_url":
            thread = threading.Thread(target=format_column, args=(i, format_url))
        
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return formatted_data



