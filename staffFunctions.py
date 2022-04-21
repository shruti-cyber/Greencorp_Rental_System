#############################################################################################
#  FILE :  staffFunctions.py                                                                #
#          Provides Staff role supported functions                                          #
#          staffPage()                                                                      #
#############################################################################################

from Utils import confirm_ExitApplication
from dbOperations import viewApartmentStatus, approveTenantProfile, approveAppointments, updateRentPaymentStatus


def staffPage(userName):
    error_entry = True
    signInSuccess = False
    while error_entry:
        print(" ****************  GREENCORP RENTALS  ****************")
        print(" ")
        print("Welcome {} !".format(userName))
        print("1. View apartment status")
        print("2. Approve Tenant Profile")
        print("3. Confirm Appointments")
        print("4. Update Rent Payment Status")
        print("5. Sign out")
        try:
            optionSelected = int(input("Choose Your Option(?): "))
            if optionSelected == 1:
                error_entry = viewApartmentStatus()
            elif optionSelected == 2:
                approveTenantProfile()
            elif optionSelected == 3:
                approveAppointments()
            elif optionSelected == 4:
                updateRentPaymentStatus()
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
                continue
            else:
                error_entry = False
                quit()
