---
layout: post
title: Building a Simple Blockchain in Python
keywords: Python, Blockchain, Cryptocurrency, Bitcoin, Ethereum, Virtualcurrency
excerpt: A Blockchain is a digital ledger in which transactions are recorded chronologically and publicly.
---

<img src="{{site.static_url}}/img/post/blockchain1.jpg" alt="blockchain part 1" style="width:80%;height:60%"/>

Since Bitcoin boom, Everybody is losing their mind, and as a result of that, we have another Cool Kid in the town, **BLOCKCHAIN**.

So What exactly Blockchain is?

As per Wikipedia,

> _A Blockchain is a continuously growing list of records, called blocks, which are linked and secured using cryptography. Each block typically contains a cryptographic hash pointer as a link to a previous block, a timestamp and transaction data._

If you are familiar with the good old LinkedList then it should be comparatively easy to understand, Afterall Blockchain is also a chain of linked blocks.

This post assumes that reader is familiar with Object-oriented programming in Python3.5, If not, I strongly recommend to check out [the previous post](/learn-python-in-10-minutes/) to get the basic idea of Classes and Objects in Python.

Alright! Let's start.  
  
You must know few terms/definitions before diving into code.

*   **Block**: A block is a unique record in the blockchain which contains transactions, timestamp, index, hash, etc. broadly 3 types of Block -  
    Genesis Block: First Block in the Blockchain known as Genesis block.  
    Current Block: Last Block in the Blockchain.  
    Orphan Block: Valid Block which is not part of the main chain(due to network constraints/Consensus logic, Will read more about this later)
*   **Mining**: Method of creating new Block
*   **Proof Of Work**: is a number(or data) which is _difficult to generate but easy to verify_. usually requires some work and processing time by a computer. Generated number/data will be used to create Block.
*   **Node**: A server will be treated as a single node in a blockchain network. In layman terms, we can compare and map with the unique HTTP servers.
*   **Consensus:** Consensus Algorithm comes into picture when we have more than one node in our blockchain network. To make sure every node in our network has the same blockchain, we make use of this algorithm.

Ok, Enough talk! Show me the code.  
  
Let's create a class of Blocks. All Blocks will have same attributes.  
  
```py
import time  
import hashlib  
  
  
class Block(object):  
      
    def __init__(self, index, proof, previous_hash, transactions):  
        self.index = index  
        self.proof = proof  
        self.previous_hash = previous_hash  
        self.transactions = transactions  
        self.timestamp = time.time()  
  
    @property  
    def get_block_hash(self):  
        block_string = "{}{}{}{}{}".format(self.index, self.proof, self.previous_hash, self.transactions, self.timestamp)  
        return hashlib.sha256(block_string.encode()).hexdigest()
```
Constructor method takes 4 parameters -  
1) **index**: This is the index of the Block in Blockchain list  
2) **proof**: this is a number which will be generated during mining and after successful mining, a Block will be created using this Proof.  
3) **previous_hash**: This will hold the hash of the previous Block in the Blockchain.  
4) **transactions**: A list which will store all transaction records.

The second method in the class **get_block_hash**  will calculate the hash based on above values. This is what makes blockchain really secure. since each block will have a hash and that hash is dependent on previous_block's hash so if attacker try to modify any block, all subsequent blocks will have invalid hash and blockchain network will discard the chain which has invalid/incorrect hash.

Finally, a Block should look like this
```
{  
    "index": 2,  
    "proof": 14,  
    "previous_hash": "8fb156e516b52afffb5860b5e3a076b0513c0d2d4489a9c4675c98e7e4a48a0d",  
    "transactions": [  
        {'sender': 'address_x', 'recipient': 'address_y', 'amount': 1}  
    ],  
    "timestamp": 1514822766.046704  
}  
```
Cool!  
  
Let's create a Blockchain Now.  
  
Below is the blueprint for the class

```py  
class BlockChain(object):  
      
    def __init__(self):  
        self.chain = []  
        self.current_node_transactions = []  
        self.create_genesis_block()  
      
    def create_genesis_block(self):  
        pass  
  
    def create_new_block(self, proof, previous_hash):  
        pass  
  
    def create_new_transaction(self, sender, recipient, amount):  
        pass  
  
    @staticmethod  
    def create_proof_of_work(previous_proof):  
        pass  
     
    @property  
    def get_last_block(self):  
        return self.chain[-1]
```
Method names are self-explanatory. let's dig each method one by one in details.  
  
In Constructor Method, I have 2 variables, **self.chain** will hold all Blocks and **self.****current_node_transactions** will store all transactions which will be inserted into the block.  
In the third line, I will be creating genesis block(first block as mentioned initially in this post), **create_genesis_block()** Method  will take care of this.

Lets detail out **create_new_block()** method-  
  
