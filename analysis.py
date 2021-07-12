import os
import sys

if __name__ == '__main__':

    if len(sys.argv) != 1:
        sys.exit("Usage: python3 analysis.py")

    if os.path.exists("/opt") and os.getuid() != 0:
        sys.exit("Not running as sudo. Either run as sudo or change the default installation path.")

    if os.popen(f"which pip3").read().rstrip() == "":
        print("\033[41mpip3 not installed...\033[00m")
        try:
            print("\nInstalling pip3... Please wait")
            os.system("DEBIAN_FRONTEND=noninteractive apt-get install -qqy python3-pip > /dev/null")
            print(u"\033[92m\u2714\033[0m \033[1mpip3 installed\033[01m")
        except Exception:
            print("An exception occurred. Try installing manually.")
            sys.exit()

    try:
        os.system("pip3 --disable-pip-version-check -q install halo")
    except Exception:
        print(u"\u2717 \033[1mCouldn't install halo\033[01m")
        print("\033[41m\nRun pip3 install halo manually\033[00m")
        print("\nAn exception occurred")
        sys.exit()

    from mforensics import Mforensics

    print("""\n\n                           MEMORY FORENSICS BY
        _       _____       _ __           __                
       (_)___  / __(_)___  (_) /___  __   / /___  ____  ____ 
      / / __ \/ /_/ / __ \/ / __/ / / /  / / __ \/ __ \/ __ \.
     / / / / / __/ / / / / / /_/ /_/ /  / / /_/ / /_/ / /_/ /
    /_/_/ /_/_/ /_/_/ /_/_/\__/\__, /  /_/\____/\____/ .___/ 
                              /____/                /_/       
                                                            """)

    file = input("Enter the full file(memory dump) path: ")
    file_path = os.path.realpath(file)

    mem = Mforensics(file_path)

    # check volatility requirements
    mem.req()
    # setting up memory image profile
    mem.get_profile()
    
    if os.path.exists("vol.py"):
        while True:
            option = mem.menu()
            print()
            process = mem.func(option)
            choice, alpha = process[0], process[1]
            mem.proc(choice, alpha)
            
    else:
        sys.exit("\nError, vol.py is not found in the entered path.")
