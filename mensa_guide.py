import os
import json
import requests
import datetime
import re
import PySimpleGUI as sg

#%%
# main program
def main():
    # setup
    # TODO variable data path
    # TODO check user-id format 
    todayMeals = get_today_meals()
    user = input("User-id eingeben: ")
    dataDir = "data"
    dataPath = "data/" + user + ".json"
    allergensPath = "data/allergens.json"
    if not os.path.isdir(dataDir):
        os.makedirs(dataDir)
        print("D: data folder created")
    if not os.path.isfile(allergensPath):
        open(allergensPath, 'a').close()
        print("D: allergens file created")
        allergens = get_allergens(todayMeals)
    else:
        print("D: allergens file found")
        allergens = load_data("allergens")
        allergens = update_allergens(allergens, todayMeals)
    save_data(allergens, "allergens")
    if not os.path.isfile(dataPath):
        open(dataPath, 'a').close()
        print("D: data file created")
        profile = init_taste(user, allergens)
    else:
        print("D: data file found")
        profile = load_data(user)
        profile = update_allergy(profile, allergens)
        
    # recommend meal and select meal
    selMeal  = select_meal(profile, todayMeals)
    if selMeal == None:
        print("D: done")
        return None
    
    # update taste profile
    profile = rate_meal(profile, selMeal)
    save_data(profile, profile["id"])
    
    print("D: done")
    
    return None

#%%
# initalize profile of new user
def init_taste(user, allergens):
    profile = {"id": user, "diet":{}, "allergens":{}, "taste":{}}
    print("Präferenzen [ja, j, Rest->nein]:")
    for i in ["Vegetarisch", "Vegan"]:
        if input(i + "? ").lower() in ["ja", "j"]:
            profile["diet"][i] = True
        else:
            profile["diet"][i] = False
    print("Allergene [ja, j, Rest->nein]:")
    for i in allergens:
        if input(i + "? ").lower() in ["ja", "j"]:
            profile["allergens"][i] = True
        else:
            profile["allergens"][i] = False
    save_data(profile, user)
    return profile


# update allergen preferences of user
def update_allergy(profile, allergens):
    new = False
    print("D: searching for new allergens")
    for i in allergens:
        if i not in profile["allergens"]:
            new = True
    if new:
        print("Allergene [ja, j, Rest->nein]:")
        for i in allergens:
            if i not in profile["allergens"]:
                if input(i + "? ").lower() in ["ja", "j"]:
                    profile["allergens"][i] = True
                else:
                    profile["allergens"][i] = False
    print("D: done")
    save_data(profile, profile["id"])
    return profile
    
# update allergens
def update_allergens(allergens, meals):
    new = get_allergens(meals)
    for i in new:
        if i not in allergens:
            allergens.append(i)
    print("D: allergens updated")
    return allergens

# get allergens from list of meals
def get_allergens(meals):
    allergens = []
    for i in meals:
        for j in i["allergens"]:
            if j["type"] == "Allergen":
                allergen = j["longName"]
                if allergen not in allergens:
                    allergens.append(allergen)
    return allergens

#%%
# load data from json
def load_data(user):
    path = "data/" + user + ".json"
    with open(path) as infile:
        data = json.load(infile)
        infile.close()
    print("D: read")
    return data

# save data to json
def save_data(data, user):
    path = "data/" + user + ".json"
    json_data = json.dumps(data, indent=4)
    with open(path, 'w') as outfile:
        outfile.write(json_data)
        outfile.close()
    print("D: written")

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

# filter unneeded meals
# (other days, Nudeltheke, Abendangebot)
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
# parse description of meal into parts
# WIP only simplified for now
# no difference between "mit" and "ohne"
# theoretically "ohne" should appear very rarely
# no gramatical cases -> Pilzen != Pilze
# TODO: junge, frische
def parse_desc(meal):
    parts = []
    words = list(filter(("").__ne__, re.split(",| mit | und | ohne | auf | bei | in | über | unter | zu | dazu | an ", " " + meal["description"] + " ")))
    for i in words:
        i = i.strip()
        if i not in parts:
            parts.append(i)
    return parts

