from datetime import datetime
import csv
import os

def main():
    while True:
        option = show_menu()
        if option == "1":
            add_expense()
        elif option == "2":
            price_variation()
        elif option == "3":
            monthly_summary()
        elif option == "4":
            break
        else:
            print("\nError: Please enter a valid option.")
        
    
def get_date():
    """
        Prompt the user for the expense date in ISO format (YYYY-MM-DD).
        Returns: datetime object.
        Behavior: Keeps looping if the date format is incorrect.
    """
    while True:
        print("\n--- ADD A NEW EXPENSE ---\n")
        date_text = input("Expense date: ")
        try:
            new_date = datetime.strptime(date_text, "%Y-%m-%d")
            return new_date
        except ValueError: 
            print("\nError: Please use the format (YYYY-MM-DD)")
        

def get_expense():
    """
        Prompt the user for the expense name.
        Returns: expense input as an uppercase string.
        Behavior: Keeps looping if the input is empty.
    """
    while True:
        expense = input("Expense name: ")
        new_expense = expense.strip().upper()
        if not new_expense:
            print("\nError: Expense name can't be empty")
        else:
            return new_expense


def get_value():
    """
        Prompt the user for the total cost (float).
        Returns: float greater than 0.
        Behavior: Keeps looping until a valid positive number is provided. 
    """
    while True:
        try:
            value = float(input("Total cost: $ ")) 
            if value > 0:
                return value
            elif value == 0:
                print("\nError: The total cost can't be 0")
            else:
                print("\nError: Total cost can't be negative")
        except ValueError:
            print("\nError: Please use only numbers for the total cost")


def save_csv(expense_date, expense, value):
    """
        Write a single expense record to the CSV file.
        Returns: None
        Behavior: Creates the file if missing, writes header if empty, then appends one row.
    """
    with open("expenses_control.csv", 'a', newline="") as csvfile:
        writer = csv.writer(csvfile)
        if os.path.getsize("expenses_control.csv") == 0:
            writer.writerow(["Date", "Expense", "Value"])
        writer.writerow([expense_date, expense, value])
    

def add_expense():
    """
        Collects expense information from the user, shows a summary, and requests confirmation before saving.
        Returns: None
        Behavior: asks the user for confirmation, if correct calls save_csv, if not prompt the user all the information again. 
    """
    while True:
        expense_date = get_date().strftime("%Y-%m-%d")
        expense = get_expense()
        value = get_value()
        print("Expense information: Date:", expense_date, "Expense:", expense, "Value:",value)

        while True:
            confirmation = input("Is the expense information correct? Y/N ")
            new_confirmation = confirmation.upper()
            if new_confirmation == "Y":
                return save_csv(expense_date, expense, value) 
            elif new_confirmation == "N":
                break
            else:
                print('\nError: Please enter "Y" or "N"')
            

def price_variation():
    """
        Analyzes price variations for a specific expense over time.
        Returns: None
        Behavior: Prompts for expense name, validates data, calculates statistics (average, highest price, total variation),
                  displays a summary report, and optionally shows detailed price change history.
    """
    while True:
        print("\n--- CHECK THE PRICE VARIATION ---")
        expense_name = input("What's the name of the expense you want to compare? ").strip().upper()
        if not expense_name:
            print("\nError: Expense name can't be empty")
        else:
            break   

    expense_list = []
    with open("expenses_control.csv", 'r', newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader: 
            if row["Expense"] == expense_name:
                expense_list.append(row)
    
    expense_list.sort(key=lambda x: x['Date'])

    if len(expense_list) == 0:
        print("\nError: Expense not found")
        return  
    elif len(expense_list) < 2:
        print("\nError: Not enough data to compare")
        return

    # Calculate statistics
    total_entries = len(expense_list)
    values = [float(row['Value']) for row in expense_list]
    average_price = sum(values) / total_entries
    
    # Find highest price and its date
    max_value = max(values)
    max_index = values.index(max_value)
    max_date = expense_list[max_index]['Date']
    
    # Total variation (first to last)
    first_value = values[0]
    last_value = values[-1]
    total_variation_amount = last_value - first_value
    total_variation_percent = round((total_variation_amount / first_value) * 100, 2)
    
    # Print report
    print(f"\n--- REPORT: {expense_name} ---")
    print(f"Total entries: {total_entries}")
    print(f"Average Price: ${average_price:.2f}")
    print(f"Highest Price Paid: ${max_value:.2f} (on {max_date})")
    print(f"Total Variation (First purchase -> Last purchase): ${total_variation_amount:.2f} / {total_variation_percent}%")
    print("\n[Press Y to see full history or N to exit]")
    
    # Ask if user wants detailed history
    while True:
        show_details = input("").strip().upper()
        if show_details == "Y":
            print(f"\n--- DETAILED HISTORY: {expense_name} ---")
            for i in range(len(expense_list) - 1):
                val_before = float(expense_list[i]["Value"])
                val_after = float(expense_list[i+1]["Value"])
                difference = val_after - val_before
                percentage = round((difference / val_before) * 100, 2)
                print(f"{expense_list[i]['Date']} → {expense_list[i+1]['Date']}: ${difference:.2f} ({percentage}%)")
            break
        elif show_details == "N":
            break
        else:
            print('\nError: Please enter "Y" or "N"')


def monthly_summary():
    """
        Summarize a monthly expenses and sum the cost for a given month. 
        Returns: None 
        Behavior: Prompts for the month needed, validates data, summarize and calculates the total. 
    """
    while True:
        print("\n--- MONTH SUMMARY ---")
        month = input("Please inform the month you need to check (YYYY-MM) ")
        try:
            new_month = datetime.strptime(month, "%Y-%m")
            break
        except ValueError:
            print("\nError: Please inform a valid date (YYYY-MM)")        
    
    monthly_list = []
    with open("expenses_control.csv", 'r', newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row_date = datetime.strptime(row["Date"], "%Y-%m-%d")
            if row_date.year == new_month.year and row_date.month == new_month.month:
                monthly_list.append(row)

        monthly_list.sort(key=lambda x: x['Date'])
        
        if len(monthly_list):
            total = sum(float(row["Value"]) for row in monthly_list)
            print(f"\n--- SUMMARY: {new_month.strftime('%B %Y')} ---")
            for row in monthly_list:
                print(f"{row['Date']}: {row['Expense']} - ${row['Value']}")
            print(f"Total: ${total:.2f}")
        else:
            print("\nError: No expenses found for this month")
    
    
def show_menu():
    """
        Shows a menu to the user and prompts for one option
        Returns: the option choosed by the user
        Behavior: prints the menu and shows input
    """
    while True:
        print("\n--- MENU --- ")
        print("1. Add a new expense")
        print("2. Check for the price variation of a specific expense")
        print("3. Month Summary")
        print("4. Exit")
        menu = input("\nEnter an option ")
        return menu
    

if __name__ == "__main__":
    main()