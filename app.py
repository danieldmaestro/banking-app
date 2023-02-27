from random import randint
from secrets import choice
import string
from csv_logger import CsvLogger
import logging
from csv import reader, writer
import pandas as pd
from decryptor import decryptor
from encryptor import encryptor
import locale

print(locale.setlocale(locale.LC_ALL, "en-NG"))

def find_user_customer(filepath, user):
    with open(filepath) as file:
        reader_obj = reader(file)
        for row in reader_obj:
            if user in row:
                customer = Customer(*row)
        return customer


def find_user_staff(filepath, user):
    with open(filepath) as file:
        reader_obj = reader(file)
        for row in reader_obj:
            if user in row:
                staff = Staff(*row)
        return staff


with open("customer_info.csv") as file:
    v = file.read()
if "account_number" not in v:
    with open("customer_info.csv", "w", newline="") as file:
        csv_writer = writer(file)
        csv_writer.writerow(["first_name", "last_name", "phone_no",
                            "acct_type", "pin", "email", "acct_balance", "account_number"])

with open("staff_info.csv") as file:
    r = file.read()
if "first_name" not in r:
    with open("staff_info.csv", "w", newline="") as file:
        csv_writer = writer(file)
        csv_writer.writerow(
            ["first_name", "last_name", "username", "password", "suspension_status", "default_p_status"])

filename = "logs.csv"
delimiter = ','
level = logging.INFO
custom_additional_levels = ['customer', 'staff', 'admin']
fmt = f'%(asctime)s{delimiter}%(levelname)s{delimiter}%(message)s'
datefmt = '%Y/%m/%d %H:%M:%S'
max_size = 10240  # 1 megabyte
max_files = 4  # 4 rotating files
header = ['date', 'user-class', 'user-name', 'action', 'amount']

csvlogger = CsvLogger(filename=filename,
                      delimiter=delimiter,
                      level=level,
                      add_level_names=custom_additional_levels,
                      add_level_nums=None,
                      fmt=fmt,
                      datefmt=datefmt,
                      max_size=max_size,
                      max_files=max_files,
                      header=header)

