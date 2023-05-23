import os
import json
import requests
import datetime

#%%
def startup():
    # TODO variable data path
    student = input("Enter student-id: ")
    dataDir = "data"
    dataPath = "data/" + student + ".json"
    ingredientsPath = "data/ingredients.json"
    if not os.path.isdir(dataDir):
        os.makedirs(dataDir)
        print("data folder created")
    if not os.path.isfile(ingredientsPath):
        open(ingredientsPath, 'a').close()
        print("ingredients file created")
        ingredients = []
        save_data(ingredients, "ingredients")
    else:
        print("ingredients file found")
        ingredients = load_data("ingredients")
    if not os.path.isfile(dataPath):
        open(dataPath, 'a').close()
        print("data file created")
        profile = init_taste(student, ingredients)
    else:
        print("data file found")
        profile = load_data(student)
        profile = update_allergy(profile, ingredients)
    return profile, ingredients

#%%
def init_taste(student, ingredients):
    profile = {"id": student, "diet":{}, "allergy":{}, "taste":{}}
    print("Diet:")
    for i in ["Vegetarisch", "Vegan"]:
        if input(i + "? ").lower() in ["yes", "y"]:
            profile["diet"][i] = True
        else:
            profile["diet"][i] = False
    print("Allergien:")
    for i in ingredients:
        if input(i + "? ").lower() in ["yes", "y"]:
            profile["allergy"][i] = True
        else:
            profile["allergy"] = False
    save_data(profile, student)
    return profile

#%%
def update_allergy(profile, ingredients):
    print("New ingredients?")
    for i in ingredients:
        if i not in profile["allergy"]:
            if input(i + "? ").lower() in ["yes", "y"]:
                profile["allergy"][i] = True
            else:
                profile["allergy"][i] = False
    print("Done")
    save_data(profile, profile["id"])
    return profile
    
    
#%%
def load_data(student):
    path = "data/" + student + ".json"
    with open(path) as infile:
        data = json.load(infile)
        infile.close()
    print("read")
    return data

def save_data(data, student):
    path = "data/" + student + ".json"
    json_data = json.dumps(data, indent=4)
    with open(path, 'w') as outfile:
        outfile.write(json_data)
        outfile.close()
    print("written")

#%%
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

#%%
profile, ingredients = startup()

#save_data(ingredients, "ingredients")

#%%
#meals = get_all_meals()

todayMeals = get_today_meals()

#%%


