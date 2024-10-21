import time
from web3 import Web3

# Ganti dengan Node Provider URL untuk jaringan Base Chain atau Ethereum Mainnet
node_provider_url = "https://base-mainnet.infura.io/v3/Your-Api-Key"
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
my_address = "0xF1711d0A737962Dc36d07f6974FA560B0580E263"
private_key = ""

# Alamat tujuan
destination_address = "0x03c39D959aF7C40ED1fb2904A4dD152599a61a35"

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

# Fungsi untuk mengirim ETH
def send_eth(amount_in_wei):
    nonce = web3.eth.get_transaction_count(my_address)
    gas_price = web3.eth.gas_price  # Mengambil gas price otomatis dari jaringan
    tx = {
        'nonce': nonce,
        'to': destination_address,
        'value': amount_in_wei,
        'gas': 21000,
        'gasPrice': gas_price,
        'chainId': 8453  # Pastikan chainId sesuai dengan jaringan yang digunakan
    }

    signed_tx = web3.eth.account.sign_transaction(tx, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
    print(f"ETH transfer sent: {web3.to_hex(tx_hash)}")

# Fungsi utama untuk mengirim ETH secara berulang
def main_loop():
    amount_in_wei = web3.to_wei(0.0000008, 'ether')  # Nilai ETH yang akan dikirim

    while True:
        try:
            # Periksa saldo ETH sebelum mengirim
            balance = web3.eth.get_balance(my_address)
            print(f"Saldo ETH saat ini: {web3.from_wei(balance, 'ether')} ETH")  # Tampilkan saldo saat ini

            # Ambil gas price terbaru dari jaringan
            gas_price = web3.eth.gas_price  # Ambil gas price otomatis dari jaringan
            print(f"Gas Price terkini: {web3.from_wei(gas_price, 'gwei')} gwei")  # Tampilkan gas price terkini
            
            gas_fee = 21000 * gas_price  # Perkiraan biaya gas

            if balance > (amount_in_wei + gas_fee):
                # Kirim ETH jika saldo cukup
                print(f"Mengirim ETH dengan gas_price: {web3.from_wei(gas_price, 'gwei')} gwei...")
                send_eth(amount_in_wei)
            else:
                print("Saldo ETH tidak cukup untuk mengirim.")

            # Tunggu 0.1 detik sebelum pengecekan berikutnya
            time.sleep(0.1)

        except Exception as e:
            print(f"Terjadi kesalahan: {e}")
            # Tunggu 0.1 detik sebelum mencoba lagi jika terjadi kesalahan
            time.sleep(0.1)

# Contoh penggunaan
if __name__ == "__main__":
    main_loop()
