import json
import hashlib
import datetime
import psycopg2
import requests
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from bs4 import BeautifulSoup
from fastapi import FastAPI
from fastapi import FastAPI, File, UploadFile, Path
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from pydantic import BaseModel, EmailStr

class EmailRequest(BaseModel):
    email: EmailStr

conf = ConnectionConfig(
    MAIL_USERNAME="dungeonoaks@gmail.com",
    MAIL_PASSWORD="pqdq ezxm fgpm cppe",
    MAIL_FROM="dungeonoaks@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True

)


tags_metadata = [
    {
        "name": "museum_api",
        "description": "API-приложение для решения кейса от команды Oaks Dungeon",
    },
]

app = FastAPI(openapi_tags=tags_metadata) #запуск FastAPI для возможности создания запросов

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Record:
    def __init__(self, name_1, name_2, name_3, phone, email, date, event, paid):
        self.name_1 = name_1
        self.name_2 = name_2
        self.name_3 = name_3
        self.phone = phone
        self.email = email
        self.date = date
        self.event = event
        self.paid = paid

class Event:
    def __init__(self, name, link, disription, photo, pub_date, museum):
        self.name = name
        self.link = link
        self.discription = disription
        self.photo = photo
        self.pub_date = pub_date
        self.museum = museum 

scheduler = BackgroundScheduler()

def delete_time_3():
    conn = psycopg2.connect(dbname="museum_db", user="postgres", password="21042005", host="127.0.0.1", port="5432")
    cursor = conn.cursor()
    #expiry_time = datetime.utcnow() - datetime.timedelta(minutes=3)
    cursor.execute(f"DELETE FROM records WHERE paid = False;")
    print('delete')
    conn.commit()
    cursor.close() 
    conn.close()

scheduler.add_job(delete_time_3, 'interval', minutes=3)
scheduler.start()

@app.on_event("startup")
async def startup_event():
    conn = psycopg2.connect(dbname="museum_db", user="postgres", password="21042005", host="127.0.0.1", port="5432")
    cursor = conn.cursor()
    r = requests.get('https://rss.app/feeds/ZidA2nFrYA3GT704.xml')
    r1 = requests.get('https://xn--e1aogg7a.xn--p1ai/upload/iblock_rss_2.xml')
    soup = BeautifulSoup(r.content, features='xml')
    soup1 = BeautifulSoup(r1.content, features='xml')
    articles = soup.findAll('item')
    articles1 = soup1.findAll('item')
    event_massive = []
    for a in articles1[:24]: #данного колличества достаточно для отображения актуальных данных
        title = a.find('title').text
        link = a.find('link').text
        description = a.find('description').text
        image = a.find('enclosure')
        url_image = image.get('url')
        pubDate = a.find('pubDate').text
        event = Event(title, link, description, url_image, pubDate, "-")

        event_massive.append(event)
    i = 0
    bufer = event_massive[0]
    event_massive[0] = event_massive[1]
    event_massive[1] = bufer
    for a in articles:
        museum = a.find('description').text
        event_massive[i].museum = museum
        i = i+1
    bufer1 = event_massive[0]
    event_massive[0] = event_massive[1]
    event_massive[1] = bufer1
    for a in event_massive:
        cursor.execute(f"SELECT COUNT(*) FROM events WHERE name = '{a.name}';")
        k = cursor.fetchone()[0]
        if k == 0:
            cursor.execute(f"INSERT INTO events (name, link, discription, photo, pub_date, museum) VALUES ('{a.name}', '{a.link}', '{a.discription}', '{a.photo}', '{a.pub_date}', '{a.museum}');")
            conn.commit()
        else:
            print ("event already add")
    cursor.close() 
    conn.close()
        

@app.post("/get_events", tags=["bd"])
async def get_events():
    conn = psycopg2.connect(dbname="museum_db", user="postgres", password="21042005", host="127.0.0.1", port="5432")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM events")
    events_mas = cursor.fetchall()
    keys = ["id", "name", "link", "discription", "photo", "pub_date", "museum"]
    events_dict_list = [dict(zip(keys, event)) for event in events_mas]
    json_string = json.dumps(events_dict_list, ensure_ascii=False)
    cursor.close() 
    conn.close()
    return(json_string)

@app.post("/get_records", tags=["bd"])
async def get_records():
    conn = psycopg2.connect(dbname="museum_db", user="postgres", password="21042005", host="127.0.0.1", port="5432")
    cursor = conn.cursor()   
    cursor.execute(f"SELECT * FROM records")
    records_mas = cursor.fetchall()
    keys = ["id", "name_1", "name_2", "name_3", "phone", "email", "c_date", "event_name", "paid"]
    records_dict_list = [dict(zip(keys, record)) for record in records_mas]
    json_string = json.dumps(records_dict_list, ensure_ascii=False)
    cursor.close() 
    conn.close()
    return(json_string)

@app.post("/add_record", tags=["bd"])      
async def add_record(name_1: str, name_2: str, name_3: str, phone: str, email: str, event: str):
    conn = psycopg2.connect(dbname="museum_db", user="postgres", password="21042005", host="127.0.0.1", port="5432")
    cursor = conn.cursor()
    current_datetime = datetime.datetime.today()
    current_year = current_datetime.year
    current_month = current_datetime.month
    current_day = current_datetime.day
    current_date = f"{current_day}.{current_month}.{current_year}"
    record = Record(name_1, name_2, name_3, phone, email, current_datetime, event, False)
    print(record.date)
    cursor.execute(f"INSERT INTO records (name_1, name_2, name_3, phone, email, c_date, event_name, paid) VALUES ('{record.name_1}', '{record.name_2}', '{record.name_3}', '{record.phone}', '{record.email}', '{record.date}', '{record.event}', {record.paid});")
    conn.commit()
    cursor.close() 
    conn.close()

