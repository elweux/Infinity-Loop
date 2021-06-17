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
        
        #install volatility if user doesn't have it
        elif check == 'n':
            #you can change install path as per your wish
            dir = "/opt/"
            os.chdir(dir)
            os.system("git clone https://github.com/volatilityfoundation/volatility3.git")
            os.chdir("volatility3")
            print("\n\nVolatility setup done!!")

        else:
            sys.exit("Error, did you choose the correct option?")


    def menu(self):
        #MENU
        print("\n\n**** MENU ****\n"\
              "1. OS Info\n"\
              "2. Hashes/Passwords\n"\
              "3. Process List\n")

        #TODO: implement control to make sure user put correct value
        option = int(input("Choose the option from menu: "))

        return option


    def process(self, option):
        check = os.path.exists("vol.py")
        
        if check == True:
            if option == 1:
                #get os information 
                os.system(f"python3 vol.py -f {self.file} -q windows.info")
            if option == 2:
                #grab common windows hashes (SAM+SYSTEM)
                os.system(f"python3 vol.py -f {self.file} -q windows.hashdump")
            if option == 3:
                #get processes tree (won't get hidden processes)
                os.system(f"python3 vol.py -f {self.file} -q windows.pstree")

        else:
            sys.exit("Check your path")


if len(sys.argv) != 2:
        sys.exit("Usage: python3 analysis.py <filename/filepath>")

file_path = os.path.realpath(sys.argv[1])

m = Mforensics(file_path)

m.req()
option = m.menu()
print()
m.process(option)
