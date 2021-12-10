#-*- coding: utf-8 -*-
from tkinter import *
from PIL import ImageTk, Image
import json
import requests
from pprint import pprint



root = Tk()
root.title('Air Quality APP')
root.iconbitmap('images/chmurka.ico')
root.geometry('230x220') # start window size

bg_color = '#68d3ed'
root.configure(background=bg_color)

# create text powered by
powered_label = Label(root, text = 'POWERED BY', background=bg_color, font=('Helvetica', 10))
powered_label.grid(row=4, column=0, columnspan=2)



# create resized logo airly
image = Image.open('images/logo_airly.png')
resize_image = image.resize((200, 78,))
logo_img = ImageTk.PhotoImage(resize_image)
logo_label = Label(image=logo_img)
logo_label.grid(row=5, column=0, columnspan=2)


def location_lookup():
    top = Toplevel()
    top.title('Your air quality')
    top.iconbitmap('images/chmurka.ico')
    top.geometry('700x320')

    try:
        url_1 = f'https://airapi.airly.eu/v2/measurements/nearest?indexType=AIRLY_CAQI&lat=' \
            f'{str(latitude.get())}&lng={str(longitude.get())}&maxDistanceKM=10'

        url_2 = f'https://airapi.airly.eu/v2/installations/nearest?lat=' \
            f'{str(latitude.get())}&lng={str(longitude.get())}&maxDistanceKM=3&maxResults=1'

        headers = {
            'Accept': 'application/json',
            'Accept-Language': 'en',
            'apikey': 'mB16sg3Mcs5DuW8QfUgKQpTJAwQMGhNM'
        }

        response_1 = requests.get(url_1, headers=headers)
        response_2 = requests.get(url_2, headers=headers)



        result_level = response_1.json()['current']['indexes'][0]['level']
        result_description = response_1.json()['current']['indexes'][0]['description']
        result_advice = response_1.json()['current']['indexes'][0]['advice']


        # background colour
        if result_level == 'VERY_LOW':
            bg_colour = '#6BC926'
        elif result_level == 'LOW':
            bg_colour = '#D1CF1E'
        elif result_level == 'MEDIUM':
            bg_colour = '#EFBB0F'
        elif result_level == 'HIGH':
            bg_colour = '#EF7120'
        elif result_level == 'VERY_HIGH':
            bg_colour = '#EF2A36'
        elif result_level == 'EXTREME':
            bg_colour = '#B00057'
        elif result_level == 'AIRMAGEDDON':
            bg_colour = '#770078'

        top.configure(background=bg_colour)

        # create addres and results frames
        address_frame = LabelFrame(top, text='Address', padx=5, pady=5, background=bg_colour)  # marginesy wewnetrzne
        address_frame.grid(row=1, column=0, padx=10, pady=10)

        results_frame = LabelFrame(top, text='Results', padx=5, pady=5, background=bg_colour)  # marginesy wewnetrzne
        results_frame.grid(row=1, column=1, padx=10, pady=10)



        level = f'Level: {result_level} => {result_description}\n{result_advice}'
        level_label = Label(top, text=level, font=('Helvetica', 15), background=bg_colour)
        level_label.grid(row=0, column=0, columnspan=2)


        # location
        result_country = response_2.json()[0]['address']['country']
        result_city = response_2.json()[0]['address']['city']
        result_street = (response_2.json()[0]['address']['street'])
        result_number = response_2.json()[0]['address']['number']


        location = f'Location: {result_country}\n' \
                   f'    City: {result_city}\n' \
                   f'  Street: {result_street} {result_number}'
        location_label = Label(address_frame, text=location, font=('Helvetica', 15), background=bg_colour)
        location_label.grid(row=0, column=0)


        # Result
        c_r = response_1.json()['current']['values'] # current_results

        pm1 = f"                  {c_r[0]['name']}: {c_r[0]['value']}um/m^3"
        pm2_5 = f"              PM 2,5: {c_r[1]['value']}um/m^3 = {response_1.json()['current']['standards'][0]['percent']}%"
        pm10 =  f"                {c_r[2]['name']}: {c_r[2]['value']}um/m^3 = {response_1.json()['current']['standards'][1]['percent']}%"
        press =  f"       {c_r[3]['name']}: {c_r[3]['value']}hPa"
        hum = f"         {c_r[4]['name']}: {c_r[4]['value']}%"
        temp = f"{c_r[5]['name']}: {c_r[5]['value']}C"

        pm1_label = Label(results_frame, text=pm1, font=('Helvetica', 15), background=bg_colour).grid(row=0, column=0, sticky=W)
        pm2_5_label = Label(results_frame, text=pm2_5, font=('Helvetica', 15), background=bg_colour).grid(row=1, column=0, sticky=W)
        pm10_label = Label(results_frame, text=pm10, font=('Helvetica', 15), background=bg_colour).grid(row=2, column=0, sticky=W)
        press_label = Label(results_frame, text=press, font=('Helvetica', 15), background=bg_colour).grid(row=3, column=0, sticky=W)
        hum_label = Label(results_frame, text=hum, font=('Helvetica', 15), background=bg_colour).grid(row=4, column=0, sticky=W)
        temp_label = Label(results_frame, text=temp, font=('Helvetica', 15), background=bg_colour).grid(row=5, column=0, sticky=W)


    except Exception as e:
        api = "ERROR"


    close_button = Button(top, text='Exit', command=top.destroy, padx=5, pady=5, )
    close_button.grid(row=10, column=0, columnspan=2)


info_label = Label(root, text='Enter the location to check the air quality', background=bg_color)
info_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

longitude_label = Label(root, text='Longitude:', anchor=W, background=bg_color)
longitude_label.grid(row=1, column=0)
longitude = Entry(root)
longitude.insert(0, '19.381666') # default text
longitude.grid(row=1, column=1)


latitude_label = Label(root, text='Latitude:', anchor=E, background=bg_color)
latitude_label.grid(row=2, column=0)
latitude = Entry(root)
latitude.insert(0, '51.742172')
latitude.grid(row=2, column=1)



check_button = Button(root, text='Check air quality', width=25, command=location_lookup, fg='yellow', bg='green')
check_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)


root.mainloop()
