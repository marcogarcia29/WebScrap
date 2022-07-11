from bs4 import BeautifulSoup
from colorama import Cursor
import requests
import sqlalchemy
import pandas as pd
from sqlalchemy.orm import sessionmaker
import requests
import sqlite3
from datetime import datetime, timezone, date

DATABASE_LOCATION = ""

html = requests.get("https://www.cptec.inpe.br/sp/sao-paulo").content

soup = BeautifulSoup(html, 'html.parser')

#temperatura_max = soup.find(class_="bloco-previsao d-flex flex-column text-center")
temperatura_max = soup.select("html body label")
temperatura_min = soup.select("html body label")

print(temperatura_max[1].string)
print(temperatura_min[2].string)
today = date.today()

engine = sqlalchemy.create_engine(DATABASE_LOCATION)
conn = sqlite3.connect('my_weather.sqlite')
cursor = conn.cursor()   

sql_query = """ 
CREATE TABLE IF NOT EXISTS my_weather(
    high_temp_value INT(2),
    low_temp_value INT(2),
    date_time DATE
)
"""
cursor.execute(sql_query)
temperatura_min = str(temperatura_min[2].string)[:-1]
temperatura_max = str(temperatura_max[1].string)[:-1]
cursor.execute(f"INSERT INTO my_weather VALUES ('{temperatura_max}' , '{temperatura_min}', '{today}')")
print("Opened database successfully")
conn.commit()
cursor.close()
print("Close database successfully")