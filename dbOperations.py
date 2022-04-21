#######################################################################################################
#  FILE :  dbOperations.py                                                                          #
#          Provides backend related functions                                                       #
#          apartmentSearchList() , bookAppointment(), createStaffAccount(), viewApartmentStatus()   #
#          addNewProperty()                                                                         #
#######################################################################################################

import re
import sqlite3

import pandas as pd
from tabulate import tabulate
from termcolor import colored

from StaffFunctions_GenerateBooking import generate_booking
from Utils import confirm_ExitApplication

connection = sqlite3.connect("Greencorp.db")

uNameRegex = r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
PropertyName = ''
Location = ''
locationInp = ''


# Function for Searching the apartments (User Level - New User(Prospects))
def apartmentSearchList():
    global PropertyID, locationInp, PropertyName, Location, UnitNumber, Type, RentperMonth, NoofBedrooms, TotalArea, NoofBathrooms
    check_loc = True
    print("***********************************************************************************")
    print("     Greencorp Rentals has properties across Kitchener, Waterloo and Cambridge ")
    print("-----------------------------------------------------------------------------------")
    while check_loc:
        try:
            locList = ["kitchener", "waterloo", "cambridge"]
            input1 = input("Enter your preferred location : ")
            locationInp = input1.lower()
            if locationInp not in locList:
                print("Please enter a valid location!")
                continue
            else:
                check_loc = False
        except ValueError:
            continue
        else:
            check_Name = False

    cursor = connection.cursor()
    query1 = "SELECT PropertyName " \
             "FROM UNIT WHERE UnitStatus = 'Available' AND Location = '{}'; ".format(locationInp)
    cursor.execute(query1)
    results1 = cursor.fetchall()
    PropertyName = str(results1)
    query2 = "SELECT UnitNumber, Type, RentperMonth, NoofBedrooms, NoofBathrooms, TotalArea " \
             "FROM UNIT WHERE UnitStatus = 'Available' AND Location = '{}'; ".format(locationInp)
    cursor.execute(query2)
    results2 = cursor.fetchall()

    if len(results2) > 0:
        print(" ")
        print("      {}       {}      ".format(results1[0][0], locationInp))
        print("-------------------------------------------------------------------------------")

        df = pd.DataFrame(results2,
                          columns=['Unit Number', 'Type', 'Rent Per Month', 'No Of Bed Rooms', 'No Of Bath Rooms',
                                   'Total Area'])
        print(colored(tabulate(df, headers='keys', tablefmt='psql'), 'blue'))

        """
        print(tabulate(results2,
                       headers=['UnitNumber', 'Type', 'Rent Per Month', 'Bedrooms', 'Bathrooms', 'TotalArea'],
                       tablefmt='simple'))
                       """
        print(" ")
        print("Please book an appointment with our staff for a tour and other details!")
        print(" ")
        cursor.close()


# Function that book an appointemnt for a prospect with the staff
def bookAppointment():
    print("******************************************************")
    print("      Book an appointment with our staff here")
    print("-------------------------------------------------------")
    success = True
    while success:
        try:
            fname = input(" First Name   : ")
            lname = input(" Last Name    : ")
            email = input(" Email ID     : ")
            matchSyntax = re.fullmatch(uNameRegex, email)
            if matchSyntax is None:
                print("Email {} is invalid. Please provide a valid one.\n".format(email))
                email = input(" Email ID     : ")
            phone = input(" Phone Number : ")
        except ValueError:
            continue
        else:
            # write to Table: UnitBooking
            writeToTableUnitBooking(fname, lname, email, phone)
            print(" Booking Request Sent To Our Staff. Please Wait for the confirmation!")
            success = False
    return True


# Function that stores appointments details into the database
def writeToTableUnitBooking(FirstName, LastName, EmailID, ContactNo):
    cursor = connection.cursor()
    query = "insert into UnitBooking (FirstName, LastName, EmailID, ContactNo, Status) values ('{}','{}','{}','{}'," \
            "'{}');".format(FirstName, LastName, EmailID, ContactNo, "New")
    cursor.execute(query)
    cursor.execute("COMMIT;")
    cursor.close()


# Function to create staff account. User Level - Admin
# email id is automatically generated with the domain 'greencorp.com'
def createStaffAccount():
    fname = ''
    lname = ''
    email = ''
    print("******************************************************")
    print("      Create Staff Account here")
    print("-------------------------------------------------------")
    success = True
    while success:
        try:
            fname = input(" First Name   : ")
            lname = input(" Last Name    : ")
        except ValueError:
            continue
        else:
            check_Name = False
            email = fname + lname + '@greencorp.com'
            newPassword = fname
            UserType = "Staff"
            cursor = connection.cursor()
            query = "insert into USER (UserType, Username, Password) values ('{}','{}','{}');".format(UserType, email,
                                                                                                      newPassword)
            cursor.execute(query)
            cursor.execute("COMMIT;")
            cursor.close()
            print(" Staff Account Created Successfully !")
            print(" Staff {} {} will be able to sign in to the portal soon", format(fname, lname))
        return True


