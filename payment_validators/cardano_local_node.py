# Check for transaction success using the cardano wallet backend.  
def check_cardano_wallets(ws):
    # Check if cardano wallet backend is running
    command_list = ['cardano-wallet', 'wallet', 'list']
    process = subprocess.Popen(command_list,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               universal_newlines=True)

    stdout = process.stdout.readline()
    stderr = process.stderr.readline()

    wallets = ws.wallets()

    if not stderr.startswith('Ok'):
        print('Are you sure the Cardano wallet backend is running')
        print(stderr)
    else:
        if not wallets:
            print('There are no wallets defined')
            print('Creating a new wallet')
            print('WARNING: Recovery phrase and password is saved in mnemonic.txt store in a safe place!!!!')

            # Gererate a mnemonic
            command_list = ['cardano-wallet', 'recovery-phrase', 'generate']
            process = subprocess.Popen(command_list,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       universal_newlines=True)
            mnemonic = process.stdout.readline()

            # Generate a password for a new wallet
            alphabet = string.ascii_letters + string.digits
            password = ''.join(secrets.choice(alphabet) for i in range(10))  # for a 20-character password

            print(mnemonic)
            print(password)

            # Save the mnemonic to a file
            f = open("mnemonic.txt", "a")
            f.write(mnemonic)
            f.write(password)
            f.close()

            wal = ws.create_wallet(
                name="Odoo shop wallet",
                mnemonic=mnemonic,
                passphrase=password,
            )

        print('\nThe following wallets are available listed by id:')
        for wallet in wallets:
            print(wallet.wid)

def payment_validate(network_type, transaction_id, wallet_id, requested_amount):
    wallet_port = 8090

    print('Connecting to wallet')

    wal0 = Wallet(wallet_id, backend=WalletREST(port=wallet_port))
    wal0.sync_progress()
    
    wallet_balance = wal0.balance().total
    # print('wallet balance')
    # print(wal0.balance().total)
    
    tnxs = wal0.transactions()
    
    transact = []
    
    result = "not_received"
    
    for tnx in tnxs:
        tnx_dict = {'id': tnx.txid, 'fee': tnx.fee, 'input': tnx.amount_in, 'output': tnx.amount_out, 'metadata': tnx.metadata, 'status' : tnx.status}
        
        #print(dir(tnx))
        print('\n')
        print(repr(tnx_dict))
        print('\n')
        
        metadata = tnx.metadata
        #print(metadata.keys())
        
        tx_id = ''
        
        try:
            tx_id = metadata[73]['title']
            print('tx_id: ' + str(tx_id))
            print('transaction_id: ' + transaction_id)
            print(': ' + transaction_id)
                     
            if tx_id == transaction_id and tnx.amount_in >= requested_amount:
                print("-------------- Success -------------")
                result = "success"   
            elif tx_id == transaction_id and tnx.amount_in < requested_amount:
                result = "Recieved amount too low => Requested: " + str(requested_amount) + "Recieved: " + str(tnx.amount_in)  
 
        except KeyError:
            pass
        
        return result 
