import os
import re
import sys
import time

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
        self.check = input("\nIs volatility installed? (y/n): ")

        # get the path of volatility if user has it
        if self.check == 'y':
            self.dir = input("\nEnter the full path (where vol.py is located): ")
            os.chdir(self.dir)
            if os.path.exists("volatility"):
                return self.dir
            else:
                print("No volatility directory exists")

        # install volatility if user doesn't have it
        elif self.check == 'n':
            # you can change install path as per your wish
            self.d = "/opt/"
            os.chdir(self.d)
            if os.path.exists("volatility") == False:
                print("\033[01m", "\033[31m\n!Cloning volatility\033[0m")
                self.halo.start()
                os.system("git clone -q https://github.com/volatilityfoundation/volatility.git")
                self.halo.stop()
                os.chdir("volatility")
                print(u"\033[92m\u2714\033[0m \033[1mDone!\033[01m")
                print(f"\nvolatility cloned in {os.path.join(self.d, 'volatility')}")
                print("\033[01m", "\033[31m\n!Installing/Checking dependencies\033[0m")
                if os.popen(f"which curl").read().rstrip() == "":
                    os.system("DEBIAN_FRONTEND=noninteractive apt-get remove -qqy curl > /dev/null")
                if os.popen(f"which pip2").read().rstrip() == "":
                    try:
                        os.system("curl https://bootstrap.pypa.io/pip/2.7/get-pip.py --output get-pip.py")
                        self.halo.start()
                        os.system("python2 -W ignore get-pip.py > /dev/null")
                        os.system("rm -f get-pip.py")
                        # installing pip2 breaks pip3; restoring pip3
                        os.system("DEBIAN_FRONTEND=noninteractive apt-get remove -qqy python3-pip > /dev/null")
                        os.system("DEBIAN_FRONTEND=noninteractive apt-get install -qqy python3-pip > /dev/null")
                        self.halo.stop()
                    except Exception:
                        sys.exit("Error, occured")
                try:
                    self.halo.start()
                    os.system("pip2 --no-python-version-warning -q install distorm3 pycrypto")
                    self.halo.stop() 
                    print(u"\033[92m\u2714\033[0m \033[1mdistorm3\033[01m")
                    self.halo.start()
                    time.sleep(1.5)
                    self.halo.stop() 
                    print(u"\033[92m\u2714\033[0m \033[1mpycrypto\033[01m")
                except Exception:
                    print("\nSome exception occured. Still continuing...")
                if os.popen(f"which yara").read().rstrip() == "": 
                    try:
                        self.halo.start()
                        os.system("DEBIAN_FRONTEND=noninteractive apt-get install -qqy yara > /dev/null")
                        self.halo.stop() 
                        print(u"\033[92m\u2714\033[0m \033[1myara installed\033[01m")
                        os.system("ln -s /usr/local/lib/python2.7/dist-packages/usr/lib/libyara.so /usr/lib/libyara.so")
                    except Exception:
                        print("\nException occured. Install yara manually")
                else:
                    print(u"\033[92m\u2714\033[0m \033[1myara found\033[01m")
                    os.system("ln -s /usr/local/lib/python2.7/dist-packages/usr/lib/libyara.so /usr/lib/libyara.so")
                self.dir = os.path.join(self.d, "volatility")
                return self.dir
            else:
                os.chdir("volatility")
                self.dir = os.path.join(self.d, "volatility")
                return self.dir

        else:
            sys.exit("Error, did you choose the correct option?")
    
    
    # get the profile of memory dump
    def get_profile(self):
        #if os.path.exists("vol.py"):
        if os.path.exists("imageinfo.txt"):
            os.system("rm -f imageinfo.txt")
            print(f"\nGetting profile info of memory image...")
            os.system(f"python2 vol.py -f {self.file} imageinfo --output-file=imageinfo.txt ")
        else:
            print(f"\nGetting profile info of memory image...")
            os.system(f"python2 vol.py -f {self.file} imageinfo --output-file=imageinfo.txt ")
        
        if os.path.exists("imageinfo.txt"):
            with open("imageinfo.txt") as fd:
                for line in fd:
                    match = re.findall(r"Win[^,]+x[23468][_\d]*", line)
                    if match:
                        profiles = match
        try:
            print("\033[01m", "\033[92m\n** Profiles Found **\n\033[0m")
            for pf in profiles:
                print(pf, end=" ")
            self.profile = profiles[0]
            print(f"\nProfile Using: \033[92m{self.profile}\033[0m")
            return self.profile
        except Exception:
            print("\nCouldn't find profile")
            sys.exit()


    # prints the menu
    def menu(self):
        # MENU
        cprint("\n\n------------------------- MENU --------------------------\n" 
                "1.  OS Info                    2.  Hashes/Passwords\n" 
                "3.  Process List               4.  CMDLine\n"
                "5.  NetScan                    6.  Registry\n"
                "7.  File Scan                  8.  MalFind\n"
                "9.  Scan shady processes       10. Yara Scan\n"
                "11. Change memory dump\n"
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
    def malwarehunt(self):
        if os.path.exists("malwarehunt") == False:
            try:
                print("\033[01m", "\033[31m\n!Setting up volatility\033[0m")
                os.system("python2 -W ignore setup.py install > /dev/null")
                print(u"\n\033[92m\u2714\033[0m \033[1mSetup success\033[01m")
            except Exception:
                self.halo.fail("Setup failed")
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
            self.halo.start()
            time.sleep(1)
            self.halo.stop()
            cprint(f"A little longer...", attrs=["bold"])
            self.halo.start()
            os.system("pip2 --disable-pip-version-check -q install requests")
            os.system("git clone -q https://github.com/elweux/malwarehunt.git")
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
                print("\033[01m", "\033[31m\n!Installing camscan\033[0m")
                self.halo.start()
                os.system("DEBIAN_FRONTEND=noninteractive apt-get install -qqy clamav clamav-daemon > /dev/null")
                self.halo.stop()
            except Exception:
                print(u"\033[91m\u2717\033[0m \033[1mInstallation failed\033[01m")
                cprint("** Try installing manually **", attrs=["bold"])
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
            cprint("\n*****************************\n"
                    "1. PsTree\n"
                    "2. PsList\n" 
                    "3. PsScan\n" 
                    "4. Menu\n"
                  "*****************************\n", "cyan", attrs=["bold"])
            alpha = self.get_alpha()
            return option, alpha
        if option == 4:
            cprint("\n*****************************\n" 
                    "1. CmdLine\n" 
                    "2. Console History\n" 
                    "3. Menu\n"
                  "*****************************\n", "cyan", attrs=["bold"])
            alpha = self.get_alpha()
            return option, alpha
        if option == 5:
            cprint("\n*****************************\n" 
                    "1. Netscan\n" 
                    "2. TCP Connections\n" 
                    "3. Open Sockets\n"
                    "4. TCP Socket Objects\n"
                    "5. Menu\n"
                  "*****************************\n", "cyan", attrs=["bold"])
            alpha = self.get_alpha()
            return option, alpha
        if option == 6:
            cprint("\n*****************************\n" 
                    "1. HiveScan\n" 
                    "2. HiveList\n" 
                    "3. PrintKey\n"
                    "4. Menu\n"
                  "*****************************\n", "cyan", attrs=["bold"])
            alpha = self.get_alpha()
            return option, alpha
        if option == 7:
            return option, 0
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
            if os.path.exists("imageinfo.txt"):
                fd = open("imageinfo.txt")
                print(fd.read())
            else:
                # get os information
                os.system(f"python2 vol.py -f {self.file} imageinfo")

        if option == 2:
            if alpha == 1:
                # grab common windows hashes (SAM+SYSTEM)
                os.system(f"python2 vol.py --profile={self.profile} hashdump -f {self.file}")
            elif alpha == 2:
                # grab domain cache hashes inside the registry
                os.system(f"python2 vol.py --profile={self.profile} cachedump -f {self.file}")
            elif alpha == 3:
                # grab lsa secrets
                os.system(f"python2 vol.py --profile={self.profile} lsadump -f {self.file}")
            elif alpha == 4:
                # back to menu
                return
            else:
                print("Oops! something went wrong!")
                return

        if option == 3:
            if alpha == 1:
                # get processes tree (won't get hidden processes)
                os.system(f"python2 vol.py --profile={self.profile} pstree -f {self.file}")
            elif alpha == 2:
                # get process list (EPROCESSES)
                os.system(f"python2 vol.py --profile={self.profile} pslist -f {self.file}")
            elif alpha == 3:
                # get hidden process list (malware)
                os.system(f"python2 vol.py --profile={self.profile} psscan -f {self.file}")
            elif alpha == 4:
                # back to menu
                return
            else:
                print("Oops! something went wrong!")
                return

        if option == 4:
            # display process command-line arguments.
            # Anything suspicious was executed?
            if alpha == 1:
                os.system(f"python2 vol.py --profile={self.profile} cmdline -f {self.file}")
            elif alpha == 2:
                os.system(f"python2 vol.py --profile={self.profile} consoles -f {self.file}")
            elif alpha == 3:
                return
            else:
                print("Oops! Something went wrong")

        if option == 5:
            if alpha == 1:
                os.system(f"python2 vol.py -f {self.file} netscan --profile={self.profile}")
            elif alpha == 2:
                #TCP Connectons
                os.system(f"python2 vol.py -f {self.file} connscan --profile={self.profile}")
            elif alpha == 3:
                #Open Sockets
                os.system(f"python2 vol.py -f {self.file} sockscan --profile={self.profile}")
            elif alpha == 4:
                #TCP Socket Ojbects
                os.system(f"python2 vol.py -f {self.file} sockets --profile={self.profile}")
            elif option == 5:
                return
            else:
                print("Oops! Something went wrong")
            
        if option == 6:
            if alpha == 1:
                os.system(f"python2 vol.py -f {self.file} hivescan --profile={self.profile}")
            elif alpha == 2:
                # list roots
                os.system(f"python2 vol.py -f {self.file} hivelist --profile={self.profile}")
            elif alpha == 3:
                os.system(f"python2 vol.py -f {self.file} printkey --profile={self.profile}")
            elif alpha == 4:
                return
            else:
                print("Oops! Something went wrong")

        if option == 7:
            os.system(f"python2 vol.py -f {self.file} filescan --profile={self.profile}")

        if option == 8:
            # Find hidden and injected code, [dump each suspicious section]
            os.system(f"python2 vol.py -f {self.file} malfind --profile={self.profile}")

        if option == 9:
            # check if we are in volatility directory
            if os.path.exists("volatility"):
                if os.path.exists("malwarehunt"):
                    try:
                        os.system(f"python2 malwarehunt/malhunt.py {self.file}")
                    except Exception:
                        os.system("rm -fr malwarehunt")
                        bool = self.malwarehunt()
                        if bool:
                            print()
                            os.system(f"python2 malwarehunt/malhunt.py {self.file}")
                        else:
                            print("\nCouldn't run malware hunt.")
                            print("Try removing 'volatility' directory and running script")
                            return
                else:
                    bool = self.malwarehunt()
                    if bool:
                        print()
                        os.system(f"python2 malwarehunt/malhunt.py {self.file}")
                    else:
                        return
            else:
                print("\nNot in 'volatility' directory. Changing directories now...")
                self.halo.start("Changing directory...")
                time.sleep(1)
                os.chdir(self.dir)
                self.halo.stop()
                if os.path.exists("volatility"):
                    print("\033[01m", "\033[92m\n** Success **033[0m")
                    print("Continue with the setup...")
                    bool = self.malwarehunt()
                    if bool:
                        print()
                        os.system(f"python2 malwarehunt/malhunt.py {self.file}")
                    else:
                        return
                else:
                    print("\033[91m\nError! Change into volatility directory and try again.\033[0m")
                    return

        if option == 10:
            if os.popen(f"which yara").read().rstrip() == "":
                try:
                    print("\033[41myara not installed...\033[00m")
                    self.halo.start("Installing yara...")
                    os.system("DEBIAN_FRONTEND=noninteractive apt-get install -qqy yara > /dev/null")
                    self.halo.stop()
                    print(u"\n\033[92m\u2714\033[0m \033[1mYara installed\033[01m")
                except Exception:
                    print(u"\033[91m\u2717\033[0m \033[1mInstallation failed\033[01m")
                    print("Install manually to proceed: apt install yara ")
                    return
                if os.popen(f"which yara").read().rstrip() == "":
                    print(u"\033[91m\u2717\033[0m \033[1myara not found\033[01m")
                    print("Install manually to proceed: apt install yara")
                    return
            if os.path.exists("volatility"):
                if not os.path.exists("malware_rules.yar"):
                    if os.path.exists("rules"):
                        os.system("rm -fr rules")
                    print("\033[01m", "\033[31m\n!Setting up yara rules\033[0m")
                    os.mkdir("rules")
                    os.system("git clone -q https://gist.github.com/29c6ea48adf3d45a979a78763cdc7ce9.git yara-rules")
                    os.system("python3 yara-rules/malware_yara_rules.py")
                    os.system("rm -fr yara-rules")
                    print(u"\n\033[92m\u2714\033[0m \033[1myara rules setup done\033[01m")
                self.halo.start("Running yara scan...")
                os.system(f"yara -weg malware_rules.yar {self.file}")
                self.halo.stop()
            else:
                print("\nNot in 'volatility' directory. Changing directories now...")
                self.halo.start("Changing directory...")
                time.sleep(1)
                os.chdir(self.dir)
                self.halo.stop()
                if os.path.exists("volatility"):
                    print("\033[01m", "\033[92m\n** Success **033[0m")
                    if not os.path.exists("malware_rules.yar"):
                        if os.path.exists("rules"):
                            os.system("rm -fr rules")
                        print("\033[01m", "\033[31m\n!Setting up yara rules\033[0m")
                        os.mkdir("rules")
                        os.system("git clone -q https://gist.github.com/29c6ea48adf3d45a979a78763cdc7ce9.git yara-rules")
                        os.system("python3 yara-rules/malware_yara_rules.py")
                        print(u"\n\033[92m\u2714\033[0m \033[1myara rules setup done\n\033[01m")
                    self.halo.start("Running yara scan...")
                    os.system(f"yara -weg malware_rules.yar {self.file} > yara-output.txt")
                    self.halo.stop()
                    print()
                    os.system("cat yara-output.txt")
                    os.system("rm -f yara-output.txt")
                else:
                    print("\033[91m\nError! Change into volatility directory and try again.\033[0m")
                    return
                
        if option == 11:
            try:
                alpha = input("Enter the full file(memory dump) path: ")
                if os.path.exists(alpha):
                    self.file = os.path.realpath(alpha)
                    print("\033[01m", "\033[92m\n*** Memory dump change successful ***\033[0m")
                    print("\nGetting profile of new memory image")
                    self.get_profile()
                else:
                    raise Exception("File/directory not found")
            except Exception:
                print("\033[01m", "\033[91m\n*** Exception occurred. Check entered path ***\033[0m")
            
            
        if option not in self.menu_options:
            print("Please choose the option from menu")
