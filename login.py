#############################################################################################
#  FILE :  login.py                                                                         #
#          Provides functions to Sign-in and Sign-up                                        #
#############################################################################################
import loginFunctions
from Utils import confirm_ExitApplication
from adminFunctions import adminPage

from loginFunctions import validateUserName, validatePassword, verifyUserExists, createUser
from staffFunctions import staffPage
from tenantFunctions import tenantPage, enterTenantDetails

userName = ''
password = ''


def login():
    print("************************************************************************")
    print("              Welcome to GreenCorp Rentals                              ")
    print("************************************************************************")

    #print("(3) Exit")

    error_entry = True
    signInSuccess = False
    while error_entry:
        print("                                                                        ")
        print("(1) Sign-in ")
        print("(2) Sign-up")
        print("                                                                        ")
        try:
            optionSelected = int(input("Choose Your Option(?): "))
            if optionSelected == 1:
                signInPage()
            elif optionSelected == 2:
                signUpPage()
            else:
                print("Wrong option Selected")
        except ValueError:
            continue
        else:
            wishtoContinue = confirm_ExitApplication()
            if wishtoContinue:
                #error_entry = True
                continue
            else:
                error_entry = False
                quit()


"""
function: signInPage()
        :used to accept and validate userName, Password
        :successful validation will take to corresponding user page (Admin, Staff, Tenant)
"""


def signInPage():
    global userName, password
    userName = validateUserName()
    password = validatePassword()
    domain = userName.split('@')[1]
    if domain.lower() == "greencorp.com":
        tag = "greencorp"
    else:
        tag = "tenants"
    if verifyUserExists(userName, password):
        role = loginFunctions.userType
        if tag == "greencorp" and role == "Admin":
            adminPage(userName)
        elif tag == "greencorp" and role == "Staff":
            staffPage(userName)
        elif tag == "tenants" and role == "NewTenant":
            enterTenantDetails(userName)
        elif tag == "tenants" and role == "User":
            print("Please wait until your Lease document is released !")
            quit()
        else:
            tenantPage(userName)
        return True
    else:
        print(' User {}, does not exist. Please try again.'.format(userName))
        return False


"""
function: signUpPage()
        :used to accept and validate userName, Password
        :upon successful validation, Create the user record in Database
"""


def signUpPage():
    newUserName = validateUserName()
    if loginFunctions.verifyUsername(newUserName):
        newPassword = validatePassword()

        if verifyUserExists(newUserName, newPassword):
            print("The User Name already exists. Please try with another User Name !")
            return False
        if loginFunctions.verifyApprovalStatus(newUserName):
            createUser("User", newUserName, newPassword)
        else:
            print('Restricted..')
            print('Please verify the Email ID entered is same as the one given during appointment request !')
            print('                                       Or                                             ')
            print('Verify your status with the GreenwinCorp Staff !')
            return False
    else:
        print("The domain entered is private and is restricted")
        return False

    return True

