---
layout: post
title: Building a Simple Blockchain in Python - Part 2
keywords: Bitcoin, Blockchain, Cryptocurrency, Encoding, Ethereum, Hash, Virtualcurrency, SHA256
excerpt: 2nd part of the previous post on building a simple Blockchain in python
---

#### _Note: This is [the 2nd part of my previous post](/building-a-simple-blockchain-in-python/)._

<img src="{{site.static_url}}/img/post/blockchain2.png" alt="blockchain part 2" style="width:80%;height:60%"/>

_image source: businessinsider.com_

In the first part, we built a simple BlockChain Class. In this post, we I'll be writing HTTP APIs, using that class, to create a simple decentralized BlockChain Network.  
  
This post also assumes that you are familiar with [Flask(Web Framework for Python)](http://flask.pocoo.org/).  
  
Alright, Let's start!

Below is the current implementation of our code (**blockchain.py** file) -

# blockchain.py  
```py  
import time  
import hashlib  
  
class Block(object):  
    ...  
  
class BlockChain(object):  
    ...
```
  
I'll continue editing this file to add HTTP APIs. You can create a separate file and import BlockChain class in it, but for the sake of this tutorial, I'll be using only this file.

1) Setting up Flask
-------------------

First, we need to install Flask. simply run `pip install flask`(in virtualenv) or `sudo pip install flask` (for system-wide installation)

Now Import Flask and create an object of that class.  
  

