#############################################################################################
#  FILE :  Utils.py                                                                #
#          Provides commons functions                                              #
#          Quit_Application(), confirm_ExitApplication()                           #
#############################################################################################

def Quit_Application():
    print("************************************************************************")
    print("Thank you for visiting us today. Good Day! ")
    quit()


def confirm_ExitApplication():
    error_entry = True
    while error_entry:
        try:
            wishtoContinue = input("Do you wish to continue Yes / No: ")
            if wishtoContinue.upper() == "YES":
                return True
            elif wishtoContinue.upper() == "NO":
                return False
            else:
                print("Wrong Option entered !. Please try again. ")
                continue
        except ValueError:
            continue
        else:
            error_entry = False
    return True


