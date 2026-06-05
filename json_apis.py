#!/usr/bin/env python3
import json
import urllib.request

#working with json directly
#python dictionary

server = {
    "name": "web-serever-01",
    "ip": "10.0.0.1",
    "status": "running",
    "ports": [80, 443, 22],
    "specs": {
        "cpu": 2,
        "ram_gb": 4
    }
    
}

#convert python dictionary to JSON string
json_string = json.dumps(server, indent=2)
print("===Dict to JSON===")
print(json_string)
print(type(json_string))

#convert json string back to python dict
parsed = json.loads(json_string)
print("\n=== JSON back to Dict ===")
print(f"server name: {parsed['name']}")
print(f"server ip: {parsed['ip']}")
print(f"First port: {parsed['ports'][0]}")
print(f"RAM: {parsed['specs']['ram_gb']}GB")

#save JSON to file
with open("server_config.json", "w") as f:
    json.dump(server, f , indent=2)
print("\n===Saved to server_config.json===")

#read JSON file
with open("server_config.json", "r") as f:
    loaded = json.load(f)
print(f"Loaded from file: {loaded['name']}")    

# ── PART 2: Calling a Real API ──
import urllib.request
import json

def get_weather(city):
    try:
        url = f"http://wttr.in/{city}?format=j1"
        
        with urllib.request.urlopen(url) as response:
            raw = response.read()
            data = json.loads(raw)
        
        # Navigate the JSON response
        current = data['current_condition'][0]
        temp_c = current['temp_C']
        feels_like = current['FeelsLikeC']
        weather_desc = current['weatherDesc'][0]['value']
        humidity = current['humidity']
        
        print(f"\n=== Weather in {city} ===")
        print(f"Temperature: {temp_c}°C")
        print(f"Feels like: {feels_like}°C")
        print(f"Condition: {weather_desc}")
        print(f"Humidity: {humidity}%")
        
    except Exception as e:
        print(f"Error getting weather: {e}")

get_weather("Nairobi")
get_weather("London")