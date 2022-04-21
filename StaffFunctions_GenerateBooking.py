#############################################################################################
#  FILE :  StaffFunctions_GenerateBooking.py                                                #
#          Provides unit Booking related functions                                          #
#          booking_exists(), booking_termination(), generate_booking(), Unit_exists()       #
#          generate_booking(), tenantdetails(), add_months()                                #
#############################################################################################


import sqlite3
import datetime
import calendar
import pandas as pd
from tabulate import tabulate
from colorama import init
from termcolor import colored


connection = sqlite3.connect("Greencorp.db")

tenantexistance = ''
unitexistance = ''


def booking_exists(BookingID):
    Bookingnumber = ''
    cursor = connection.cursor()
    query = "SELECT BOOKINGID FROM BOOKING WHERE BOOKINGID = ?"
    execute = cursor.execute(query, (BookingID,))
    records = cursor.fetchall()
    for row in records:
        Bookingnumber = row[0]
    if Bookingnumber == BookingID:
        return Bookingnumber
    else:
        return ''


def booking_termination():
    print("Please enter the booking details:")
    BookingID = input("Booking ID : ")
    bookingnumber = booking_exists(BookingID)
    if bookingnumber == '':
        print("Please enter valid booking ID!\n")
    else:
        terminate_confirmation = input(
            "Are you sure, you want to terminate the booking " + bookingnumber + " (Yes/No) : ")
        if terminate_confirmation.upper() == 'YES':
            cursor = connection.cursor()
            query_terminate = "UPDATE BOOKING SET BOOKINGSTATUS = ? WHERE BOOKINGID = ?"
            parameters_terminate = ('Terminated', BookingID)
            cursor.execute(query_terminate, parameters_terminate)
            connection.commit()
            print("Booking", bookingnumber, " terminated successfully!\n")


def Unit_exists(Unitid):
    Unitnumber = ''
    cursor = connection.cursor()
    query = "SELECT UNITNUMBER FROM UNIT WHERE UNITNUMBER = ?"
    execute = cursor.execute(query, (Unitid,))
    records = cursor.fetchall()
    for row in records:
        Unitnumber = row[0]
    if Unitnumber == Unitid:
        return 1
    else:
        return 0


def tenantdetails(TenantID):
    tenant = ''
    cursor = connection.cursor()
    query = "SELECT FIRSTNAME,LASTNAME FROM TENANT WHERE TENANTID = ?"
    execute = cursor.execute(query, (TenantID,))
    records = cursor.fetchall()
    for row in records:
        if row[0] != None:
            tenant = str(row[0])
        if row[1] != None:
            tenant += " " + str(row[1])
    return tenant


def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)


def tenant_exists(Tenantid):
    User_id = ''
    cursor = connection.cursor()
    query = "SELECT TENANTID FROM TENANT WHERE TENANTID = ?"
    execute = cursor.execute(query, (Tenantid,))
    records = cursor.fetchall()
    for row in records:
        User_id = row[0]
    if User_id == Tenantid:
        return 1
    else:
        return 0


def generate_booking(userName):
    global tenantexistance, unitexistance
    print("Please enter the booking details:")
    StaffID = (input("Enter Advisor ID : "))
    BookingID = (input("Booking ID : "))
    UnitID = (input("Unit ID : "))
    TenantID = (input("Tenant ID : "))
    TenancyStartDate = (input("Tenancy Start Date(Format : YYYY-MM-DD) : "))
    TenancyEndDate = (input("Tenancy End Date(Format : YYYY-MM-DD) : "))
    Rentpermonth = int(input("Rent per month after discount : "))
    Noofdays = datetime.datetime.strptime(TenancyEndDate, '%Y-%m-%d') - datetime.datetime.strptime(TenancyStartDate,
                                                                                                   '%Y-%m-%d')
    if BookingID == "" or UnitID == "" or TenantID == "" or TenancyStartDate == "" or TenancyEndDate == "" or Rentpermonth == "":
        print("Please enter the relevant booking details and proceed!")
        generate_booking(userName)
    else:
       tenantexistance = tenant_exists(TenantID)
       unitexistance = Unit_exists(UnitID)
    if tenantexistance == 0:
        print("Please enter valid tenant ID!\n")
        generate_booking(userName)
    elif unitexistance == 0:
        print("Please enter valid unit ID!\n")
        generate_booking(userName)
    elif int(Noofdays.days) < 364:
        print("Please enter a valid Tenancy End Date(Duration of tenancy period should be one year)!!\n")
        generate_booking(userName)
    else:
        Totalleaseprice = 12 * Rentpermonth
        cursor = connection.cursor()
        query = "INSERT INTO BOOKING (BOOKINGID,UNITID,TENANTID, NOOFINSTALMENTS, TENANCYSTARTDATE, TENANCYENDDATE, SECURITYDEPOSIT, RENTPERMONTH, TOTALLEASEPRICE, BOOKINGSTATUS, LEASEADVISORID) VALUES(?,?,?,?,?,?,?,?,?,?,?);"
        parameters = (
        BookingID, UnitID, TenantID, 12, TenancyStartDate, TenancyEndDate, Rentpermonth, Rentpermonth, Totalleaseprice,
        'Booked', StaffID)
        cursor.execute(query, parameters)
        connection.commit()
        print(colored("-----------------------------------------------------------------", 'blue'))
        print(colored("Booking generated successfully! Please find below booking details", 'blue'))
        print(colored("\n Booking Details:", 'green'))
        print(colored("***********************************", 'green'))
        print(colored("Booking ID :" + BookingID, 'blue'))
        print(colored("Unit :" + UnitID, 'blue'))
        print(colored("Tenant Name :" + tenantdetails(TenantID), 'blue'))
        print(colored("Number of instalments : 12", 'blue'))
        print(colored("Total Lease Price :" + str(Totalleaseprice), 'blue'))
        print(colored("\n Payment Plan Item Details:", 'green'))
        print(colored("***********************************", 'green'))
        paymentStatus = 'Pending'
        for i in range(12):
            PPIdate = datetime.datetime.strptime(TenancyStartDate, '%Y-%m-%d')
            InstalmentDate = add_months(datetime.date(PPIdate.year, PPIdate.month, PPIdate.day), i)
            query1 = "INSERT INTO PAYMENTPLANITEMS (BOOKINGID,TENANTID, DUEDATE, INSTALMENTNUMBER, INSTALMENTAMOUNT, " \
                     "UNITID, PAYMENTSTATUS) VALUES(?,?,?,?,?,?,?); "
            parameters1 = (BookingID, TenantID, InstalmentDate, i + 1, Rentpermonth, UnitID,paymentStatus)
            cursor.execute(query1, parameters1)
            connection.commit()
        query_update = "UPDATE UNIT SET UNITSTATUS = ? WHERE UNITNUMBER = ?"
        parameters_update = ('Leased', UnitID)
        cursor.execute(query_update, parameters_update)
        connection.commit()
        query2 = "SELECT PAYMENTPLANITEMID, DUEDATE, INSTALMENTNUMBER, INSTALMENTAMOUNT FROM PAYMENTPLANITEMS WHERE " \
                 "BOOKINGID = ? "
        execute = cursor.execute(query2, (BookingID,))
        df = pd.DataFrame(cursor.fetchall(),
                          columns=['PAYMENT PLAN ITEM ID', 'DUE DATE', 'INSTALMENT NUMBER', 'INSTALMENT AMOUNT'])
        print(colored(tabulate(df, headers='keys', tablefmt='psql'), 'blue'))
        cursor.close()
