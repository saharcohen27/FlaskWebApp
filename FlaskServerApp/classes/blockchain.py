from pywallet import wallet
from DataBase import Database
import hashlib

class blockchain_wallet():
    def __init__(self, net='BTC'): # options:  BTC, BTG, BCH, LTC, DASH, DOGE
        # generate 12 word mnemonic seed
        seed = wallet.generate_mnemonic()

        # create bitcoin wallet
        self.wlt = wallet.create_wallet(network=net, seed=seed, children=0)
        self.save()
        
    def get_seed(self):
        return self.wlt['seed']

    def get_public_key(self):
        return self.wlt['public_key']
        
    def get_private_key(self):
        return self.wlt['private_key']
    
    def get_address(self):
        return self.wlt['address']
    
    def save(self):
        db = Database()
        hashed_seed = hashlib.md5(self.wlt['seed'].encode()).hexdigest()

        db.ask(f"INSERT INTO Blockchain (publicKey, privateKey, addr, seed) \
                 VALUES ('{self.wlt['public_key']}','{self.wlt['private_key']}', \
                 '{self.wlt['address']}','{hashed_seed}');")


from bitcoinlib.wallets import HDWallet, wallet_delete
from bitcoinlib.mnemonic import Mnemonic

class blockchain_wallet2():
    def __init__(self, username, net='bitcoin'):
        passphrase = Mnemonic().generate()
        hashed_seed = hashlib.md5(passphrase.encode()).hexdigest()
        print(hashed_seed)
        self.wallet = HDWallet.create(username, keys=passphrase, network=net)
        self.key = self.wallet.get_key
        self.address = self.key.address
        self.accounts = {}
    
    def get_info(self):
        self.wallet.scan()
        return self.wallet.info()

    def send_currency(self, receiver, amount):
        transaction = self.wallet.send_to(receiver, amount)
        return transaction.info # Shows transaction information and send results

    def create_account(self, name, net='bitcoin'):
        account = self.wallet.new_account(name, network=net)
        self.accounts[name] = account
        return self.wallet.get_key(account.account_id)

