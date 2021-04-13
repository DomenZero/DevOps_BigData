'''
Task 2
Develop a procedure to print all even numbers from a numbers list which is given as an argument.
Keep the original order of numbers in list and stop printing if a number 254 was met.
Don't forget to add a check of the passed argument type.
'''

def even_check(argi):
    for number in argi:
        op=int(number) % 2
        if (int(number) != 254) and (op==0):
            print(number)

value = input('Please input numbers with a comma-separator: ')
numbers = value.split(',')
try:
    even_check(numbers)
except ValueError:
    print("Value Error")

