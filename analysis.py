import os
import sys

class Mforensics:
   
    def __init__(self, filename):
        self.file = filename

    
    def req(self):
        #ask if the user have volatility or not
        check = input("Is volatility installed? (y/n): ")
        
        #get the path of volatility if user has it
        if check == 'y':
            dir = input("Enter the full path (where vol.py is located):")
            os.chdir(dir)
            return dir
        
        #install volatility if user doesn't have it
        elif check == 'n':
            #you can change install path as per your wish
            dir = "/opt/"
            os.chdir(dir)
            os.system("git clone https://github.com/volatilityfoundation/volatility3.git")
            os.chdir("volatility3")
            print("\n\nVolatility setup done!!")
            return os.path.join(dir, "volatility3")

        else:
            sys.exit("Error, did you choose the correct option?")


    def menu(self):
        #MENU
        print("\n**** MENU ****\n"\
              "1. OS Info\n"\
              "2. Hashes/Passwords\n"\
              "3. Process List\n"\
              "0. Quit\n")

        #TODO: implement control to make sure user put correct value
        option = int(input("Choose the option from menu: "))

        return option


    def proc(self, option):
        if option == 0:
            sys.exit()

        if option == 1:
            #get os information 
            os.system(f"python3 vol.py -f {self.file} -q windows.info")
            
        if option == 2:
            print("********************\n"\
                    "1. Hash Dump\n"\
                    "2. Cache Dump\n"\
                    "3. Lsa Dump\n")                       
            alpha = int(input("Enter the choice: "))
            if alpha == 1:
                #grab common windows hashes (SAM+SYSTEM)
                os.system(f"python3 vol.py -f {self.file} -q windows.hashdump")
            if alpha == 2:
                #grab domain cache hashes inside the registery
                os.system(f"python3 vol.py -f {self.file} -q windows.cachedump")
            if alpha == 3:
                #grab lsa secrets
                os.system(f"python3 vol.py -f {self.file} -q windows.lsadump")

        if option == 3:
            print("********************\n"\
                  "1. PsTree\n"\
                  "2. PsList\n"\
                  "3. PsScan\n")
            alpha = int(input("Enter the choice: "))
            if alpha == 1:
                #get processes tree (won't get hidden processes)
                os.system(f"python3 vol.py -f {self.file} -q windows.pstree")
            if alpha == 2:
                #get process list (EPROCESSES)
                os.system(f"python3 vol.py -f {self.file} -q windows.pslist")
            if alpha == 3:
                #get hidden process list (malware)
                os.system(f"python3 vol.py -f {self.file} -q windows.psscan")


if len(sys.argv) != 2:
        sys.exit("Usage: python3 analysis.py <filename/filepath>")

file_path = os.path.realpath(sys.argv[1])

m = Mforensics(file_path)

check = m.req()

if os.path.exists("vol.py") is True: 
    while True:
        option = m.menu()
        print()
        m.proc(option)
else:
    sys.exit("\nError, vol.py is not found in the entered path.")
