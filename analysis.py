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
            a = input("\nInstall pip3?(y/n): ").lower()
            if a == "y" or a == "yes":
                os.system("DEBIAN_FRONTEND=noninteractive apt-get install -qqy python3-pip > /dev/null")
            elif a == "n" or a == "no":
                sys.exit("Exiting...")
            else:
                print("Choose y/n only")
        except Exception:
            print("An exception occurred")
            sys.exit()

    try:
        os.system("pip3 --no-python-version-warning -q install halo")
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

    m = Mforensics(file_path)

    check = m.req()

    if os.path.exists("vol.py"):
        while True:
            option = m.menu()
            print()
            process = m.func(option)
            choice, alpha = process[0], process[1]
            m.proc(choice, alpha)
            
    else:
        sys.exit("\nError, vol.py is not found in the entered path.")
