# -*- coding: utf-8 -*-
"""
Created on Sun Dec 08 21:38:46 2019

@author: Samuel Gandy

"""


import dweepy
import re
import sqlite3
from tkinter import *
import tkinter.messagebox

accXlast = 0
accYlast = 0
accZlast = 0
walkX = 0
walkY = 0
walkZ = 0

def GUI(time,date,episode,latitude,longitude): #[4] used the functions from 4
    GUItime = StringVar()
    GUItime.set(time)
    
    GUIdate = StringVar()
    GUIdate.set(date)
    
    GUIstatus = StringVar()
    GUIstatus.set(episode)
    
    GUIlat = StringVar()
    GUIlat.set(latitude)
    
    GUIlong = StringVar()
    GUIlong.set(longitude)
    
    
    labTime = Label(root, text = "Time: ")
    labDate = Label(root, text = "Date: ")
    labStatus= Label(root, text = "Status: ")
    labLat = Label(root, text = "Latuide: ")
    labLong = Label(root, text = "longitude: ")
    
    disTime = Label(root, textvariable = GUItime)
    disDate = Label(root, textvariable = GUIdate)
    disHeart = Label(root, textvariable = GUIstatus)
    disLat = Label(root, textvariable = GUIlat)
    disLong = Label(root, textvariable = GUIlong)
    
    labTime.grid(row = 0, column = 0, sticky = W)
    disTime.grid(row = 0, column = 1, sticky = W)
    labDate.grid(row = 1, column = 0, sticky = W)
    disDate.grid(row = 1, column = 1, sticky = W)
    labStatus.grid(row = 2, column = 0, sticky = W)
    disHeart.grid(row = 2, column = 1, sticky = W)
    labLat.grid(row = 3, column = 0, sticky = W)
    disLat.grid(row = 3, column = 1, sticky = W)
    labLong.grid(row = 4, column = 0, sticky = W)
    disLong.grid(row = 4, column = 1, sticky = W)


def episodeCal(accX,accY,accZ,episode,accXlast,accYlast,accZlast, walkX, walkY, walkZ):
    if int(accX) > (accXlast + 500) or int(accX) < (accXlast - 500):
        print("X walking")
        walkX = 1
    
    if int(accY) > (accYlast + 500) or int(accY) < (accYlast - 500):
        print("Y walking")
        walkY = 1
        
    if int(accZ) > (accZlast + 500) or int(accZ) < (accZlast - 500):
        print("Z walking")
        walkZ = 1
        
    if (int(walkX) > 0) and (int(walkZ) > 0) or (int(walkY) > 0 and int(walkZ) > 0):
        if episode == 'R':
            print("Please check but could be running")
            tkinter.messagebox.showinfo('Samuel', 'Please check but could be running')
        elif episode == 'M':
            print("Problely just walking but keep an eye out")
        elif episode == 'G':
            print("All good")
    else:
        if episode == 'R':
            print("Episode is happening please stay calm")
            tkinter.messagebox.showinfo('Samuel', 'Episode is happening')
        elif episode == 'M':
            print("students heart beat has raisen")
            tkinter.messagebox.showinfo('Samuel', 'Potential Episode')
        else:
            print("Student is calm")

    walkX = 0
    walkY = 0
    walkZ = 0
    accXlast = accX
    accYlast = accY
    accZlast = accZ
    return accXlast, accYlast, accZlast, walkX, walkY, walkZ

    

print("Read Dweet and sent to DataBase")

conn = sqlite3.connect('wristbandData.db') #connect to DataBase
c = conn.cursor() #create cursor
c.execute('CREATE TABLE IF NOT EXISTS dweetData(Date INTEGER, Time TEXT, Names TEXT, Acc TEXT, Latitude TEXT, Longitude TEXT, Episode TEXT)') #[1]creating Table

root = Tk()
root.title("Austim Software")
root.resizable(width=FALSE, height=FALSE)
root.geometry('200x200')

