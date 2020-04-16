---
layout: dsa_post
title: Stack in Python
keywords: python, dsa, data structure, algorithm, search, sort, stack, queue, tree, heap, graph
excerpt: Simple Stack data structure implementation in Python for beginners and learners
code_url: https://github.com/gjain0/Python-DSA/blob/master/stack/stack.py
hidden: true
---


Implementing a Stack datastructure using Python

A stack is a datastructure with two basic operations, those are `push` and `pop`. 
 - Push: Add items in the stack from top e.g putting books on top of other books
 - Pop: Remove items from the top in the stack and return the removed item  e.g removing top book to get the second top book

Apart from these two necessary operations, There are few other useful actions as well.
 - Peek: It's similar to Pop operations but it doesnt remove the item, it just return the value
 - is_empty: to check if stack is empty or has at least 1 item in it. return True if empty, False otherwise
 - size: to get the current size(how many items are in the stack at the moment)

Based on above features, there are multiple ways you can design your stack datastructure


#### 1. Unlimited capacity/length/size of the stack
```py
class Stack:

    def __init__(self):
        self.stack = []

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        if self.is_empty():
            return "Stack Is Empty"
        return self.stack.pop()

    def peek(self):
        return self.stack[len(self.stack) - 1]

    def is_empty(self):
        return len(self.stack) == 0

    def size(self):
        return len(self.stack)
```
This will create a stack of unlimited size/capacity (i.e we can store as many items as we want). In real world scenarios, we do have limited size. Im going to discuss most common ones in this post.

Usage:

```sh
>>> s = Stack()
>>> s.is_empty()
True
>>> s.size()
0
>>> s.push('cat')
>>> s.push('dog')
>>> s.push('cow')
>>> s.is_empty()
False
>>> s.size()
3
>>> s.peek()
'cow'
>>> s.pop()
'cow'
>>> s.pop()
'dog'
>>> s.size()
1
>>> s.peek()
'cat'
```

To have a stack of limited size, we have to maintain another variable which will keep track of the length has been covered so far.

#### 2. Limited capacity, without maintaining a pointer to last(top/most recent) element
```py
class Stack:

    def __init__(self, capacity):
        self.stack = []
        self.capacity = capacity   # This will maintain the size/length of the Stack

    def push(self, item):
        if self.size() >= self.capacity:
            return "Stack Is Full"
        self.stack.append(item)

    def pop(self):
        if self.is_empty():
            return "Stack Is Empty"
        return self.stack.pop()

    def peek(self):
        return self.stack[len(self.stack) - 1]

    def is_empty(self):
        return len(self.stack) == 0

    def size(self):
        return len(self.stack)
```

Usage:

```sh
>>> s = Stack(capacity=10)  # Create a stack of length 10
...
```

#### 3. Limited capacity, with maintaining a pointer to last(top) element
```py
class Stack:

    def __init__(self, capacity):
        self.stack = []
        self.capacity = capacity
        self.top = -1  # This will have a pointer to the last/most_recent element.

    def push(self,data):
        if self.size() >= self.capacity:
            return "Stack Is Full"
        self.stack.append(data)
        self.top += 1

    def pop(self):
        if self.is_empty():
            return "Stack Is Empty"
        self.top -= 1
        return self.stack.pop()

    def peek(self):
        return self.stack[self.top]

    def is_empty(self):
        return self.top < 0

    def size(self):
        return self.top + 1

    def top_element(self):
        return self.stack[self.top]  # self.stack[-1]
```

Usage:

```sh
>>> s = Stack(capacity=10)  # Create a stack of length 10
>>> s.top   # will give you index of top/most_recent element
>>> s.top_element()  # will give you top/most_recent element
```