# select meal from rated list of fitting meals
def select_meal(profile, meals):
    f_meals = filter_meals(profile, meals)
    orders = []
    print("Heutige Gerichte:")
    print("Bewertung:\t | Nummer:\t | Gericht:")
    rated = get_rated_meals(profile, f_meals)
    for i in rated:
        r = round(i[0],1)
        if r < 0:
            print(str(round(i[0],1)) + "\t\t | " + str(i[1]) + "\t\t | " + i[2] + " " + str(tuple(i[3])))
        else:
            print(str(round(i[0],1)) + "\t\t\t | " + str(i[1]) + "\t\t | " + i[2] + " " + str(tuple(i[3])))
        orders.append(str(i[1]))
    orders.append("0")
    print("---\t\t\t | 0\t\t | Nichts essen")
    s = None
    while s not in orders:
        print(orders)
        s = input("Gericht von oben auswählen: ")
    if s == "0":
        return None
    for i in f_meals:
        if str(i["order"]) == s: return i
    else: return None

# filter meals by diet and allergens
def filter_meals(profile, meals):
    filtered_meals = []
    p_allergens = []
    for i in profile["allergens"]:
        if profile["allergens"][i]:
            p_allergens.append(i)
    diet = set()
    for i in profile["diet"]:
        if profile["diet"][i]:
            diet = diet | {i}
    # vegetarians can also eat vegan meals
    if "Vegetarisch" in diet:
        diet = diet | {"Vegan"}
    for i in meals:
        if (diet & set(i["type"])) or not diet:
            m_allergens = get_allergens([i])
            if not set(p_allergens) & set(m_allergens):
                filtered_meals.append(i)
    return filtered_meals
                

# rate meal and update taste profile
def rate_meal(profile, meal):
    parts = parse_desc(meal)
    print("Gericht bewerten von -5 (sehr schlecht) bis 5 (sehr gut):")
    rating = -6
    while not (-5 <= rating <= 5):
        rating = input(meal["description"] + ": ").strip()
        if rating.lstrip('-').isdigit():
            rating = int(rating)
        else:
            rating = -11
    for i in parts:
        if i in profile["taste"]:
            profile["taste"][i] = round(0.7 * rating + 0.3 * profile["taste"][i])
        else:
            profile["taste"][i] = rating
    return profile

# get rating for meal based on profile
def calc_rating(profile, meal):
    parts = parse_desc(meal)
    rating = 0
    for i in parts:
        if i in profile["taste"]:
            rating += profile["taste"][i]
    return (rating / len(parts))

# rate meals
def get_rated_meals(profile, meals):
    rated = []
    for i in meals:
        rated.append((calc_rating(profile, i), i["order"], i["description"], i["type"]))
    return reversed(sorted(rated))


#%%
# reset taste profile
# not used
def reset_taste(profile):
    for i in profile["taste"]:
        profile["taste"][i] = 0
    return profile

# update diet and allergens profile
# WIP, not used
def update_profile(profile):
    return init_taste(profile["id"], list(profile["allergens"].keys()))

def create_blank_profile(user):
    profile = {"id": user, "diet":{}, "allergens":{}, "taste":{}}
    save_data(profile, user)
    return profile
# TODO function to reset/update user profile
#%%

# TODO gray out filtered options instead of removing
def make_meal_layout(profile, todayMeals):
    meallist_layout = [
        [sg.Text('Gericht wählen:')],
        [sg.Text('Heutige Gerichte:')],
        ]
    f_meals = filter_meals(profile, todayMeals)
    rated = get_rated_meals(profile, f_meals)
    orders = []
    for i in rated:
        meallist_layout.append([sg.Text(str(round(i[0],1)) + " | "  + i[2]), 
                                sg.Radio('', 1, default=False, key=str(i[1]))])
        orders.append(str(i[1]))
    meallist_layout.append([sg.Text("0.0 | Nichts essen"), 
                            sg.Radio('', 1, default=True, key='0')])
    meallist_layout.append([sg.Button('Weiter')])
    return meallist_layout, orders, f_meals

