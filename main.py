import requests
import json
import base64
from urllib.request import urlopen
from tkinter import *
from cities import city_dict

file_path = "./weather.json"

apiKey = "618414cd7a1e665025fb2cc40426aa75"
lang = 'kr'
units = 'metric'

root = Tk()
root.title("날?씨")
root.geometry('330x200')

frame = Frame(root)

frame.grid(row=0, column=1)

icon_url = "http://openweathermap.org/img/w/10d.png"
image_byt = urlopen(icon_url).read()
image_b64 = base64.encodebytes(image_byt)
photo = PhotoImage(data=image_b64)

listbox = Listbox(root, height=10, selectmode="browse")
city_dict_keys = list(city_dict.keys())

keys = []

for i in range(len(city_dict_keys)):
    keys.insert(0, city_dict_keys[i])
for i in range(len(keys)):
    listbox.insert(0, keys[i])

cityLabel = Label(text="도시이름")

weatherTemp = Label(frame, text="현재온도: 273K   ")
weatherStatus = Label(frame, text="날씨: 맑?음")
imagelab = Label(frame, image=photo)

feelTemp = Label(frame, text="체감온도: 273K")

max_temp = Label(frame, text="최고온도: 273K")
min_temp = Label(frame, text="최저온도: 273K")

humidity = Label(frame, text="습도: 100%")

wind_speed = Label(frame, text="풍속: 100m/s")

def getWeather():
    try:
        slt_index = listbox.curselection()[0]
    except:
        print("선택안함")
        
    city_name = city_dict_keys[slt_index]
    city = city_dict[city_name]

    api = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={apiKey}&lang={lang}&units={units}"
    result = requests.get(api)
    result= json.loads(result.text)

    print(result["weather"][0]["icon"], type(result["weather"][0]["icon"]))

    iconUrl = "http://openweathermap.org/img/w/"+ result["weather"][0]["icon"] +".png"
    byt = urlopen(iconUrl).read()
    b64 = base64.encodebytes(byt)
    photo = PhotoImage(data=b64)
    imagelab.configure(image=photo)
    imagelab.image = photo

    # with open(file_path, 'w') as outfile:
    #     json.dump(result, outfile)

    cityLabel["text"] = city_name


    wStatus = result["weather"][0]["description"]
    weatherStatus["text"] = f"날씨: {wStatus}"

    wTemp = result["main"]["temp"]
    weatherTemp["text"] =  f"현재온도: {round(wTemp + 273.15)}K   "

    wfTemp = result["main"]["feels_like"]
    feelTemp["text"] = f"체감온도: {round(wfTemp + 273.15)}K"

    temp_max = result["main"]["temp_max"]
    max_temp["text"] = f"최고온도: {round(temp_max + 273.15)}K   "

    temp_min = result["main"]["temp_min"]
    min_temp["text"] = f"최저온도: {round(temp_min + 273.15)}K"

    value_humidity =  result["main"]["humidity"]
    humidity["text"] = f"습도: {round(value_humidity)}%   "

    speed_wind = result["wind"]["speed"]
    wind_speed["text"] = f"풍속: {round(speed_wind)}m/s"


getWeather_btn = Button(text="날?씨" ,command=getWeather)


weatherStatus.grid(row=0, column=0)
imagelab.grid(row=0, column=1)

weatherTemp.grid(row=1, column=0)
feelTemp.grid(row=1, column=1)

max_temp.grid(row=2, column=0)
min_temp.grid(row=2, column=1)

humidity.grid(row=3, column=0)
wind_speed.grid(row=3, column=1)

getWeather_btn.grid(row=2, column=1)

listbox.grid(row=0,column=0, rowspan=3)

root.mainloop()