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

accXlast = 0 #declaring episdoeCal function globle variables
accYlast = 0
accZlast = 0
walkX = 0
walkY = 0
walkZ = 0

def GUI(time,date,episode,latitude,longitude): #[4] used the functions from 4
    GUItime = StringVar() #StringVar function sets the varaible up as string for the interface
    GUItime.set(time) #set GUI time set to the time value
    
    GUIdate = StringVar() 
    GUIdate.set(date) #set GUI date set to the date value
    
    GUIstatus = StringVar()
    GUIstatus.set(episode) #set GUI status set to the status value
    
    GUIlat = StringVar()
    GUIlat.set(latitude) #set GUI latitude set to the latitude
    
    GUIlong = StringVar()
    GUIlong.set(longitude) #set GUI longitude set to the longitude
    
    
    labTime = Label(root, text = "Time: ") #set the labels to the labels text
    labDate = Label(root, text = "Date: ")
    labStatus= Label(root, text = "Status: ")
    labLat = Label(root, text = "Latuide: ")
    labLong = Label(root, text = "longitude: ")
    
    disTime = Label(root, textvariable = GUItime) #set the labels for the dynamic varables
    disDate = Label(root, textvariable = GUIdate)
    disHeart = Label(root, textvariable = GUIstatus)
    disLat = Label(root, textvariable = GUIlat)
    disLong = Label(root, textvariable = GUIlong)
    
    labTime.grid(row = 0, column = 0, sticky = W) #printing all the labels for dynamic and none dynamic in a grid so it is all organised
    disTime.grid(row = 0, column = 1, sticky = W)
    labDate.grid(row = 1, column = 0, sticky = W)
    disDate.grid(row = 1, column = 1, sticky = W)
    labStatus.grid(row = 2, column = 0, sticky = W)
    disHeart.grid(row = 2, column = 1, sticky = W)
    labLat.grid(row = 3, column = 0, sticky = W)
    disLat.grid(row = 3, column = 1, sticky = W)
    labLong.grid(row = 4, column = 0, sticky = W)
    disLong.grid(row = 4, column = 1, sticky = W)


def episodeCal(accX,accY,accZ,episode,accXlast,accYlast,accZlast, walkX, walkY, walkZ): #function to check all the varaibles and passing the varaibles into the function
    if int(accX) > (accXlast + 500) or int(accX) < (accXlast - 500): #if the interger value is greater or less then 500 from the last acc value
        print("X walking")#print X walking for debug
        walkX = 1 #set X axis to one and equal walkX that is used later
    
    if int(accY) > (accYlast + 500) or int(accY) < (accYlast - 500):#if the interger value is greater or less then 500 from the last acc value
        print("Y walking")
        walkY = 1 #set Y axis to one and equal walkY that is used later
        
    if int(accZ) > (accZlast + 500) or int(accZ) < (accZlast - 500):#if the interger value is greater or less then 500 from the last acc value
        print("Z walking")
        walkZ = 1 #set Z axis to one and equal walkZ that is used later
        
    if (int(walkX) > 0) and (int(walkZ) > 0) or (int(walkY) > 0 and int(walkZ) > 0): #if X and Z or Y and Z are both 1 then run this loop
        if episode == 'R':
            print("Episode is happening please stay calm")
            tkinter.messagebox.showinfo('Samuel', 'Episode is happening')
        elif episode == 'M':
            print("students heart beat has raisen")
            tkinter.messagebox.showinfo('Samuel', 'Potential Episode')
        elif episode == 'G':
            print("All good") #all good print on console for debug
    else:
        if episode == 'R': #They are not walking so they are having an episode
            print("Please check but could be running")
            tkinter.messagebox.showinfo('Samuel', 'Please check but could be running')
        elif episode == 'M': #There will be a melt down soon 
            print("Problely just walking but keep an eye out")
        else:
            print("Student is calm") #print student is calm for debug

    walkX = 0 #reset the variables
    walkY = 0
    walkZ = 0
    accXlast = accX
    accYlast = accY
    accZlast = accZ
    return accXlast, accYlast, accZlast, walkX, walkY, walkZ


conn = sqlite3.connect('wristbandData.db') #connect to DataBase
c = conn.cursor() #create cursor
c.execute('CREATE TABLE IF NOT EXISTS dweetData(Date INTEGER, Time TEXT, Names TEXT, Acc TEXT, Latitude TEXT, Longitude TEXT, Episode TEXT)') #[1]creating Table

root = Tk() #declare the root for the GUI
root.title("Austim Software") #Title for the appilcation
root.resizable(width=FALSE, height=FALSE) #No resizing of the app
root.geometry('200x200') #setting teh size of the app

