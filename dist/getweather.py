import requests
import time
import json
import csv

URL = 'https://api.weather.gov/stations/KIPJ/observations/latest'
FILE = 'weatherData.csv'
def save_data(data):
   # Access properties
   properties = data['properties']

   # Extract specific data points
   station_name = properties.get('stationName')
   temperature = properties.get('temperature', {}).get('value')
   dewpoint = properties.get('dewpoint', {}).get('value')
   wind_direction = properties.get('windDirection', {}).get('value')
   wind_speed = properties.get('windSpeed', {}).get('value')
   barometric_pressure = properties.get('barometricPressure', {}).get('value')
   visibility = properties.get('visibility', {}).get('value')
   humidity = properties.get('relativeHumidity', {}).get('value')
   maxTemperatureLast24Hours = properties.get('maxTemperatureLast24Hours', {}).get('value')
   minTemperatureLast24Hours = properties.get('minTemperatureLast24Hours', {}).get('value')
   precipitationLastHour = properties.get('precipitationLastHour', {}).get('value')
   windChill = properties.get('windChill', {}).get('value')
   heatIndex = properties.get('heatIndex', {}).get('value')
   textDescription = properties.get('textDescription')

   # For cloud layers, join details into a string
   cloud_layers = properties.get('cloudLayers', [])
   cloud_info = '; '.join([f"{layer.get('amount')} at {layer.get('base', {}).get('value')}m" for layer in cloud_layers])

   # Data to write into CSV
   row = {
      'Station': station_name,
      'Temperature (°C)': temperature,
      'Dew Point (°C)': dewpoint,
      'Wind Direction (°)': wind_direction,
      'Wind Speed (km/h)': wind_speed,
      'Barometric Pressure (Pa)': barometric_pressure,
      'Visibility (m)': visibility,
      'Humidity (%)': humidity,
      'maxTemperatureLast24Hours (%)': maxTemperatureLast24Hours,
      'minTemperatureLast24Hours (%)': minTemperatureLast24Hours,
      'precipitationLastHour (%)': precipitationLastHour,
      'windChill (%)': windChill,
      'heatIndex (%)': heatIndex,
      'Cloud Layers': cloud_info,
      'Text Description': textDescription
   }

   # Write to CSV file
   csv_file = FILE
   with open(csv_file, 'a', newline='') as csvfile:
      fieldnames = list(row.keys())
      writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

      writer.writeheader()
      writer.writerow(row)

   print(f"Data saved to {csv_file}")

def get_weather():
   response = requests.get(URL)
   if response.status_code == 200:
      weather_data = response.json()
      print(weather_data)  # Or process/store the data as needed
   else:
      print(f"Failed to fetch data: {response.status_code}")

   return response.json()


#while True:
data=get_weather()
save_data(data)
   #time.sleep(3600)  # Wait for 600 seconds (10 minutes)