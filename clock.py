#!/usr/bin/python3
from time import gmtime, sleep, strftime
import gpsdclient
import threading
import subprocess

import tkinter as tk
import tkinter.font as tkFont
from PIL import Image, ImageTk

"""
This is free software released under MIT License

Copyright (c) 2015, 2019, 2022 Giorgio L. Rutigliano
(www.iltecnico.info, www.i8zse.eu, www.giorgiorutigliano.it)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

locator = "------"
high = "---- m"
nsat = "--"
fix = "---"
clksrc = "---"
flexit = False
timesrc = "---"
timecol = "red"

def get_locator(lat, lng):
    """
    Convert decimal lat,lng into QRA locator
    """
    global locator
    lat += 90.0
    lng += 180.0
    L2 = chr(65 + int(lat / 10))
    L1 = chr(65 + int(lng / 20))
    N2 = str(int(lat % 10))
    N1 = str(int((lng / 2) % 10))
    llat = (lat % 1) * 60 / 2.5
    llng = (lng - int(lng / 2) * 2) * 60 / 5
    L4 = chr(97 + int(llat))
    L3 = chr(97 + int(llng))
    locator = L1 + L2 + N1 + N2 + L3 + L4
    return locator


def chrony():
    data = subprocess.run(['chronyc', '-c', 'tracking'], stdout=subprocess.PIPE).stdout.decode('utf-8').split(",")
    if data[2] == "0":
        return "RTC", '#f5aeae'
    if data[1] == "PPS":
        return "GPS", '#cdedbb'
    return "NTP", '#e9edab'

def gpsdcomm():
    global high, nsat, fix, flexit, timesrc, timecol

    gps = gpsdclient.GPSDClient()
    for data in gps.dict_stream(convert_datetime=True, filter=["TPV", "SKY"]):
        if data['class'] == "SKY":
            nsat = str(data['nSat'])
            timesrc, timecol = chrony()

        if data['class'] == "TPV":
            if 'altMSL' in data.keys():
            	high = "%s m" % int(data['altMSL'])
            fix = ['??', 'No', '2D', '3D'][data['mode']]
            get_locator(data['lat'], data['lon'])
            if nsat != "--":
                for i in range(30):
                    if flexit:
                        break
                    sleep(1)
        if flexit:
            return

def gpsstart():
    threading.Thread(target=gpsdcomm).start()
    return

def on_closing():
    global flexit

    flexit = True
    root.destroy()


def update():
    lbTime.config(text=strftime('%H:%M:%S', gmtime()))
    lbLoc.config(text=locator)
    lbhigh.config(text=high)
    lbnsat.config(text=nsat)
    lbfix.config(text=fix)
    lbtimesrc.config(text=timesrc, background=timecol)
    lbTime.after(500, update)


root = tk.Tk()

# setting title
root.title("GpsClock by I8ZSE")
# setting window size
width = 400
height = 143
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
root.geometry(alignstr)
root.resizable(width=False, height=False)
# background image
img = Image.open('panel.png')
bg = ImageTk.PhotoImage(img)
# Add image
bglabel = tk.Label(root, image=bg)
bglabel.place(x = 0,y = 0)
# time label
ft = tkFont.Font(family='Arial', size=46, weight='bold')
lbTime = tk.Label(root, font=ft, justify='center')
lbTime.place(x=22, y=15, width=300, height=70)
# Locator
ft = tkFont.Font(family='arial', size=13, weight='bold')
lbLoc = tk.Label(root, font=ft, justify='center')
lbLoc.place(x=50, y=98, width=80, height=30)
# high
ft = tkFont.Font(family='arial', size=13)
lbhigh = tk.Label(root, font=ft, justify='center', text=high)
lbhigh.place(x=180, y=98, width=80, height=30)
# nsat
lbnsat = tk.Label(root, font=ft, justify='center', text=nsat)
lbnsat.place(x=310, y=98, width=30, height=30)
# fix
lbfix = tk.Label(root, font=ft, justify='center', text=fix)
lbfix.place(x=355, y=98, width=30, height=30)
# clock source
lbtimesrc = tk.Label(root, font=ft, justify='center', text=fix)
lbtimesrc.place(x=332, y=58, width=52, height=30)

# start gpsd comm thread
root.protocol("WM_DELETE_WINDOW", on_closing)
root.after(1000, gpsstart())
update()
root.iconphoto(False, tk.PhotoImage(file='clock.png'))
root.mainloop()
