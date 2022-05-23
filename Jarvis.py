import time, pyttsx3, datetime ,os, os_online2, os_off, pyautogui, sys
from random import choice
import requests
from PIL import Image
from decouple import AutoConfig
import subprocess as sp
import webbrowser as wb
import speech_recognition as sr
from tkinter import messagebox
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QTimer, QTime, QDate, Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from gui import Ui_MainWindow

# getting username from our .env file 
config = AutoConfig(search_path = 'C:\\Users\\Dev Gupta\\Documents\\R')
USERNAME = config('NAME')
BOTNAME = config('BOTNAME')

# Extracting voices that is available 
engines = pyttsx3.init('sapi5')
engines.setProperty('rate',180)
# engines.setProperty('volume',2.0)
voices = engines.getProperty('voices')

# Setting it's properties 
# There are two built-in voices at index [0] its David and at [1] its Zira
# print(voices[1].id)
engines.setProperty('voice',voices[0].id)

# Creating a speak function
def speak(audio):

    engines.say(audio)
    engines.runAndWait()

def wish():
    """ Here we are getting time by the time module, exact hour of it. Then sets if condition to greet"""
    # Checking time by datetime module 
    hour = int(datetime.datetime.now().hour)

    # Greeting as per the time interval
    if hour >= 0 and hour < 12 :
        speak('Good Morning')
    elif hour >= 12 and hour < 18 :
        speak('Good Afternoon')
    else:
        speak('Good Evening')

    speak(f'Hi Sir,i am Jarvis what can i do for you')

def voice_cmd():
    opening_text = [
    "Cool, I'm on it sir.",
    "Okay sir, I'm working on it.",
    "Just a second sir.",
]
    '''Taking command from user through microphone and then converting it into string to use it as query'''
    take = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening.......')
        take.pause_threshold = 0.5
        take.energy_threshold = 4000
        
        audio = take.listen(source)
# Putting try block to check if any exception occurs, So that it doesn't make any any problem while running
    try :
        
        print('Recognizing.....\r')
        query= take.recognize_google(audio, language = 'en-in')
        print('User said = ', query)

        
        
        if 'exit' in query.lower() or  'quit' in query.lower():

            hour =  datetime.datetime.now().hour
            if hour > 19 and hour <=24:
                speak('Good night sir , Take care!')
            else:
                speak('Have a good day sir')

            exit()
        elif query.lower() in GREETINGS:
                speak(choice(GREETINGS_RES))
            
        else:
            speak(choice(opening_text))

    except sr.UnknownValueError:
        messagebox.showerror('Error while fetching command','Sorry! was not able to understand. Could you please Speak that again....')
        speak('Sorry! was not able to understand. Could you please Speak that again....')
        query = 'NONE'
    
    return query
# ================================ MEMORY ============================================================================================

GREETINGS = ["hello jarvis", "jarvis", "wake up jarvis", "you there jarvis", "time to work jarvis", "hey jarvis",
             "ok jarvis", "are you there"]

GREETINGS_RES = ["always there for you sir", "i am ready sir",
                 "your wish my command", "how can i help you sir?", "i am online and ready for your command sir"]

# ======================================================================================================================================

