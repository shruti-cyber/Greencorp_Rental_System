#######################################################################################################
#  FILE :  displays reports                                                                        #
#######################################################################################################

import re
import sqlite3

import colored as colored
import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate
import numpy as np
from colorama import init
from termcolor import colored


def fetchResults():
    connection = sqlite3.connect("Greencorp.db")
    cursor = connection.cursor()

    ## Flats which are being Leased
    query1 = "select count(UnitNumber) count, LeaseAdvisorID as advisorid from Unit u join Booking b on " \
             "u.UnitNumber=b.UniTID group by LeaseAdvisorID "
    # cursor.execute(query1)
    # results1 = cursor.fetchall()
    # df_unit = pd.DataFrame(results1)
    df_unit = pd.read_sql(query1, connection)
    print("List of Units f Units being leased by an Advisor")
    print(colored(tabulate(df_unit,
                   headers=['UnitNumber_Count', 'LeaseAdvisorID'],
                   tablefmt='simple'), 'blue'))
    df_unit.plot.bar(title='Booking By Advisor Report', y='count', x='advisorid')

    ### Unit Status
    query2 = "select count(UnitNumber) as count , UnitStatus as status from Unit group by UnitStatus"
    # cursor.execute(query2)
    # results2 = cursor.fetchall()
    df_unit = pd.read_sql(query2, connection)
    lb = [row for row in df_unit['status']]  # Labels of graph
    print("UNIT STATUS REPORT")
    print(colored(tabulate(df_unit, headers=['UnitNumber_Count', 'Unit_Status'], tablefmt='psql'),'blue'))
    plot = df_unit.plot.pie(title="Unit Status Report", y='count',
                            labels=lb, autopct='%1.0f%%')

    ### Payment Forecast
    query3 = "select sum(Instalmentamount) as total , TenantID from PaymentPlanItems group by TenantID "
    df_unit = pd.read_sql(query3, connection)
    # print(df_unit)
    # lb= [row for row in df_unit['TenantID']] # Labels of graph
    print("PAYMENT FORECAST REPORT")
    print(colored(tabulate(df_unit, headers=['Total', 'TenantID'], tablefmt='psql'),'blue'))
    df_unit.plot.bar(title='Payment forecast Report', y='total', x='TenantID')

    ###### Booking Status Report
    query4 = "select count(BookingID) as count , BookingStatus from Booking group by BookingStatus "
    df_unit = pd.read_sql(query4, connection)
    lb = [row for row in df_unit['BookingStatus']]  # Labels of graph
    print("BOOKING STATUS REPORT")
    print(colored(tabulate(df_unit, headers=['Booking_Count', 'Booking_Status'], tablefmt='psql'),'blue'))
    plot = df_unit.plot.pie(title="Booking Status Report", y='count',
                            labels=lb, autopct='%1.0f%%')

    ######  Complaints Logged
    query5 = "select count(UnitID) as count, EmailID from Complaints group by UnitID"
    df_complaint = pd.read_sql(query5, connection)
    # lb= [row for row in df_complaint['USER']] # Labels of graph
    # print("NUMBER OF COMPLAINTS LOGGED BY TENANT")
    print(colored(tabulate(df_complaint, headers=['count', 'EmailID'], tablefmt='psql'),'blue'))
    df_complaint.plot.bar(title='Complaints Logged By Tenant', y='count', x='EmailID')

    plt.show()
