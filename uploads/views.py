from django.shortcuts import render

def data():
    with open("static/skills.txt", "r") as file:
        f = file.readlines()
        lst = [lst.strip() for lst in f]
        return lst