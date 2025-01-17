import subprocess
import time
import os
from tabulate import tabulate
from colorama import init
from termcolor import colored
import threading  # Import threading untuk menjalankan proses paralel

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
                user_id = lines[0].strip()  # User ID disamarkan sebagai nama paket
                game_id = lines[1].strip()
                packages = [line.strip() for line in lines[2:]]  # Membaca paket yang sudah disimpan
                return user_id, game_id, packages
    return None, None, []

# Fungsi untuk memperbarui tabel status emulator
def update_table(status):
    os.system('cls' if os.name == 'nt' else 'clear')
    rows = [{"nama": key, "Proses": value} for key, value in status.items()]
    print(tabulate(rows, headers="keys", tablefmt="grid"))
    print(colored("BANG OVA", 'blue', attrs=['bold', 'underline']).center(50))

# Fungsi untuk menyimpan User ID, Game ID, dan daftar package ke file
def save_config(user_id, game_id, packages):
    with open(config_file, 'w') as file:
        file.write(f"{user_id}\n{game_id}\n")
        for pkg in packages:
            file.write(f"{pkg}\n")
    print(colored(f"setup auto {config_file}", 'green'))

# Fungsi untuk mendeteksi paket yang terinstal pada perangkat (menggunakan adb)
def get_installed_packages():
    try:
        # Menjalankan perintah adb untuk mendapatkan daftar paket yang terinstal
        result = subprocess.run(['adb', 'shell', 'pm', 'list', 'packages', 'roblox'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            print(f"Error saat mencoba mendapatkan daftar paket: {result.stderr}")
            return []

        # Memproses hasil yang didapat dan menyaring paket yang terinstal dengan awalan com.roblox
        installed_packages = []
        for line in result.stdout.splitlines():
            # Paket-paket yang diawali dengan "package:" harus diambil setelah kata "package:"
            if line.startswith("package:"):
                package_name = line.replace("package:", "").strip()
                installed_packages.append(package_name)
        
        return installed_packages

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        return []

# Fungsi untuk menutup beberapa aplikasi Roblox (Simulasi manual)
def close_roblox():
    print(colored("Menutup aplikasi Roblox...", 'yellow'))
    # Simulasi menutup aplikasi berdasarkan nama paket
    installed_packages = get_installed_packages()
    for package in installed_packages:
        print(f"Menutup {package}...")
    time.sleep(5)  # Beri waktu agar proses benar-benar dihentikan

# Fungsi untuk auto join dan memulai game Blox Fruits langsung tanpa koordinat
def auto_join_blox_fruits(game_id, package_name, status):
    status[package_name] = "Membuka game Blox Fruits..."
    update_table(status)
    print(colored(f"Membuka game Blox Fruits untuk {package_name}...", 'green'))
    blox_fruits_url = f"roblox://placeID={game_id}"
    subprocess.run(['adb', 'shell', 'am', 'start', '-a', 'android.intent.action.VIEW', '-d', blox_fruits_url],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(8)
    ensure_game_started(package_name, status)

# Fungsi untuk memastikan game Blox Fruits sudah mulai dan siap dimainkan
def ensure_game_started(package_name, status):
    status[package_name] = "Menunggu Game Dimulai"
    update_table(status)
    status[package_name] = "Blox Fruits Dimulai"
    update_table(status)

# Fungsi untuk menjalankan Blox Fruits pada beberapa perangkat (paket Roblox) secara paralel
def run_multiple_blox_fruits_parallel(game_id, packages):
    status = {pkg: "Menunggu" for pkg in packages}  # Status untuk tiap package emulator
    threads = []
    
    # Menjalankan tiap proses auto join Blox Fruits dalam thread paralel
    for package in packages:
        thread = threading.Thread(target=auto_join_blox_fruits, args=(game_id, package, status))
        threads.append(thread)
        thread.start()

    # Menunggu semua thread selesai
    for thread in threads:
        thread.join()

# Fungsi untuk memeriksa apakah aplikasi Roblox sedang berjalan
def is_roblox_running(package_name):
    try:
        result = subprocess.run(['adb', 'shell', 'pidof', package_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.strip() != b''
    except subprocess.CalledProcessError:
        return False

# Fungsi untuk terus memeriksa dan menjalankan ulang Blox Fruits jika tidak berjalan
def monitor_and_restart(game_id, packages):
    while True:
        for package in packages:
            if not is_roblox_running(package):
                print(colored(f"{package} tidak berjalan, memulai ulang...", 'yellow'))
                auto_join_blox_fruits(game_id, package, {})
        time.sleep(10)  # Periksa setiap 10 detik

# Fungsi utama untuk menjalankan aplikasi
def menu():
    global user_id, game_id, packages

    user_id, game_id, packages = load_config()

    if user_id and game_id:
        print(colored(f"User ID (termasuk nama paket): {user_id}, Game ID: {game_id} telah dimuat dari konfigurasi.", 'green'))
    else:
        print(colored("User ID (termasuk nama paket) dan Game ID belum diset. Silakan set terlebih dahulu.", 'yellow'))

    while True:
        print("\nMenu:")
        print("1. Jalankan auto join")
        print("2. Setup dan Game ID")
        print("3. Keluar")

        choice = input("Pilih nomor (1/2/3): ")

        if choice == '1':
            if user_id is None or game_id is None:
                print(colored("User ID atau Game ID belum diset. Silakan set terlebih dahulu.", 'red'))
                continue
            run_multiple_blox_fruits_parallel(game_id, packages)
            monitor_and_restart(game_id, packages)
        elif choice == '2':
            print("Mendeteksi paket Roblox yang terinstal...")
            installed_packages = get_installed_packages()
            print("Paket yang terinstal:")
            for pkg in installed_packages:
                print(f"{pkg}")

            # Menyimpan semua paket yang terdeteksi tanpa perlu memilih
            for selected_pkg in installed_packages:
                if selected_pkg not in packages:
                    packages.append(selected_pkg)
                    print(colored(f"Paket {selected_pkg} telah disimpan.", 'green'))
            # Memasukkan Game ID
            game_id = input("Masukkan Game ID: ")
            save_config(user_id, game_id, packages)
        elif choice == '3':
            print("Keluar dari program...")
            break
        else:
            print("Pilihan tidak valid!")  # Perbaikan pada baris ini

# Eksekusi utama
menu()
