import os
import json
import requests
import datetime
import re

#%%
# main program
def main():
    # TODO variable data path
    todayMeals = get_today_meals()
    student = input("Enter student-id: ")
    dataDir = "data"
    dataPath = "data/" + student + ".json"
    allergensPath = "data/allergens.json"
    if not os.path.isdir(dataDir):
        os.makedirs(dataDir)
        print("data folder created")
    if not os.path.isfile(allergensPath):
        open(allergensPath, 'a').close()
        print("allergens file created")
        allergens = get_allergens(todayMeals)
        save_data(allergens, "allergens")
    else:
        print("allergens file found")
        allergens = load_data("allergens")
        allergens = update_allergens(allergens, todayMeals)
    if not os.path.isfile(dataPath):
        open(dataPath, 'a').close()
        print("data file created")
        profile = init_taste(student, allergens)
    else:
        print("data file found")
        profile = load_data(student)
        profile = update_allergy(profile, allergens)
    return None

#%%
# initalize profile of new user
def init_taste(student, ingredients):
    profile = {"id": student, "diet":{}, "allergens":{}, "taste":{}}
    print("Diet:")
    for i in ["Vegetarisch", "Vegan"]:
        if input(i + "? ").lower() in ["yes", "y"]:
            profile["diet"][i] = True
        else:
            profile["diet"][i] = False
    print("Allergien:")
    for i in ingredients:
        if input(i + "? ").lower() in ["yes", "y"]:
            profile["allergens"][i] = True
        else:
            profile["allergens"][i] = False
    save_data(profile, student)
    return profile

#%%
# update allergen preferences of user
def update_allergy(profile, allergens):
    print("New allergens?")
    for i in allergens:
        if i not in profile["allergens"]:
            if input(i + "? ").lower() in ["yes", "y"]:
                profile["allergens"][i] = True
            else:
                profile["allergens"][i] = False
    print("Done")
    save_data(profile, profile["id"])
    return profile
    
# update allergens
def update_allergens(allergens, meals):
    new = get_allergens(meals)
    for i in new:
        if i not in allergens:
            allergens.append(i)
    print("allergens updated")
    return allergens

# get allergens from list of meals
def get_allergens(meals):
    allergens = []
    for i in meals:
        for j in i["allergens"]:
            if j["type"] == "Allergen":
                allergens.append(j["longName"])
    return allergens

#%%
# load data from json
def load_data(student):
    path = "data/" + student + ".json"
    with open(path) as infile:
        data = json.load(infile)
        infile.close()
    print("read")
    return data

# save data to json
def save_data(data, student):
    path = "data/" + student + ".json"
    json_data = json.dumps(data, indent=4)
    with open(path, 'w') as outfile:
        outfile.write(json_data)
        outfile.close()
    print("written")

