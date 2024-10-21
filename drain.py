import time
from web3 import Web3

# Ganti dengan Node Provider URL untuk jaringan Base Chain atau Ethereum Mainnet
node_provider_url = "https://base-mainnet.infura.io/v3/Your-API-KEY"
web3 = Web3(Web3.HTTPProvider(node_provider_url))

# Fungsi untuk memeriksa koneksi
def check_connection():
    if not web3.is_connected():
        raise Exception("Tidak dapat terhubung ke jaringan Base Chain. Periksa node provider URL atau koneksi internet Anda.")
    else:
        print("Terhubung ke jaringan Base Chain.")

# Periksa koneksi ke jaringan
try:
    check_connection()
except Exception as e:
    print(e)
    exit()

# Alamat wallet dan private key Anda
my_address = Web3.to_checksum_address("0x03c39D959aF7C40ED1fb2904A4dD152599a61a35")
private_key = ""

# Alamat tujuan
destination_address = Web3.to_checksum_address("0x93CdED77c3559b3E9e526d05d9Bd292c942aEF4E")

# Alamat token yang ingin dikirim
token_address = Web3.to_checksum_address("0x4ed4e862860bed51a9570b96d89af5e1b0efefed")

# Fungsi untuk memeriksa apakah private key cocok dengan alamat
def verify_private_key_address():
    account_from_key = web3.eth.account.from_key(private_key).address
    if account_from_key.lower() != my_address.lower():
        raise Exception("Private key tidak sesuai dengan alamat pengirim. Pastikan private key dan alamat benar.")

# Verifikasi kecocokan private key dengan alamat
try:
    verify_private_key_address()
except Exception as e:
    print(e)
    exit()

# Fungsi untuk mengirim token ERC20
def send_token(token_address, amount_in_wei):
    erc20_abi = '[{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"}]'
    token_contract = web3.eth.contract(address=token_address, abi=erc20_abi)

    nonce = web3.eth.get_transaction_count(my_address)
    gas_price = web3.eth.gas_price  # Mengambil gas price otomatis dari jaringan
    tx = token_contract.functions.transfer(destination_address, amount_in_wei).buildTransaction({
        'nonce': nonce,
        'gas': 70000,  # Gas untuk transfer token
        'gasPrice': gas_price,
        'chainId': 8453  # Pastikan chainId sesuai dengan jaringan yang digunakan
    })

    signed_tx = web3.eth.account.sign_transaction(tx, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print(f"Token transfer sent: {web3.to_hex(tx_hash)}")

# Fungsi utama untuk mengirim token secara berulang
def main_loop():
    amount_in_wei = web3.to_wei(26, 'ether')  # Nilai token yang akan dikirim (1 token, sesuaikan sesuai kebutuhan)

    while True:
        try:
            # Periksa saldo token
            token_contract = web3.eth.contract(address=token_address, abi='[{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}]')
            token_balance = token_contract.functions.balanceOf(my_address).call()  # Memanggil balanceOf dengan argumen
            print(f"Saldo token saat ini: {token_balance} token")  # Tampilkan saldo token saat ini

            gas_price = web3.eth.gas_price  # Ambil gas price otomatis dari jaringan
            print(f"Gas Price terkini: {web3.from_wei(gas_price, 'gwei')} gwei")  # Tampilkan gas price terkini

            gas_fee = 70000 * gas_price  # Perkiraan biaya gas untuk transfer token

            if token_balance >= amount_in_wei:
                # Kirim token jika saldo cukup
                print(f"Mengirim token dengan gas_price: {web3.from_wei(gas_price, 'gwei')} gwei...")
                send_token(token_address, amount_in_wei)
            else:
                print("Saldo token tidak cukup untuk mengirim.")

            # Tunggu 0.1 detik sebelum pengecekan berikutnya
            time.sleep(0.1)

        except Exception as e:
            print(f"Terjadi kesalahan: {e}")
            # Tunggu 0.1 detik sebelum mencoba lagi jika terjadi kesalahan
            time.sleep(0.1)

# Contoh penggunaan
if __name__ == "__main__":
    main_loop()
