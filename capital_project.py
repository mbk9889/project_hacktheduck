authJWT = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJuYmYiOjE2OTYwMzIwMDAsImFwaV9zdWIiOiJhMmRlMjUxNGRmZTAwYjM5OTFhNzg0NTY4NzJkZDJjOTE1YWY5NjgzOTc2ZDAyZTdiZjk5NTIzMWE2MDllMDVjMTcxNzIwMDAwMDAwMCIsInBsYyI6IjVkY2VjNzRhZTk3NzAxMGUwM2FkNjQ5NSIsImV4cCI6MTcxNzIwMDAwMCwiZGV2ZWxvcGVyX2lkIjoiYTJkZTI1MTRkZmUwMGIzOTkxYTc4NDU2ODcyZGQyYzkxNWFmOTY4Mzk3NmQwMmU3YmY5OTUyMzFhNjA5ZTA1YyJ9.NiTvZUyTERVaV7krUmkiRgXbXhAeWEEZHkaus8aJ5pTMG4RYbZSP5reayEl1xi8kHO9g8jOWkj6v8ygUqyuPGcsL2jtqTMen1kUhe5m2bO6qQmdOvF6leyQkf7qWeYC8pzcIYhCnII5ZAcJxs3Lx3F3o6Zqy3aLsP1OxmG_TWiyWfdfhdCO8dekvQxXnp61oYAT8BvMPTbvoh6g9xPPO3q5KyYEAeLDGiPNeFML6CaDpvrwH_gf_ilDZJ84jGXuRGN5q_BqUgJq8QXahrbhvzM1ewNsC48Ljt0jFVD1kErMn4AVzJUkpZhzT6RJUvWC0e-lVObJ85yDCcbNdKOn7Dw'
final_balance = list()
full_dictionarry = {'Transactions':[]}

import json
import requests
from collections import Counter


def generate_the_data():
    global full_dictionarry
    headers = {
    'Authorization': f'Bearer {authJWT}',
    'Content-Type': 'application/json',
    'version': '1.0'
    }
    for i in range(4):
        quantity = 25
        payload = json.dumps({"quantity": quantity})
        account_id = "95526223"

        response = requests.post(f"https://sandbox.capitalone.co.uk/developer-services-platform-pr/api/data/transactions/accounts/{account_id}/create", headers=headers, data=payload).text
        json_response = json.loads(response)

        final_balance.append(json_response["newBalance"])
        json_response.pop('newBalance')
        for x in range(len(json_response["Transactions"])):
            if json_response["Transactions"][x]['status'] != "Successful":
                continue
            else:
                # if the transaction is fine and accepted then we will add it to the dictionary to build the database we want and test on it ... we append the (transaction [x] because it is a list of a transactions so its indix is x ) ... 
                full_dictionarry["Transactions"].append(json_response["Transactions"][x])
def categories_list():
    categories_list = []
    
    # Loop through the list of dictionaries and extract the 'category' key
    for i in full_dictionarry['Transactions']:
        # Check if 'merchant' key exists in the transaction dictionary
        if 'merchant' in i and 'category' in i['merchant']:
            # Append the 'category' value to the categories_list
            categories_list.append(i['merchant']['category'])
    
    sorted_dict = Counter(categories_list)
    return sorted_dict
def ploting_categories(sorted_dict):
    import matplotlib.pyplot as plt

    # Extract category names and their counts
    categories = list(sorted_dict.keys())
    counts = list(sorted_dict.values())

    # Create a bar chart
    plt.figure(figsize=(10, 6))
    plt.barh(categories, counts, color='skyblue')
    plt.xlabel('Number of Occurrences')
    plt.ylabel('Categories')
    plt.title('Occurrences of Categories')
    plt.gca().invert_yaxis()  # Invert the y-axis for better readability
    
    
    plt.tight_layout()

    # Save the plot as an image (optional)
    plt.savefig('categories_bar_chart.png')

    # Show the plot
    plt.show()


    pass
generate_the_data()
def user_question():
    food_and_Dining_budget = float(input('Enter how much you want to spend on Food and Dining'))
    bills_Utilities_budget  = float(input('Enter how much you want to spend on Bills and Utilities'))
    auto_Transport_budget = float(input('Enter how much you want to spend on Auto and Transport'))
    shopping_budget = float(input('Enter how much you want to spend on Shopping'))
    other_budget = float(input('Enter how much you want to spend on other'))


# print(categories_list())
# print(final_balance)
ploting_categories(categories_list())




# the new balance is the balance that that uer had after all his transactions ...
# and for the original balance we can get it from the user account him self ... 