#%%
# use api to get meals
def get_all_meals():
    headers = {
        'accept': 'application/json;charset=utf-8',
        'apikey': 'eyJ4NXQiOiJOVGRtWmpNNFpEazNOalkwWXpjNU1tWm1PRGd3TVRFM01XWXdOREU1TVdSbFpEZzROemM0WkE9PSIsImtpZCI6ImdhdGV3YXlfY2VydGlmaWNhdGVfYWxpYXMiLCJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJPTERBUC1QUk9YWVwvbW9lYmVydEBjYXJib24uc3VwZXIiLCJhcHBsaWNhdGlvbiI6eyJvd25lciI6Ik9MREFQLVBST1hZXC9tb2ViZXJ0IiwidGllclF1b3RhVHlwZSI6bnVsbCwidGllciI6IlVubGltaXRlZCIsIm5hbWUiOiJQZXJ2YXNpdmUgQ29tcHV0aW5nIiwiaWQiOjE1OSwidXVpZCI6ImY0Njc5NDcxLTliYWQtNGEyMS1hZDFmLTFjMDYyMzViNDY0MSJ9LCJpc3MiOiJodHRwczpcL1wvYXBpdXAudW5pLXBvdHNkYW0uZGU6NDQzXC9vYXV0aDJcL3Rva2VuIiwidGllckluZm8iOnsiVW5saW1pdGVkIjp7InRpZXJRdW90YVR5cGUiOiJyZXF1ZXN0Q291bnQiLCJncmFwaFFMTWF4Q29tcGxleGl0eSI6MCwiZ3JhcGhRTE1heERlcHRoIjowLCJzdG9wT25RdW90YVJlYWNoIjp0cnVlLCJzcGlrZUFycmVzdExpbWl0IjowLCJzcGlrZUFycmVzdFVuaXQiOm51bGx9fSwia2V5dHlwZSI6IlNBTkRCT1giLCJzdWJzY3JpYmVkQVBJcyI6W3sic3Vic2NyaWJlclRlbmFudERvbWFpbiI6ImNhcmJvbi5zdXBlciIsIm5hbWUiOiJtZW5zYUFQSSIsImNvbnRleHQiOiJcL21lbnNhQVBJXC8yLjAiLCJwdWJsaXNoZXIiOiJaSU0iLCJ2ZXJzaW9uIjoiMi4wIiwic3Vic2NyaXB0aW9uVGllciI6IlVubGltaXRlZCJ9XSwiaWF0IjoxNjg0MTU3NTk0LCJqdGkiOiIwNDNhMmYxNy0zODAwLTQ2ZjItYTdjYS03ODg1NWQwYWEyYzcifQ==.Cso60hvx1-CoTk47hsiJUtQfHnwgvFK3nCiNkJ2RAMemJ8_XG80j-8hS0yCxGDfHWvbIU2bWP79nmM7G7uGncyAjUbuFkRIZZZArHdcs1xSCHENS2gSpw4a-Ek0Nz5VVy5c4Yttr_MSNozLMpClUVf5ew-0FcpBxfZCwhNKuHZtjLW12iBEuh4xPauVdRna6pLJc0zhDWhq66ubwU99UmfEGMYtdBP3UvXd4AJDtBTBQBNSjXzYzBosHgvGtta2sOHMeNn9tNLdtGc1thZD_7Ge76J_ieZt_90cgYmhD7YsNEXeWoH4nPsoWEOHZNZ2LL5Y6f0DAcDCMNAvqvY8mVw==',
    }

    params = {
        'location': 'Golm',
    }

    response = requests.get('https://apiup.uni-potsdam.de/endpoints/mensaAPI/2.0/meals', params=params, headers=headers)
    return response.json()["meal"]

# filter not needed meals
# (not today, Nudeltheke, Abendangebot)
def get_today_meals():
    meals = get_all_meals()
    day = datetime.datetime.now().strftime("%Y-%m-%d")
    tmeals = []
    for i in meals:
        if i["date"][:10] == day:
            if i["description"] != "." and "Nudeltheke" not in i["title"] and "Abendangebot" not in i["title"]:
                tmeals.append(i)
    return tmeals

#%%
# TODO integrate into main

# parse name of meal into parts
# WIP only simplified for now
# no difference between "mit" and "ohne"
# theorretically "ohne" should appear very rarely
# no gramatical cases -> Pilzen != Pilze
def parse_name(meal):
    parts = []
    words = re.split(",|mit|und|ohne|auf|bei|in|über|unter|zu",meal["description"])
    for i in words:
        i = i.strip()
        if i not in parts:
            parts.append(i)
    print(parts)

# select meal from list of meals
def select_meal(meals):
    orders = []
    print("Todays meals:")
    for i in meals:
        print(str(i["order"]) + ": " + i["description"])
        orders.append(str(i["order"]))
    s = None
    while s not in orders:
        print(orders)
        s = input("Select meal from above: ")
    print(str(s) + " selected")
    for i in meals:
        if str(i["order"]) == s: return i

#%%
# TODO:
# rate selected meal
# update taste profile
    
#%%
main()

#%%