```py
def create_new_block(self, proof, previous_hash):  
    block = Block(  
        index=len(self.chain),  
        proof=proof,  
        previous_hash=previous_hash,  
        transactions=self.current_node_transactions  
    )  
    self.current_node_transactions = [] # Reset the transaction list  
  
    self.chain.append(block)  
    return block
```
In the first line, I am creating a block by using information provided in params. The **index** would be `last_index+1` which is essentially the length of the chain. **proof** and **previous_hash** should be passed by caller function/method. **transactions** will have all a list of transactions which are not part of any block on the node.

  
Now next line is little tricky
```py
self.current_node_transactions = []
```
  
what I am doing here is that once a block has been created and all transactions assigned to it, I reset the list `self.current_node_transactions` so that all future transactions can be inserted into this list and that again, list in future, will be assigned to a new block and so on. take some time and let it sink in.  
  
In next line, I am appending newly created block to the chain, (No rocket science here)  
finally, I am returning created block object.

Now let's create genesis block. For that, I shall make use of `create_new_block()` method
```py
def create_genesis_block(self):  
    self.create_new_block(proof=0, previous_hash=0)
```
As mentioned earlier, Genesis block is a special block, to create that I pass some default values to the `create_new_block` method. I chose **proof** and **previous_hash** both zero, These value can be anything though.

Next method in the class is `create_new_transaction`
```py
def create_new_transaction(self, sender, recipient, amount):  
    self.current_node_transactions.append({  
        'sender': sender,  
        'recipient': recipient,  
        'amount': amount  
    })  
  
    return self.get_last_block.index + 1 # Returning new block's index where this transaction will be stored
```
It's a very straightforward method, just accept three parameters (sender's address, recipient's address and amount) and append the transaction data to `self.current_node_transactions`list. Whenever the new block is mined, this list will be assigned to that block and reset again as described in `create_new_block` method.

in the last line, I'm returning that future (to be mined) block's index, which will be **current block's index + 1**.  
(Remember Current block is the last block in the chain).

Alright, Now let's talk about another method called `create_proof_of_work`.

This method is very important to keep blockchain safe from spamming. This method will use an algorithm to generate a number that will be used to create a new mined block.
```py
@staticmethod  
def create_proof_of_work(previous_proof):  
    """  
    Generate "Proof Of Work"  
    A very simple \`Proof of Work\` Algorithm -  
    -> Find a number such that, Sum of the number and previous POW number is divisible by 7  
    """  
    proof = previous_proof + 1  
    while (proof + previous_proof) % 7 != 0:  
        proof += 1  
  
    return proof
```
For this tutorial's purpose, I used this simple algorithm. you can use your own algorithm and set a difficulty level so that people can't mine block easily.  
(Remember, To Mine a new block, one needs to generate **Proof Of Work**)

Bitcoin uses the [Hashcash](https://en.bitcoin.it/wiki/Hashcash "Hashcash") proof of work system.

  
Last method(`get_last_block`) is just a helper method to get the last(current block) in the chain.

Awesome! Now we have a fully functional Blockchain class which can be used to create actual mining and transactions HTTP APIs.  
  
Let's test our BlockChain class -
```py
blockchain = BlockChain()  
  
print(">>>>> Before Mining...")  
print(blockchain.chain)  
  
last_block = blockchain.get_last_block  
last_proof = last_block.proof  
proof = blockchain.create_proof_of_work(last_proof)  

# Sender "0" means that this node has mined a new block  
# For mining the Block(or finding the proof), we must be awarded with some amount(in our case this is 1)  

blockchain.create_new_transaction(  
    sender="0",  
    recipient="address_x",  
    amount=1,  
)  

last_hash = last_block.get_block_hash  
block = blockchain.create_new_block(proof, last_hash)  
  
print(">>>>> After Mining...")  
print(blockchain.chain)
```
OUTPUT:
```
>>>>> Before Mining...  
0 - 0 - 0 - [] - 1514822766.046376  
  
>>>>> After Mining...  
0 - 0 - 0 - [] - 1514822766.046376  
1 - 7 - 96da8fdda8a8dea8a445ee220e27b961f64017f111c39145984eca146a048161 - [{'sender': '0', 'amount': 1, 'recipient': 'address_x'}] - 1514822766.046598
```
That's all for this post. I hope you learned something.

Thank you for reading this :)

[You can find the complete source code here](https://github.com/gjain0/blockchain-python/blob/master/blockchain.py).

I kept it very simple just for educational purpose. If you have any suggestions or questions or found any errors/bugs, let me know in the comments.

In part-2, We'll be implementing fully decentralized blockchain network by exposing few APIs written in [Flask](http://flask.pocoo.org/). That will cover remaining concepts like **Node**, **Consensus,** etc**.**

### EDIT: [Part-2 is here](/building-a-simple-blockchain-in-python-part-2/)!