# Import necessary modules
from dotenv import load_dotenv
import os
import requests

# Load environment variables from the .env file
load_dotenv()

# Function to search using SerpAPI
def search_serpapi(query):
    api_key = os.getenv("SERPAPI_KEY")  # Fetch the API key from environment variables

    if not api_key:
        return {"error": "API key is missing."}

    params = {
        "q": query,
        "api_key": api_key  # Using the API key from environment variables
    }

    # Send GET request to SerpAPI
    response = requests.get("https://serpapi.com/search", params=params)
    
    # Check if response is valid and return the result
    if response.status_code == 200:
        return response.json()  # Return the response in JSON format
    else:
        return {"error": f"Error {response.status_code}: {response.text}"}

# Example usage
query = "Artificial Intelligence"
results = search_serpapi(query)
print(results)  # Print the results or handle as needed
