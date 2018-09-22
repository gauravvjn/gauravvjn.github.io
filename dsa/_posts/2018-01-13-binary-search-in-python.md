---
layout: dsa_post
title: Binary Search in Python
keywords: python, dsa, data structure, algorithm, search, sort, stack, queue, tree, heap, graph
excerpt: Simple Binary search algorithm implementation in Python for beginners and learners
code_url: https://github.com/gjain0/Python-DSA/blob/master/search/binary_search.py
hidden: true
---


Return the index of a number in the given list/array

```py
def binary_search(alist, num):
    l, r = 0, len(alist) - 1

    while l <= r:
        mid = (l + r) // 2
        if alist[mid] < num:
            l = mid + 1
        elif alist[mid] > num:
            r = mid - 1
        else:
            return mid

    return None  # If number doesn't exist in the list
```

Usage:

```
>>> mylist = [1, 2, 3, 4, 5, 6, 7]
>>> num = 3  # number to be searched
>>> binary_search(mylist, num)
2
>>>
```
