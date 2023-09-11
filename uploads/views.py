from django.shortcuts import render

# def data():
#     with open("static/skills.txt", "r") as file:
#         f = file.readlines()
#         lst = [lst.strip() for lst in f]
#         return lst
    


def data():
    with open("static/industry.txt", "r") as file:
        f = file.readlines()
        lst = [i.strip() for i in f]
        return lst