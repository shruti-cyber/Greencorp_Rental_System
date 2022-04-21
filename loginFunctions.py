#############################################################################################
#  FILE :  LoginFunctions.py                                                                #
#          Provides functions to create, verify and validate the user                       #
#############################################################################################
import base64
import sqlite3
import re

import login

connection = sqlite3.connect("Greencorp.db")

# regular expression to validate email id and password format
uNameRegex = r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
passwordRegex = r"^[A-Za-z0-9]+\b"
access_count = 0
userType = ""

#  Function to Validate the username


def validateUserName():
    check_Name = True
    userName = input('Enter the Username:')
    while check_Name:
        try:
            matchSyntax = re.fullmatch(uNameRegex, userName)
            if matchSyntax is None:
                print("User name {} is invalid. Please provide a valid one.\n".format(userName))
                userName = input('Enter the Username:')

                continue
        except Exception:
            continue
        else:
            check_Name = False
    return userName


def verifyUsername(username):
    domain = username.split('@')[1]
    if domain.lower() == "greencorp.com":
        return False
    else:
        return True


# Function to validate password
def validatePassword():
    check_Password = True
    password = input('Enter your Password:')
    while check_Password:
        match = re.fullmatch(passwordRegex, password)
        try:
            if match is None:
                print("Password should contain only alpha-numeric characters. Please provide a valid one.\n")
                password = input('Enter your Password:')
                continue
        except Exception:
            continue
        else:
            check_Password = False
    return password


# Function to verify whether the user exists or not
def verifyUserExists(userName, password):
    global access_count, userType
    #encryptedPassword = base64.b64decode(password) #password #encrypt(password)
    #print("Decoded Pwd:{}".format(encryptedPassword))
    encryptedPassword = password
    cursor = connection.cursor()
    query = "select UserType from User where Username='{}' and Password='{}' ;".format(userName, encryptedPassword)
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    if len(results) > 0:
        userType = results[0][0]
        return True
    else:
        return False


# Function to create a new user
def createUser(UserType, userName, password):
    #password = password.encode("utf-8")
    #str.encode(password,"utf-8")
    #encryptedPassword = base64.b64encode(password)
    #encryptedPassword = base64.encode(password) #encrypt(password)
    #print("Encoded Pwd:{}".format(encryptedPassword))

    encryptedPassword = password
    cursor = connection.cursor()
    query = "insert into USER (UserType, Username, Password) values ('{}','{}','{}');".format(UserType, userName, encryptedPassword)
    cursor.execute(query)
    cursor.execute("COMMIT;")
    cursor.close()
    print(" User Account Created Successfully !\n")
    login.login()


def verifyApprovalStatus(userName):
    cursor = connection.cursor()
    query = "select Status from UnitBooking where EmailID='{}';".format(userName)
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    if len(results) > 0:
        status = results[0]
        if status[0] == 'Approved':
            return True
        else:
            return False
    else:
        return False
