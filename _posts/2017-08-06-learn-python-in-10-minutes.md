---
layout: post
title: Learn Python in 10 minutes
keywords: Python, Programming, Beginner
excerpt: This a very basic tutorial for beginners who wants to learn Python. You will learn about types, variables, functions, etc.
---

![](/images/post/python.png)  
## Abstract

We have plenty of online resources to learn Python language. Here, in this post, I am also trying to make a dent in the Python world.

This a very basic tutorial for beginners who are just starting with Python. As, with any language, you need to read and practice more to grasp concepts in depth.

Initially, most of the people get confused between Python2 and Python3 So lets clear this for once and all.

Development of Python has been stopped. Python 2.7 is the last version of the Python2 series.

[Here](https://hg.python.org/peps/rev/76d43e52d978#l1.8) is the commit from the creator of Python, Guido van Rossum.

> +Update  
> +======  
> +  
> +The End Of Life date (EOL, sunset date) for Python 2.7 has been moved  
> +five years into the future, to 2020. This decision was made to  
> +clarify the status of Python 2.7 and relieve worries for those users  
> +who cannot yet migrate to Python 3. See also PEP 466.  
> +  
> +This declaration does not guarantee that bugfix releases will be made  
> +on a regular basis, but it should enable volunteers who want to  
> +contribute bugfixes for Python 2.7 and it should satisfy vendors who  
> +still have to support Python 2 for years to come.  
> +  
> +There will be no Python 2.8.  
> +

Python3 is now more mature and stable hence this tutorial is based on Python3, however, I shall mention Python2 difference wherever needed in this post.

### Hello World

The famous "Hello World" program in Python
```py
print("hello World")
```
Yep! That’s all, One line of code. No need to include any library, declaring function or class.

Isn’t that cool?

### Variables and Data Types

In Python, to declare a variable, you don’t specify the datatype of the variable as we do in other languages e.g C, C++, Java, etc. You just declare and initialize it.

#### 1) Numbers
```py
a = 3       # Integer  
a = 2.345   # float/double  
a = 1E3 # scientific notation,  equivalent to 10^3 = 1000.0  
a = 1e3 # scientific notation(with small letter)  equivalent to 10^3 = 1000.0
```
Mathematical Operations can be done easily without having to worry about different datatype
```py
a = 3  
b = 2.5  
c = a + b   # c = 5.5  
c = a * b   # c = 7.5  
c = a / b   # c = 1.2
```
You can read more about these [here](https://docs.python.org/3/library/decimal.html#decimal-objects)

#### 2) Strings
```py
a = "Hello World"   # enclosed in double quotes  
a = 'Hello World'   # enclosed in single quotes
```
There is no difference between double quote string and single quote string. More details on Strings in upcoming section in this post.

#### 3) Booleans
```py
a = True  
a = False
```
#### 4) List, Tuple & Set
```py
a = [1, 2, 3]          # List  
a = (1, 2, 3)          # Tuple, similar to List but immutable  
a = {"a", "b", "c"}    # Set of unique items/objects
```
List, Tuple and Set, all are iterable, that means we can loop over these to get a specific item.

More details on iterables in upcoming section in this post.

#### 5) Dictionary
```py
a = {"name": "Monty", "age": 100}   # Key: Value pair, JSON like object
```
### Strings: Formatting and Operations

Python uses C-style string formatting options, like "%s", "%d", etc.
```py
"Hello %s" % ("World")  # "Hello World"  
"%s is %d feet tall" % ("Tom", 6)   # "Tom is 6 feet tall"
```
Recommended way is to use `string.format()`
```py
"{} is {} feet tall".format("Tom", 6)   # "Tom is 6 feet tall"
```
Further, you can pass placeholders i.e. keyword, number and other formatting options.

### Iterables (Lists, Tuple & Set)

#### 1) List

Lists are similar to arrays. A list can contain any type of variable.
```py
a = [1, "Hello world", 2.34, False]     # List or mix datatype variables
```
The number of items in a list defines the length of the list. Use `len(a_list)` To get the length of the List.
```py
len(a)  # length = 4
```
To get a value from this List you need to use an index. What is index now?

An index is a number assigned to each value

e.g index of 1st value is 0, index of 2nd value is 1, … index of last value is:`length_of_list - 1` in above case, this is 3.
```py
print(a[0])   #  1  
print(a[1])   #  "Hello world"  
print(a[3])   #  False
```
Use `append()` If you want to add an item at the end of a List.
```py
a = [1, "Hello world", 2.34, False]  
a.append("PYC")     # Now a = \[1, "Hello world", 2.34, False, "PYC"\]
```
If you want to insert an item at arbitrary position in the List, Use `insert()`

The first parameter is an index where you want to insert and the second parameter is the value. All other items will be shifted accordingly.
```py
a = [1, "Hello world", 2.34, False]  
a.insert(2, "PYC")  # Now a = \[1, "Hello world", "PYC", 2.34, False\]
```
[More methods of List](https://docs.python.org/3/tutorial/datastructures.html)

#### 2) Set

Set is an unordered collection of unique items
```py
a = set('abracadabra')      # a = {'a', 'r', 'b', 'c', 'd'}   unique letters in a  
b = set('alacazam')         # b = {'z', 'l', 'c', 'a', 'm'}
```
Performing operations on sets
```py
c = a - b       # c = {'r', 'd', 'b'}
```
Generating set from a list
```py
c = set([1, "Hello world", 2.34, False])    #  c = {False, 1, 2.34, 'Hello world'}
```
### Dictionaries
```py
a = {"name": "Monty", "age": 100}  
a["name"]   # "Monty"  
a["age"]    # 100
```
Check if a key exists in the dictionary
```py
"age" in a  # True
```
### Boolean/Logical Operators

Inbuilt logical operators are:`in,``is`, `not`, `not in`, `is not`, `and`, `or`
```py
basket = ['apple', 'orange', 'apple', 'pear', 'orange', 'banana']  
'orange' in basket  # True  
'crabgrass' in basket   # False  
'crabgrass' not in basket   # True
```
### Control Flow: Conditional Statements

`if`, `elif` & `else`
```py
a = 2  
if a > 1:  
    print('a is greater than 1')elif a == 1:  
    print('a is equal to 1')else:  
    print('a is less than 1')
```
### Loops
```py
for i in range(1, 10):  # will print number from 1 to 9, in separate lines  
    print(i)

fruit_list = ['apple', 'orange', 'apple', 'pear', 'orange', 'banana']  
  
for fruit in fruit_list:   # will print each fruit name from the list, in separate lines  
    print(fruit)

while True:  
    print('infinite loop')

a = 1  
while a < 5:    #  will print number from 1 to 4, each in separate line  
    print(a) a = a + 1    #  similar to a += 1
```
### Functions

To define a function you need to use `def` keyword and then your function name(signature)
```py
def hello_world():  
    print('Hello, World!')

def addition(a, b):  
    c = a + b
    print(c)

def factorial(n):  
    f = 1  
    for i in range(1, n+1):
        f = f * i
        return f
```
### Classes and Objects
```py
class Fruit(object):        # 'object' is an inbuilt super class  
    def print_obj(self):    # first parameter, by convention, is 'self' this defines the instance method 
        print("this is a Fruit class's object")
        
apple = Fruit()     # here 'apple' is an object of Fruit class
print(apple.print_obj())    # Accessing object method, will print "this is a Fruit class's object"
```
Now let's see with constructor method. In python, this is a `__init__` method.
```py
class Fruit(object):  
 def __init__(self, name):
    self.name = name    # setting fruit name to object level self.name represents \`object.name\` 
    def fruit_name(self):
        print("{}, An object of Fruit".format(self.name))   # Note the string formatting we mentinoed in above section

apple = Fruit('Green Apple')  
print(apple.fruit_name())   # will print "Green Apple, An object of Fruit"  
print(apple.name)           # will print "Green Apple"
```
### Modules and Packages

In layman language Module is a Python file and package is a collection of modules

To create a module just place a `__init__.py` file(empty file) in the folder where all other python files are placed, then this folder will be interpreted as a package and can be imported into your project.

  
That's all for this post!

Comment your views, if there is something wrong or something that can be improved. Also, share topics for the future post that you want me to write about.