def make_gui(theme=None):
    
    todayMeals = get_today_meals()
    
    # TODO manage users
    user = sg.popup_get_text('Bitte User-ID eingeben')
    if not user:
        sg.popup_cancel('Ungültige ID. Programm beendet')
        raise SystemExit()
    
    dataDir = "data"
    dataPath = "data/" + user + ".json"
    allergensPath = "data/allergens.json"
    if not os.path.isdir(dataDir):
        os.makedirs(dataDir)
        print("D: data folder created")
    if not os.path.isfile(allergensPath):
        open(allergensPath, 'a').close()
        print("D: allergens file created")
        allergens = get_allergens(todayMeals)
    else:
        print("D: allergens file found")
        allergens = load_data("allergens")
        allergens = update_allergens(allergens, todayMeals)
    save_data(allergens, "allergens")
    
    
    if not os.path.isfile(dataPath):
        open(dataPath, 'a').close()
        print("D: data file created")
        window = 0
    else:
        print("D: data file found")
        profile = load_data(user)
        window = 1
    

    if window == 0:
        profile = create_blank_profile(user)
        save_data(profile, user)
        
        np_layout = [
            [sg.Text('Neues Geschmacksprofil:')],
            [sg.Text('Vegetarisch'), sg.Radio('ja', 1, default=False, key='-VEGE-'), sg.Radio('nein', 1, default=True)],
            [sg.Text('Vegan'), sg.Radio('ja', 2, default=False, key='-VEGA-'), sg.Radio('nein', 2, default=True)],
            [sg.Button('Weiter')]
            ]
        np_win = sg.Window('Neues Geschmacksprofil', np_layout, element_justification='c')
     
    new_allergens = []
    for i in allergens:
        if i not in profile['allergens']:
            new_allergens.append(i)
    new_all_num = len(new_allergens)
    all_count = 0
    
    if not new_all_num:
        window = 2
        meallist_layout, orders, f_meals = make_meal_layout(profile, todayMeals)
        meallist_win = sg.Window('Gerichtauswahl', meallist_layout, element_justification='c')
    else:
        all_layout = [
            [sg.ProgressBar(new_all_num, orientation='h', size=(20,10), key='-ALLER_PROGRESS-')],
            [sg.Text('Allergene: ')],
            [sg.Text(new_allergens[0], key='-ALLER-')],
            [sg.Text('allergisch'), sg.Radio('ja', 1, default=False, key='-ALLER_YES-'), sg.Radio('nein', 1, default=True, key='-ALLER_NO-')],
            [sg.Button('Weiter')]
            ]
                   
    if window == 1:
        all_win = sg.Window('Allergene', all_layout, element_justification='c')
        
    # windows:
    # 0: np
    # 1: all
    # 2: recommendation
    # 3: rating
    while True:
        if window == 0:
            event, values = np_win.read()
            if event == sg.WINDOW_CLOSED or event == 'Exit':
                break
            
            if event == 'Weiter':
                profile["diet"]['Vegetarisch'] = values['-VEGE-']
                profile["diet"]['Vegan'] = values['-VEGA-']
                window = 1
                np_win.close()
                all_win = sg.Window('Allergene', all_layout, element_justification='c')
                
        if window == 1:
            event, values = all_win.read()
            if event == sg.WINDOW_CLOSED or event == 'Exit':
                break
            if event == 'Weiter':
                profile["allergens"][new_allergens[all_count]] = values['-ALLER_YES-']
                if all_count < new_all_num-1:
                    all_count += 1
                    all_win['-ALLER-'].update(new_allergens[all_count])
                    all_win['-ALLER_YES-'].update(False)
                    all_win['-ALLER_NO-'].update(True)
                    all_win['-ALLER_PROGRESS-'].update_bar(all_count)
                else:
                    save_data(profile, user)
                    
                    meallist_layout, orders, f_meals = make_meal_layout(profile, todayMeals)
                    
                    window = 2
                    all_win.close()
                    meallist_win = sg.Window('Gerichtauswahl', meallist_layout, element_justification='c')
        
        if window == 2:
            event, values = meallist_win.read()
            if event == sg.WINDOW_CLOSED or event == 'Exit':
                break
            if event == 'Weiter':
                if values['0']:
                    meallist_win.close()
                    break
                else:
                    for i in orders:
                        if values[i]:
                            for j in f_meals:
                                if str(j["order"]) == i:
                                    s_meal = j
                    parts = parse_desc(s_meal)
                    window = 3
                    meallist_win.close()
                    rate_layout = [
                        [sg.Text('Gericht bewerten')],
                        [sg.Text(s_meal['description'])],
                        [sg.Slider((-5,5), orientation='h', s=(25,20), key='-RATING-')],
                        [sg.Button('Fertig')]
                        ]
                    rate_win = sg.Window('Bewertung', rate_layout, element_justification='c')
                    
        if window == 3:
           event, values = rate_win.read()
           if event == sg.WINDOW_CLOSED or event == 'Exit':
               break
           if event == 'Fertig':
               for i in parts:
                   if i in profile["taste"]:
                       profile["taste"][i] = round(0.7 * values['-RATING-'] + 0.3 * profile["taste"][i])
                   else:
                       profile["taste"][i] = values['-RATING-']
               save_data(profile, user)
               rate_win.close()
               break
          
#%% 
#main()

make_gui()
#%%




