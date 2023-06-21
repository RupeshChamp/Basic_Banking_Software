import csv
import os
import sys
import babel.numbers
import re
from prettytable import PrettyTable
import datetime

"""
`EMI_Calculator` class:
   - This class represents an EMI (Equated Monthly Installment) calculator.
   - It is inherited by the `BankingSystem` class, indicating that the `BankingSystem` class has access to the
    EMI calculation functionality.
"""


class EMI_Calculator:
    def __init__(self):
        self.loan_detail_folder = None
        self.banking_path_loan = None
        self.current_age = None
        self.interestRate = None
        self.salary = None
        self.loanAmount = None
        self.loanTerm = None
        self.loan_details_path = None
        self.loan_details_path_csv = None
        self.display_emi_chart = ""

    """
    `get_values(self, age, banking_path)` method: 
        - This method will get the required values from the Banking_Home_page class and stores it.
    """
    def get_values(self, age, banking_path):
        self.current_age = age
        self.banking_path_loan = banking_path
        file_exists = self.banking_path_loan
        if file_exists:
            self.loan_detail_folder = self.create_loan_detail_folder(self.banking_path_loan)
        else:
            print("Parent file not existing.")
        self.initial(self.current_age)

    """
    `initial(self, age)` method:
        - This method get the age a the parameter from the get value, and validate whether the age is greater than or not.
        - If the age is greater than 18 it will ask the user for the loan term and validate it using the validate_loan_term method.
    """

    def initial(self, age):
        age = int(age)
        if age >= 18:
            # try:
            self.loanTerm = input("Please enter your loan term: ")
            if self.validate_loan_term(self.loanTerm):
                self.loanTerm = int(self.loanTerm)
                print(self.loanTerm)
            else:
                print("Please Enter the loan term in years like (1,3,5,12) etc.")
                self.initial(age)
            # except
        else:
            print("You must be 18+ to take a loan.")
            # self.initial()
        self.userInput_emi(age, self.loanTerm)

    """
    `validate_loan_amount(loanRequired)` static method:
        - This method will get the loan_Required as a parameter and match the regex pattern given.
    """
    @staticmethod
    def validate_loan_amount(loanRequired):
        pattern = r"^\d{6,}$"
        # The pattern ^\d{6,}$ checks if the input consists of at least 6 digits (minimum loan amount of 1 lakh)

        if re.match(pattern, loanRequired):
            return True
        else:
            return False

    """
    `validate_loan_term(loanTerm)` static method:
        - This method get the loan Term as a parameter, and validate it to the pattern.
    """
    @staticmethod
    def validate_loan_term(loanTerm):
        pattern = r"^0?([1-9]|[12]\d|30)$"
        # The pattern ^\d{6,}$ checks if the input consists of at least 6 digits (minimum loan amount of 1 lakh)

        if re.match(pattern, loanTerm):
            return True
        else:
            return False

    """
    def calculate_emi_and_save_as_csv(self, age, interest, loanTerm, loanRequired):
        - This method calculate the Emi for the given loan Term and loan Amount they have taken.
    """
    def calculate_emi_and_save_as_csv(self, age, interest, loanTerm, loanRequired):
        roi = interest / 12 / 100
        totalMonths = loanTerm * 12
        print(f"Rate of Interest for General Citizens, with loan term less than 5 years will be {self.interestRate}")
        ci = (1 + interest / 12 / 100) ** totalMonths
        monthly_EMI = loanRequired * roi * ci / (ci - 1)
        amountPayable = monthly_EMI * totalMonths
        totalInterest = amountPayable - loanRequired
        cur_amount_payable = babel.numbers.format_currency(amountPayable, 'INR', locale="en_IN")
        cur_total_Interest = babel.numbers.format_currency(totalInterest, 'INR', locale="en_IN")
        cur_monthly_EMI = babel.numbers.format_currency(monthly_EMI, 'INR', locale="en_IN")
        print(f"Total Amount to be paid: {cur_amount_payable}")
        print(f"Interest to be paid: {cur_total_Interest}")
        print(f"EMI to be paid every month will be {cur_monthly_EMI}")
        current_date = datetime.datetime.now()
        emi_table = PrettyTable()
        emi_table.field_names = ['Month - Year', 'EMI', 'Principal Amount', 'Interest Amount',
                                 'Balance Amount to pay']
        remaining_principal = loanRequired
        file_name = f"{loanTerm}_years_{loanRequired}_lakhs.csv"
        self.loan_details_path_csv = self.loan_details_path + "\\" + file_name
        if not os.path.isfile(self.loan_details_path_csv):
            with open(self.loan_details_path_csv, "a", newline="", encoding="utf-8") as mycsv:
                myFile = csv.writer(mycsv)
                myFile.writerow(
                    ['Month - Year', 'EMI (INR)', 'Principal Amount (INR)', 'Interest Amount (INR)',
                     'Balance Amount to pay (INR)'])
                for i in range(totalMonths):
                    interest_component = remaining_principal * roi
                    cur_interest_component = babel.numbers.format_currency(interest_component, 'INR',
                                                                           locale="en_IN")
                    principal_component = monthly_EMI - interest_component
                    cur_principal_component = babel.numbers.format_currency(principal_component, 'INR',
                                                                            locale="en_IN")
                    remaining_principal = remaining_principal - principal_component
                    cur_remaining_principal = babel.numbers.format_currency(remaining_principal, 'INR',
                                                                            locale="en_IN")
                    next_month = current_date + datetime.timedelta(days=30 * i)
                    cur_month_year = next_month.strftime("%b-%Y")

                    myFile.writerow([str(cur_month_year), str(round(monthly_EMI, 2)),
                                     str(round(principal_component, 2)),
                                     str(round(interest_component, 2)), str(round(remaining_principal, 2))])
                    emi_table.add_row(
                        [str(cur_month_year), str(cur_monthly_EMI), str(cur_principal_component),
                         str(cur_interest_component), str(cur_remaining_principal)])
                self.display_emi_chart = emi_table
                print(self.display_emi_chart)
        else:
            print("File already exists!")
            with open(self.loan_details_path_csv, "a", newline="", encoding="utf-8") as mycsv:
                myFile = csv.writer(mycsv)
                for i in range(totalMonths):
                    interest_component = remaining_principal * roi
                    cur_interest_component = babel.numbers.format_currency(interest_component, 'INR',
                                                                           locale="en_IN")
                    principal_component = monthly_EMI - interest_component
                    cur_principal_component = babel.numbers.format_currency(principal_component, 'INR',
                                                                            locale="en_IN")
                    remaining_principal = remaining_principal - principal_component
                    cur_remaining_principal = babel.numbers.format_currency(remaining_principal, 'INR',
                                                                            locale="en_IN")
                    next_month = current_date + datetime.timedelta(days=30 * i)
                    cur_month_year = next_month.strftime("%b-%Y")

                    emi_table.add_row(
                        [str(cur_month_year), str(cur_monthly_EMI), str(cur_principal_component),
                         str(cur_interest_component), str(cur_remaining_principal)])
                self.display_emi_chart = emi_table
                print(self.display_emi_chart)
            self.userInput_emi(age, loanTerm)
    """
    `create_loan_detail_folder(self,banking_path)`: Creates a "LoanDetails" folder inside the "Banking" folder and returns the path.
    """
    def create_loan_detail_folder(self, banking_path):
        # Create the UserDetails folder inside the Banking folder
        self.loan_details_path = os.path.join(banking_path, "LoanDetails")
        file_exists = os.path.exists(banking_path)
        if file_exists:
            try:
                if not os.path.isfile(self.loan_details_path):
                    os.mkdir(self.loan_details_path)
                    print("LoanDetails folder created successfully!")
                    return self.loan_details_path
            except FileExistsError:
                return self.loan_details_path
            except PermissionError:
                print("Permission Denied, cannot not create new file or folder in this path.")
        else:
            print("Parent folder Banking is not created, please create a folder to Banking and continue.")
            sys.exit()

    """
    userInput_emi(self, age, loanTerm) method:
        - This method gets the age and loanTerm as a parameter, and based on the age it calls the different methods like
        Student, Senior Citizen or General Citizen methods.
    """
    def userInput_emi(self, age, loanTerm):
        print("Welcome to the E-con EMI Calculator")
        try:
            if 18 <= age < 22:
                option = "1"
            elif age >= 58:
                option = "2"
            elif 22 <= age < 58:
                option = "3"
            else:
                option = "4"

            if option == "1":
                self.Student(age, loanTerm)
            elif option == "2":
                self.SeniorCitizen(age, loanTerm)
            elif option == "3":
                self.GeneralCitizen(age, loanTerm)
            elif option == "4":
                print("Thank you, Visit again!")
                sys.exit()
            else:
                print("Please select the correct option")
                self.userInput_emi(age, loanTerm)
        except KeyboardInterrupt:
            print("Keyboard Interrupted")
            self.userInput_emi(age, loanTerm)
        except ValueError:
            print("Invalid Key")
            self.initial(age)

    def Student(self, age, loanTerm):
        try:
            self.loanAmount = 1000000
            self.loanAmount = babel.numbers.format_currency(self.loanAmount, 'INR', locale="en_IN")
            print(f"Loan Sanction for students in {self.loanAmount}")
            loanRequired = input("How much loan do you want to take? Minimum Loan must be 1 lakh.")
            if self.validate_loan_amount(loanRequired):
                loanRequired = int(loanRequired)
                print("Loan amount is valid.")
                if age < 22 and loanTerm < 5:
                    self.interestRate = 6
                    self.calculate_emi_and_save_as_csv(age, self.interestRate, loanTerm, loanRequired)
                elif age < 22 and loanTerm >= 5:
                    self.interestRate = 8
                    self.calculate_emi_and_save_as_csv(age, self.interestRate, loanTerm, loanRequired)
                else:
                    print("Your age should be less than 22 to get the student loan")
                    # self.initial()
            else:
                print("Invalid loan amount. Minimum loan amount should be 1 lakh.")
                self.Student(age, loanTerm)
        except KeyboardInterrupt:
            print("Keyboard Interrupted")
            self.initial(age)
        except ValueError:
            print("Invalid Key")
            self.initial(age)

    def SeniorCitizen(self, age, loanTerm):
        try:
            self.loanAmount = 1500000
            self.loanAmount = babel.numbers.format_currency(self.loanAmount, 'INR', locale="en_IN")
            print(f"Loan Sanction for senior citizens in {self.loanAmount}")
            loanRequired = input("How much loan do you want to take? Minimum Loan must be 1 lakh.")
            if self.validate_loan_amount(loanRequired):
                loanRequired = int(loanRequired)
                print("Loan amount is valid.")
                if age >= 58 and loanTerm < 5:
                    self.interestRate = 8
                    self.calculate_emi_and_save_as_csv(age, self.interestRate, loanTerm, loanRequired)
                elif age >= 58 and loanTerm >= 5:
                    self.interestRate = 10
                    self.calculate_emi_and_save_as_csv(age, self.interestRate, loanTerm, loanRequired)
            else:
                print("Invalid loan amount. Minimum loan amount should be 1 lakh.")
                self.SeniorCitizen(age, loanTerm)
        except KeyboardInterrupt:
            print("Keyboard Interrupted")
            self.initial(age)
        except ValueError:
            print("Invalid Key")
            self.initial(age)

    def GeneralCitizen(self, age, loanTerm):
        try:
            self.salary = int(input("Please enter your salary: "))
            max_loanAmount = 2500000
            Salary_loanAmount = self.salary * 10
            self.loanAmount = Salary_loanAmount if max_loanAmount < Salary_loanAmount else max_loanAmount
            self.loanAmount = babel.numbers.format_currency(self.loanAmount, 'INR', locale="en_IN")
            print(f"Loan Sanction for general citizens in {self.loanAmount}")
            loanRequired = input("How much loan do you want to take? Minimum Loan must be 1 lakh.")
            if self.validate_loan_amount(str(loanRequired)):
                loanRequired = int(loanRequired)
                print("Loan amount is valid.")
                if 22 <= age < 58 and loanTerm < 5:
                    self.interestRate = 12
                    self.calculate_emi_and_save_as_csv(age, self.interestRate, loanTerm, loanRequired)
                elif 22 <= age < 58 and loanTerm >= 5:
                    self.interestRate = 14
                    self.calculate_emi_and_save_as_csv(age, self.interestRate, loanTerm, loanRequired)
                else:
                    print("Your age should be between 22 and 58 to get the general citizen loan")
                    # self.initial()
            else:
                print("Invalid loan amount. Minimum loan amount should be 1 lakh.")
                self.GeneralCitizen(age, loanTerm)
        except KeyboardInterrupt:
            print("Keyboard Interrupted")
            self.initial(age)
        except ValueError:
            print("Invalid Key")
            self.initial(age)


# emi_calculator = EMI_Calculator()
# emi_calculator.initial(58)
