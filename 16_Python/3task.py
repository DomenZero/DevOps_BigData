'''
Task 3
Something old in a new way :). Self-study positional arguments for Python scripts (sys.argv).
Write a script that takes a list of words (or even phrases)aScript should ask a user to write
something to stdin until user won't provide one of argument phrases.
'''

import sys

n=False
list_words=()
try:
    with open(sys.argv[1], 'r') as file_input:
        list_words = file_input.read().splitlines()

    while n=False:
        user_input = input("Please input word ")
        listtest = user_input
        for word in list_words:
            if word in listtest:
                n=True
                print("Stop, You insert "+word)
                break
    file_input.close()
except TypeError:
    print("It is not the good file")
