import functools
from collections import Counter
def FizzBuzz():
    print_list = []
    for num in range(100):
        real_num = num+1
        if real_num % 3 == 0 and real_num % 5 == 0:
            print_list.append("Fizz Buzz")
        elif real_num % 3 == 0:
            print_list.append("Fizz")
        elif real_num % 5 == 0:
            print_list.append("Buzz")
        else:
            print_list.append(str(real_num))
    return print_list


def factorial(n):
    a = 1
    for i in range(1, n+1):
        a *= i
        yield a


def dedupe(inputList):
    s = []
    for i in inputList:
       if i not in s:
          s.append(i)
    return s

def countApperance(inputList):
    counter_list = Counter(inputList)
    string=""
    for k, v in counter_list.items():
        string += "{} appeared {} times \n".format(str(k), str(v))
    return string

def checkPalindrome(string):
    """
    verify is a string a palindrome, this task is fast in Python since string can be sliced
    """
    return string == string[::-1]

def getNum(a):
    """
    This is the most efficient way to deal with the problem. 
    """
    n = len(a)
    x1 = a[0]
    x2 = 1
    for i in range(1, n):
        x1 = x1 ^ a[i]
    for i in range(2, n + 2):
        x2 = x2 ^ i
    return x1 ^ x2 # still prints 7

def mergeSortedList(left, right):
    from collections import deque
    """
    Merge sort merging function.
    """
    result = []

    while left and right:
        if left[0] > right[0]:
            result.append(right.pop(0))
        else:
            result.append(left.pop(0))
    return result + left + right

@lru_cache
def fibonacci(n):
    if n == 1 :
        return 1
    elif n == 2:
        return 2
    elif n > 2:
        return fibonacci(n-1) + fibonacci(n-2)
    

def quick_sort(array=arr):
    low, same, high = [], [], []

    if len(array) > 1:
        pivot = array[0]

        for element in array:

            if element < pivot:
                low.append(element)

            elif element == pivot:
                same.append(element)

            else:
                high.append(element)

        return quick_sort(low) + same + quick_sort(high)

    else: 
        return array
    
def main():
    # for x in factorial(6):
    #     print(x)
    # print(functools.reduce(lambda x, y: x*y, factorial(6)))

    # print(countApperance([1, 2, 3, 1, 2, 5, 6, 7, 8]))
    # print(checkPalindrome('cafe'))
    print(mergeSortedList([1,2,3,6,8,9,10], [1,5,8]))



if __name__ == '__main__':
    main()
