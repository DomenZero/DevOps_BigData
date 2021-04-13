'''
Task 7
Develop a procedure that will have a size argument and print a table where num of columns
and rows will be of this size. Cells of table should contain numbers from 1 to n ** 2 placed
 in a spiral fashion. Spiral should start from top left cell and has a clockwise direction (see the example below).

example:

>>> print_spiral(5)
1 2 3 4 5
16 17 18 19 6
15 24 25 20 7
14 23 22 21 8
13 12 11 10 9
'''

import numpy as np


def print_spiral(num):
    max_index = num - 1
    min = 0
    next_num = 1
    for num_levels in range(num):
        for y in range(min, max_index + 1):
            spiral_mas[num_levels][y] = next_num
            next_num = next_num + 1
        for y in range(min + 1, max_index + 1):
            spiral_mas[y][max_index] = next_num
            next_num = next_num + 1
        for y in range(max_index - 1, min - 1, -1):
            spiral_mas[max_index][y] = next_num
            next_num = next_num + 1
        for y in range(max_index - 1, min, -1):
            spiral_mas[y][min] = next_num
            next_num = next_num + 1

        min += 1
        max_index -= 1
    return spiral_mas


num = int(input("Number spiral: "))
spiral_mas = [[0] * num for i in range(num)]

spiral_mas = print_spiral(num)

for i in range(num):
    for j in range(num):
        print(spiral_mas[i][j], end="\t")
    print()
