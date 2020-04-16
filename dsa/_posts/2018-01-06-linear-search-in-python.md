---
layout: dsa_post
title: Linear Search in Python
keywords: python, dsa, data structure, algorithm, search, sort, stack, queue, tree, heap, graph
excerpt: Simple Linear search algorithm implementation in Python for beginners and learners
code_url: https://github.com/gjain0/Python-DSA/blob/master/search/linear_search.py
hidden: true
---


Return the index of a number in the given list/array

```py
def linear_search(alist, num):
    for i, elem in enumerate(alist):
        if elem == num: 
            return i 

    return None  # If number doesn't exist in the list
```

Usage:

```
>>> mylist = [1, 2, 3, 4, 5, 6, 7]
>>> num = 3  # number to be searched
>>> linear_search(mylist, num)
2
>>>
```
