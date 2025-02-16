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

# Function to format the event date and time
def format_date_and_time(date_str):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "Your task is to convert date and time in any format into the standardized format `YYYY-MM-DD HH:MM:SS`. Only return the formatted date and time, without extra explanation."
            },
            {
                "role": "user",
                "content": f"Format the date and time: {date_str}"
            }
        ],
        model="llama3-70b-8192",
    )
    return chat_completion.choices[0].message.content.strip()

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

# Function to format the event cost
def format_cost(cost_str):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "Your task is to format event costs in a consistent manner, including ranges (e.g., 'From $10 to $20') and single values (e.g., 'Cost: $50'). Only return the formatted cost."
            },
            {
                "role": "user",
                "content": f"Format the event cost: {cost_str}"
            }
        ],
        model="llama3-70b-8192",
    )
    return chat_completion.choices[0].message.content.strip()

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

# Example formatting functions
def format_event_name(event_name):
    return event_name.title()  # Just an example formatting

def format_date_and_time(date_str):
    return date_str.replace("st", "").replace("th", "").replace("nd", "").replace("rd", "")  # Simplified example

def format_description(description):
    return description.strip()  # Just an example formatting

def format_location(location):
    return location.strip()  # Just an example formatting

def format_cost(cost_str):
    return cost_str.replace("-", " to ")  # Just an example formatting

def format_url(url):
    if not url.startswith("https://"):
        return "https://" + url[7:]  # Fixing missing https
    return url


def format_columns_parallel(data, columns):
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