# Function for the admin and staff to view the apartment status
def viewApartmentStatus():
    status = ''
    location = ''
    print("******************************************************")
    print("                GREENCORP RENTALS                     ")
    print("------------------------------------------------------")
    print(" ")
    error_entry = True
    while error_entry:
        print(" 1. Available Units ")
        print(" 2. Leased Units ")
        print(" 3. Return to main page")
        try:
            optionSelected = int(input("Choose Your Option(?): "))
            if optionSelected == 1:
                status = "Available"
                unitStatusQueryFunction(status)
            elif optionSelected == 2:
                status = "Leased"
                unitStatusQueryFunction(status)
            elif optionSelected == 3:
                return False
            else:
                print("Wrong option Selected")
                continue
        except ValueError:
            continue
        else:
            error_entry = True
        # wishtoContinue = confirm_ExitApplication()
        # if wishtoContinue:
        #     error_entry = True
        #     continue
        # else:
        #    error_entry = False


# Function to Query the unit status data for admin and staff
def unitStatusQueryFunction(status):
    check_loc = True
    while check_loc:
        try:
            locList = ["kitchener", "waterloo", "cambridge"]
            input1 = input("Enter Property location : ")
            if input1.lower() not in locList:
                print("Please enter a valid location!")
                continue
            else:
                check_loc = False
                location = input1.lower()
        except ValueError:
            continue
        else:
            check_loc = False

    cursor = connection.cursor()
    query = "SELECT UnitNumber, Type " \
            "FROM UNIT WHERE UnitStatus = ? AND Location = ?;"
    cursor.execute(query, (status, location))
    results = cursor.fetchall()
    cursor.close()
    if len(results) > 0:
        print(" ")
        print("      {}       {}      ".format(results[0][0], locationInp))
        print("-------------------------------------------------------------------------------")
        # print(tabulate(results, headers=['UnitNumber', 'Type'], tablefmt='simple'))
        df = pd.DataFrame(results,
                          columns=['Unit Number', 'Type'])
        print(colored(tabulate(df, headers='keys', tablefmt='psql'), 'blue'))

        print(" ")
        return True
    else:
        print("No Units present for the selected option !")
        return False


# Function to fetch tenant data from database , User Level - Tenant (dashboard)
def fetchTenantDetails(userName):
    cursor = connection.cursor()
    query1 = "SELECT FirstName, LastName, EmailID, ContactNo FROM Tenant WHERE EmailID='{}';".format(userName)
    cursor.execute(query1)
    results = cursor.fetchall()
    cursor.close()
    if len(results) > 0:
        # print(tabulate(results, headers=['FirstName', 'LastName', 'EmailID', 'ContactNumber'], tablefmt='simple'))
        df = pd.DataFrame(results,
                          columns=['First Name', 'Last Name', 'Email ID', 'Contact No'])
        print(colored(tabulate(df, headers='keys', tablefmt='psql'), 'blue'))
        print("---------------------------------------------------------------")


# function to add a new property. User Level - Admin
def addNewProperty():
    propertyIDTemp = ''
    str1 = ''
    print("******************************************************")
    print("      Add New Property Details here")
    print("-------------------------------------------------------")
    success = True
    while success:
        try:
            projectID = input("Project ID       : ")
            projectName = input("Project Name     : ")
            projectLocation = input("Project Location :")
        except ValueError:
            continue
        else:
            success = False
            cursor = connection.cursor()
            query1 = "SELECT PropertyID FROM Property ORDER BY PropertyID DESC LIMIT 1"
            cursor.execute(query1)
            results = cursor.fetchall()
            for result in results:
                propID = result[0]

            idNum = int(propID.split('-')[1]) + 1
            propertyID = "PROP-" + str(idNum)
            query = "insert into Property (PropertyID, ProjectID, PropertyName, Location) values ('{}','{}','{}','{}');" \
                .format(propertyID, projectID, projectName, projectLocation)
            cursor.execute(query)
            cursor.execute("COMMIT;")
            cursor.close()
            print(" Property Details Added/Created Successfully !")
        return True


