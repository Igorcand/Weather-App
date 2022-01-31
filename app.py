import requests
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'

db = SQLAlchemy(app)
class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),  nullable=False)


@app.before_first_request
def create_database():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        new_city = request.form.get('city')
        if new_city:
            new_city_obj = City(name=new_city)
            db.session.add(new_city_obj)
            db.session.commit()

    cities = City.query.all()
    print(cities)

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=271d1234d3f497eed5b1d80a07b3fcd1'

    weather_data = [] 

    city = 'Las vegas'
    for city in cities:
        
        r = requests.get(url.format(city.name)).json()

        weather = {
            'city': city,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon']
        }


        weather_data.append(weather)
    return render_template('weather.html', weather_data=weather_data)

if __name__ == '__main__':
    db.init_app(app)
    app.run()