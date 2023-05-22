import os
import json
import requests

#%%
def startup():
    # TODO variable data path
    # TODO one file per student
    dataDir = "data"
    dataPath = "data/data.json"
    if not os.path.isdir(dataDir):
        os.makedirs(dataDir)
        print("data folder created")
    if not os.path.isfile(dataPath):
        open(dataPath, 'a').close()
        print("data file created")
    else:
        print("data file found")
    # get student id TODO: make robust
    student = input("Enter student-id: ")
    return student
    
#%%
def load_data(path = "data/data.json"):
    with open(path) as infile:
        data = json.load(infile)
        infile.close()
    print("read")
    return data
#%%
def save_data(data, path = "data/data.json"):
    json_data = json.dumps(data, indent=4)
    with open(path, 'w') as outfile:
        outfile.write(json_data)
        outfile.close()
    print("written")

#%%
def get_meals():
    headers = {
        'accept': 'application/json;charset=utf-8',
        'apikey': 'eyJ4NXQiOiJOVGRtWmpNNFpEazNOalkwWXpjNU1tWm1PRGd3TVRFM01XWXdOREU1TVdSbFpEZzROemM0WkE9PSIsImtpZCI6ImdhdGV3YXlfY2VydGlmaWNhdGVfYWxpYXMiLCJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJPTERBUC1QUk9YWVwvbW9lYmVydEBjYXJib24uc3VwZXIiLCJhcHBsaWNhdGlvbiI6eyJvd25lciI6Ik9MREFQLVBST1hZXC9tb2ViZXJ0IiwidGllclF1b3RhVHlwZSI6bnVsbCwidGllciI6IlVubGltaXRlZCIsIm5hbWUiOiJQZXJ2YXNpdmUgQ29tcHV0aW5nIiwiaWQiOjE1OSwidXVpZCI6ImY0Njc5NDcxLTliYWQtNGEyMS1hZDFmLTFjMDYyMzViNDY0MSJ9LCJpc3MiOiJodHRwczpcL1wvYXBpdXAudW5pLXBvdHNkYW0uZGU6NDQzXC9vYXV0aDJcL3Rva2VuIiwidGllckluZm8iOnsiVW5saW1pdGVkIjp7InRpZXJRdW90YVR5cGUiOiJyZXF1ZXN0Q291bnQiLCJncmFwaFFMTWF4Q29tcGxleGl0eSI6MCwiZ3JhcGhRTE1heERlcHRoIjowLCJzdG9wT25RdW90YVJlYWNoIjp0cnVlLCJzcGlrZUFycmVzdExpbWl0IjowLCJzcGlrZUFycmVzdFVuaXQiOm51bGx9fSwia2V5dHlwZSI6IlNBTkRCT1giLCJzdWJzY3JpYmVkQVBJcyI6W3sic3Vic2NyaWJlclRlbmFudERvbWFpbiI6ImNhcmJvbi5zdXBlciIsIm5hbWUiOiJtZW5zYUFQSSIsImNvbnRleHQiOiJcL21lbnNhQVBJXC8yLjAiLCJwdWJsaXNoZXIiOiJaSU0iLCJ2ZXJzaW9uIjoiMi4wIiwic3Vic2NyaXB0aW9uVGllciI6IlVubGltaXRlZCJ9XSwiaWF0IjoxNjg0MTU3NTk0LCJqdGkiOiIwNDNhMmYxNy0zODAwLTQ2ZjItYTdjYS03ODg1NWQwYWEyYzcifQ==.Cso60hvx1-CoTk47hsiJUtQfHnwgvFK3nCiNkJ2RAMemJ8_XG80j-8hS0yCxGDfHWvbIU2bWP79nmM7G7uGncyAjUbuFkRIZZZArHdcs1xSCHENS2gSpw4a-Ek0Nz5VVy5c4Yttr_MSNozLMpClUVf5ew-0FcpBxfZCwhNKuHZtjLW12iBEuh4xPauVdRna6pLJc0zhDWhq66ubwU99UmfEGMYtdBP3UvXd4AJDtBTBQBNSjXzYzBosHgvGtta2sOHMeNn9tNLdtGc1thZD_7Ge76J_ieZt_90cgYmhD7YsNEXeWoH4nPsoWEOHZNZ2LL5Y6f0DAcDCMNAvqvY8mVw==',
    }

    params = {
        'location': 'Golm',
    }

    response = requests.get('https://apiup.uni-potsdam.de/endpoints/mensaAPI/2.0/meals', params=params, headers=headers)
    print(response.text)
    
get_meals()
#%%
student = startup()


data = load_data()
    