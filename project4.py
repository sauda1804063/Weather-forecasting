import mysql.connector

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "reddot",
}




from tkinter import *
import tkinter as tk

import subprocess

from geopy.geocoders import Nominatim
from tkinter import ttk, messagebox
from timezonefinder import TimezoneFinder
from datetime import *
import requests
import pytz
from PIL import Image, ImageTk

def convert_temperature():
    selected_unit = temperature_unit.get()
    if selected_unit == "°C":
        selected_unit = "°F"
        temperature_unit.set(selected_unit)
        convert_to_fahrenheit()
    elif selected_unit == "°F":
        selected_unit = "°C"
        temperature_unit.set(selected_unit)
        convert_to_celsius()

def convert_to_fahrenheit():
    current_temp = float(t.cget("text").split(" ")[0])
    temp_fahrenheit = (current_temp * 9/5) + 32
    t.config(text=f"{temp_fahrenheit:.2f} °F")

def convert_to_celsius():
    current_temp = float(t.cget("text").split(" ")[0])
    temp_celsius = (current_temp - 32) * 5/9
    t.config(text=f"{temp_celsius:.2f} °C")

root=Tk()
root.title("Weather App")
root.geometry("890x470+300+200")
root.configure(bg="#57adff")
root.resizable(False, False)

temperature_unit = StringVar()
temperature_unit.set("°C")

celsius_radio = Radiobutton(root, text="°C", variable=temperature_unit, value="°C", command=convert_to_celsius)
fahrenheit_radio = Radiobutton(root, text="°F", variable=temperature_unit, value="°F", command=convert_to_fahrenheit)

celsius_radio.place(x=400, y=80)
fahrenheit_radio.place(x=350, y=80)

def get_weather_by_coordinates(lat, lon, a):
    api2= f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&exclude=current,minutely,hourly,alerts&APPID=4d14885de745197224d39e3004f76ee9"
    json_data2=requests.get(api2).json()

    temp2=json_data2['main']['temp']
    humidity2=json_data2['main']['humidity']
    pressure2=json_data2['main']['pressure']
    wind2=json_data2['wind']['speed']
    description2=json_data2['weather'][0]['description']

    selected_unit = temperature_unit.get()
    if selected_unit == "°C":
        t2.config(text=(temp2,"°C"))

        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            query = "INSERT INTO red2 (city, temp, humidity, pressure, wind, description) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (a, temp2, humidity2, pressure2, wind2, description2))
            conn.commit()

            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            print(f"Error: {err}")

    elif selected_unit == "°F":
        temp2 = (temp2 * 9/5) + 32
        t2.config(text=(temp2, "°F"))

        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            query = "INSERT INTO red2 (city, temp, humidity, pressure, wind, description) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (a, temp2, humidity2, pressure2, wind2, description2))
            conn.commit()

            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            print(f"Error: {err}")

    h2.config(text=(humidity2,"%"))
    p2.config(text=(pressure2,"hPa"))
    w2.config(text=(wind2,"km/h"))
    d2.config(text=description2)


def get_weather_by_city(city):
    user_agent = "YourAppName"
    geolocator=Nominatim(user_agent=user_agent)
    location=geolocator.geocode(city)

    api= "https://api.openweathermap.org/data/2.5/weather?lat="+str(location.latitude)+"&lon="+str(location.longitude)+"&units=metric&exclude=current,minutely,hourly,alerts&APPID=4d14885de745197224d39e3004f76ee9"
    json_data=requests.get(api).json()

    temp=json_data['main']['temp']
    humidity=json_data['main']['humidity']
    pressure=json_data['main']['pressure']
    wind=json_data['wind']['speed']
    description=json_data['weather'][0]['description']



    selected_unit = temperature_unit.get()
    if selected_unit == "°C":
        t.config(text=(temp,"°C"))

        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            query = "INSERT INTO red2 (city, temp, humidity, pressure, wind, description) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (city, temp, humidity, pressure, wind, description))
            conn.commit()

            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            print(f"Error: {err}")

    elif selected_unit == "°F":
        temp = (temp * 9/5) + 32
        t.config(text=(temp, "°F"))

        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            query = "INSERT INTO red2 (city, temp, humidity, pressure, wind, description) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (city, temp, humidity, pressure, wind, description))
            conn.commit()

            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            print(f"Error: {err}")

    h.config(text=(humidity,"%"))
    p.config(text=(pressure,"hPa"))
    w.config(text=(wind,"km/h"))
    d.config(text=description)


def getWeather():

    city=textfield.get()


    if city=="current":
        response = requests.get('https://ipinfo.io/json')
        data = response.json()
        
        a=data['city']
        b=data['country']

        a1.config(text=("Current City is: ", a))
        b1.config(text=("Current Country is: ", b))

        lat, lon = data['loc'].split(',')
        get_weather_by_coordinates(lat, lon, a)

    elif city!="current":
        get_weather_by_city(city)

        
    

Round_box=PhotoImage(file=r"C:\Users\HP\Desktop\Anaconda Navigator\black.png")
Label(root, image=Round_box, bg="#57adff", width=300, height=110).place(x=30, y=80)

label1=Label(root, text="Temperature", font=('Helvetica', 11), fg="white", bg="#203243").place(x=50, y=85)
label2=Label(root, text="Humidity", font=('Helvetica', 11), fg="white", bg="#203243").place(x=50, y=105)
label3=Label(root, text="Pressure", font=('Helvetica', 11), fg="white", bg="#203243").place(x=50, y=125)
label4=Label(root, text="Wind Speed", font=('Helvetica', 11), fg="white", bg="#203243").place(x=50, y=145)
label5=Label(root, text="Description", font=('Helvetica', 11), fg="white", bg="#203243").place(x=50, y=165)

textfield=tk.Entry(root, justify='center', width=21, font=('poppins', 25, 'bold'),bg="#203243", border=0, fg="white")
textfield.place(x=350, y=120)

search_icon=PhotoImage(file=r"C:\Users\HP\Desktop\Anaconda Navigator\search_icon.png")
myimage_icon=Button(image=search_icon, borderwidth=0, cursor="hand2", bg="#203243", width=30, height=30, command=getWeather)
myimage_icon.place(x=645, y=125)



#thpwd
t=Label(root, font=("Helvetica", 11), fg="white", bg="#203243")
t.place(x=155, y=85)
h=Label(root, font=("Helvetica", 11), fg="white", bg="#203243")
h.place(x=155, y=105)
p=Label(root, font=("Helvetica", 11), fg="white", bg="#203243")
p.place(x=155, y=125)
w=Label(root, font=("Helvetica", 11), fg="white", bg="#203243")
w.place(x=155, y=145)
d=Label(root, font=("Helvetica", 11), fg="white", bg="#203243")
d.place(x=155, y=165)


t2=Label(root, font=("Helvetica", 11), fg="white", bg="#203243")
t2.place(x=150, y=85)
h2=Label(root, font=("Helvetica", 11), fg="white", bg="#203243")
h2.place(x=150, y=105)
p2=Label(root, font=("Helvetica", 11), fg="white", bg="#203243")
p2.place(x=150, y=125)
w2=Label(root, font=("Helvetica", 11), fg="white", bg="#203243")
w2.place(x=150, y=145)
d2=Label(root, font=("Helvetica", 11), fg="white", bg="#203243")
d2.place(x=150, y=165)


a1=Label(root, font=("Helvetica", 11), fg="white", bg="#203243")
a1.place(x=60, y=20)

b1=Label(root, font=("Helvetica", 11), fg="white", bg="#203243")
b1.place(x=60, y=40)


root.mainloop()