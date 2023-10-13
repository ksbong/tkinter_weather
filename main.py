import requests
import json
import base64
from urllib.request import urlopen
from tkinter import *
from tkinter import ttk
from cities import city_dict

file_path = "./weather.json"

tempCode = '°C'

apiKey = "618414cd7a1e665025fb2cc40426aa75"
lang = 'kr'
units = 'metric'

root = Tk()
root.title("날?씨")
root.geometry('330x180')

runOnce = False


frame = Frame(root)

listFrame = Frame(root)

selectionFrame = Frame(root)

frame.grid(row=0, column=1)

icon_url = "http://openweathermap.org/img/w/10d.png"
image_byt = urlopen(icon_url).read()
image_b64 = base64.encodebytes(image_byt)
photo = PhotoImage(data=image_b64)

listbox = Listbox(listFrame, height=10)
listbox.pack(side="left", fill="y")

scrollbar = ttk.Scrollbar(listFrame,orient="vertical",command=listbox.yview)

listbox.config(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")

city_dict_keys = list(city_dict.keys())

keys = []

for i in range(len(city_dict_keys)):
    keys.insert(0, city_dict_keys[i])
for i in range(len(keys)):
    listbox.insert(0, keys[i])

    
options =["섭씨 °C","화씨 ℉","캘빈 K"]

selected_option = StringVar(selectionFrame)
selected_option.set(options[0])


dropdown = ttk.OptionMenu(selectionFrame, selected_option, options[0], *options)
dropdown.pack(side="left", fill="y")



cityLabel = Label(text="도시이름")

weatherTemp = ttk.Label(frame, text="현재온도: ???   ")
weatherStatus = ttk.Label(frame, text="날씨: 맑?음")
imagelab = ttk.Label(frame, image=photo)

feelTemp = ttk.Label(frame, text="체감온도: ???")

max_temp = ttk.Label(frame, text="최고온도: ???")
min_temp = ttk.Label(frame, text="최저온도: ???")

humidity = ttk.Label(frame, text="습도: ??%")

wind_speed = ttk.Label(frame, text="풍속: ??m/s")

def on_option_selected(*args):
    selected_value = selected_option.get()
    print("Selected Option: ", selected_value)
    print("type: ", type(selected_value))
    selected_option.set(selected_value)
    # if runOnce : getWeather()

selected_option.trace_add("write", on_option_selected)

def getWeather():
    global runOnce
    if not runOnce : runOnce = True

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
    selected = selected_option.get()


    wfTemp = result["main"]["feels_like"]
    temp_max = result["main"]["temp_max"]
    temp_min = result["main"]["temp_min"]

    ## options =["섭씨 °C","화씨 ℉","캘빈 K"]

    if selected == options[0]: # 섭씨일 경우

        tempCode = '°C'
        current_Temp = round(wTemp)
        perceived_Temp = round(wfTemp)
        max_Temp = round(temp_max)
        min_Temp = round(temp_min)

    elif selected == options[1]: # 화씨일 경우

        tempCode = '℉'
        current_Temp = round(wTemp*(9/5)+32)
        perceived_Temp = round(wfTemp*(9/5)+32)
        max_Temp = round(temp_max*(9/5)+32)
        min_Temp = round(temp_min*(9/5)+32)
        
    elif selected == options[2]: # 캘빈일 경우

        tempCode = 'K'
        current_Temp = round(wTemp + 273.15)
        perceived_Temp = round(wfTemp + 273.15)
        max_Temp = round(temp_max + 273.15)
        min_Temp = round(temp_min + 273.15)

    weatherTemp["text"] =  f"현재온도: {current_Temp}{tempCode}   "

    
    feelTemp["text"] = f"체감온도: {perceived_Temp}{tempCode}"

    
    max_temp["text"] = f"최고온도: {max_Temp}{tempCode}   "

    
    min_temp["text"] = f"최저온도: {min_Temp}{tempCode}"

    value_humidity =  result["main"]["humidity"]
    humidity["text"] = f"습도: {round(value_humidity)}%   "

    speed_wind = result["wind"]["speed"]
    wind_speed["text"] = f"풍속: {round(speed_wind)}m/s"


getWeather_btn = ttk.Button(selectionFrame, text="날?씨" ,command=getWeather)

getWeather_btn.pack(side="right", fill="y")


weatherStatus.grid(row=0, column=0)
imagelab.grid(row=0, column=1)

weatherTemp.grid(row=1, column=0)
feelTemp.grid(row=1, column=1)

max_temp.grid(row=2, column=0)
min_temp.grid(row=2, column=1)

humidity.grid(row=3, column=0)
wind_speed.grid(row=3, column=1)

selectionFrame.grid(row=2, column=1)

listFrame.grid(row=0,column=0, rowspan=3)

root.mainloop()