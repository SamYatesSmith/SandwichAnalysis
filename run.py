import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')


def get_sales_data():
    """Get sales data figures input from the user"""
    print("Enter sales data from the last week.")
    print("Input should be 6 numbers, seperated by commas")
    print("EG. 10,20,30,40,50,60")

    data_str = input("Enter your data here: ")
    print(f"The data provided is {data_str}")

get_sales_data()