# blockchain.py  
```py
import time  
import hashlib  
  
class Block(object):  
    ...  
  
class BlockChain(object):  
    ...  
  
from flask import Flask  
  
app = Flask(__name__)  
  
@app.route('/create-transaction', methods=['POST'])  
def create_transaction():  
    pass  
  
app.run(debug=True)
```
In the line,`app = Flask(__name__)` we are creating an object of Flask class which will be a [WSGI](https://en.wikipedia.org/wiki/Web_Server_Gateway_Interface) application.  
  
In next 2 lines, I'm binding a URL to a function, So whenever someone calls the URL, this function will be executed.  
I'm using `route()` decorator to binding URL. This decorator takes a number of arguments. For now, we need to worry about only two arguments, URL and HTTP Verb(Method).  
  
In the last line, I'm calling `run()` method to run the application server.  
  
At this point, you should be able to see below output after running the command (`python blockchain.py`)
```
$ python blockchain.py  
 \* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)  
 \* Restarting with stat  
 \* Debugger is active!  
 \* Debugger PIN: 123-456-789
```
_NOTE: default HOST is 127.0.0.1 and PORT is 5000. (If you wish to run on different host/port, you can do so by providing the information in `run()` method itself. `app.run(host=your_host, port=your_port, debug=True)`_

You can also provide host and port on the command line, for that I use [argparse](https://docs.python.org/3/library/argparse.html) module.

Just add below code before app.run() statement
```py
from argparse import ArgumentParser  
  
parser = ArgumentParser()  
parser.add_argument('-H', '--host', default='127.0.0.1')  
parser.add_argument('-p', '--port', default=5000, type=int)  
args = parser.parse_args()
```
and then use args variable to pass the information in the run() method
```py
app.run(host=args.host, port=args.port, debug=True)
```
You can test this by running the server as
```
$ python app.py -p 5001  
\* Running on http://127.0.0.1:5001/ (Press CTRL+C to quit)  
\* Restarting with stat  
\* Debugger is active!  
\* Debugger PIN: 123-456-789
```
Awesome! you are all set to write APIs

  
2) Writing BlockChain Network APIs
-------------------------------------

Let's create a blueprint of basic required APIs.

# blockchain.py  
```py  
...  
  
from uuid import uuid4  
from flask import Flask  
  
app = Flask(__name__)  
  
blockchain = BlockChain()  
  
node_address = uuid4().hex  # Unique address for current node  
  
@app.route('/create-transaction', methods=['POST'])  
def create_transaction():  
    pass  
  
@app.route('/mine', methods=['GET'])  
def mine():  
    pass  
  
@app.route('/chain', methods=['GET'])  
def get_full_chain():  
    pass  
  
  
from argparse import ArgumentParser  
parser = ArgumentParser()  
parser.add_argument('-H', '--host', default='127.0.0.1')  
parser.add_argument('-p', '--port', default=5000, type=int)  
args = parser.parse_args()  
  
app.run(host=args.host, port=args.port, debug=True)
```
I've bound three URLs to 3 method -

1.  The first method will be used to process the new transaction (will accept send, recipient and amount information in payload)
2.  The second method will be used to mine a new block and some reward money will be awarded to current node/server.
3.  The third method will be used to get the full chain on this node  
      

Also, you might be wondering what is the use of line `node_address = uuid4().hex`

This will give us a globally unique string and I'll be using that to as a current node's address. This address will be used when we have multiple nodes in blockchain network.  
  
Great!

Let's fill these functions with some logic.

Before that, we need to import`jsonify`. APIs will use this method to return the response in JSON format(JSON Content-Type).  
Modify the line where you are importing Flask.
```py
from flask import Flask, jsonify
```

*   **Create Transaction** 
```py    
    @app.route('/create-transaction', methods=['POST'])  
    def create_transaction():  
        transaction_data = request.get_json()  # Accepting Payload from user in JSON content type  
      
        index = blockchain.create_new_transaction(**transaction_data)  
      
        response = {  
            'message': 'Transaction has been submitted successfully',  
            'block_index': index  
        }  
      
        return jsonify(response), 201
```
    Will accept transaction payload

*   **Mine**  
```py    
    @app.route('/mine', methods=['GET'])  
    def mine():  
        block = blockchain.mine_block(node_address)  
      
        response = {  
            'message': 'Successfully Mined the new Block',  
            'block_data': block  
        }  
        return jsonify(response)
```    
    Will Mine new block

*   **Get Full Chain**
```py    
    @app.route('/chain', methods=['GET'])  
    def get_full_chain():  
        response = {  
            'chain': blockchain.get_serialized_chain  
        }  
        return jsonify(response)
```    
    Will return full chain


Let's interact with these APIs.  
  
Start your Flask app server `$ python blockchain.py`

let's check what we have in our blockchain's chain...
```sh
$ curl "http://127.0.0.1:5000/chain"  
{  
    "chain": [  
     {  
        "index": 0,  
        "previous_hash": 0,  
        "proof": 0,  
        "timestamp": 1515310711.279973,  
        "transactions": []  
     }  
    ]  
}
```
That was expected. I have one block in my chain which genesis block.

Let's create a transaction now -
```sh
$ curl -X POST -H "Content-Type: application/json" -d '{"sender": "addr1", "recipient": "addr2", "amount": 3}' "http://127.0.0.1:5000/create-transaction"  
{  
   "block_index": true,  
   "message": "Transaction has been submitted successfully"  
}
```
But if I check the chain again(as shown above) you won't see any change, that's because you haven't mined a new block that will hold this newly created transaction. Okay, In that case, we should mine a new block. Let's do that.
```sh
$ curl "http://127.0.0.1:5000/mine"  
{  
     "block_data": {  
         "index": 1,  
         "previous_hash": "d10ef66c6672fdd5552d8ffde95692bdce80cf65cc901f96659bb802657c3f52",  
         "proof": 7,  
         "timestamp": 1515311824.6986,  
         "transactions": [  
           {  
             "amount": 3,  
             "recipient": "addr2",  
             "sender": "addr1"  
           },  
           {  
             "amount": 1,  
             "recipient": "1e1b776c1ef1477883391a2bb3160c5b",  
             "sender": "0"  
           }  
         ]  
     },  
     "message": "Successfully Mined the new Block"  
}
```
As you can see I have two transactions in the transactions list. The first one is we created in previous API call and the second transaction is awarded to miner by system(If you are not sure what exactly is this, I would recommend checking the first part of this post [here](/building-a-simple-blockchain-in-python/))

Now let's see what our chain looks like now...
```sh
$ curl "http://127.0.0.1:5000/chain"  
{  
 "chain": [  
  {  
    "index": 0,  
    "previous_hash": 0,  
    "proof": 0,  
    "timestamp": 1515311789.924022,  
    "transactions": []  
  },  
  {  
    "index": 1,  
    "previous_hash": "d10ef66c6672fdd5552d8ffde95692bdce80cf65cc901f96659bb802657c3f52",  
    "proof": 7,  
    "timestamp": 1515311824.6986,  
    "transactions": [  
      {  
       "amount": 3,  
       "recipient": "addr2",  
       "sender": "addr1"  
      },  
      {  
       "amount": 1,  
       "recipient": "1e1b776c1ef1477883391a2bb3160c5b",  
       "sender": "0"  
      }  
    ]  
  }  
 ]  
}
```
Great! we can see two blocks. This is a very simple Blockchain service, but this is not decentralized yet.  
Let's make it decentralized. We need two more services for that.

1) Register a node  
2) Sync/Resolve Chain
```py
@app.route('/register-node', methods=['POST'])  
def register_node():  
    node_data = request.get_json()  
    blockchain.create_node(node_data.get('address'))  
    response = {  
        'message': 'New node has been added',  
        'node_count': len(blockchain.nodes),  
        'nodes': list(blockchain.nodes),  
    }  
    return jsonify(response), 201
```
This API will accept an address in the payload, after that, I'm calling **create_node** method which I created in the previous article. This method will register a node to our blockchain node set/list.

Getting confused?  
  
In a decentralized network, all nodes/servers have the copy of all transactions/chain etc. If someone made any changes in any node(i.e. new transaction or mine a new block), we have to somehow inform other nodes and make them sync their chain with the updated data.

So whenever we create a new node in Blockchain network we have to send our node's address to all other nodes available in the network so that they can register our node and in future, all node can sync with each other.

Still not clear? take some time to let that sink in.

let's register one node to our server. hit the blow curl command -
```sh
$ curl -X POST -H "Content-Type: application/json" -d '{"address": "http://127.0.0.1:5001"}' "http://127.0.0.1:5000/register-node"  
{  
   "message": "New node has been added",  
   "node_count": 1,  
   "nodes": [  
     "http://127.0.0.1:5001"  
   ]  
}
```
Did you notice? I'm running the server on 5000 port but in the payload, I pass **5001\.** That's another server's port number which we are going to run parallelly. Because I'm running on the same machine, I had to provide a different port number. if you have two machines you can pass the address of that machine.

