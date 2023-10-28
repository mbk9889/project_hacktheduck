authJWT = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJuYmYiOjE2OTYwMzIwMDAsImFwaV9zdWIiOiJhMmRlMjUxNGRmZTAwYjM5OTFhNzg0NTY4NzJkZDJjOTE1YWY5NjgzOTc2ZDAyZTdiZjk5NTIzMWE2MDllMDVjMTcxNzIwMDAwMDAwMCIsInBsYyI6IjVkY2VjNzRhZTk3NzAxMGUwM2FkNjQ5NSIsImV4cCI6MTcxNzIwMDAwMCwiZGV2ZWxvcGVyX2lkIjoiYTJkZTI1MTRkZmUwMGIzOTkxYTc4NDU2ODcyZGQyYzkxNWFmOTY4Mzk3NmQwMmU3YmY5OTUyMzFhNjA5ZTA1YyJ9.NiTvZUyTERVaV7krUmkiRgXbXhAeWEEZHkaus8aJ5pTMG4RYbZSP5reayEl1xi8kHO9g8jOWkj6v8ygUqyuPGcsL2jtqTMen1kUhe5m2bO6qQmdOvF6leyQkf7qWeYC8pzcIYhCnII5ZAcJxs3Lx3F3o6Zqy3aLsP1OxmG_TWiyWfdfhdCO8dekvQxXnp61oYAT8BvMPTbvoh6g9xPPO3q5KyYEAeLDGiPNeFML6CaDpvrwH_gf_ilDZJ84jGXuRGN5q_BqUgJq8QXahrbhvzM1ewNsC48Ljt0jFVD1kErMn4AVzJUkpZhzT6RJUvWC0e-lVObJ85yDCcbNdKOn7Dw'

import json
import requests


Entertainment_budget = int(input('Enter how much you want to spend on Entertainment'))
Education_budget = int(input('Enter how much you want to spend on Education'))
Shopping_budget = int(input('Enter how much you want to spend on Shopping'))
Personal_Care_budget = int(input('Enter how much you want to spend on Personal Care'))
Health_and_Fitness_budget = int(input('Enter how much you want to spend on Health and Fitness'))
Food_and_Dining_budget = int(input('Enter how much you want to spend on Food and Dining'))
Gifts_Donations_budget = int(input('Enter how much you want to spend on Gifts and Donations'))
Bills_Utilities_budget  = int(input('Enter how much you want to spend on Bills and Utilities'))
Auto_Transport_budget = int(input('Enter how much you want to spend on Auto Transport')
Travel_budget = int(input('Enter how much you want to spend on Travel')
                    
headers = {
    'Authorization': f'Bearer {authJWT}',
    'Content-Type': 'application/json',
    'version': '1.0'
}
quantity = 25
payload = json.dumps({"quantity": quantity})
account_id = "95526223"

response = requests.post(f"https://sandbox.capitalone.co.uk/developer-services-platform-pr/api/data/transactions/accounts/{account_id}/create", headers=headers, data=payload).text
json_response = json.loads(response)

print(len(json_response['Transactions']))



# the new balance is the balance that that uer had after all his transactions ...
# and for the original balance we can get it from the user account him self ... 
