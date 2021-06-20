import os
import sys
from loader import Loader

class Mforensics:

    def __init__(self, filename):
        self.file = filename
        self.yara_file = "malware_rules.yar"
        # MENU options
        self.menu_options =  list(x for x in range(11))


    # check the volatility requirements
    def req(self):
        # ask if the user have volatility or not
        self.check = input("Is volatility3 installed? (y/n): ")

        # get the path of volatility if user has it
        if self.check == 'y':
            self.dir = input("Enter the full path (where vol.py is located): ")
            os.chdir(self.dir)
            return self.dir

        # install volatility if user doesn't have it
        elif self.check == 'n':
            # you can change install path as per your wish
            self.dir = "/opt/"
            os.chdir(self.dir)
            os.system("git clone https://github.com/volatilityfoundation/volatility3.git")
            os.chdir("volatility3")
            print("\nVolatility setup done!!")
            print(f"Volatility installed at {os.path.join(self.dir, 'volatility3')}")
            return os.path.join(self.dir, "volatility3")

        else:
            sys.exit("Error, did you choose the correct option?")


    # prints the menu
    def menu(self):
        # MENU
        print("\n\n------------------- MENU --------------------\n" 
                "1. OS Info            2.  Hashes/Passwords\n" 
                "3. Process List       4.  CMDLine\n"
                "5. NetScan            6.  Registry\n"
                "7. File Scan          8.  MalFind\n"
                "9. Yara Scan          10. More\n"
                "0. Quit\n"
              "-------------------------------------------------\n\n")
        try:
            self.option = int(input("Choose the option from menu: "))
        except ValueError:
            print("Are you entering the correct option?")
            self.menu()

        return self.option


    # function to get alpha input and checks any ValueErrors
    def get_alpha(self):
        try:
            alpha = int(input("Enter the choice: "))
        except ValueError:
            print("Are you entering the correct choice?")
        return alpha


    # function checks or setup yara rules for malware
    def yara(self, choice):
        if choice == 'y':
            if os.path.exists(self.yara_file):
                return True

        if choice == 'n':
            # check if we are in volatility3 directory
            if os.path.exists("volatility3"):
                os.system("wget https://gist.githubusercontent.com/andreafortuna/"
                          "29c6ea48adf3d45a979a78763cdc7ce9/raw/"
                          "4ec711d37f1b428b63bed1f786b26a0654aa2f31/malware_yara_rules.py")
                os.system("mkdir rules")
                os.system("python malware_yara_rules.py")
                print("Yara rule file created!")
                if os.path.exists(self.yara_file):
                    return True
                else:
                    print(f"Check if '{self.yara_file}' file exists in volatility3")
                    return False
            else:
                print("Check the directory. You must be in 'volatility3' dir")
                return False


    # function prints out the mini menus
    # return the option and alpha
    def func(self, option):
        if option == 0:
            return option, 0
        if option == 1:
            return option, 0
        if option == 2:
            print("*****************************\n"
                    "1. Hash Dump\n" 
                    "2. Cache Dump\n" 
                    "3. Lsa Dump\n" 
                    "4. Menu\n"
                  "*****************************\n")
            alpha = self.get_alpha()
            return option, alpha
        if option == 3:
            print("*****************************\n"
                    "1. PsTree\n"
                    "2. PsList\n" 
                    "3. PsScan\n" 
                    "4. Menu\n"
                  "*****************************\n")
            alpha = self.get_alpha()
            return option, alpha
        if option == 4:
            return option, 0
        if option == 5:
            print("*****************************\n" 
                    "1. Netscan\n" 
                    "2. Netstat\n" 
                    "3. Menu\n"
                  "*****************************\n")
            alpha = self.get_alpha()
            return option, alpha
        if option == 6:
            print("*****************************\n" 
                    "1. HiveScan\n" 
                    "2. HiveList\n" 
                    "3. PrintKey\n"
                    "4. Menu\n"
                  "*****************************\n")
            alpha = self.get_alpha()
            return option, alpha
        if option == 7:
            print("*****************************\n"
                    "1. File Scan\n"
                    "2. File Dump\n"
                    "3. Menu\n"
                  "*****************************\n")
            alpha = self.get_alpha()
            return option, alpha
        if option == 8:
            return option, 0
        if option == 9:
            return option, 0


    # main function; run all the processes
    def proc(self, option, alpha):
        if option == 0:
            sys.exit()

        if option == 1:
            # get os information
            os.system(f"python3 vol.py -f {self.file} -q windows.info")

        if option == 2:
            if alpha == 1:
                # grab common windows hashes (SAM+SYSTEM)
                os.system(f"python3 vol.py -f {self.file} -q windows.hashdump")
            elif alpha == 2:
                # grab domain cache hashes inside the registry
                os.system(f"python3 vol.py -f {self.file} -q windows.cachedump")
            elif alpha == 3:
                # grab lsa secrets
                os.system(f"python3 vol.py -f {self.file} -q windows.lsadump")
            elif alpha == 4:
                # back to menu
                return
            else:
                print("Oops! something went wrong!")
                return

        if option == 3:
            if alpha == 1:
                # get processes tree (won't get hidden processes)
                os.system(f"python3 vol.py -f {self.file} -q windows.pstree")
            elif alpha == 2:
                # get process list (EPROCESSES)
                os.system(f"python3 vol.py -f {self.file} -q windows.pslist")
            elif alpha == 3:
                # get hidden process list (malware)
                os.system(f"python3 vol.py -f {self.file} -q windows.psscan")
            elif alpha == 4:
                # back to menu
                return
            else:
                print("Oops! something went wrong!")
                return

        if option == 4:
            # display process command-line arguments.
            # Anything suspicious was executed?
            os.system(f"python3 vol.py -f {self.file} -q windows.cmdline")

        if option == 5:
            if alpha == 1:
                os.system(f"python3 vol.py -f {self.file} -q windows.netscan")
            elif alpha == 2:
                os.system(f"python3 vol.py -f {self.file} -q windows.netstat")
            elif option == 3:
                return
            else:
                print("Oops! Something went wrong")
            
        if option == 6:
            if alpha == 1:
                os.system(f"python3 vol.py -f {self.file} -q windows.registry.hivescan")
            elif alpha == 2:
                # list roots
                os.system(f"python3 vol.py -f {self.file} -q windows.registry.hivelist")
            elif alpha == 3:
                os.system(f"python3 vol.py -f {self.file} -q windows.registry.printkey")
            elif alpha == 4:
                return
            else:
                print("Oops! Something went wrong")

        if option == 7:
            if alpha == 1:
                os.system(f"python3 vol.py -f {self.file} -q windows.filescan")
            elif alpha == 2:
                os.system(f"python3 vol.py -f {self.file} -q windows.dumpfiles")
            elif alpha == 3:
                return
            else:
                print("Oops! Something went wrong")

        if option == 8:
            # Find hidden and injected code, [dump each suspicious section]
            os.system(f"python3 vol.py -f {self.file} -q windows.malfind")

        if option == 9:
            choice = input(f"Do you have file '{self.yara_file}' setup?(y/n): ").lower()
            alpha = self.yara(choice)
            if alpha:
                #if os.path.exists("malware_rules.yar"):
                os.system(f"python3 vol.py -f {self.file} -q yarascan.yarascan --yara-file {self.yara_file}")
                #else:
                    #print("Yara rule file doesn't exist in current directory")
                    #print("Do you have 'malware_rules.yar' in some other dir?")
                    #print("Move it in 'volatility3' directory")
            if alpha is False:
                return

        if option == 10:
            pass

        if option not in self.menu_options:
            print("Please choose the option from menu")