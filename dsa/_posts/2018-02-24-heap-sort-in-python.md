---
layout: dsa_post
title: Heap Sort in Python
keywords: python, dsa, data structure, algorithm, search, sort, stack, queue, tree, heap, graph
excerpt: Simple Heap Sort algorithm implementation in Python for beginners and learners for beginners and learners
code_url: https://github.com/gjain0/Python-DSA/blob/master/sort/heap_sort.py
hidden: true
---

As per wikipedia -
Heap sort is a comparison-based sorting algorithm.

Since, Heapsort in based on Complete Binary Tree, we'll try to represent our list in the form of a binary tree.

mylist = [17, 87, 62, 55, 42, 42, 5, 37, 50, 88]

                     17(0)
                  /        \
             87(1)           62(2)           # Numbers in bracket represent the index of the corresponding element
          /        \        /      \
        55(3)      42(4) 42(5)     5(6)
        /   \      /
    37(7)  50(8) 88(9)

Steps are -

1. Convert Array/List into a heap in O(n) operations. Thats called buildMaxHeap() or heapify().
2. After first step we'll have max value at the root (0th index). Swap this value with last element and freez the last element. Now reduce the considered range of the list by 1.
3. Call the siftDown() function on the list to sift the new first element to its appropriate index in the heap.
4. Go to step2 and repeat untill considered range of the list is 1.

[Visualization can be seen here ](https://www.cs.usfca.edu/~galles/visualization/HeapSort.html){:target="_blank"}


Here is the implementation-

```py
def swap(a, b):
    a, b = b, a


def heap_sort(alist):
    n = len(alist)

    # Build a maxheap.
    for i in range(n, -1, -1):
        heapify(alist, n, i)

    # One by one extract elements
    for i in range(n - 1, 0, -1):
        swap(alist[i], alist[0])
        heapify(alist, i, 0)

    return alist
```

Above heap_sort() function is structured based on aforementioned rules.
Now, Let's look at the implementation of heapify function.

```py
def heapify(alist, n, i):
    largest = i       # Initialize largest as root
    l = 2 * i + 1     # left = 2 * i + 1
    r = 2 * i + 2     # right = 2 * i + 2

    # See if left child of the node `i` exists and is greater than root
    if l < n and alist[l] > alist[largest]:
        largest = l

    # See if right child of the node `i` exists and is greater than previously found largest number
    if r < n and alist[r] > alist[largest]:
        largest = r

    # If current number is not the largest, we swap it.
    if largest != i:
        swap(alist[i], alist[largest])
        heapify(alist, n, largest)  # Recursively heapify

```

Usage:

```sh
>>> mylist = [17, 87, 62, 55, 42, 42, 5, 37, 50, 88]
>>> heap_sort(mylist)
>>> mylist
[5, 17, 37, 42, 42, 50, 55, 62, 87, 88]
>>>
```