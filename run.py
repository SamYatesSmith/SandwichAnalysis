import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

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
    while True:
        print("Enter sales data from the last week.")
        print("Input should be 6 numbers, seperated by commas")
        print("EG. 10,20,30,40,50,60")

        data_str = input("Enter your data here: ")

        sales_data = data_str.split(",")

        if validate_data(sales_data):
            print("Data is valid!")
            break

    return sales_data
         
def validate_data(values):
    """Conversts all string values into integers.  
    Raises ValueError if strings cannot be converted into integers, 
    or if there are not 6 values"""
    
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"invalid data: {e}, please try again.\n")
        return False

    return True

def update_sales_worksheet(data):
    """Update sales worksheet, add new row with the user inputed list"""

    print("updating sales worksheet...\n")
    sales_worksheet = SHEET.worksheet('sales')
    sales_worksheet.append_row(data)
    print("Sales worksheet updated successfully!\n")

def update_surplus_worksheet(data):
    """Update surplus worksheet, deduces surplus and adds new row with the user inputed list"""

    print("updating surplus worksheet...\n")
    surplus_worksheet = SHEET.worksheet('surplus')
    surplus_worksheet.append_row(data)
    print("Surplus worksheet updated successfully!\n")

def calculate_surplus_data(sales_row):
    """Comparing sales with stock and calculating surplus"""
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]

    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    
    return surplus_data

def main():
    """Run all programs funciton"""
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)
    new_surplus_data = calculate_surplus_data(sales_data)
    update_surplus_worksheet(new_surplus_data)
    
print("Welcome to Love Sandwiches data automation")
main()