class Customer:
    def __init__(self, f_name, l_name, phone_no, acct_type, pin, email, acct_balance=randint(5000, 15000), acct_no=str(randint(1324145265, 5628158894))):
        self.f_name = f_name
        self.l_name = l_name
        self.phone_no = phone_no
        self.acct_type = acct_type
        self.pin = pin
        self.email = email
        self.acct_balance = acct_balance
        self.is_loggedin = False
        self.acct_no = acct_no
        self.full_name = self.f_name + " " + self.l_name
        with open("customer_info.csv") as file:
            v = file.read()
        if self.f_name not in v:
            print(
                f"Welcome, {self.f_name}. Your account has been created. \nAccount Number: {self.acct_no}\nThanks for banking with us.")
        with open("customer_info.csv") as file:
            s = file.read()
        if acct_no not in s:
            with open("customer_info.csv", "a", newline="") as file:
                csv_writer = writer(file)
                csv_writer.writerow([f_name, l_name, phone_no, acct_type,
                    pin, email, acct_balance, self.acct_no])
            csvlogger.customer([self.full_name, "SIGN_UP", self.acct_balance])

    def view_balance(self):
        view = locale.currency(int(self.acct_balance), grouping=True)
        print(
            f"Dear {self.f_name}, your account balance is {view}. \nThanks for banking with us.")
        csvlogger.customer([self.full_name, "VIEW_BALANCE", self.acct_balance])

    def withdrawal(self, amount):
        b = int(self.acct_balance)
        if b >= amount:
            b -= amount
            self.acct_balance = b
            c_info = []
            with open("customer_info.csv") as file:
                reader_obj = reader(file)
                for row in reader_obj:
                    c_info.append(row)
            
            with open('customer_info.csv') as file:
                reader_obj = reader(file)
                for row in reader_obj:
                    if self.f_name in row:
                        c = row

            index = c_info.index(c) - 1
            df = pd.read_csv("customer_info.csv")
            df.loc[index, 'acct_balance'] = self.acct_balance
            df.to_csv("customer_info.csv", index=False)
            view1 = locale.currency(amount, grouping=True)
            view2 = locale.currency(self.acct_balance, grouping=True)
            print(f"Dear {self.f_name}, you have successfully withdrawn {view1}. Your new balance is {view2}. \nThanks for banking with us.")
            csvlogger.customer([self.full_name, "WITHDRAWAL", amount])
        else:
            print("Withdrawal amount greater than bank account balance")

    def deposit(self, amount):
        b = int(self.acct_balance)
        b += amount
        self.acct_balance = b
        c_info = []
        with open("customer_info.csv") as file:
            reader_obj = reader(file)
            for row in reader_obj:
                c_info.append(row)
            
        with open('customer_info.csv') as file:
            reader_obj = reader(file)
            for row in reader_obj:
                if self.f_name in row:
                    c = row

        index = c_info.index(c) - 1
        df = pd.read_csv("customer_info.csv")
        df.loc[index, 'acct_balance'] = self.acct_balance
        df.to_csv("customer_info.csv", index=False)
        view1 = locale.currency(amount, grouping=True)
        view2 = locale.currency(self.acct_balance, grouping=True)
        print(f"Dear {self.f_name}, you have successfully deposited {view1}. Your new balance is {view2}. \nThanks for banking with us.")
        csvlogger.customer([self.full_name, "DEPOSIT", amount])

    def transfer(self, amount, recipient):
        if int(self.acct_balance) >= amount:
            b = int(self.acct_balance)
            b -= amount
            self.acct_balance = b
            c_info = []
            with open("customer_info.csv") as file:
                reader_obj = reader(file)
                for row in reader_obj:
                    c_info.append(row)
            
            with open('customer_info.csv') as file:
                reader_obj = reader(file)
                for row in reader_obj:
                    if self.f_name in row:
                        c = row

            index = c_info.index(c) - 1
            df = pd.read_csv("customer_info.csv")
            df.loc[index, 'acct_balance'] = self.acct_balance
            df.to_csv("customer_info.csv", index=False)
            recipient.deposit(amount)
            view1 = locale.currency(amount, grouping=True)
            print(
                f"Dear {self.f_name}, you have successfully transferred ${view1} to {recipient.f_name}. \nThanks for banking with us.")
            csvlogger.customer([self.full_name, "TRANSFER", amount])
        else:
            print("Transfer amount greater than Bank balance.")

    def login(self, email, pin):
        if email == self.email and pin == decryptor(self.pin):
            self.is_loggedin = True
            print("You have successfully logged in.")
            csvlogger.customer([self.full_name, "LOGIN", "NIL"])
        else:
            print("Wrong Credentials. Try again.")

    def logout(self):
        if self.is_loggedin:
            self.is_loggedin = False
            print("You have successfully logged out.")
            csvlogger.customer([self.full_name, "LOGOUT", "NIL"])
        else:
            print("You have to be logged in to log out.")

