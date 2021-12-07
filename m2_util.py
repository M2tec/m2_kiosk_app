
import secrets
import string
import subprocess





def is_port_in_use(port):
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def check_odoo_and_cardano(odoo_port, wallet_port):

    # Check if Odoo is running
    if is_port_in_use(int(odoo_port)):
        print("Connecting to Odoo on port: " + str(odoo_port))
    else:
        print("Make sure Odoo is running on port: " + str(odoo_port))
        quit()

    # Check if Cardano wallet backend is running
    if is_port_in_use(int(wallet_port)):
        print("Connecting to Cardano wallet backend on port: " + str(wallet_port))
    else:
        print("Make sure the Cardano wallet backend is running on port: " + str(wallet_port))
        quit()

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