'''
Task 6
Create a function that will take a string as an argument and return a dictionary
where keys are symbols from the string and values are the count of inclusion of that symbol.
'''
from collections import OrderedDict
from collections import Counter
from collections import defaultdict


def dict_count(user_string):
    new_dict = defaultdict(int)
    for i in user_string:
        new_dict[i] += 1

    return new_dict

st=input("Please, input string ")
print(dict_count(st))