while(1):
    dweet = str(dweepy.get_latest_dweet_for("group")) #[2]
    #print("Recived signal is ", dweet)
    
    #print("The final dweet")
    mainDweet = dweet[28:-1]
    #print(mainDweet)
    
    #read the strings values 
    #print(" ")
    #print("Dweet values below ")
        
    dweetValues = re.findall(r"[+-]?\d+(?:\.\d+)?", mainDweet) #[3]
    #print(dweetValues)
    
    #print("Dweet Chars below")
    dweetChars = re.findall(r"\w\D",mainDweet) #[2]
    #print(dweetChars)
    
    print(" ")
    print("The date is ")
    
    dayStr = dweetValues[2]
    day = dayStr[1:3]
    
    monthStr = dweetValues[1]
    month = monthStr[1:3]
    
    date = day
    date += "/"
    date += month
    date += "/"
    date += dweetValues[0]
    print(date)
    
    print("The time is ")
    
    hour = dweetValues[3]
    minute = dweetValues[4]
    time = str(hour) + ":" + str(minute)
    print(time)
    
    print("The user is")
    name = mainDweet[52:58]
    print(name)
    
    print("The Accelerometer is ")
    
    accX = dweetValues[6]
    accY = dweetValues[7]
    accZ = dweetValues[8]
    
    acc = str(accX) + ":" + str(accY) + ":" + str(accZ) #Issues with negitive numbers being read as positive
    print(acc)
    
    print("The GPS is ") #GPS problem with letters and numbers need to found. Also having 0s in front missing. 
    
    latitudeNum = dweetValues[9]
    latitudeChar = dweetChars[-9]
    latitude = str(latitudeNum) + str(latitudeChar)
    
    longitudeNum = dweetValues[10]
    longitudeChar = dweetChars[-7]
    longitude = str(longitudeNum) + str(longitudeChar)
    
    print(latitude) 
    print(longitude)
    
    print("Heart Beat is ")
    
    episodeChars = dweetChars[-1] #This is the only value position will stay the same
    episode = episodeChars[0]
    print(episode) #print episode
    
    #Putting this data into Data Base
    c.execute("INSERT INTO dweetData (Date, Time, Names, Acc, Latitude, Longitude, Episode) VALUES (?, ?, ?, ?, ?, ?, ?)", 
              (date, time, name, acc, latitude, longitude, episode)) #Dynamic variable inserted into database[1]
    conn.commit()
    #reading data below
    c.execute("SELECT * FROM dweetData WHERE episode=episode", {'episode':'G'}) #[1]
    print("All the tables data is below")
    allDweets = c.fetchall()
    print(allDweets)
    
    
    #GUI below (Small issue the program only runs though once)
    
    GUI(time,date,episode,latitude,longitude)
    
    #Analysis of data is below
    
    episodeCal(accX,accY,accZ,episode,accXlast,accYlast,accZlast,walkX, walkY, walkZ)
    
#The program is always connected but for a fail safe closing the cursor and database file
c.close()
conn.close()
root.mainloop()
   

 
""" Refances for the program

[1]"Python Programming Tutorials", Pythonprogramming.net. [Online]. Available: https://pythonprogramming.net/sqlite-part-2-dynamically-inserting-database-timestamps/. [Accessed: 30- Dec- 2020].

[2]S. Singanamalla, "How to print a particular value from dweet?", Stack Overflow, 2019. [Online]. Available: https://stackoverflow.com/questions/48717928/how-to-print-a-particular-value-from-dweet. [Accessed: 07- Dec- 2020].

[3]G. Haskins and S. Marnach, "Regular expression to find any number in a string", Stack Overflow, 2019. [Online]. Available: https://stackoverflow.com/questions/6508043/regular-expression-to-find-any-number-in-a-string. [Accessed: 08- Dec- 2020].

[4] [4]"Tkinter labels with textvariables", YouTube, 2020. [Online]. Available: https://www.youtube.com/watch?v=41lmZPwjmNw. [Accessed: 03- Jan- 2020].
"""
