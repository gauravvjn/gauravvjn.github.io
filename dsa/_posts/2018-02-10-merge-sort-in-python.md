---
layout: dsa_post
title: Merge Sort in Python
keywords: python, dsa, data structure, algorithm, search, sort, stack, queue, tree, heap, graph
excerpt: Simple Merge Sort algorithm implementation in Python for beginners and learners
code_url: https://github.com/gjain0/Python-DSA/blob/master/sort/merge_sort.py
hidden: true
---

Merge sort is an O(n log n) divide-and-conquer sorting algorithm.

The idea is to split the the input list/array into two halves, repeating the process on those halves, and merge the two sorted halves together again.

You can visualize the process below -

```
             [17, 87, 62, 55, 42, 42, 5, 37, 50, 88]

      [17, 87, 62, 55, 42]                 [42, 5, 37, 50, 88]

   [17, 87]       [62, 55, 42]          [42, 5]      [37, 50, 88]

 [17]    [87]   [62]    [55, 42]      [42]    [5]   [37]    [50, 88]

 [17]    [87]   [62]   [55]  [42]     [42]    [5]   [37]   [50]  [88]

 [17]    [87]   [62]    [42, 55]      [42]    [5]   [37]    [50, 88]

   [17, 87]       [42, 55, 62]          [5, 42]       [37, 50, 88]

      [17, 42, 55, 62, 87]                 [5, 37, 42, 50, 88]

             [5, 17, 37, 42, 42, 50, 55, 62, 87, 88]
```

```py
def merge_sort(alist):
    """
    Sort the array using merge sort algorithm
    >>> mylist = [17, 87, 62, 55, 42, 42, 5, 37, 50, 88]
    >>> merge_sort(mylist)
    [5, 17, 37, 42, 42, 50, 55, 62, 87, 88]
    >>>
    """
    if len(alist) > 1:
        mid = len(alist) // 2  # Mid of the array
        left_list = alist[:mid]  # Creating another list for first half
        right_list = alist[mid:]  # Creating another list for second half

        merge_sort(left_list)  # Sorting the left list recursively
        merge_sort(right_list)  # Sorting the right list recursively

        i = j = k = 0

        while i < len(left_list) and j < len(right_list):
            if left_list[i] < right_list[j]:
                alist[k] = left_list[i]
                i += 1
            else:
                alist[k] = right_list[j]
                j += 1
            k += 1

        # Remaining elements
        while i < len(left_list):
            alist[k] = left_list[i]
            i += 1
            k += 1

        while j < len(right_list):
            alist[k] = right_list[j]
            j += 1
            k += 1
```

Usage:

```sh
>>> mylist = [17, 87, 62, 55, 42, 42, 5, 37, 50, 88]
>>> merge_sort(mylist)
>>> mylist
[5, 17, 37, 42, 42, 50, 55, 62, 87, 88]
>>>
```