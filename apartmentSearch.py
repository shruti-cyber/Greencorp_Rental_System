#####################################################################################################
#  FILE :  apartmentSearch.py                                                                       #
#          Provides apartment related functions                                                     #
#          search() , suiteFeatures(), contact()                                                    #

#####################################################################################################

from Utils import confirm_ExitApplication
from dbOperations import apartmentSearchList, bookAppointment


def search():

    error_entry = True

    while error_entry:
        print("--------------------------------------------------------------")
        print("*********     GreenCorp - Modern Rental Community    ******** ")
        print("--------------------------------------------------------------")
        print("(1)  List of available apartments ")
        print("(2)  Suite Features ")
        print("(3)  Book an Appointment")
        print("(4)  Contact")
        print("(5)  Exit")
        try:
            optionSelected = int(input(" PLEASE CHOOSE YOUR OPTIONS  : "))
            if optionSelected == 1:
                apartmentSearchList()
            elif optionSelected == 2:
                suiteFeatures()
            elif optionSelected == 3:
                bookAppointment()
            elif optionSelected == 4:
                contact()
            elif optionSelected == 5:
                quit()
            else:
                print("Wrong option Selected")
        except ValueError:
            continue
        else:
            wishtoContinue = confirm_ExitApplication()
            if wishtoContinue:
                continue
            else:
                error_entry = False
                quit()


def suiteFeatures():
    print("  ***************************  SUITE FEATURES  *************************** ")
    print("  ------------------------------------------------------------------------ ")
    print("  * ENJOY A PALETTE OF SUITE FEATURES AND FINISHES THAT ARE AS STYLISH AS THEY ARE PRACTICAL")
    print("  * ALL ENSUITES WITH GLASS WALK-IN SHOWERS")
    print("  * BATHROOMS WITH TUB SURROUND, VANITY AND CONTEMPORARY TILES")
    print("  * BELL FIBER OPTICS AND ROGERS CAT6 CONNECTION IN EACH SUITE")
    print("  * CUSTOM ROLLER SHADES ON EVERY SUITE WINDOW")
    print("  * HIGH-END LIGHTING FIXTURES THROUGHOUT")
    print("  * INDIVIDUALLY CLIMATE CONTROLLED SUITE WITH HEATING AND AIR CONDITIONING")
    print("  * IN-SUITE LAUNDRY")
    print("  * LARGE BALCONIES")
    print("  * LAMINATE AND CERAMICS TILES THROUGHOUT")
    print("  * MODERN CERAMIC TILES IN BATHROOM, KITCHEN AND ENTRANCE")
    print("  * SIX ENERGY EFFICIENT APPLIANCES")
    print("  * SMARTONE TECHNOLOGY")
    print("  * SMART LOCKS")

def contact():
    print("    FOR INFORMATION &  ")
    print("    RENTAL INQUIRES CONTACT: ")
    print("    EMAIL: rentals@greencorp.COM ")
    print("    TEL: 123-456-7890 ")




