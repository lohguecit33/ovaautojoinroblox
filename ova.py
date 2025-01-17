import os
import glob
from tabulate import tabulate
from colorama import init
from termcolor import colored
import threading
import time
import subprocess  # Pastikan subprocess diimpor

# Inisialisasi Colorama untuk pewarnaan teks
init(autoreset=True)

# Nama file untuk menyimpan User ID, Game ID, dan daftar package
config_file = "roblox_config.txt"

# Fungsi untuk memuat User ID, Game ID, dan daftar package yang disimpan dari file
def load_config():
    if os.path.exists(config_file):
        with open(config_file, 'r') as file:
            lines = file.readlines()
            if len(lines) >= 2:
                user_id = lines[0].strip()
                game_id = lines[1].strip()
                packages = [line.strip() for line in lines[2:]]
                return user_id, game_id, packages
    return None, None, []

# Fungsi untuk menyimpan User ID, Game ID, dan daftar package ke file
def save_config(user_id, game_id, packages):
    with open(config_file, 'w') as file:
        file.write(f"{user_id}\n{game_id}\n")
        for pkg in packages:
            file.write(f"{pkg}\n")
    print(colored(f"Konfigurasi disimpan ke {config_file}", 'green'))

# Fungsi untuk memperbarui tabel status emulator
def update_table(status):
    os.system('cls' if os.name == 'nt' else 'clear')
    rows = [{"Nama Paket": key, "Status": value} for key, value in status.items()]
    print(tabulate(rows, headers="keys", tablefmt="grid"))
    print(colored("BANG OVA", 'blue', attrs=['bold', 'underline']).center(50))

# Fungsi untuk auto join ke game Blox Fruits tanpa adb
def auto_join_blox_fruits(game_id, package_name, status):
    status[package_name] = "Membuka game Blox Fruits..."
    update_table(status)
    print(colored(f"Membuka game Blox Fruits untuk {package_name} dengan Game ID {game_id}...", 'green'))

    # Simulasi peluncuran game menggunakan URL
    blox_fruits_url = f"roblox://placeID={game_id}"
    command = ['am', 'start', '-a', 'android.intent.action.VIEW', '-d', blox_fruits_url]

    # Log perintah untuk debugging (tanpa adb)
    print(colored(f"Menjalankan perintah: {' '.join(command)}", 'cyan'))

    # Simulasi menjalankan perintah
    time.sleep(2)  # Simulasi waktu eksekusi
    print(colored("Perintah berhasil dijalankan (simulasi).", 'green'))

    # Simulasi memastikan game dimulai
    time.sleep(6)
    ensure_game_started(package_name, status)

# Fungsi untuk memastikan game Blox Fruits sudah mulai dan siap dimainkan
def ensure_game_started(package_name, status):
    status[package_name] = "Menunggu Game Dimulai"
    update_table(status)
    time.sleep(2)
    status[package_name] = "Blox Fruits Dimulai"
    update_table(status)

# Fungsi untuk menjalankan auto join pada beberapa perangkat secara paralel
def run_multiple_blox_fruits_parallel(game_id, packages):
    status = {pkg: "Menunggu" for pkg in packages}
    threads = []
    for package in packages:
        thread = threading.Thread(target=auto_join_blox_fruits, args=(game_id, package, status))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

# Fungsi untuk mendeteksi paket Roblox yang terinstal menggunakan ADB
def get_installed_packages():
    # Direktori yang umum untuk aplikasi di Android (tanpa root)
    package_dirs = [
        "/data/app/",
        "/system/app/",
        "/system/priv-app/"
    ]
    installed_packages = []
    
    # Menelusuri setiap direktori untuk mencari paket Roblox
    for package_dir in package_dirs:
        if os.path.exists(package_dir):
            try:
                # Gunakan glob untuk mencari folder yang dimulai dengan 'com.roblox'
                installed_packages += glob.glob(os.path.join(package_dir, "com.roblox*"))
            except PermissionError:
                print(f"Permission denied saat mengakses {package_dir}.")
            except FileNotFoundError:
                print(f"Direktori {package_dir} tidak ditemukan.")
    
    if installed_packages:
        print("Paket Roblox yang terdeteksi:")
        for pkg in installed_packages:
            print(f" - {pkg}")
    else:
        print("Tidak ada paket Roblox yang terdeteksi.")
    
    return installed_packages

# Panggil fungsi untuk melihat hasilnya
get_installed_packages()

# Fungsi utama untuk menjalankan menu
def menu():
    global user_id, game_id, packages

    user_id, game_id, packages = load_config()

    if user_id and game_id:
        print(colored(f"User ID: {user_id}, Game ID: {game_id} telah dimuat dari konfigurasi.", 'green'))
    else:
        print(colored("User ID dan Game ID belum diset. Silakan set terlebih dahulu.", 'yellow'))

    while True:
        print("\nMenu:")
        print("1. Jalankan auto join")
        print("2. Setup User ID dan Game ID")
        print("3. Auto setup paket Roblox")
        print("4. Keluar")

        choice = input("Pilih nomor (1/2/3/4): ")

        if choice == '1':
            if user_id is None or game_id is None:
                print(colored("User ID atau Game ID belum diset. Silakan set terlebih dahulu.", 'red'))
                continue
            run_multiple_blox_fruits_parallel(game_id, packages)
        elif choice == '2':
            # Memasukkan User ID
            user_id = input("Masukkan User ID: ")
            # Memasukkan Game ID
            game_id = input("Masukkan Game ID: ")
            save_config(user_id, game_id, packages)
        elif choice == '3':
            # Auto setup paket
            packages = get_installed_packages()
            if packages:
                print(colored("Paket Roblox yang terdeteksi:", 'green'))
                for pkg in packages:
                    print(f" - {pkg}")
            else:
                print(colored("Tidak ada paket Roblox yang terdeteksi.", 'red'))
            save_config(user_id, game_id, packages)
        elif choice == '4':
            print("Keluar dari program...")
            break
        else:
            print("Pilihan tidak valid!")

# Eksekusi utama
menu()
