import requests
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
db = SQLAlchemy(app)

#Class to create Database table
class City(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable=False)

@app.route('/', methods=['POST', 'GET'])
def index():
    #User adding new city to check for weather
    if request.method == 'POST':
        new_city = request.form.get('city')
        if new_city:
            new_city_obj = City(name=new_city)
            db.session.add(new_city_obj)
            db.session.commit()
    #Accessing all cities in the Database table
    cities = City.query.all()
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=51731c8f68639d7d211baa8fcbde4584'

    weather_data = []

    for city in cities:

        r = requests.get(url.format(city.name)).json()

        weather = {
            'city' : city.name,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }
        
        weather_data.append(weather)

    return render_template('weather.html', weather_data=weather_data)