class Staff:
    def __init__(self, f_name, l_name, username, password, suspension_status="not_suspended", default_p = "not_changed"):
        self.f_name = f_name
        self.l_name = l_name
        self.password = password
        self.username = username
        self.full_name = self.f_name + " " + self.l_name
        self.is_suspended = suspension_status
        self.is_loggedin = False
        self.default_p = default_p
        with open("staff_info.csv") as file:
            s = file.read()
        if username not in s:
            with open("staff_info.csv", "a", newline="") as file:
                csv_writer = writer(file)
                csv_writer.writerow(
                    [f_name, l_name, username, password, self.is_suspended, self.default_p])
            csvlogger.staff([self.full_name, "STAFF CREATED", "NIL"])

    def view_c_balance(self, customer):
        view1 = locale.currency(int(customer.acct_balance), grouping=True)
        print(
            f"Customer name: {customer.full_name}.\nAccount Balance: {view1}")
        csvlogger.staff(
            [self.full_name, f"VIEW_BALANCE({customer.f_name})", customer.acct_balance])

    def customer_deposit(self, amount, customer):
        customer.deposit(amount)
        # print(f"Customer Name: {customer.full_name()} \nAmount Deposited: {amount}. \nNew Balance: {customer.acct_balance}.")
        csvlogger.staff(
            [self.full_name, f"DEPOSIT({customer.f_name})", amount])
        
    def setpassword(self, new_password):
        self.password = encryptor(new_password)
        self.default_p = "changed"
        s_info = []
        with open("staff_info.csv") as file:
            reader_obj = reader(file)
            for row in reader_obj:
                s_info.append(row)
            
        with open('staff_info.csv') as file:
            reader_obj = reader(file)
            for row in reader_obj:
                if self.f_name in row:
                    c = row

        index = s_info.index(c) - 1
        df = pd.read_csv("staff_info.csv")
        df.loc[index, ['default_p_status', 'password']] = [self.default_p, self.password]
        df.to_csv("staff_info.csv", mode = "w", index=False)
        print(f"Dear, {self.f_name}, you default password has been successfully changed.")

    def login(self, username, password):
        if self.is_suspended == "suspended":
            print("You are currently suspended. Refer to Admin")
        elif username == self.username and password == decryptor(self.password):
            self.is_loggedin = True
            print("You have successfully logged in.")
            csvlogger.staff([self.full_name, "LOGIN", "NIL"])
        else:
            print("Wrong credentials. Try again")

    def logout(self):
        if self.is_loggedin:
            self.is_loggedin = False
            print("You have successfully logged out.")
            csvlogger.staff([self.full_name, "LOGOUT", "NIL"])
        else:
            print("You have to be logged in to log out.")

class Admin:
    def __init__(self, f_name, l_name, username, password):
        self.f_name = f_name
        self.l_name = l_name
        self.full_name = self.f_name + " " + self.l_name
        self.username = username
        self.password = encryptor(password)
        self.is_loggedin = False

    def create_staff(self, f_name, l_name, username, password =''.join((choice(string.ascii_letters) for i in range(8)))):
        print(f"New Staff Created. Your default password is {password}")
        return Staff(f_name, l_name, username, encryptor(password))

    def suspension(self, staff):
        staff.is_suspended = "suspended"
        s_info = []
        with open("staff_info.csv") as file:
            reader_obj = reader(file)
            for row in reader_obj:
                s_info.append(row)
            
        with open('staff_info.csv') as file:
            reader_obj = reader(file)
            for row in reader_obj:
                if self.f_name in row:
                    c = row

        index = s_info.index(c) - 1
        df = pd.read_csv("staff_info.csv")
        df.loc[index, 'suspension_status'] = "suspended"
        df.to_csv("staff_info.csv", index=False)

    def end_suspension(self, staff):
        staff.is_suspended = "not_suspended"
        s_info = []
        with open("staff_info.csv") as file:
            reader_obj = reader(file)
            for row in reader_obj:
                s_info.append(row)
            
        with open('staff_info.csv') as file:
            reader_obj = reader(file)
            for row in reader_obj:
                if self.f_name in row:
                    c = row

        index = s_info.index(c) - 1
        df = pd.read_csv("staff_info.csv")
        df.loc[index, 'suspension_status'] = "not_suspended"
        df.to_csv("staff_info.csv", index=False)

    def login(self, username, password):
        if username == self.username and password == decryptor(self.password):
            self.is_loggedin = True
            print("You have successfully logged in.")
            csvlogger.admin([self.full_name, "LOGIN", "NIL"])
        else:
            print("Wrong credentials. Try again")

    def logout(self):
        if self.is_loggedin:
            self.is_loggedin = False
            print("You have successfully logged out.")
            csvlogger.admin([self.full_name, "LOGOUT", "NIL"])
        else:
            print("You have to be logged in to log out.")


