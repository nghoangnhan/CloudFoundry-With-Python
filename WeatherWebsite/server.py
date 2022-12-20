#%%
import os
from flask import Flask, render_template, request
from datetime import date, datetime
import geocoder, requests, moment
from geopy.geocoders import Nominatim


app = Flask(__name__,static_folder='static', template_folder='templates')
port = int(os.environ.get('PORT', 3000))

g = geocoder.ip("me") 

@app.route('/')
def show():
    return render_template('input.html')

@app.route('/sendata',methods=['POST'])
def index():
    name=request.form['cityname']
    data = test(name)
    
    if data is None:
        return render_template('input.html')
    else:
        current_data = data["current"]

        humidity = current_data['humidity']
        pressure = current_data['pressure']
        windspeed = current_data['wind_speed']


        temp = current_data["temp"]
        temp_feellike = current_data["feels_like"]

        sunrise = moment.unix(current_data["sunrise"]).strftime("%H:%M")
        sunset = moment.unix(current_data["sunset"]).strftime("%H:%M")

        position = data["timezone"].replace("_", " ")

        today = date.today().strftime("%A, %d %B ")
        date_time = datetime.now().strftime("%H:%M %p")

        daily_weather = []
        data_daily = data["daily"]
        for i in range (7):
            daily_weather.append(data_daily[i]) 
            daily_weather[i]["dt"] = moment.unix(daily_weather[i]["dt"]).strftime("%A")

        return render_template('index1.html', humidity=humidity,pressure=pressure, windspeed=windspeed,
                                            sunrise=sunrise, sunset=sunset,
                                            temp_feellike = temp_feellike, temp=temp, position=position,
                                            date=today, datetime=date_time, data_daily=data_daily)
def test(name):
   try:
        #API key for using OpenWeatherMap
        API_Key = '49cc8c821cd2aff9af04c9f98c36eb74'
        #Headers for accepted browsers for requeting data
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

        
        if name != '':
            geolocator = Nominatim(user_agent="user",timeout=10)

            #get the position by name of the city by user input
            g = geolocator.geocode(name)
            
            latitude = g.latitude
            longitude = g.longitude
        else:
            #get the current position
            g = geocoder.ip("me")
            latitude = g.latlng[0]
            longitude = g.latlng[1]

        #get the weather data by LATITUDE AND LONGITUDE of the place
        res = requests.get(f'https://api.openweathermap.org/data/2.5/onecall?lat={latitude}&lon={longitude}&exclude=hourly,minutely&units=metric&appid={API_Key}', 
                        headers=headers) 
        return res.json()
   except:
       print("Please enter a valid city name")
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)