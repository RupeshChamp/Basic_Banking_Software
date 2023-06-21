import os
import sys
import random
import re
import csv
from datetime import date, datetime
import shutil
import tempfile
from Banking_Emi_Calculation import EMI_Calculator
from prettytable import PrettyTable


"""
`BankingSystem` class:
   - This class represents the main banking system and contains various methods to perform banking operations.
   - It inherits from the `EMI_Calculator` class, which means it has access to the EMI calculation functionality.
   - The class constructor initializes instance variables and sets up file paths for storing user details and other data.
"""


class BankingSystem(EMI_Calculator):
    def __init__(self):  # Constructor for the Class BankingSystem
        super(BankingSystem, self).__init__()
        self.accountInfo = {}
        self.userInfo = {}
        self.accountNumber = ""
        self.validated_dob = ""
        self.interestRate = None
        self.salary = None
        self.loanAmount = None
        self.loanTerm = None
        self.banking_path = self.folder_creation()
        self.user_details_path = os.path.join(self.banking_path, "UserDetails")
        self.user_detail_path_csv = self.create_user_detail_folder()
        self.user_details_csv_file = self.user_detail_path_csv + "\\" + "User_details.csv"
        self.emi_obj = EMI_Calculator()

    """
    `account_exist(self, accountNumber)`: Checks if an account number already exists in the user details CSV file.
    """
    def account_exist(self, accountNumber):
        """
        This function checks for the Account Number present in the csv file.
        If Account Number already exists, it will regenerate the Account Number one more time.
        """
        try:
            file_exists = os.path.exists(self.user_details_csv_file)
            if file_exists:
                with open(self.user_details_csv_file, "r") as read_csv:
                    reader = csv.DictReader(read_csv)
                    for row in reader:
                        if row["ACCOUNTNUMBER"] != accountNumber:
                            return True
                        return False
            else:
                print("No such file or directory. Please create a new account. ")
                return True
        except OSError as e:
            print(f"Error occurred while creating the CSV file: {e}")
            self.index()

    """
    `validate_phone_number(phone_number)`: Validates a phone number to ensure it consists of only digits.
    """
    @staticmethod
    def validate_phone_number(phone_number):
        if phone_number.isdigit():
            return True
        else:
            return False

    """
    `get_phone_number_from_csv(self)`: Retrieves all phone numbers from the user details CSV file and returns them as a list.
    """
    def get_phone_number_from_csv(self):
        try:
            with open(self.user_details_csv_file, "r") as readFile:
                reader = csv.DictReader(readFile)
                phone_numbers = [row["PHONENUMBER"] for row in reader]
            return phone_numbers
        except FileNotFoundError:
            print("File not found in the given path, Please try to create a new file.")

    """
        `get_account_number(self, phone_number)`: Retrieves the account number associated with a given phone number from the user details CSV file.
    """
    def get_account_number(self, phone_number):
        try:
            with open(self.user_details_csv_file, "r") as readFile:
                reader = csv.DictReader(readFile)
                for row in reader:
                    if row["PHONENUMBER"] == phone_number:
                        return row["ACCOUNTNUMBER"]
            return None
        except OSError as e:
            print(f"Error occurred while creating the CSV file: {e}")
            self.index()

    """
        `calculate_age(dob)`: Calculates the age based on the provided date of birth.
    """
    @staticmethod
    def calculate_age(dob):
        """This method will calculate the age, using the given DOB."""
        # Convert the DOB string to a datetime object
        born = datetime.strptime(dob, "%Y-%m-%d")
        today = date.today()
        age = (
            today.year - born.year - ((today.month, today.day) < (born.month, born.day))
        )
        return age

    """
        `get_current_balance(self, accNumber)`: Retrieves the current balance for a given account number from the user details CSV file.
    """
    def get_current_balance(self, accNumber):
        try:
            """This method will return the Current Balance for the given Account Number."""
            with open(self.user_details_csv_file, "r") as Edit_csv:
                reader = csv.DictReader(Edit_csv)
                for val in reader:
                    if val["ACCOUNTNUMBER"] == accNumber:
                        current_Balance = val["AMOUNT"]
                        return current_Balance
        except FileNotFoundError:
            print("File not found in the given path. Try creating new.")

    """
        `update_user_details(self, account_number, updating_column, value)`: Updates a specific column value in the user details CSV file for a given account number.
    """
    def update_user_details(self, account_number, updating_column, value):
        """This method will update the user details. Here we used temporary file and shutil package to update."""
        try:
            temp_file = tempfile.NamedTemporaryFile(mode="w", newline="", delete=False)
            with open(self.user_details_csv_file, "r") as csvfile, temp_file:
                reader = csv.DictReader(csvfile)
                fieldnames = reader.fieldnames
                writer = csv.DictWriter(temp_file, fieldnames=fieldnames)
                writer.writeheader()
                for row in reader:
                    if row["ACCOUNTNUMBER"] == account_number:
                        row[updating_column] = value
                    writer.writerow(row)
            shutil.move(temp_file.name, self.user_details_csv_file)
        except PermissionError:
            print(
                "File has already been opened. Please try to update after closing the file. Thanks!"
            )
        except FileNotFoundError:
            print("File not found in the given path.")
    """
        `update_amount(self, accountNumber, Initial_Account_Balance)`: Updates the amount column in the user details CSV file for a given account number.
    """
    def update_amount(self, accountNumber, Initial_Account_Balance):
        """
        This method will update the amount column after Transactions.
        Here we used temporary file and shutil package to update.
        """

        try:
            temp_file = tempfile.NamedTemporaryFile(mode="w", newline="", delete=False)
            with open(self.user_details_csv_file, "r") as csvfile, temp_file:
                reader = csv.DictReader(csvfile)
                fieldnames = reader.fieldnames
                writer = csv.DictWriter(temp_file, fieldnames=fieldnames)
                writer.writeheader()
                for row in reader:
                    if row["ACCOUNTNUMBER"] == accountNumber:
                        row["AMOUNT"] = Initial_Account_Balance
                    writer.writerow(row)
            shutil.move(temp_file.name, self.user_details_csv_file)
            print("Amount updated successfully!")
        except PermissionError:
            print(
                "File has already been opened. Please try to update after closing the file. Thanks!"
            )
        except FileNotFoundError:
            print("File not found in the given path.")
    """
        `folder_creation(self)`: Creates a "Banking" folder on the desktop and returns the path.
    """
    def folder_creation(self):
        try:
            # Create the Banking folder on the Desktop
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            self.banking_path = os.path.join(desktop_path, "Banking")
            file_exists = os.path.exists(self.banking_path)
            if not file_exists:
                os.makedirs(self.banking_path)
                print("Banking folder created successfully!")
                return self.banking_path
            else:
                print("Main Folder already exists.")
                return self.banking_path
        except FileExistsError as e:
            print("File already exist in the given path.")
        except PermissionError:
            print("You cannot create a file or folder to the given path. Please change directory.")
        except FileNotFoundError:
            print("File not found in the given path.")
    """
        `create_user_detail_folder(self)`: Creates a "UserDetails" folder inside the "Banking" folder and returns the path.
    """
    def create_user_detail_folder(self):
        try:
            # Create the UserDetails folder inside the Banking folder
            file_exists = os.path.exists(self.banking_path)
            if file_exists:
                try:
                    if not os.path.isfile(self.user_details_path):
                        os.makedirs(self.user_details_path)
                        print("UserDetails folder created successfully!")
                        return self.user_details_path
                except FileExistsError:
                    return self.user_details_path
                except PermissionError:
                    print("You cannot create a file or folder to the given path. Please change directory.")
            else:
                print("Parent folder Banking is not created, please create a folder to Banking and continue.")
        except FileNotFoundError:
            print("File not found in the given path.")
        except PermissionError:
            print("You dont have permission to create a file or directory to this path.")
    """
        `index(self)`: Displays the main menu and handles user input for various banking operations.
    """

    """
        `continue_or_exit(self)` method:
           - This method prompts the user to choose whether to continue using the banking system or exit the program.
           - It takes user input and returns `True` if the user wants to continue or `False` if the user chooses to exit.
        """

    def continue_or_exit(self, account):
        try:
            user_choice = input(
                """
                Press 1 to Continue
                Press 2 to Exit
                """
            )
            if user_choice == "1":
                self.Transaction(account)
            elif user_choice == "2":
                self.index()
            else:
                print("Invalid option selected")
                self.continue_or_exit(account)
        except OSError as e:
            print(f"Error occurred while creating the CSV file: {e}")
            self.index()

    def index(self):
        # The program starts with a menu-driven 'index()' function that allows users to select various
        # options.

        print("Welcome to the E-con Banking System")
        try:
            option = int(
                input(
                    """
            Press 1 to Create an Account
            Press 2 for Make Transaction
            Press 3 for Edit Account
            Press 4 for View Account details
            Press 5 for Check for Loan Eligibility and Detailed EMI Plans
            Press 6 for Exit
            """
                )
            )

            if option == 1:
                self.Account_Creation()
            elif option == 2:
                phone_verification = input("Please Enter your Phone Number to verify: ")
                if self.validate_phone_number(phone_verification):
                    phone_numbers = self.get_phone_number_from_csv()
                    if phone_verification in phone_numbers:
                        account_verification = self.get_account_number(
                            phone_verification
                        )
                        self.Transaction(account_verification)
                    else:
                        print(
                            "Phone Number doesn't exist! Please enter the correct Phone Number to verify your account."
                        )
                        self.index()
                else:
                    print("Invalid Phone Number")
                    self.index()
            elif option == 3:
                phone_verification = input("Please Enter your Phone Number to verify: ")
                if self.validate_phone_number(phone_verification):
                    phone_numbers = self.get_phone_number_from_csv()
                    if phone_verification in phone_numbers:
                        account_verification = self.get_account_number(
                            phone_verification
                        )
                        self.Edit_Account(account_verification)
                    else:
                        print(
                            "Phone Number doesn't exist! Please enter the correct Phone Number to verify your account."
                        )
                        self.index()
                else:
                    print("Invalid Phone Number")
                    self.index()

            elif option == 4:
                phone_verification = input("Please Enter your Phone Number to verify: ")
                if self.validate_phone_number(phone_verification):
                    phone_numbers = self.get_phone_number_from_csv()
                    if phone_verification in phone_numbers:
                        account_verification = self.get_account_number(
                            phone_verification
                        )
                        self.display_account(account_verification)
                    else:
                        print(
                            "Phone Number doesn't exist! Please enter the correct Phone Number to View your account "
                            "details."
                        )
                        self.index()
                else:
                    print("Invalid Phone Number")
                    self.index()
            elif option == 5:
                print("Thanks for choosing the E-con Loans, please verify yourself.")
                phone_verification = input("Enter your Phone Number: ")
                if self.validate_phone_number(phone_verification):
                    phone_numbers = self.get_phone_number_from_csv()
                    if phone_verification in phone_numbers:
                        account_verification = self.get_account_number(
                            phone_verification
                        )
                        with open(self.user_details_csv_file, "r") as read_csv:
                            reader = csv.DictReader(read_csv)
                            for row in reader:
                                row = dict(row)
                                if row["ACCOUNTNUMBER"] == account_verification:
                                    current_age = row["AGE"]
                                    self.emi_obj.get_values(current_age, str(self.banking_path))

                    else:
                        print(
                            "Phone Number doesn't exist! Please enter the correct Phone Number to View your account "
                            "details."
                        )

                        self.index()
                else:
                    print("Invalid Phone Number")
                    self.index()
            elif option == 6:
                print("Thank you, Visit again!")
                sys.exit()  # sys.exit() to stop execution
            else:
                print("Please select the correct option")
                self.index()
        except OSError as e:
            print(f"Error occurred while creating the CSV file: {e}")
            self.index()
        except KeyboardInterrupt:
            print("Keyboard Interrupted")
        except ValueError:
            print("Invalid Key")
            self.index()
        except TypeError as e:
            print(f"{e}")

    """
    Validate() is used to validate the FirstName, LastName, Email, Amount, Gender, PhoneNumber, Profession, Age
    using the regex pattern and conditional statements.
    """

    def validate(self, key, val, index):
        try:

            if key == "AGE":
                if val.isdigit() and int(val) <= 130:
                    if int(val) >= 18:
                        return val
                    elif int(val) < 18 and val != 0:
                        print(
                            "Sorry! your age must be greater than 18 to create an account "
                        )
                        return self.inputs("DATE_OF_BIRTH", 2)
                    else:
                        print("Age must not be zero")
                        return self.inputs(key, index)
                else:
                    print("Please input the valid Age")
                    return self.inputs(key, index)
            elif key == "AMOUNT":
                if val.isdigit() and int(val) >= 500:
                    return val
                else:
                    print("Minimum deposit amount will be 500 or more")
                    return self.inputs(key, index)
            elif key == "PHONENUMBER":
                pattern = r"^\d{10}$"  # Assuming a 10-digit phone number format
                if re.match(pattern, val):
                    return val
                else:
                    print("Please enter only a 10-digit phone number")
                    return self.inputs(key, index)
            elif key == "EMAIL":
                pattern = r"^[a-zA-Z]+[a-zA-Z0-9]*@[a-zA-Z]+\.[a-zA-Z]{2,3}$"
                if re.match(pattern, val):
                    return val
                else:
                    print("Email address must contain A-Z, a-z, @, . are Mandatory")
                    return self.inputs(key, index)
            elif key == "DATE_OF_BIRTH":
                date_pattern = r"^\d{4}-\d{1,2}-\d{1,2}$"
                if re.match(date_pattern, val):
                    return val
                else:
                    print("Enter the Date of Birth in mention format.")
                    return self.inputs(key, index)
                pass
            elif key in ["FIRSTNAME", "LASTNAME", "GENDER", "PROFESSION"]:
                pattern = r"^[a-zA-Z\s]+$"
                if re.match(pattern, val):
                    return val
                else:
                    return self.inputs(key, index)
            else:
                print("Keyword not matched..")
        except OSError as e:
            print(f"Error occurred while creating the CSV file: {e}")
            self.index()

    # `userinput(self)`: Collects user input for creating a new account and validates the inputs.
    def userinput(self):
        try:
            for j, i in enumerate(self.userInfo.keys()):
                valid_input = self.inputs(i, j)
                self.userInfo[i] = valid_input
            return self.userInfo
        except OSError as e:
            print(f"Error occurred while creating the CSV file: {e}")
            self.index()

    # `inputs(self, key, index)`: Handles user input for a specific data field and calls the appropriate validation method.
    def inputs(self, key, index):
        try:
            if key == "GENDER":
                opt = input(
                    """
                Press 1 for Male
                Press 2 for Female
                Press 3 for Transgender
                Press 4 for Not mention
                Press 5 for Exit
                """
                )
                if opt == "1":
                    return "Male"
                elif opt == "2":
                    return "Female"
                elif opt == "3":
                    return "Transgender"
                elif opt == "4":
                    return "Not mention"
                elif opt == "5":
                    self.inputs("GENDER", 3)
                else:
                    print("Invalid option selected")
                    self.inputs("GENDER", 3)
            elif key == "ACCOUNTNUMBER":
                while True:
                    current_year = datetime.now().year % 100
                    current_month = datetime.now().strftime("%m")
                    self.accountNumber = random.randint(100000, 10 ** 6)
                    if self.account_exist(self.accountNumber):
                        self.accountNumber = f"{current_year}{current_month}{self.accountNumber}"
                        return self.accountNumber
                    break

            elif key == "DATE_OF_BIRTH":
                print("Please Enter the DOB in 'yyyy-mm-dd' format.")
                DoB = input(f"Enter your {key}: ")
                self.validated_dob = self.validate(key, DoB, index)
                return self.validated_dob
            elif key == "AGE":
                age = str(self.calculate_age(self.validated_dob))
                validated_age = self.validate(key, age, index)
                return validated_age

            else:
                value = input(f"Enter your {key}: ")
                validated_value = self.validate(key, value, index)
                while validated_value is None:
                    print(f"Invalid {key}. Please enter a valid value.")
                    value = input(f"Enter your {key}: ")
                    validated_value = self.validate(key, value, index)
                return validated_value
        except OSError as e:
            print(f"Error occurred while creating the CSV file: {e}")
            self.index()

    """
        `addingDataToCsv(self, file_exists, user_account, fieldnames)`: Adds the user account details to the user details CSV file.
    """
    def addingDataToCsv(self, file_exists, user_account, fieldnames):
        try:
            with open(self.user_details_csv_file, "a", newline="") as csvFile:
                writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
                if not file_exists:
                    writer.writeheader()
                writer.writerow(user_account)
            print(
                """Account Created Successfully! Use your Phone Number to login and make transaction, Edit your
                information or to view you View account details"""
            )
            self.index()
        except OSError as e:
            print("Data not found. Please create a new account to make this operation")
            self.index()

    """
    1. Account creation:
       - The `Account creation` method is responsible for creating a new bank account for a customer.
       - It would typically prompt the user for necessary information such as name, address, phone number, date of birth, and initial deposit amount.
       - The method would validate the user input, ensuring the data is in the correct format and meets any specified criteria (e.g., minimum initial deposit).
       - Once the input is validated, the method would generate a unique account number for the new account.
       - It would then update the user details CSV file with the new account information, including the account number, customer details, and initial balance.
    """
    def Account_Creation(self):
        print("Welcome to the E-con Family")
        self.userInfo = {
            "ACCOUNTNUMBER": "",
            "FIRSTNAME": "",
            "LASTNAME": "",
            "DATE_OF_BIRTH": "",
            "AGE": "",
            "GENDER": "",
            "PROFESSION": "",
            "PHONENUMBER": "",
            "EMAIL": "",
            "AMOUNT": "",
        }
        userAccounts = self.userinput()
        fieldnames = list(self.userInfo.keys())
        file_exists = os.path.isfile(self.user_details_csv_file)
        try:
            self.addingDataToCsv(file_exists, userAccounts, fieldnames)
        except PermissionError:
            print("Your file is open. Please close the file before adding new data.")
            self.index()

    """
    2. Transaction:
       - The `Transaction` method handles various types of transactions between bank accounts, such as deposits, withdrawals, and transfers.
       - It would typically prompt the user to specify the type of transaction they wish to perform (e.g., deposit, withdrawal, or transfer).
       - Depending on the selected transaction type, the method would request additional details like the account numbers involved, transaction amount, etc.
       - The method would validate the provided information and ensure that the necessary funds are available for withdrawals or transfers.
       - After performing the transaction, the method would update the account balances for the affected accounts in the user details CSV file.

    """
    def Transaction(self, account):
        try:

            Transit_Selection = int(
                input(
                    """
                Press 1 to "Add Money"
                Press 2 to "Withdraw Money"
                Press 3 to "View Balance"
                Press 4 to "For Exit"
                """
                )
            )

            if (
                Transit_Selection == 1
            ):  # this condition will execute to add money to the existing balance
                Initial_Account_Balance = int(self.get_current_balance(account))
                Deposit_Amount = int(input("Enter the amount to be Deposited: "))
                if Deposit_Amount >= 100:
                    Initial_Account_Balance += Deposit_Amount
                    print("Amount has been deposited successfully")
                    print(f"Your current balance is: {Initial_Account_Balance}")
                    self.update_amount(account, Initial_Account_Balance)
                    # self.accountInfo[account]["AMOUNT"] = Initial_Account_Balance
                    self.continue_or_exit(account)
                else:
                    print("Minimum Amount to be deposited will be more than 100")
                    self.Transaction(account)

            elif (
                Transit_Selection == 2
            ):  # this condition will execute to withdraw money from the existing balance
                minimum_balance = 1000
                Initial_Account_Balance = int(self.get_current_balance(account))
                print(f"Your current balance is: {Initial_Account_Balance}")
                if Initial_Account_Balance >= 1000:
                    Withdraw_Money = int(input("Please Enter the Amount to be withdrawn: "))
                    if Withdraw_Money >= 100:
                        if Withdraw_Money < Initial_Account_Balance:
                            Initial_Account_Balance -= Withdraw_Money
                            if Initial_Account_Balance >= minimum_balance:
                                print(f"{Withdraw_Money} is be debited from your account")
                                self.update_amount(account, Initial_Account_Balance)
                                currentBalance = int(self.get_current_balance(account))
                                print(f"Your current balance is: {currentBalance}")
                                self.Transaction(account)
                            else:
                                print(f"Minimum Balance should be {minimum_balance}. ")
                                self.Transaction(account)
                        else:
                            print(f"Minimum Balance should be {minimum_balance}. ")
                            self.Transaction(account)
                    else:
                        print("Minimum amount to be withdrawn must be 100 or more.")
                        self.Transaction(account)
                else:
                    print("Insufficient Balance")
                    self.Transaction(account)

            elif Transit_Selection == 3:
                Initial_Account_Balance = int(self.get_current_balance(account))
                print(f"Your current balance is: {Initial_Account_Balance}")
                self.continue_or_exit(account)

            elif Transit_Selection == 4:
                self.index()

            else:
                print("Please select the correct option")
                self.Transaction(account)
        except OSError as e:
            print("Data not found. Please create a new account to make this operation")
            self.index()

    """
    3. EditAccount:
       - The `EditAccount` method allows customers to modify their account details, such as their phone number, address, or other personal information.
       - It would typically prompt the user to select the specific information they want to update and provide the necessary input for the chosen field.
       - The method would validate the user input and ensure that it meets any specified criteria or format requirements.
       - Once the input is validated, the method would update the corresponding field in the user details CSV file with the new information.
    """
    def Edit_Account(self, account):
        try:
            update_selection = int(
                input(
                    """
                Press 1 to Edit Your Details
                Press 2 to Exit
                """
                )
            )
            with open(self.user_details_csv_file, "r") as read_csv:
                reader = csv.DictReader(read_csv)
                fieldNames = reader.fieldnames
                print(f"Fields Present in the Database {fieldNames}")
                if update_selection == 1:
                    edit_option = int(
                        input(
                            """
                    Please select the option to edit:
                        Press 1 to Edit FirstName
                        Press 2 to Edit LastName
                        Press 3 to Edit DATE_OF_BIRTH
                        Press 4 to Edit Gender
                        Press 5 to Edit Profession
                        Press 6 to Edit Phone Number
                        Press 7 to Edit Email
                    """
                        )
                    )
                    if edit_option == 1:
                        update_field = "FIRSTNAME"
                    elif edit_option == 2:
                        update_field = "LASTNAME"
                    elif edit_option == 3:
                        update_field = "DATE_OF_BIRTH"
                    elif edit_option == 4:
                        update_field = "GENDER"
                    elif edit_option == 5:
                        update_field = "PROFESSION"
                    elif edit_option == 6:
                        update_field = "PHONENUMBER"
                    elif edit_option == 7:
                        update_field = "EMAIL"
                    else:
                        print("Invalid Option, Please select the correct option")
                        self.Edit_Account(account)
                    if update_field in fieldNames:
                        for i, _ in enumerate(fieldNames):
                            new_value = self.inputs(update_field, i)
                            print(new_value)
                            self.update_user_details(account, update_field, new_value)
                            print("Account details updated successfully!")
                            self.Edit_Account(account)
                    else:
                        print("Invalid field selected")
                        self.Edit_Account(account)

                elif update_selection == 2:
                    self.index()

                else:
                    print("Invalid option selected")
                    self.Edit_Account(account)
        except OSError as e:
            print("Data not found. Please create a new account to make this operation")
            self.index()
    """
    4. `display_account(self, account_number)` method:
       - This method displays the account details for a given account number.
       - It retrieves the account details from the user details CSV file and presents them to the user.
    """
    def display_account(self, account):
        try:
            with open(self.user_details_csv_file, "r") as readFile:
                reader = csv.DictReader(readFile)
                for row in reader:
                    if row["ACCOUNTNUMBER"] == account:
                        user = row["FIRSTNAME"] + " " + row["LASTNAME"]
                        print(f"Welcome {user} the E-con Banking Systems!")
                        account_details = dict(row)
                        break
                else:
                    return None

                table = PrettyTable()
                table.field_names = account_details.keys()
                table.add_row(account_details.values())
                print(table)
                self.index()
        except OSError as e:
            print("Data not found. Please create a new account to make this operation")
            self.index()


banking_system = BankingSystem()
banking_system.index()