admin = Admin("Daniel", "Momodu", "Dmaestro", "sapa&cruise")
app_state = True
while app_state:
    log_or_sign = input(
        "MAIN MENU\nWhat do you want to do?\n\n1.LOGIN SCREEN\n2. SIGN UP SCREEN\n0. CLOSE APP\n\nINPUT: ")
    login = True
    while login:
        if log_or_sign == "1":
            # while loop makes sure you're inputting valid queries
            while True:
                # input for choice of login. while loop to make sure correct input is put in
                u_type = input(
                    "LOGIN SCREEN\nChoose type of user\n\n1. ADMIN\n2. STAFF\n3. CUSTOMER\n0.MAIN MENU\n\nInput here: ")
                if u_type == "1":
                    #if admin, while loop to make sure of correct username and password 
                    while True:
                        username = input("Type in your username: ")
                        password = input("Type in your password: ")
                        # admin login method to validate username and password
                        admin.login(username, password)
                        if admin.is_loggedin:
                            break
                    while admin.is_loggedin:

                        while True:
                            # while loop to choose action for admin
                            action = input(
                                f"Welcome, {admin.f_name}.\nWhat do you want to do? Here are the inputs\n\n1. Create new Staff\n2. Suspend staff\n3. Remove staff from suspension\n4. View all staff and customer\n5. View all logs\n0.Log out\n\nInput here: ")
                            # CREATE STAFF
                            if action == "1":
                                f_name = input("Type in First Name: ")
                                l_name = input("Type in Last Name: ")
                                username = input("Type in Username: ")
                                admin.create_staff(f_name, l_name, username)
                                break
                            # SUSPEND STAFF 
                            elif action == "2":
                                s_staff = input("Input Staff username: ")
                                with open("staff_info.csv") as file:
                                    reader_obj = reader(file)
                                    for row in reader_obj:
                                        if s_staff in r:
                                            staff = Staff(*row)
                                # if staff is already suspended, exception message
                                if staff.is_suspended == "suspended":
                                    print("Staff is already suspended.")
                                else:
                                    admin.suspension(staff)
                                break
                            # REMOVE STAFF FROM SUSPENSION
                            elif action == "3":
                                s_staff = input("Input Staff username: ")
                                with open("staff_info.csv") as file:
                                    reader_obj = reader(file)
                                    for row in reader_obj:
                                        if s_staff in r:
                                            staff = Staff(*row)
                                if staff.is_suspended == "suspended":
                                    admin.end_suspension(staff)
                                else:
                                    print("Staff is not suspended")
                                break
                            # VIEW ALL STAFF AND CUSTOMERS
                            elif action == "4":
                                # print all staff
                                with open("staff_info.csv") as file:
                                    reader_obj = reader(file)
                                    for row in reader_obj:
                                        if "first_name" not in row:
                                            staff = Staff(*row)
                                            print(staff.full_name, "- STAFF")
                                # print all customers
                                with open("customer_info.csv") as file:
                                    reader_obj = reader(file)
                                    for row in reader_obj:
                                        if "first_name" not in row:
                                            customer = Customer(*row)
                                            print(customer.full_name,
                                                  "-CUSTOMER")
                                break
                            # VIEW ALL LOGS
                            elif action == "5":
                                with open("logs.csv") as file:
                                    reader_obj = reader(file)
                                    for row in reader_obj:
                                        if "user-class" not in row:
                                            print(" ".join(row))
                                break
                            elif action == "0":
                                admin.logout()
                                break
                            else:
                                print("Wrong Input. Try again.")
                # STAFF LOGIN
                elif u_type == "2":
                    while True:
                        username = input("Type in your username: ")
                        password = input("Type in your password: ")

                        staff_details = ""

                        with open("staff_info.csv") as file:
                            reader_obj = reader(file)
                            for row in reader_obj:
                                if username in row and encryptor(password) in row:
                                    staff_details = row
                                    
                            if staff_details:
                                staff = Staff(*staff_details)
                                staff.login(username, password)
                                if staff.is_loggedin:
                                    if staff.is_suspended == "suspended":
                                        break
                                    # changed default password on first login
                                    if staff.default_p == "not_changed":
                                        print(f"Dear, {staff.f_name}, please change your default password.")
                                        new_pword = input("Type in new password: ")
                                        staff.setpassword(new_pword)
                                        break
                                    else:
                                        break
                            else:
                                print("Wrong credentials. Try again.")
                                
                    while staff.is_loggedin:
                        while True:
                            action = input(
                                f"Welcome, {staff.f_name}.\nWhat do you want to do? Here are the inputs.\n\n1. View customer balance\n2. Take customer deposit\n0. Logout\n\nInput here: ")
                            if action == "1":
                                c_email = input("Customer Email Address: ")
                                with open("customer_info.csv") as file:
                                    reader_obj = reader(file)
                                    for row in reader_obj:
                                        if c_email in row:
                                            customer = Customer(*row)
                                if customer:
                                    staff.view_c_balance(customer)
                                    break
                                else:
                                    print("Customer not found.")
                            elif action == "2":
                                c_email = input("Customer Email Address: ")
                                c_deposit = int(input("Amount to deposit: "))
                                customer = find_user_customer(
                                    "customer_info.csv", c_email)
                                if customer:
                                    staff.customer_deposit(c_deposit, customer)
                                    break
                                else:
                                    print("Customer not found.")
                            elif action == "0":
                                staff.logout()
                                break
                            else:
                                print("Wrong input. Try again")
                elif u_type == "3":
                    while True:
                        email = input("Type in your email: ")
                        pin = input("Type in your pin: ")

                        with open("customer_info.csv") as file:
                            reader_obj = reader(file)
                            for row in reader_obj:
                                if encryptor(pin) in row and email in row:
                                    customer = Customer(*row)
                        if customer:
                            customer.login(email, pin)
                            if customer.is_loggedin:
                                break

                    while customer.is_loggedin:
                        while True:
                            action = input(
                                f"Welcome, {customer.f_name}.\nWhat do you want to do? Here are the inputs:\n\n1. View Account Balance\n 2. Make a withdrawal\n3. Make a transfer\n0. Logout.\n\nInput Here: ")
                            if action == "1":
                                customer.view_balance()
                                break
                            elif action == "2":
                                amount = int(
                                    input("How much do you want to withdraw: "))
                                customer.withdrawal(amount)
                            elif action == "3":
                                r_email = input("Email address of Recipient: ")
                                amount = int(
                                    input("How much do you want to transfer: "))
                                recipient = find_user_customer(
                                    "customer_info.csv", r_email)
                                customer.transfer(amount, recipient)
                                break
                            elif action == "0":
                                customer.logout()
                                break
                            else:
                                print("Wrong input. Try again.")
                elif u_type == "0":
                    login = False
                    break
                else:
                    print("Inappropriate Input. Try again.")
        elif log_or_sign == "2":
            f_name = input("Enter First Name: ")
            l_name = input("Enter Last Name: ")
            phone_no = input("Enter Phone Number: ")
            while True:
                acct = input(
                    "Enter 1 for Savings account. Enter 2 for Current Account: ")
                if acct == "1":
                    acct_type = "Savings"
                    break
                elif acct == "2":
                    acct_type = "Current"
                    break
                else:
                    print("Wrong Input")
            pin = encryptor(input("Please put in a secure 6-digit pin: "))
            email = input("Please input your email: ")
            customer = Customer(f_name, l_name, phone_no,
                                acct_type, pin, email)
            break

        elif log_or_sign == "0":
            app_state = False
            break
        else:
            print("Wrong Input. Try again.")
            break
