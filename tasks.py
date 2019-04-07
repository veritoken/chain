import os, sys, time, json
from invoke import task

def getw3():
    global w3
    import web3
    w3 = web3.Web3(web3.WebsocketProvider())
    w3.eth.defaultAccount = w3.eth.accounts[0]
    return w3

@task
def clean(c):
    os.system('''rm -fr *~ out;
tree
''')
    
@task
def compile(c, filename):
   print("COMPILE", filename)
   os.system('''solc %s --abi --bin -o out''' % filename)

@task(iterable=['a'])
def call(c, filename, address, func, a):
    print("CALL", os.path.splitext(filename)[0]+'.abi', address, a)
    fileroot = os.path.splitext(filename)[0]
    abi = json.load(open(fileroot+'.abi'))
    getw3()
    greeter = w3.eth.contract(address=address, abi=abi)
    f = greeter.find_functions_by_name(func)
    if f:
        g = f[0](*a).call()
        print("G", g)
    else:
        print("NO WAY")
    
@task(iterable=['a'])
def transact(c, filename, address, func, a):
    print("TRANSACT", os.path.splitext(filename)[0]+'.abi', address, a)
    fileroot = os.path.splitext(filename)[0]
    abi = json.load(open(fileroot+'.abi'))
    getw3()
    greeter = w3.eth.contract(address=address, abi=abi)
    f = greeter.find_functions_by_name(func)
    if f:
        tx_hash = f[0](*a).transact()
        # Wait for transaction to be mined...
        print("TX HASH", tx_hash.hex())
        x = w3.eth.waitForTransactionReceipt(tx_hash)
        print("X", x)
    else:
        print("NO WAY")
    
@task
def filter(c, filename, address, name):
    print("FILTER", os.path.splitext(filename)[0]+'.abi', address, name)
    fileroot = os.path.splitext(filename)[0]
    abi = json.load(open(fileroot+'.abi'))
    getw3()
    greeter = w3.eth.contract(address=address, abi=abi)
    myfilter = greeter.eventFilter(name, {'fromBlock': 0,'toBlock': 'latest'});
    while 1:
        print(myfilter.get_new_entries())
        time.sleep(1)
    
@task
def deploy(c, filename):
    #print("DEPLOY", os.path.splitext(filename)[0]+'.{abi,bin}')
    fileroot = os.path.splitext(filename)[0]
    abi = json.load(open(fileroot+'.abi'))
    bin = open(fileroot+'.bin').read()
    getw3()
    print("export ACCT=" + w3.eth.accounts[0])
    Greeter = w3.eth.contract(abi=abi, bytecode=bin)
    tx_hash = Greeter.constructor().transact()
    print("export TX_HASH=" + tx_hash.hex())
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    address=tx_receipt.contractAddress
    print("export ADDRESS=" + address)