You can add as many as nodes you want.

Let's start another node in a new tab -

If you are following this post line by line you should have a blockchain.py file.  
**$ python blockchain.py -p 5000**

Cool, Now we have two nodes/servers running on the same machine.

Now comes the most interesting and important part of Blockchain Network called **Consensus**.

First, we need a helper function to get all chain from all nodes in blockchain network so that we can sync with the correct chain
```py
def get_neighbour_chains():  
    neighbour_chains = []  
  
    for node_address in blockchain.nodes:  
        resp = requests.get(node_address + url_for('get_full_chain')).json()  
        chain = resp['chain']  
        neighbour_chains.append(chain)  
  
    return neighbour_chains
```
Above function will return a list of chains of all nodes in the Network. I'm calling each and every node's chain API to get the chain.

`url_for('get_full_chain')`this statement will give us the relative URL bound to the method **get_full_chain()** and that is **'/chain'**. It's similar to **reverse()** in Django.
```py
node_address + url_for('get_full_chain') # equals to 'http://127.0.0.1:5000 + '/chain'
```
and the popular [python-requests](http://docs.python-requests.org/en/master/user/quickstart/) library to call HTTP API. A really Simple function!  
  
Alright! Let's write the final API for our BlockChain Network. This API will sync all nodes with the correct chain.

You must be wondering how do I know which chain is correct if I have 1000 nodes in the network? so for the sake of this tutorial, I'll be assuming that the longest chain is a valid chain and if there is more than one chain of the same length I would consider calling node's chain is correct.  
  
Ofcourse, this is not the fully logically correct algorithm and may vary business to business, but you get the point!

Let's code the API, shall we?

```py
@app.route('/sync-chain', methods=['GET'])
def consensus():
    neighbour_chains = get_neighbour_chains()
    if not neighbour_chains:
       return jsonify({'message': 'No neighbour chain is available'})
    
    longest_chain = max(neighbour_chains, key=len) # Get the longest chain

    if len(blockchain.chain) >= len(longest_chain):  # If our chain is longest, then do nothing
        response = {
            'message': 'Chain is already up to date',
            'chain': blockchain.get_serialized_chain
        }
    else:  # If our chain isn't longest, then we store the longest chain
        blockchain.chain = [blockchain.get_block_object_from_block_data(block) for block in longest_chain]
        response = {
           'message': 'Chain was replaced',
           'chain': blockchain.get_serialized_chain
        }

    return jsonify(response)
```

Above Code is self-explanatory but still, you might be lost in `else` block.

    blockchain.chain = [blockchain.get_block_object_from_block_data(block) for block in longest_chain]

We know that **blockchain.****chain** attribute is a list of **Block** objects but longest chain we got from the neighbour_chain function is a list of python native Dict type. So we need to convert those Dicts into Block Object and insert into a list then we assign that list to **blockchain.chain** attribute.

And finally, we return the response if the chain has been replaced or not.

Let's test these API. (Make sure you are running both nodes/servers as described above)

# Few API calling helper functions  
```py 
def register_node(node_addr, parent_server):  
    requests.post(parent_server + '/register-node', json={'address': node_addr})  
    print("\\nOn Server {}: Node-{} has been registered successfully!\\n".format(parent_server, node_addr))  
  
def create_transaction(server, data):  
    requests.post(server + '/create-transaction', json=data).json()  
    print("On Server {}: Transaction has been processed!\\n".format(server))  
  
def mine_block(server):  
    requests.get(server + '/mine').json()  
    print("On Server {}: Block has been mined successfully!\\n".format(server))  
  
def get_server_chain(server):  
    resp = requests.get(server + '/chain').json()  
    print("On Server {}: Chain is-\\n{}\\n".format(server, resp))  
    return resp  
  
def sync_chain(server):  
    print("On Server {}: Started Syncing Chain . . .".format(server))  
    resp = requests.get(server + '/sync-chain')  
    print("On Server {}: Chain synced!\\n".format(server))  
  
  
# two servers are running on 5000 and 5001 port  
  
server1 = 'http://127.0.0.1:5000'  
server2 = 'http://127.0.0.1:5001'  
  
register_node(server2, server1) # server2 node will be register inside server1  
  
create_transaction(server2, {'sender': 'I', 'recipient': 'you', 'amount': 3})  
  
mine_block(server2) # Mined a new block on server2  
  
get_server_chain(server1) # server1's chain  
get_server_chain(server2) # server2's chain  
  
sync_chain(server1) # updating server1's chain with neighbour node's chain  
  
get_server_chain(server1) # server1's chain after syncing
```
After running above code you will see the difference between server1's chain before and after syncing.  
  
That's all for this post. I hope you enjoyed and learned something.  
You can find the complete source code [here](https://github.com/gjain0/blockchain-python).  

If you have any suggestions or questions or found any errors/bugs, let me know in the comments.  
  
Happy Mining :)