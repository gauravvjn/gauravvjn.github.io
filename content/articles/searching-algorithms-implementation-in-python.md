---
title: Searching Algorithms implementation in Python
date: 2019-03-01
category: Datastructure And Algorithm
tags: algorithm, binary-search, datastructure, linear-search, searching
authors: Gaurav Jain
summary: 
coverimage: /images/searching_algorithm_in_python.png
---

In this post we’ll try to implement most popular searching algorithms using Python. Some of them are –

1. Linear Search
2. Binary Search

All these algorithms returns the index of a number to be searched in the given list/array.

### Linear Search

```python
def linear_search(alist, num):
    for i, elem in enumerate(alist):
        if elem == num: 
            return i 

    return None  # If the number doesn't exist in the list
```

Usage:

```python
>>> mylist = [1, 2, 3, 4, 5, 6, 7]
>>> num = 3  # number to be searched
>>> linear_search(mylist, num)
2
>>>
```

### Binary Search

```python
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

    return None  # If the number doesn't exist in the list
```

Usage:

```python
>>> mylist = [1, 2, 3, 4, 5, 6, 7]
>>> num = 3  # number to be searched
>>> binary_search(mylist, num)
2
>>>
```

That's all for this post. Let me know in the comment if you want me to write about any other searching Algorithm.

All code can be found [here](https://github.com/gauravvjn/Python-DSA/tree/master/sort)!
