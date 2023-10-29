import PySimpleGUI as sg
import matplotlib.pyplot as plt
from collections import Counter
import json
import requests
from collections import Counter
import matplotlib.pyplot as plt

# Global variables for financial data
authJWT = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJuYmYiOjE2OTYwMzIwMDAsImFwaV9zdWIiOiJhMmRlMjUxNGRmZTAwYjM5OTFhNzg0NTY4NzJkZDJjOTE1YWY5NjgzOTc2ZDAyZTdiZjk5NTIzMWE2MDllMDVjMTcxNzIwMDAwMDAwMCIsInBsYyI6IjVkY2VjNzRhZTk3NzAxMGUwM2FkNjQ5NSIsImV4cCI6MTcxNzIwMDAwMCwiZGV2ZWxvcGVyX2lkIjoiYTJkZTI1MTRkZmUwMGIzOTkxYTc4NDU2ODcyZGQyYzkxNWFmOTY4Mzk3NmQwMmU3YmY5OTUyMzFhNjA5ZTA1YyJ9.NiTvZUyTERVaV7krUmkiRgXbXhAeWEEZHkaus8aJ5pTMG4RYbZSP5reayEl1xi8kHO9g8jOWkj6v8ygUqyuPGcsL2jtqTMen1kUhe5m2bO6qQmdOvF6leyQkf7qWeYC8pzcIYhCnII5ZAcJxs3Lx3F3o6Zqy3aLsP1OxmG_TWiyWfdfhdCO8dekvQxXnp61oYAT8BvMPTbvoh6g9xPPO3q5KyYEAeLDGiPNeFML6CaDpvrwH_gf_ilDZJ84jGXuRGN5q_BqUgJq8QXahrbhvzM1ewNsC48Ljt0jFVD1kErMn4AVzJUkpZhzT6RJUvWC0e-lVObJ85yDCcbNdKOn7Dw'
final_balance = list()
full_dictionarry = {'Transactions':[]}
# Function to generate financial data

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
        response = requests.post(
            f"https://sandbox.capitalone.co.uk/developer-services-platform-pr/api/data/transactions/accounts/{account_id}/create",
            headers=headers, data=payload).text
        json_response = json.loads(response)
        final_balance.append(json_response["newBalance"])
        json_response.pop('newBalance')
        for x in range(len(json_response["Transactions"])):
            if json_response["Transactions"][x]['status'] != "Successful":
                continue
            else:
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
def ploting_categories():
    sorted_dict = categories_list()
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
def categorize_transactions():
    sorted_amount_list = sorted_amount()
    categories_data = {}  # Dictionary to store category-wise spending information

    for x in sorted_amount_list:
        amount, credit_debit, category = x[0], x[1], x[2]
        if category not in categories_data:
            categories_data[category] = {
                'total_amount': 0,
                'debit_amount': 0,
                'credit_amount': 0
            }
        categories_data[category]['total_amount'] += amount
        if credit_debit == 'Debit':
            categories_data[category]['debit_amount'] += amount
        elif credit_debit == 'Credit':
            categories_data[category]['credit_amount'] += amount

    return categories_data

def create_gui():
    sg.theme("LightBlue2")  # Set theme
    
    layout = [
        [sg.Text("Enter Budgets:", font=("Helvetica", 14))],
        [sg.Text("Food & Dining:", size=(15, 1)), sg.InputText(key="FoodDining", size=(15, 1))],
        [sg.Text("Bills & Utilities:", size=(15, 1)), sg.InputText(key="BillsUtilities", size=(15, 1))],
        [sg.Text("Auto & Transport:", size=(15, 1)), sg.InputText(key="AutoTransport", size=(15, 1))],
        [sg.Text("Shopping:", size=(15, 1)), sg.InputText(key="Shopping", size=(15, 1))],
        [sg.Text("Education:", size=(15, 1)), sg.InputText(key="Education", size=(15, 1))],
        [sg.Text("Personal Care:", size=(15, 1)), sg.InputText(key="PersonalCare", size=(15, 1))],
        [sg.Text("Gifts & Donations:", size=(15, 1)), sg.InputText(key="GiftsDonations", size=(15, 1))],
        [sg.Text("Entertainment:", size=(15, 1)), sg.InputText(key="Entertainment", size=(15, 1))],
        [sg.Button("Submit", size=(10, 1), font=("Helvetica", 12))],
        [sg.Button("All Transactions in Categories", size=(25, 1), font=("Helvetica", 12))],
        [sg.Button("Detailed Budget", size=(25, 1), font=("Helvetica", 12))],
        [sg.Image(filename='Capital_One_logo.svg.png', key='IMAGE')],
    ]
    window = sg.Window("Financial Data Analysis", layout, finalize=False, element_justification='c')
    
    
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == "Submit":
            user_budgets = {
                'Food & Dining': int(values['FoodDining']),
                'Bills & Utilities': int(values['BillsUtilities']),
                'Auto & Transport': int(values['AutoTransport']),
                'Shopping': int(values['Shopping']),
                'Education': int(values['Education']),
                'Personal Care': int(values['PersonalCare']),
                'Gifts & Donations': int(values['GiftsDonations']),
                'Entertainment': int(values['Entertainment'])
            }
            if any(value < 0 for value in user_budgets.values()):
                sg.popup_error("Error", "Budget values cannot be negative.")
            else:
                sg.popup("Success", "Budgets submitted successfully!")
        
        if event == "All Transactions in Categories":
            ploting_categories()
        if event == "Detailed Budget":
            plot_category_spending(user_budgets)

    window.close()
def ploting_categories():
    explosion = (0,0.2,0,0,0,0,0,0)
    # Replace this line with your logic to get sorted_dict
    sorted_dict = categories_list()
    
    # Extract category names and their counts
    categories = list(sorted_dict.keys())
    counts = list(sorted_dict.values())

    # Calculate percentages
    total_occurrences = sum(counts)
    percentages = [(count / total_occurrences) * 100 for count in counts]

    # Create a pie chart with percentages
    plt.figure(figsize=(8, 8))
    plt.pie(percentages, labels=categories, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors,shadow=True,explode=explosion)
    plt.title('Occurrences of Categories')
    

    # Show the plot
    plt.show()


    pass
def plot_category_spending(user_budgets):
    "this will give exact spent the long graph we have been working on since moring "
    categories_data = categorize_transactions()
    categories = list(categories_data.keys())
    total_amounts = [categories_data[category]['total_amount'] for category in categories]
    debit_amounts = [categories_data[category]['debit_amount'] for category in categories]
    credit_amounts = [categories_data[category]['credit_amount'] for category in categories]
    budget_limits = [user_budgets[category] for category in categories]

    # Calculate differences between total spent and budget for each category
    differences = [total - budget for total, budget in zip(total_amounts, budget_limits)]

    # Define colors for total amount, total debit, total credit, and exceeded budget
    colors = ['blue', 'yellow', 'green', 'red']

    # Create a bar chart with distinct colors for total amount, total debit, total credit, and exceeded budget
    plt.style.use('dark_background')
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


if __name__ == "__main__":
    create_gui()
