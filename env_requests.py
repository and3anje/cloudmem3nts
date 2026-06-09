import os
import requests

#1:Environment variables
#setting environment variable from within python(for testing)
os.environ['MY_API_KEY']='test-key-12345'
os.environ['MY_SERVER'] = 'web-server -01'

#read environment server
api_key = os.environ.get('MY_API_KEY')
server = os.environ.get('MY_SERVER')
missing = os.environ.get('MISSING_VAR', 'default value')

print("Environment Variables")
print(f"API KEY: {api_key}")
print(f"Server: {server}")
print(f"Missing var: {missing}")

#2:Requests library

def get_weather(city):
    try:
        url = f"http://wttr.in/{city}?format=j1"
        
        # Make GET request
        response = requests.get(url, timeout=10)
        
        # Check if request succeeded
        print(f"\n=== Request to {url} ===")
        print(f"Status code: {response.status_code}")
        print(f"Response size: {len(response.text)} bytes")
        
        # Check status code before processing
        if response.status_code == 200:
            data = response.json()
            current = data['current_condition'][0]
            
            print(f"\n=== Weather in {city} ===")
            print(f"Temperature: {current['temp_C']}°C")
            print(f"Feels like: {current['FeelsLikeC']}°C")
            print(f"Condition: {current['weatherDesc'][0]['value']}")
            print(f"Humidity: {current['humidity']}%")
        else:
            print(f"Request failed with status: {response.status_code}")
            
    except requests.exceptions.Timeout:
        print(f"Request timed out for {city}")
    except requests.exceptions.ConnectionError:
        print(f"Connection error for {city}")
    except Exception as e:
        print(f"Unexpected error: {e}")

get_weather("Nairobi")