class MainThread(QThread):
    def __init__(self):
        super(MainThread, self).__init__()

    def run(self):
        self.Matching_cases()

    def Matching_cases(self):
        wish()

        while True:
            Query = voice_cmd().lower()

            if 'command' in Query or 'cmd' in Query:
                os_off.open_cmd()

            elif 'calculator' in Query:
                os_off.calculator()
            
            elif 'camera'in Query:
                os_off.open_camera()
            
            elif 'notepad' in Query:
                os_off.notepad()

            elif 'time' in Query:
                ti = os_off.curr_time()
                speak(f"Sir the time is {ti}")
                # speak('for your convenience i am printing in on the screen ')
                print('\nTime = ',ti)

            elif 'creation' in Query:
                os_off.graphi()


            if 'open' in Query and 'paint' in Query:
                os_off.paint()
                speak('sir, you are now in the paint mode. In this mode i can draw some figures and lines over voice command')
                speak('What do you like to draw sir')
                
                while True:
                    
                    draw = voice_cmd()
                    if 'no' in draw:
                        break
                    
                    if 'line' in draw:
                        speak('in which way sir up, down, left, right')
                        direction = voice_cmd()
                        distance = 200
                        if 'up' in direction:
                            pyautogui.dragRel(0, -distance, duration=0.2) #move up

                        elif 'right' in direction:
                            pyautogui.dragRel(distance, 0, duration=0.2) #move right
                        
                        elif 'down' in direction:
                            pyautogui.dragRel(0, distance, duration=0.2) #move down

                        elif 'left' in direction:
                            pyautogui.dragRel(-distance, 0, duration=0.2) #move left

                    elif 'spiral'in draw:
                        pyautogui.click()
                        distance = 200

                        while distance > 0:
                            pyautogui.dragRel(distance, 0, duration=0.2) # move right
                            distance = distance - 10
                            pyautogui.dragRel(0, distance, duration=0.2) # move down

                            pyautogui.dragRel(-distance, 0, duration=0.2) #move left
                            distance = distance - 10

                            pyautogui.dragRel(0, -distance, duration=0.2) #move up
                
                    speak('Anything else sir')

            elif 'close the paint' in Query or 'close paint' in Query:
                speak('Closing the Ms paint')
                os.system('taskkill /f /im mspaint.exe')

            if 'ip' in Query:
                ip_adr = os_online2.my_ip()
                speak(f'Your ip address is {ip_adr}. For your convenience i am printing it on screen')
                print('Your ip address is',ip_adr)

            elif 'change tab' in Query or 'switch window' in Query:
                speak("Okay sir, Switching the window")
                pyautogui.keyDown("alt")
                pyautogui.press("tab")
                time.sleep(1)
                pyautogui.keyUp("alt")
            
            elif 'hide my folder' in Query or 'hide all files' in Query or 'hide' in Query:
                os.system('attrib +h /s /d')
                speak('sir, All files in this folder are now hidden')

            elif 'visible' in Query :
                os.system('attrib -h /s /d')
                speak('All the hidden files are now visible')

            elif 'open'in Query and 'youtube' in Query :
                speak('What do you want to play on Youtube')
                video = voice_cmd().lower()
                os_online2.play_onyt(video)
                
            elif 'geek' in Query or 'geek for geeks' in Query:
                wb.open('https://www.geeksforgeeks.org/')

            elif 'open google' in Query:
                wb.open('google.com')
                speak('What do you want to search on Google')
                search = voice_cmd().lower()
                os_online2.search_on_google(search)

            elif 'system' in Query and 'stats' in Query:
                stat = os_online2.system_stats()
                speak(stat)
                speak("For your convenience, I'm printing it on your screen ")
                print(stat)

            elif 'notes' in Query:
                speak('what do you wanna take as note sir write it down ')
                note = input('\n  Notes = ')
                os_online2.take_notes(note)

            elif 'play'in Query and 'music' in Query:
                    music_dir = 'C:\\Users\\Dev Gupta\\Music'
                    songs = os.listdir(music_dir)
                    for song in songs:
                        os.startfile(os.path.join(music_dir, song))
                
            elif "take screenshot" in Query or "take a screenshot" in Query or "capture the screen" in Query :
                speak('By what name you wanna save this screenshot')
                name = voice_cmd().lower()
                speak('Alright sir, taking the screenshot')
                os_off.screenshot(name)
                speak('Succesfully taken the screenshot')

            elif 'show me screenshot' in Query:
                try:
                    img = Image.open(f"D:\\{name}.png")
                    img.show(img)
                    speak('Here it is sir')
                    time.sleep(2)
                except IOError:
                    print( 'sorry')
                    # speak('Sorry, I am unable to display it now sir ')

            elif 'show' in Query and 'pictures' in Query:
                try:
                    # name = voice_cmd().lower()
                    img = Image.open(f"Pictures\\{'Diwali'}.png")
                    img.show(img)
                    speak('Here it is sir')
                    time.sleep(2)
                except IOError:
                    speak('Sorry, I am unable to display it now sir ')

            elif 'excel' in Query:
                speak('Just a minute sir opening excel')
                os_online2.excel()

            elif 'send' in Query and 'whatsapp' in Query:
                speak('Please write down the number in the terminal whom you want to send msg')
                print('\n=================Sending Whatsapp message=============\n')
                num = int(input('\nEnter the number = '))
                if num > 6000000000 and num < 9999999999:
                    speak('What to do you wanna say please type it in the terminal')
                    msg = input('\nEnter msg = ')
                    os_online2.whatapps(num,msg)
                else:
                    speak('Please enter valid phone number')

            elif 'wikipedia' in Query :
                speak(os_online2.wikipedia_search())
            
            elif 'introduce'in Query and 'yourself' in Query:

                speak("Allow me to introduce myself, I am Parker a virtual artificial intelligence and i am here to assist you with variety of tasks. Your wish my command i can perform several task , But i'm still under development so there are some things that is not possible for now but will be very soon")
                
            elif 'joke' in Query:
                
                jok = os_online2.random_joke()
                speak(f"here's your joke sir {jok}")

            elif 'shinchan' in Query:
                os_off.shinchan()
                speak('now creating a shinchan ')
            
            elif 'movies' in Query:
                movie = os_online2.trend_movie()
                speak(f'Some of the trending movie are {movie}')
                speak("For your convenience, I'm printing it on your screen ")
                print(f'Movie names = {movie}', sep='\n')

            elif 'about' in Query and 'weather' in Query:
                # ip_adr = os_online2.my_ip()
                # city = requests.get(f"https://ipapi.co/{ip_adr}/city/").text()
                speak('Which cities weather report you wanna know about Sir')
                city = voice_cmd()
                weather,temp,fells = os_online2.weather_report(city)
                speak(f'Here is the weather report of {city} ')
                speak(f'Temperature is {temp}, but it feels like {fells}')
                speak(f'Also, the weather report talks about {weather}')
                speak("For your convenience, I'm printing it on your screen ")
                print(f'\n\t Weather Report \n\nTemperature = {temp}\n Feels like = {fells}\n Weather = {weather}\n')

            elif 'news' in Query  or 'latest' in Query and 'news' in Query:
                news = os_online2.news_teller()
                speak(f"I'm reading out the latest news headlines, sir")
                speak(news)
                speak("For your convenience, I'm printing it on your screen ")
                print(f'Latest news = {news}', sep='\n')

            elif 'goodbye jarvis' in Query or 'sleep jarvis' in Query:
                speak('Ok sir shuting down, take care sir ')
            
            else:
                speak("The command given doesn't seems to be appropriate or isn't in my function ")

            speak('Any other request sir')

startExecution = MainThread()

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)

    def __del__(self):
        sys.stdout = sys.__stdout__

    # def run(self):
    #     self.TaskExection
    def startTask(self):
        self.ui.movie = QtGui.QMovie("C:\\Users\\Dev Gupta\\Pictures\\Jarvis pics\\live_wallpaper.gif")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("C:\\Users\\Dev Gupta\\Pictures\\Jarvis pics\\initiating.gif")
        self.ui.label_2.setMovie(self.ui.movie)
        self.ui.movie.start()
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        startExecution.start()

    def showTime(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        label_time = current_time.toString('hh:mm:ss')
        label_date = current_date.toString(Qt.ISODate)
        self.ui.textBrowser.setText(label_date)
        self.ui.textBrowser_2.setText(label_time)


app = QApplication(sys.argv)
jarvis = Main()
jarvis.show()
exit(app.exec_())


    