@app.post("/get_count", tags=["bd"])      
async def get_count(event: str):
    conn = psycopg2.connect(dbname="museum_db", user="postgres", password="21042005", host="127.0.0.1", port="5432")
    cursor = conn.cursor()
    date1 = datetime.date.today()
    date2 = datetime.date.today() - datetime.timedelta(days=1)
    date3 = datetime.date.today() - datetime.timedelta(days=2)
    date4 = datetime.date.today() - datetime.timedelta(days=3)
    date5 = datetime.date.today() - datetime.timedelta(days=4)
    date6 = datetime.date.today() - datetime.timedelta(days=5)    
    date7 = datetime.date.today() - datetime.timedelta(days=6)
    count_records = 0
    cursor.execute(f"SELECT COUNT(*) FROM records WHERE c_date = '{date1}' AND event_name = '{event}';")
    count_records = count_records + cursor.fetchone()[0]
    cursor.execute(f"SELECT COUNT(*) FROM records WHERE c_date = '{date2}' AND event_name = '{event}';")
    count_records = count_records + cursor.fetchone()[0]
    cursor.execute(f"SELECT COUNT(*) FROM records WHERE c_date = '{date3}' AND event_name = '{event}';")
    count_records = count_records + cursor.fetchone()[0]
    cursor.execute(f"SELECT COUNT(*) FROM records WHERE c_date = '{date4}' AND event_name = '{event}';")
    count_records = count_records + cursor.fetchone()[0]
    cursor.execute(f"SELECT COUNT(*) FROM records WHERE c_date = '{date5}' AND event_name = '{event}';")
    count_records = count_records + cursor.fetchone()[0]
    cursor.execute(f"SELECT COUNT(*) FROM records WHERE c_date = '{date6}' AND event_name = '{event}';")
    count_records = count_records + cursor.fetchone()[0]
    cursor.execute(f"SELECT COUNT(*) FROM records WHERE c_date = '{date7}' AND event_name = '{event}';")
    count_records = count_records + cursor.fetchone()[0]
    return(count_records)

@app.post("/send_mail/", tags=["email"])
async def send_email(api: str, email: str):
    conn = psycopg2.connect(dbname="museum_db", user="postgres", password="21042005", host="127.0.0.1", port="5432")
    cursor = conn.cursor()
    cursor.execute(f"SELECT id FROM records WHERE email = '{email}' AND paid = False;")
    token = cursor.fetchone()[0]
    url = f"{api}confirm_mail/?token={token}"
    message = MessageSchema(
        subject="Подтверждение брони",
        recipients=[email],
        body=f"Для подтверждения покупки билета перейдите по ссылке: {url}",
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message)
    cursor.close() 
    conn.close()

@app.get("/confirm_mail/", tags=["email"])
async def confirm_mail(token: str):
    conn = psycopg2.connect(dbname="museum_db", user="postgres", password="21042005", host="127.0.0.1", port="5432")
    cursor = conn.cursor()   
    cursor.execute(f"UPDATE records SET paid = True WHERE id = {token};")
    conn.commit()
    cursor.close() 
    conn.close()    
    return("Вернитесь на сайт")

@app.post("/register", tags=["auth"])      
async def register(login: str, password: str, check: str):
    conn = psycopg2.connect(dbname="museum_db", user="postgres", password="21042005", host="127.0.0.1", port="5432")
    cursor = conn.cursor()
    hsh = hashlib.sha1()
    hsh.update(password.encode('utf-8'))
    pass_hash = hsh.hexdigest()
    if check == "admin":
        check_admin = True
    else:
        check_admin = False
    cursor.execute(f"SELECT COUNT(*) FROM users WHERE login = '{login}';")
    count = cursor.fetchone()[0]
    if count == 0:
        cursor.execute(f"INSERT INTO users (login, pass, administrator) VALUES ('{login}', '{pass_hash}', '{check_admin}');")
        conn.commit()
    else:
        return("errror")
    cursor.close() 
    conn.close()
    
@app.post("/login", tags=["auth"])      
async def login(login: str, password: str):
    conn = psycopg2.connect(dbname="museum_db", user="postgres", password="21042005", host="127.0.0.1", port="5432")
    cursor = conn.cursor()
    hsh = hashlib.sha1()
    hsh.update(password.encode('utf-8'))
    pass_hash = hsh.hexdigest()
    cursor.execute(f"SELECT COUNT(*) FROM users WHERE login = '{login}';")
    count = cursor.fetchone()[0]
    if count == 1:
        cursor.execute(f"SELECT pass FROM users WHERE login = '{login}';")
        password_check = cursor.fetchall()[0]
        print(type(password_check))
        print(f"('{pass_hash}',)")
        if f"('{pass_hash}',)" == f"{password_check}":
            cursor.execute(f"SELECT administrator FROM users WHERE login = '{login}';")
            admin = cursor.fetchall()[0]
            if f"(True,)" == f"{admin}":
                admin_v = True
            else:
                admin_v = False
            print(admin_v)
            cursor.close() 
            conn.close()    
            return (admin_v)
        else:
            cursor.close() 
            conn.close()    
            return("error")
    else:
        cursor.close() 
        conn.close()
        return("error")        