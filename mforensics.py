import os
import sys

from halo import Halo
from termcolor import cprint


class Mforensics:

    def __init__(self, filename):
        self.file = filename
        # MENU options
        self.menu_options =  list(x for x in range(12))
        # Spinner
        self.halo = Halo("Loading...", spinner="dots", color="green")


    # check the volatility requirements
    def req(self):
        # ask if the user have volatility or not
        self.check = input("Is volatility3 installed? (y/n): ")

        # get the path of volatility if user has it
        if self.check == 'y':
            self.dir = input("Enter the full path (where vol.py is located): ")
            os.chdir(self.dir)
            if os.path.exists("volatility3"):
                return self.dir
            else:
                print("No volatility3 directory exists")

        # install volatility if user doesn't have it
        elif self.check == 'n':
            # you can change install path as per your wish
            self.dir = "/opt/"
            os.chdir(self.dir)
            if os.path.exists("volatility3") == False:
                print("\033[01m", "\033[31m\n!Cloning volatility3\033[0m")
                self.halo.start()
                os.system("git clone -q https://github.com/volatilityfoundation/volatility3.git")
                self.halo.stop()
                os.chdir("volatility3")
                print(u"\033[92m\u2714\033[0m \033[1mDone!\033[01m")
                print(f"\nVolatility3 cloned in {os.path.join(self.dir, 'volatility3')}")
                return os.path.join(self.dir, "volatility3")
            else:
                os.chdir("volatility3")
                return os.path.join(self.dir, "volatility3")

        else:
            sys.exit("Error, did you choose the correct option?")


    # prints the menu
    def menu(self):
        # MENU
        cprint("\n\n------------------------- MENU --------------------------\n" 
                "1.  OS Info                    2.  Hashes/Passwords\n" 
                "3.  Process List               4.  CMDLine\n"
                "5.  NetScan                    6.  Registry\n"
                "7.  File Scan                  8.  MalFind\n"
                "9.  Scan shady processes       10. Change memory dump\n"
                "11. More\n"
                "0.  Quit\n"
              "---------------------------------------------------------\n\n", "cyan", attrs=["bold"])
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


    # Setup malware hunt
    def malhunt(self):
        if os.path.exists("volatility") == False:
            print("\033[01m", "\033[31m\n!Setting up volatility\033[0m")
            self.halo.start()
            os.system("git clone -q https://github.com/volatilityfoundation/volatility.git")
            os.chdir("volatility")
            self.halo.stop()
            os.system("python2 -W ignore setup.py install > /dev/null")
            print(u"\n\033[92m\u2714\033[0m \033[1mSetup success\033[01m")

        if os.path.exists("malhunt") == False:
            print("\033[01m", "\033[31m\n!Setting up Malware Hunt\033[0m")
            if os.popen(f"which pip2").read().rstrip() == "":
                os.system("curl https://bootstrap.pypa.io/pip/2.7/get-pip.py --output get-pip.py")
                self.halo.start()
                os.system("python2 -W ignore get-pip.py > /dev/null")
                os.system("rm -f get-pip.py")
                # installing pip2 breaks pip3; restoring pip3
                os.system("DEBIAN_FRONTEND=noninteractive apt-get remove -qqy python3-pip > /dev/null")
                os.system("DEBIAN_FRONTEND=noninteractive apt-get install -qqy python3-pip > /dev/null")
                self.halo.stop()
            cprint(f"A little longer...", attrs=["bold"])
            self.halo.start()
            os.system("pip2 --no-python-version-warning -q install requests")
            os.system("git clone -q https://github.com/elweux/malhunt.git")
            self.halo.stop()
            print(u"\033[92m\u2714\033[0m \033[1mSetup success\033[01m")

        print("\033[01m", "\033[31m\n!Checking for dependencies\033[0m")
        dep = []
        if os.popen(f"which clamscan").read().rstrip() == "":
            print(u"\033[91m\u2717\033[0m \033[1mClamscan not found\033[01m")
            dep.append("clamscan")
        else:
            print(u"\033[92m\u2714\033[0m \033[1mClamscan found\033[01m")
            return True

        if len(dep) != 0:
            try:
                a = input("\nProceed with installing missing dependencies?(y/n): ").lower()
            except Exception:
                print("\n Oops! Something went wrong")

        if a == "y" or a == "yes":
            try:
                print("\033[01m", "\033[31m\n!Installing camscan\033[0m")
                self.halo.start()
                os.system("DEBIAN_FRONTEND=noninteractive apt-get install -qqy clamav clamav-daemon > /dev/null")
                self.halo.stop()
            except Exception:
                print(u"\033[91m\u2714\033[0m \033[1mInstallation failed\033[01m")
                print("** Try installing manually")

        if a == "n" or a == "no":
            return False

        return True

    # function prints out the mini menus
    # return the option and alpha
    def func(self, option):
        if option == 0:
            return option, 0
        if option == 1:
            return option, 0
        if option == 2:
            cprint("\n*****************************\n"
                    "1. Hash Dump\n" 
                    "2. Cache Dump\n" 
                    "3. Lsa Dump\n" 
                    "4. Menu\n"
                  "*****************************\n", "cyan", attrs=["bold"])
            alpha = self.get_alpha()
            return option, alpha
        if option == 3:
            print("\n*****************************\n"
                    "1. PsTree\n"
                    "2. PsList\n" 
                    "3. PsScan\n" 
                    "4. Menu\n"
                  "*****************************\n", "cyan", attrs=["bold"])
            alpha = self.get_alpha()
            return option, alpha
        if option == 4:
            return option, 0
        if option == 5:
            print("\n*****************************\n" 
                    "1. Netscan\n" 
                    "2. Netstat\n" 
                    "3. Menu\n"
                  "*****************************\n", "cyan", attrs=["bold"])
            alpha = self.get_alpha()
            return option, alpha
        if option == 6:
            print("\n*****************************\n" 
                    "1. HiveScan\n" 
                    "2. HiveList\n" 
                    "3. PrintKey\n"
                    "4. Menu\n"
                  "*****************************\n", "cyan", attrs=["bold"])
            alpha = self.get_alpha()
            return option, alpha
        if option == 7:
            print("\n*****************************\n"
                    "1. File Scan\n"
                    "2. File Dump\n"
                    "3. Menu\n"
                  "*****************************\n", "cyan", attrs=["bold"])
            alpha = self.get_alpha()
            return option, alpha
        if option == 8:
            return option, 0
        if option == 9:
            return option, 0
        if option == 10:
            return option, 0
        if option == 11:
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
            # check if we are in volatility3 directory
            if os.path.exists("volatility3"):
                try:
                    alpha = input("\nIs malware hunt setup?(y/n) [choose n if not sure]: ").lower()
                    if alpha == 'n' or alpha == 'no':
                        bool = self.malhunt()
                        if bool:
                            print()
                            os.system(f"python2 malhunt/malhunt.py {self.file}")
                        else:
                            return
                    if alpha == 'y' or alpha == 'yes':
                        if os.path.exists("malhunt"):
                            print()
                            os.system(f"python2 malhunt/malhunt.py {self.file}")
                        else:
                            print("\nCan't find 'malhunt' directory. Please choose 'n' if not sure.")
                            return
                except Exception:
                        print("\nOops! something went wrong")
            else:
                print("\nNot in 'volatility3' directory. Changing directories now...")
                os.chdir(self.dir)
                print("Success")
                print("Continue with the setup...")
                bool = self.malhunt()
                if bool:
                    print()
                    os.system(f"python2 malhunt/malhunt.py {self.file}")
                else:
                    return

        if option == 10:
            try:
                alpha = input("Enter the full file(memory dump) path: ")
                self.file = os.path.realpath(alpha)
            except Exception:
                print("\nException occurred. Check entered path.")

        if option == 11:
            pass

        if option not in self.menu_options:
            print("Please choose the option from menu")