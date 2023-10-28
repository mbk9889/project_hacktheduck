authJWT = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJuYmYiOjE2OTYwMzIwMDAsImFwaV9zdWIiOiJhMmRlMjUxNGRmZTAwYjM5OTFhNzg0NTY4NzJkZDJjOTE1YWY5NjgzOTc2ZDAyZTdiZjk5NTIzMWE2MDllMDVjMTcxNzIwMDAwMDAwMCIsInBsYyI6IjVkY2VjNzRhZTk3NzAxMGUwM2FkNjQ5NSIsImV4cCI6MTcxNzIwMDAwMCwiZGV2ZWxvcGVyX2lkIjoiYTJkZTI1MTRkZmUwMGIzOTkxYTc4NDU2ODcyZGQyYzkxNWFmOTY4Mzk3NmQwMmU3YmY5OTUyMzFhNjA5ZTA1YyJ9.NiTvZUyTERVaV7krUmkiRgXbXhAeWEEZHkaus8aJ5pTMG4RYbZSP5reayEl1xi8kHO9g8jOWkj6v8ygUqyuPGcsL2jtqTMen1kUhe5m2bO6qQmdOvF6leyQkf7qWeYC8pzcIYhCnII5ZAcJxs3Lx3F3o6Zqy3aLsP1OxmG_TWiyWfdfhdCO8dekvQxXnp61oYAT8BvMPTbvoh6g9xPPO3q5KyYEAeLDGiPNeFML6CaDpvrwH_gf_ilDZJ84jGXuRGN5q_BqUgJq8QXahrbhvzM1ewNsC48Ljt0jFVD1kErMn4AVzJUkpZhzT6RJUvWC0e-lVObJ85yDCcbNdKOn7Dw'
final_balance = list()
full_dictionarry = {'Transactions':[]}

import json
import requests
from collections import Counter
import matplotlib.pyplot as plt

def generate_the_data():
    global full_dictionarry
    headers = {
    'Authorization': f'Bearer {authJWT}',
    'Content-Type': 'application/json',
    'version': '1.0'
    }
    for i in range(1):
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

def sorted_amount():
    sorted_amount_list = [(transaction['amount'], transaction['creditDebitIndicator'], transaction['merchant']['category'])
                  for transaction in full_dictionarry['Transactions']]
    return sorted_amount_list
def categorize_transactions(sorted_amount_list):
    categories_data = {}  # Dictionary to store category-wise spending information

    for x in sorted_amount_list:
        amount, credit_debit, category = x[0], x[1], x[2] 
        (29.36, 'Debit', 'Education')
        # Check if the category is already in the dictionary, if not, create it
        if category not in categories_data:
            categories_data[category] = {
                'total_amount': 0,
                'debit_amount': 0,
                'credit_amount': 0
            }

        # Update total amount for the category
        categories_data[category]['total_amount'] += amount

        # Categorize transactions into debit and credit
        if credit_debit == 'Debit':
            categories_data[category]['debit_amount'] += amount
        elif credit_debit == 'Credit':
            categories_data[category]['credit_amount'] += amount

    return categories_data

def user_question():
    food_and_dining_budget = float(input('Enter how much you want to spend on Food and Dining: '))
    bills_utilities_budget = float(input('Enter how much you want to spend on Bills and Utilities: '))
    auto_transport_budget = float(input('Enter how much you want to spend on Auto and Transport: '))
    shopping_budget = float(input('Enter how much you want to spend on Shopping: '))
    education_budget = float(input('Enter how much you want to spend on Education: '))
    personal_care_budget = float(input('Enter how much you want to spend on Personal Care: '))
    gifts_donations_budget = float(input('Enter how much you want to spend on Gifts and Donations: '))
    entertainment_budget = float(input('Enter how much you want to spend on Entertainment: '))
    
    return {
        'Food & Dining': food_and_dining_budget,
        'Bills & Utilities': bills_utilities_budget,
        'Auto & Transport': auto_transport_budget,
        'Shopping': shopping_budget,
        'Education': education_budget,
        'Personal Care': personal_care_budget,
        'Gifts & Donations': gifts_donations_budget,
        'Entertainment': entertainment_budget
    }
def plot_category_spending(categories_data, budgets):
    categories = list(categories_data.keys())
    total_amounts = [categories_data[category]['total_amount'] for category in categories]
    debit_amounts = [categories_data[category]['debit_amount'] for category in categories]
    credit_amounts = [categories_data[category]['credit_amount'] for category in categories]
    budget_limits = [budgets[category] for category in categories]

    # Calculate differences between total spent and budget for each category
    differences = [total - budget for total, budget in zip(total_amounts, budget_limits)]

    # Define colors for total amount, total debit, total credit, and exceeded budget
    colors = ['blue', 'yellow', 'green', 'red']

    # Create a bar chart with distinct colors for total amount, total debit, total credit, and exceeded budget
    plt.figure(figsize=(12, 8))
    bar_width = 0.2
    opacity = 0.8

    index = range(len(categories))
    plt.bar(index, total_amounts, bar_width, alpha=opacity, color=colors[0], label='Total Amount')
    plt.bar([p + bar_width for p in index], debit_amounts, bar_width, alpha=opacity, color=colors[1], label='Total Debit')
    plt.bar([p + 2 * bar_width for p in index], credit_amounts, bar_width, alpha=opacity, color=colors[2], label='Total Credit')
    plt.bar([p + 3 * bar_width for p in index], differences, bar_width, alpha=opacity, color=colors[3], label='Exceeded Budget')

    plt.xlabel('Categories')
    plt.ylabel('Amount')
    plt.title('Category-wise Spending and Budget Comparison')
    plt.xticks([p + 1.5 * bar_width for p in index], categories)
    plt.legend()
    plt.tight_layout()

    # Save the plot as an image (optional)
    plt.savefig('category_spending_and_budget_chart.png')

    # Show the plot
    plt.show()

# Example usage:
# user_budgets = user_question()
# categorized_data = {'Bills & Utilities': {'total_amount': -55.33, 'debit_amount': -55.33, 'credit_amount': 0}, ...}
# plot_category_spending(categorized_data, user_budgets)


print(plot_category_spending(categories_data=categorize_transactions(sorted_amount_list=sorted_amount()), budgets=user_question()))
# print(categories_list())
# print(final_balance)
# ploting_categories(categories_list())




# the new balance is the balance that that uer had after all his transactions ...
# and for the original balance we can get it from the user account him self ... 
