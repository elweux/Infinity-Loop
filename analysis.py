import os
import sys

from mforensics import Mforensics

if __name__ == '__main__':

    if len(sys.argv) != 2:
        sys.exit("Usage: python3 analysis.py <filename/filepath>")

    file_path = os.path.realpath(sys.argv[1])

    if os.path.exists("/opt") and os.getuid() != 0:
        sys.exit("Not running as sudo. Either run as sudo or change the default installation path.")

    print("""\n\n                           MEMORY FORENSICS BY
        _       _____       _ __           __                
       (_)___  / __(_)___  (_) /___  __   / /___  ____  ____ 
      / / __ \/ /_/ / __ \/ / __/ / / /  / / __ \/ __ \/ __ \.
     / / / / / __/ / / / / / /_/ /_/ /  / / /_/ / /_/ / /_/ /
    /_/_/ /_/_/ /_/_/ /_/_/\__/\__, /  /_/\____/\____/ .___/ 
                              /____/                /_/       
                                                            """)

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
