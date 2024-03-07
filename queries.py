import mysql.connector
import streamlit as st

#connection
conn=mysql.connector.connect(
    host="localhost",
    port="3306",
    user="root",
    password="",
    db="mental_health_db"
)

c=conn.cursor()

#fetching

def fetch_all_data():
    c.execute("select * from mental_health_db")
    data=c.fetchall()
    return data
