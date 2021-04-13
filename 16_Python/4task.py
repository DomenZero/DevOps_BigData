'''
Task 4
We took a little look on os module. Write a small script which will print a string using all the
types of string formatting which were considered during the lecture with the following context:
This script has the following PID: <ACTUAL_PID_HERE>. It was ran by <ACTUAL_USERNAME_HERE> to work
happily on <ACTUAL_OS_NAME>-<ACTUAL_OS_RELEASE>.
'''

import os
import platform
# For Win
# print(re.match('')os.name)

print("PID: %d It was ran by %s to work happily on %s - %s  years old." % (os.getpid(), os.getuid(), platform.system(), platform.release()))

print(f'PID: {os.getpid()} It was ran by {os.getuid()} to work happily on {platform.system()} - {platform.release()}  years old.')
