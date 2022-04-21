#############################################################################################
#  FILE :  main.py                                                                #
#          Entry file for the project                                             #
#############################################################################################

from Utils import confirm_ExitApplication
from apartmentSearch import search
from login import login, signInPage, signUpPage


def greenCorp_main():
    print("************************************************************************")
    print("              Welcome to GreenCorp Rentals                              ")
    print("************************************************************************")
    print("                                                                        ")
    print("(1) Sign-IN ")
    print("(2) Sign-UP ")
    print("(3) Apartment Search ")

    error_entry = True

    while error_entry:
        try:
            optionSelected = int(input(" Please Choose Your Option  : "))
            if optionSelected == 1:
                signInPage()
            elif optionSelected == 2:
                signUpPage()
            elif optionSelected == 3:
                search()
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


if __name__ == "__main__":
    greenCorp_main()