while(1): #Constantly run though the loop for until program is stopped
    dweet = str(dweepy.get_latest_dweet_for("group")) #[2] reading the dweet
    #print("Recived signal is ", dweet)
    
    #print("The final dweet")
    mainDweet = dweet[28:-1] #read the main dweet
    #print(mainDweet)
    
    #read the strings values 
    #print(" ")
    #print("Dweet values below ")
        
    dweetValues = re.findall(r"[+-]?\d+(?:\.\d+)?", mainDweet) #[3] reading the numbers in the dweet
    #print(dweetValues)
    
    #print("Dweet Chars below")
    dweetChars = re.findall(r"\w\D",mainDweet) #[2] reading the chars in the dweet
    #print(dweetChars)
    
    print(" ")
    print("The date is ")
    
    dayStr = dweetValues[2] #the date is the seconded value in the dweetValues string
    day = dayStr[1:3] #day value is between 1 and 3 in the day string removing unnessary values
    
    monthStr = dweetValues[1] #the date is the first value in the dweetValues string
    month = monthStr[1:3] #the number for the month is between 1 andd 3 in monthString
    
    date = day #add day, month and year to the end of the string in the Uk order of date 
    date += "/"
    date += month
    date += "/"
    date += dweetValues[0]
    print(date) #print date for debug
    
    print("The time is ")
    
    hour = dweetValues[3] #hour is the thrid dweetValue
    minute = dweetValues[4] #hour is the forth dweetValue
    time = str(hour) + ":" + str(minute) #add the hours and minutes together with a : inbetween for storge
    print(time) #print time
    
    print("The user is") 
    name = mainDweet[52:58] #name is betwee these values. The only problem is it can only accpet names with 6 or less chars
    print(name)
    
    print("The Accelerometer is ")
    
    accX = dweetValues[6] #X axis equals the sixth dweetValue
    accY = dweetValues[7] #Y axis equals the sixth dweetValue
    accZ = dweetValues[8] #Z axis equals the sixth dweetValue
    
    acc = str(accX) + ":" + str(accY) + ":" + str(accZ) #Issues with negitive numbers being read as positive
    print(acc)
    
    print("The GPS is ") #GPS problem with letters and numbers need to found. Also having 0s in front missing. 
    
    latitudeNum = dweetValues[9] #latitudeNum equals the dweetValues 9th letter 
    latitudeChar = dweetChars[-9] #latitudeChar is the 9th number from the back in teh chars string
    latitude = str(latitudeNum) + str(latitudeChar) #add the values together in a string
    
    longitudeNum = dweetValues[10] #Longitude equals the dweetValue 10 
    longitudeChar = dweetChars[-7] #latitudeChar is the 7th number from the back in teh chars string
    longitude = str(longitudeNum) + str(longitudeChar) #add the values together in a string
    
    print(latitude) 
    print(longitude)
    
    print("Heart Beat is ")
    
    episodeChars = dweetChars[-1] #This is the only value position will stay the same
    episode = episodeChars[0] #only the first Value in the Chars this is becuase there are two values together
    print(episode) #print episode
    
    #Putting this data into Data Base
    c.execute("INSERT INTO dweetData (Date, Time, Names, Acc, Latitude, Longitude, Episode) VALUES (?, ?, ?, ?, ?, ?, ?)", 
              (date, time, name, acc, latitude, longitude, episode)) #Dynamic variable inserted into database[1]
    conn.commit() #add the values to database
    #reading data below
    c.execute("SELECT * FROM dweetData WHERE episode=episode", {'episode':'G'}) #[1] search the data base 
    print("All the tables data is below") 
    allDweets = c.fetchall() #fetch te data 
    print(allDweets) #print fetched data
    
    
    #GUI below (Small issue the program only runs though once)
    
    GUI(time,date,episode,latitude,longitude) #call GUI function with the varaibles
    
    #Analysis of data is below
    
    episodeCal(accX,accY,accZ,episode,accXlast,accYlast,accZlast,walkX, walkY, walkZ) #call the episode calucator function
    
#The program is always connected but for a fail safe closing the cursor and database file
c.close() #out of loop close the cursor
conn.close() #close database
root.mainloop() #returns the visuals when closed down
   

 
""" Refances for the program

[1]"Python Programming Tutorials", Pythonprogramming.net. [Online]. Available: https://pythonprogramming.net/sqlite-part-2-dynamically-inserting-database-timestamps/. [Accessed: 30- Dec- 2020].

[2]S. Singanamalla, "How to print a particular value from dweet?", Stack Overflow, 2019. [Online]. Available: https://stackoverflow.com/questions/48717928/how-to-print-a-particular-value-from-dweet. [Accessed: 07- Dec- 2020].

[3]G. Haskins and S. Marnach, "Regular expression to find any number in a string", Stack Overflow, 2019. [Online]. Available: https://stackoverflow.com/questions/6508043/regular-expression-to-find-any-number-in-a-string. [Accessed: 08- Dec- 2020].

[4] [4]"Tkinter labels with textvariables", YouTube, 2020. [Online]. Available: https://www.youtube.com/watch?v=41lmZPwjmNw. [Accessed: 03- Jan- 2020].
"""
