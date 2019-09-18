from flask import Flask, request
import sqlite3 as lite
import os

# import cv2

app = Flask(__name__)


def add_to_db(name, funfact, tribe, image, job_title):
    db = lite.connect("Photo Card Database.db")
    c = db.cursor()
    c.execute(''' INSERT INTO Photo_Card(Name, Tribe, Image, JobTitle, FunFact)
    VALUES(?,?,?,?,?)''', (name, tribe, image, job_title, funfact))
    db.commit()