'''
Task 5
Develop a function that takes a list of integers (by idea not in fact) as an argument and returns list of
top-three max integers. If passed list contains not just integers collect them and print the following error
message: You've passed some extra elements that I can't parse: [<"elem1", "elem2" .... >].
If return value will have less than 3 elements for some reason it's ok and shouldn't cause any problem,
but some list should be returned in any case.
'''

def list_int_sort(value):
    fail_numbers = []
    int_numbers = []
    elem = value.split(',')
    list_numbers=elem

    print("The list of numbers is: \n", list_numbers)

    for number in list_numbers:
        try:
            number=int(number)
            if isinstance(number, int):
                int_numbers.append(number)
        except ValueError:
            fail_numbers.append(number)

    limit=3
    i=0
    if len(fail_numbers)==0:
        print_numbers=sorted(int_numbers,reverse=True)
        if limit<len(print_numbers):
            while i < limit:
                print(print_numbers[i])
                i+=1
        else:
            limit=len(print_numbers)
            while i < limit:
                print(print_numbers[i])
                i+=1

    else:
        print("You've passed some extra elements that I can't parse: ",fail_numbers)

numbers=input('Please input numbers with a comma-separator: ')
list_int_sort(numbers)