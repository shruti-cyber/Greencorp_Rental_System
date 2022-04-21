#############################################################################################
#  FILE :  adminFunctions.py                                                                #
#          Provides Admin role supported functions                                          #
#          addProperty() , adminPage()
#############################################################################################

from Utils import confirm_ExitApplication
from charts import fetchResults
from dbOperations import createStaffAccount, viewApartmentStatus, addNewProperty


def addProperty():
    error_entry = True
    while error_entry:
        try:
            projectName = input("Property Name : ")
            propertyID = input("Property ID : ")
            projectCount = int(input("Number of Units : "))
            projectLocation = input("Property Location : ")
        except ValueError:
            continue


def adminPage(userName):
    error_entry = True
    signInSuccess = False
    while error_entry:
        print(" ****************  GREENCORP RENTALS  ****************")
        print(" ")
        print("Welcome {} !".format(userName))
        print("1. View Reports")
        print("2. Add Staff Account")
        print("3. View apartment status")
        print("4. Add New Property")
        print("5. Sign out")
        try:
            optionSelected = int(input("Choose Your Option(?): "))
            if optionSelected == 1:
                fetchResults()
            elif optionSelected == 2:
                error_entry = createStaffAccount()
            elif optionSelected == 3:
                error_entry = viewApartmentStatus()
            elif optionSelected == 4:
                error_entry = addNewProperty()
            elif optionSelected == 5:
                error_entry = False
                quit()
            else:
                print("Wrong option Selected")
        except ValueError:
            continue
        else:
            error_entry = True
            wishtoContinue = confirm_ExitApplication()
            if wishtoContinue:
                error_entry = True
                continue
            else:
                error_entry = False
                quit()
