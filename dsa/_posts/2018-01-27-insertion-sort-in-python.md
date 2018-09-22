---
layout: dsa_post
title: Insertion Sort in Python
keywords: python, dsa, data structure, algorithm, search, sort, stack, queue, tree, heap, graph
excerpt: Simple Insertion Sort algorithm implementation in Python for beginners and learners
code_url: https://github.com/gjain0/Python-DSA/blob/master/sort/insertion_sort.py
hidden: true
---

```py
def insertion_sort(alist):
    """
    Sort the array using insertion sort algorithm
    >>> mylist = [17, 87, 62, 55, 42, 42, 5, 37, 50, 88]
    >>> insertion_sort(mylist)
    >>> mylist
    [5, 17, 37, 42, 42, 50, 55, 62, 87, 88]
    >>>
    """
    for i in range(1, len(alist)):
        curr_num = alist[i]
        # Next while loop will traverse all previous elements to figure out the correct location of this number and put there
        j = i - 1  # Will start from this index and traverse the list till 0 index

        while j >= 0 and alist[j] > curr_num:
            alist[j + 1] = alist[j]
            j -= 1

        alist[j + 1] = curr_num
```

Usage:

```sh
>>> mylist = [17, 87, 62, 55, 42, 42, 5, 37, 50, 88]
>>> insertion_sort(mylist)
>>> mylist
[5, 17, 37, 42, 42, 50, 55, 62, 87, 88]
>>>
```
