import os, requests
import csv
from datetime import datetime, timedelta, timezone

URL = 'https://api.weather.gov/stations/KIPJ/observations/'
FILE = 'weatherData.csv'

def fahrenheit(celsius):
   return (celsius * 9/5) + 32

def save_data(data):
   # Access properties
   features = data['features']

   # If CSV file is new, insert header
   if os.path.exists(FILE):
      header = False
   else:
      header = True

   with open(FILE, 'a', newline='') as csvfile:

      for feature in features:
         properties = feature['properties']

         # Extract specific data points
         station_name = properties.get('stationName')
         timestamp = properties.get('timestamp')
         excel_timestamp = excel_date(properties.get('timestamp'))
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
         my_timezone = timezone(timedelta(hours=0))

         # Data to write into CSV
         row = {
            'Station': station_name,
            'ISO_Timestamp': timestamp,
            'Excel_Timestamp': excel_timestamp,
            'Temperature (F)': fahrenheit(temperature),
            'Dew Point (F)': fahrenheit(dewpoint),
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
            'Text Description': textDescription,
            'Time Created': datetime.now(my_timezone).isoformat()
         }

         # Write data to file
         fieldnames = list(row.keys())
         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

         if header:
            writer.writeheader() 
            header = False
         writer.writerow(row)

      #  End features loop

   # Closes file

   print(f"Data saved to {FILE}")

def get_weather():
   response = requests.get(URL)
   weather_data = f"Failed to fetch data: {response.status_code}"
   if response.status_code == 200:
      weather_data = response.json()
   else:
      print(f"Failed to fetch data: {response.status_code}")

   return weather_data

def excel_date(iso_string):

   # Parse the ISO date string
   dt = datetime.fromisoformat(iso_string)

   # Define Excel start date
   excel_start_date = datetime(1899, 12, 30, tzinfo=timezone.utc)

   # Calculate the difference in days
   delta = dt - excel_start_date
   excel_date_value = delta.days + (delta.seconds / 86400)

   return excel_date_value


#while True:
data=get_weather()
save_data(data)
   #time.sleep(3600)  # Wait for 600 seconds (10 minutes)