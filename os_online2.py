import time, requests, wikipedia, smtplib,psutil, math, subprocess, datetime
from tkinter import messagebox
import pywhatkit as kit
from email.message import EmailMessage
from decouple import AutoConfig
import webbrowser as wb
import wolframalpha


c = AutoConfig(search_path = 'C:\\Users\\Dev Gupta\\Documents\\R')
EMAIL = c('EMAIL')
PASS = c('PASSWORD')
NEWS_API = c('NEWS_API_KEY')
WEATHER_API = c('WEATHER_API_KEY')
MOVIE_API = c('MOVIE_API_KEY')
# WOLFRAM = c('WOLRFRAM_API')

def my_ip():
    ip_adress = requests.get('https://api64.ipify.org?format=json').json()
    return ip_adress['ip']

def wikipedia_search(query):
    return  wikipedia.summary(query, sentences= 2)

def translator():
    kit.search('english to hindi')

def play_onyt(video):
    kit.playonyt(video)

def search_on_google(search):
    kit.search(search)

def whatapps(number,msg):
    kit.sendwhatmsg_instantly(f'+91{number}', msg)

def advice():
    adcv = requests.get("https://api.adviceslip.com/advice").json()
    return adcv['slip']['advice']

# helping function for system_stats 
def convert_size(size_bytes):
    if size_bytes == 0:
        return '0B'
    else:
        sizes = ['B','KB','MB','GB','TB','PB','EB','ZB']
        i = int(math.floor(math.log(size_bytes, 1024)))
        power = math.pow(1024,i)
        s = round(size_bytes / power, 2)
        print("%s %s" % (s, sizes[i]))
        return "%s %s" % (s, sizes[i])

def system_stats():
    battery_percent = psutil.sensors_battery().percent
    cpu_stats = str(psutil.cpu_percent())
    memory_in_use = convert_size(psutil.virtual_memory().used)
    total_memory = convert_size(psutil.virtual_memory().total)
    return f"Currently {cpu_stats} percent of CPU is being used, {memory_in_use} of RAM out of total {total_memory} is being used and battery level is at {battery_percent} percent"
     
def take_notes(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(':',"-") + '-note.txt'

    with open(file_name,'w+') as f:
        f.write(text)

# def computational_intelligence(question):
#     try:
#         client = wolframalpha.Client(WOLFRAM)
#         answer = client.query(question)
#         answer = next(answer.results).text
#         print(answer)
#         return answer
#     except:
#         print("Sorry sir I couldn't fetch your question's answer. Please try again ")
#         return None

def excel():
    subprocess.Popen('start excel', shell = True)

def random_joke():
    head = {
        'Accept' : 'application/json' 
    }
    ans = requests.get("https://icanhazdadjoke.com/",headers= head).json()
    return ans['joke']

def send_email(receiver_add,msg,sub):
    try :
        email = EmailMessage()
        email['To'] = receiver_add 
        email['Subject'] = sub
        email['From'] = EMAIL
        email.set_content(msg)
        s = smtplib.SMTP('smtp.gmail.com',568)
        s.starttls()
        s.login(EMAIL,PASS)
        s.send_message(email)
        s.close()
        print('Behj diya ja jakar check kar')
        return True
    except Exception as e:
        print(e)
        messagebox.showerror('The Exception Occured',e)
        return False

def news_teller():
    
    result = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API}&category=general").json() 
    articles = result['articles']
    
    headline = [news['title'] for news in articles]

    return headline[:5]

def weather_report(city):
    res = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API}&units=metric").json()
    weather = res['weather'][0]['main']
    temp = res['main']['temp']
    fells = res['main']['feels_like']

    return weather,f'{temp}℃',f'{fells}℃'

def trend_movie():
    tren = []
    result = requests.get(f"https://api.themoviedb.org/3/trending/movie/day?api_key={MOVIE_API}").json()
    ans = result['results']
    for movie in ans:
        tren.append(movie['original_title'])
    
    return str(tren[:5])

if __name__ == '__main__':
    # computational_intelligence('What is distribution')
    take_notes('trying my best')
    # system_stats()
    # excel()
    # send_email('sarita.official1983@gmail.com','Trying my program','apna program check kar raha hu ki automatic hai ki nahi ')
    # print(random_joke())                       
    # whatapps(9625946640,'hlo mai programmer hu mera jarvis msg kar raha hai hehehe')