# Function to approve the appointments. User Level - Staff
def approveAppointments():
    print("******************************************************")
    print("      Pending Appointment Approvals")
    print("-------------------------------------------------------")

    cursor = connection.cursor()
    query = "SELECT FirstName, LastName, EmailID, ContactNo FROM UnitBooking WHERE Status = '{}';".format("New")
    cursor.execute(query)
    userresults = cursor.fetchall()
    # cursor.close()
    if len(userresults) > 0:
        print(" ")
        # print(tabulate(userresults, headers=['First Name', 'Last Name', 'Email ID', 'Contact'], tablefmt='simple'))
        df = pd.DataFrame(userresults,
                          columns=['First Name', 'Last Name', 'Email ID', 'Contact No'])
        print(colored(tabulate(df, headers='keys', tablefmt='psql'), 'blue'))
        print(" ")

    else:
        print("No Pending Appointments !")
        return False

    pendingAppointmentList = []
    for name in userresults:
        pendingAppointmentList.append(str(name[2]))

    success = True
    while success:
        try:
            print(" 1. Approve user.")
            print(" 2. Go to main page")
            options = int(input(" PLEASE CHOOSE YOUR OPTIONS  : "))
            if options == 1:
                userNameToApprove = input("Enter the user Email ID for approval       : ")
                if userNameToApprove.lower() not in pendingAppointmentList:
                    print("Please enter a valid Email ID!")
                    continue
            if options == 2:
                return True
        except ValueError:
            continue
        else:
            query = "UPDATE UnitBooking SET Status='{}' WHERE EmailID='{}';".format("Approved", userNameToApprove)
            cursor.execute(query)
            cursor.execute("COMMIT;")
            cursor.close()
            print(" Appointment for user '{}' is Approved ! Notification sent to user.\n".format(userNameToApprove))
            success = False
    return True


# Function to approve tenant profile. User Level - Staff
def approveTenantProfile():
    propertyIDTemp = ''
    str1 = ''
    print("******************************************************")
    print("      Approve Tenant Profile Page")
    print("-------------------------------------------------------")

    cursor = connection.cursor()
    query = "SELECT UserName FROM User WHERE UserType = '{}';".format("User")
    cursor.execute(query)
    userresults = cursor.fetchall()
    # cursor.close()
    if len(userresults) > 0:
        print(" ")
        # print(tabulate(userresults, headers=['Profiles To Approve'], tablefmt='simple'))
        df = pd.DataFrame(userresults,
                          columns=['User Name'])
        print(colored(tabulate(df, headers='keys', tablefmt='psql'), 'blue'))

        print(" ")
    else:
        print("No Pending Approvals !")
        return False

    userList = []
    for name in userresults:
        userList.append(str(name[0]))

    success = True
    while success:
        try:
            userNameToApprove = input("Enter the Tenant EmailID for approval       : ")
            if userNameToApprove.lower() not in userList:
                print("Please enter the correct EmailID!")
                continue
        except ValueError:
            continue
        else:
            createTenant(userNameToApprove)
            generate_booking(userNameToApprove)
            query = "UPDATE User SET UserType='{}' WHERE Username='{}';".format("NewTenant", userNameToApprove)
            cursor.execute(query)
            cursor.execute("COMMIT;")
            cursor.close()
            print(" Tenant profile {} is Approved !".format(userNameToApprove))
            success = False
    return True


# Function to create a new Tenant
def createTenant(userName):
    cursor = connection.cursor()
    query2 = "SELECT Firstname, Lastname, ContactNo FROM UnitBooking WHERE EmailID = '{}';".format(userName)
    cursor.execute(query2)
    results1 = cursor.fetchall()
    for row in results1:
        tFname = str(row[0])
        tLname = str(row[1])
        tContactNo = str(row[2])

    # Fetch Last Added TenantID
    query1 = "SELECT TenantID FROM Tenant ORDER BY TenantID DESC LIMIT 1"
    cursor.execute(query1)
    results = cursor.fetchall()
    tempID = str(results[0][0])

    idNum = int(tempID[1:len(tempID)]) + 1
    newTenantID = "T" + str(idNum)

    # Query to Add Tenant into Tenant table
    query = "insert into Tenant (TenantID, TenantType, FirstName, LastName, EmailID, ContactNo) values ('{}'," \
            "'{}','{}','{}','{}','{}');".format(newTenantID, "NewTenant", tFname, tLname, userName, tContactNo)
    cursor.execute(query)
    cursor.execute("COMMIT;")
    print(" Tenant Account Created Successfully !")

    # change UserType in USER table to Tenant
    query = "UPDATE User SET UserType='{}' WHERE Username='{}';".format("Tenant", userName)
    cursor.execute(query)
    cursor.execute("COMMIT;")
    cursor.close()
    return True


