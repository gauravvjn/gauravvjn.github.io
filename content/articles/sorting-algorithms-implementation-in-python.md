---
title: Sorting Algorithms implementation in Python
date: 2019-02-05
category: Datastructure And Algorithm
tags: algorithm, bubble-sort, datastructure, heap-sort, insertion-sort, merge-sort, quicksort, selection-sort, sorting
authors: Gaurav Jain
summary: 
coverimage: /images/sorting_algorithms.png
---

In this post we'll try to implement most popular sorting algorithms using Python. Some of them are -

1. Bubble Sort
2. Insertion Sort
3. Selection Sort
4. Merge Sort
5. Quick Sort
6. Heap Sort

Lets begin with the most popular and simplest one, **Bubble Sort**!

### Bubble Sort

```python
def bubble_sort(alist):
    n = len(alist)  # Number of items in the list
    for i in range(n):
        for j in range(0, n - i - 1):
            if alist[j] > alist[j + 1]:
                alist[j], alist[j + 1] = alist[j + 1], alist[j]
```

Usage:

```python
>>> mylist = [17, 87, 62, 55, 42, 42, 5, 37, 50, 88]
>>> bubble_sort(mylist)
>>> mylist
[5, 17, 37, 42, 42, 50, 55, 62, 87, 88]
>>>
```

Above implementation comes with some limitation. It sort the array/list in ascending order only. We can slightly tweak the logic and have a support for descending sort based on the parameter.

```python
def bubble_sort(alist, reverse=False):
    """
    Sort the array in desired order using bubble sort algorithm
    `reverse` parameter controls the order of elements, if `reverse=True`, this will sort the array in descending order
    """
    n = len(alist)  # Number of items in the list

    for i in range(n):
        for j in range(0, n - i - 1):
            if reverse and alist[j] < alist[j + 1]:
                alist[j], alist[j + 1] = alist[j + 1], alist[j]
            elif not reverse and alist[j] > alist[j + 1]:
                alist[j], alist[j + 1] = alist[j + 1], alist[j]
```

Usage:

```python
>>> mylist = [17, 87, 62, 55, 42, 42, 5, 37, 50, 88]
>>> bubble_sort(mylist, reverse=True)
>>> mylist
[88, 87, 62, 55, 50, 42, 42, 37, 17, 5]
>>>
```

### Insertion Sort

```python
def insertion_sort(alist):

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

```python
>>> mylist = [17, 87, 62, 55, 42, 42, 5, 37, 50, 88]
>>> insertion_sort(mylist)
>>> mylist
[5, 17, 37, 42, 42, 50, 55, 62, 87, 88]
>>>
```

### Selection Sort

```python
def selection_sort(alist):

    n = len(alist)

    for i in range(n):
        # Find the minimum element from index i+1 till last element in the list
        min_index = i
        for j in range(i + 1, n):
            if alist[j] < alist[min_index]:
                min_index = j

        # Swap the minimum element with the first element
        alist[i], alist[min_index] = alist[min_index], alist[i]
```

Usage:

```python
>>> mylist = [17, 87, 62, 55, 42, 42, 5, 37, 50, 88]
>>> selection_sort(mylist)
>>> mylist
[5, 17, 37, 42, 42, 50, 55, 62, 87, 88]
>>>
```

### Merge Sort

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

```python
def merge_sort(alist):

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

```python
>>> mylist = [17, 87, 62, 55, 42, 42, 5, 37, 50, 88]
>>> merge_sort(mylist)
>>> mylist
[5, 17, 37, 42, 42, 50, 55, 62, 87, 88]
>>>
```

### Quick Sort

Quicksort is an O(n log n) in-place sorting algorithm. It works by dividing the list into two partitions as we did in Merge Sort. The only difference here is, we don't divide the list in two equal half. instead, we pick a random element(pivot) from the list and based on that pivot we create two partitions. All the numbers less than the pivot would be moved in the left side of the list and numbers greater than pivot would be in the right of the pivot. This way the pivot element will be at the correct position. It's common practice to pick the first or last element as a pivot if we want to avoid any other complexities in choosing pivot.

```python
def partition(alist, start, end):
    """
    This function assumes the last element as pivot
    """
    pivot = alist[start]
    i = start
    j = end

    while True:
        while (i <= j and alist[i] <= pivot):
            i = i + 1
        while (i <= j and alist[j] >= pivot):
            j = j - 1

        if i <= j:
            alist[i], alist[j] = alist[j], alist[i]
        else:
            alist[start], alist[j] = alist[j], alist[start]
            return j
```

```python
def quick_sort_helper(alist, start, end):
    if start < end:
        # p is partitioning index, the element alist[p] is now at right position
        p = partition(alist, start, end)

        # Individually sort elements before and after partition, recursively!
        quick_sort_helper(alist, start, p - 1)
        quick_sort_helper(alist, p + 1, end)
```

```python
def quick_sort(alist):
    quick_sort_helper(alist, 0, len(alist) - 1)
```

Usage:

```python
>>> mylist = [17, 87, 62, 55, 42, 42, 5, 37, 50, 88]
>>> quick_sort(mylist)
>>> mylist
[5, 17, 37, 42, 42, 50, 55, 62, 87, 88]
>>>
```

### Heap Sort

Heap sort is a comparison-based sorting algorithm.

Since, Heapsort in based on Complete Binary Tree, we’ll try to represent our list in the form of a binary tree.

mylist = \[17, 87, 62, 55, 42, 42, 5, 37, 50, 88\]

```
                 17(0)
              /        \
         87(1)           62(2)           # Numbers in bracket represent the index of the corresponding element
      /        \        /      \
    55(3)      42(4) 42(5)     5(6)
    /   \      /
37(7)  50(8) 88(9)
```

Steps are -

1. Convert Array/List into a heap in O(n) operations. Thats called buildMaxHeap() or heapify().
2. After first step we’ll have max value at the root (0th index). Swap this value with last element and freez the last element. Now reduce the considered range of the list by 1.
3. Call the siftDown() function on the list to sift the new first element to its appropriate index in the heap.
4. Go to step2 and repeat untill considered range of the list is 1.

[Visualization can be seen here](https://www.cs.usfca.edu/~galles/visualization/HeapSort.html)

Here is the implementation-

```python
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

Above heap\_sort() function is structured based on aforementioned rules. Now, Let’s look at the implementation of heapify function.

```python
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

```python
>>> mylist = [17, 87, 62, 55, 42, 42, 5, 37, 50, 88]
>>> heap_sort(mylist)
>>> mylist
[5, 17, 37, 42, 42, 50, 55, 62, 87, 88]
>>>
```

That's all for this post. Let me know in the comment if you want me to write about any other sorting Algorithm.

All code can be found [here](https://github.com/gauravvjn/Python-DSA/tree/master/sort)!
