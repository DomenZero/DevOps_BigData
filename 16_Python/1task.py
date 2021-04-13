'''
Task 1
Self-study input() function.Write a script which accepts a sequence of comma-separated numbers from user
and generate a list and a tuple with those numbers
and prints these objects as-is (just print(list) without any formatting).
'''
def study_input(value):
    list_numbers = []
    elem = value.split(',')
    list_numbers=elem
    print("The list of numbers is: \n", list_numbers)
    print(type(list_numbers))
    list_tuple = tuple(elem)
    print("The tuple of numbers is: \n", list_tuple)
    print(type(list_tuple))

numbers=input('Please input numbers with a comma-separator: ')
study_input(numbers)