# Function that displays the booked unit details. User Level - Tenant
def displayBookedUnit(userName):
    cursor = connection.cursor()
    query1 = "SELECT TenantID FROM Tenant where EmailID = '{}'".format(userName)
    cursor.execute(query1)
    results1 = cursor.fetchall()
    TenantID = str(results1[0][0])

    query2 = "select UnitID from Booking where TenantID='{}'".format(TenantID)
    cursor.execute(query2)
    results2 = cursor.fetchall()
    unitID = str(results2[0][0])

    print(colored("Unit Details:" + unitID, 'blue'))


# Function that displays the payment plan created. User Level - Tenant
def displayPaymentPlan(userMobileNo):
    cursor = connection.cursor()
    query1 = "SELECT TenantID FROM Tenant where ContactNo = '{}'".format(userMobileNo)
    cursor.execute(query1)
    results = cursor.fetchall()
    TenantID = str(results[0][0])
    query2 = "SELECT PAYMENTPLANITEMID, DUEDATE, INSTALMENTNUMBER, INSTALMENTAMOUNT FROM PAYMENTPLANITEMS WHERE " \
             "TenantID = ? "
    execute = cursor.execute(query2, (TenantID,))
    df = pd.DataFrame(cursor.fetchall(),
                      columns=['PAYMENT PLAN ITEM ID', 'DUE DATE', 'INSTALMENT NUMBER', 'INSTALMENT AMOUNT'])
    print(colored(tabulate(df, headers='keys', tablefmt='psql'), 'blue'))
    cursor.close()


#  Function to display outstanding payment details . User Level - Tenant
def displayPaymentDetails(userName):
    cursor = connection.cursor()
    query2 = "SELECT TenantID FROM Tenant where EmailID = '{}'".format(userName)
    cursor.execute(query2)
    results = cursor.fetchall()
    TenantID = str(results[0][0])
    query1 = "SELECT PAYMENTPLANITEMID, DUEDATE, INSTALMENTNUMBER, INSTALMENTAMOUNT FROM PaymentPlanItems where " \
             "PaymentStatus = 'Pending' AND TenantID = '{}' LIMIT 1;".format(TenantID)
    cursor.execute(query1)
    df = pd.DataFrame(cursor.fetchall(),
                      columns=['PAYMENT PLAN ITEM ID', 'DUE DATE', 'INSTALMENT NUMBER', 'INSTALMENT AMOUNT'])
    print(colored(tabulate(df, headers='keys', tablefmt='psql'), 'blue'))
    cursor.close()


# Function to update tenant status upon lease confirmation - User Level - Tenant
def updateTenant(userName):
    cursor = connection.cursor()
    query = "UPDATE User SET UserType='{}' WHERE Username='{}';".format("Tenant",
                                                                        userName)
    cursor.execute(query)
    cursor.execute("COMMIT;")
    cursor.close()


# Function to display tenant details for dashboard
def getTenantDetails(userName):
    LeaseEndData = ''
    TenantID = ''
    cursor = connection.cursor()
    query = "SELECT TENANTID FROM TENANT WHERE EMAILID = ?"
    execute = cursor.execute(query, (userName,))
    records = cursor.fetchall()
    for row in records:
        TenantID = row[0]
    query1 = "SELECT TENANCYENDDATE FROM BOOKING WHERE TENANTID = ?"
    cursor.execute(query1, (TenantID,))
    records1 = cursor.fetchall()
    for row1 in records1:
        LeaseEndData = row1[0]
    print(colored("Your Lease Expires On   :  {}".format(LeaseEndData), 'blue'))


# Fucntion to store the complaints to the database. User Level -  Tenant
def logComplaint(userName):
    print("*********************************************************************")
    print(" ")
    eom = True
    while eom:
        try:
            unitID = input(" Please Enter Your UnitID  : ")
            msg = input("Please enter the message : ")
            cursor = connection.cursor()
            query = "insert into Complaints (Message, EmailID, UnitID) values ('{}','{}','{}');".format(msg, userName,
                                                                                                        unitID)
            cursor.execute(query)
            cursor.execute("COMMIT;")
            print(" Complaint Logged Successfully !")
        except ValueError:
            continue
        else:
            eom = False


# Function to update the payment status of tenant. User Level - Staff
def updateRentPaymentStatus():
    tenantID = input("Enter the TenantID :")
    dueDate = input("Enter the Due Date (YYYY-MM-DD): ")
    cursor = connection.cursor()
    query = "UPDATE PaymentPlanItems SET PaymentStatus = 'Done' WHERE TenantID='{}' AND DueDate = '{}';".format(tenantID,dueDate)
    cursor.execute(query)
    cursor.execute("COMMIT;")
    cursor.close()
    print("Payment status updated successfully")

