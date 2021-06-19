import os
import sys


class Mforensics:

    def __init__(self, filename):
        self.file = filename
        # MENU options
        self.menu_options =  list(x for x in range(4))

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

    def menu(self):
        # MENU
        print("\n*********** MENU ************\n" \
              "1. OS Info\n" \
              "2. Hashes/Passwords\n" \
              "3. Process List\n" \
              "0. Quit\n"\
              "*****************************\n")

        try:
            self.option = int(input("Choose the option from menu: "))
        except ValueError:
            print("Are you entering the correct option?")
            self.menu()

        return self.option

    def proc(self, option):
        if option == 0:
            sys.exit()

        if option == 1:
            # get os information
            os.system(f"python3 vol.py -f {self.file} -q windows.info")

        if option == 2:
            print("*****************************\n" \
                  "1. Hash Dump\n" \
                  "2. Cache Dump\n" \
                  "3. Lsa Dump\n"\
                  "4. Menu\n"
                  "*****************************\n")
            alpha = int(input("Enter the choice: "))
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
            print("*****************************\n" \
                  "1. PsTree\n" \
                  "2. PsList\n" \
                  "3. PsScan\n"\
                  "4. Menu\n"
                  "*****************************\n")
            alpha = int(input("Enter the choice: "))
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

        if option not in self.menu_options:
            print("Please choose the option from menu")


if __name__ == '__main__':

    if len(sys.argv) != 2:
        sys.exit("Usage: python3 analysis.py <filename/filepath>")

    file_path = os.path.realpath(sys.argv[1])

    if os.path.exists("/opt") and os.getuid() != 0:
        sys.exit("Not running as sudo. Either run as sudo or change the default installation path.")

    print("""\n\n                                     MEMORY FORENSICS BY
     __  .__   __.  _______  __  .__   __.  __  .___________.____    ____    __        ______     ______   .______   
    |  | |  \ |  | |   ____||  | |  \ |  | |  | |           |\   \  /   /   |  |      /  __  \   /  __  \  |   _  \  
    |  | |   \|  | |  |__   |  | |   \|  | |  | `---|  |----` \   \/   /    |  |     |  |  |  | |  |  |  | |  |_)  | 
    |  | |  . `  | |   __|  |  | |  . `  | |  |     |  |       \_    _/     |  |     |  |  |  | |  |  |  | |   ___/  
    |  | |  |\   | |  |     |  | |  |\   | |  |     |  |         |  |       |  `----.|  `--'  | |  `--'  | |  |      
    |__| |__| \__| |__|     |__| |__| \__| |__|     |__|         |__|       |_______| \______/   \______/  | _| 
                                                                                                                """)

    m = Mforensics(file_path)

    check = m.req()

    if os.path.exists("vol.py"):
        while True:
            option = m.menu()
            print()
            m.proc(option)
    else:
        sys.exit("\nError, vol.py is not found in the entered path.")
