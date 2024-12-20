import subprocess
import time
import os
from termcolor import colored
from tabulate import tabulate
from colorama import init

# Inisialisasi Colorama untuk pewarnaan teks
init(autoreset=True)

# Nama file untuk menyimpan User ID dan Game ID
config_file = "roblox_config.txt"

# Fungsi untuk memuat User ID dan Game ID dari file
def load_config():
    if os.path.exists(config_file):
        with open(config_file, 'r') as file:
            lines = file.readlines()
            if len(lines) >= 2:
                user_id = lines[0].strip()
                game_id = lines[1].strip()
                return user_id, game_id
    return None, None

# Fungsi untuk menyimpan User ID dan Game ID ke file
def save_config(user_id, game_id):
    with open(config_file, 'w') as file:
        file.write(f"{user_id}\n{game_id}\n")
    print(colored(f"User ID dan Game ID telah disimpan di {config_file}", 'green'))

# Fungsi untuk memeriksa apakah aplikasi Roblox sedang berjalan
def is_roblox_running():
    result = subprocess.run(['adb', 'shell', 'pidof', 'com.roblox.client'], stdout=subprocess.PIPE)
    return result.stdout.strip() != b''

# Fungsi untuk menutup Roblox
def close_roblox():
    print(colored("Menutup aplikasi Roblox...", 'yellow'))
    subprocess.run(['adb', 'shell', 'am', 'force-stop', 'com.roblox.client'])
    time.sleep(5)  # Beri waktu agar proses benar-benar dihentikan

# Fungsi untuk menjalankan Roblox
def run_roblox():
    subprocess.run(['adb', 'shell', 'am', 'start', '-n', 'com.roblox.client/.startup.ActivitySplash'])
    time.sleep(9)  # Menunggu beberapa detik agar Roblox dapat diluncurkan

# Fungsi untuk auto join dan memulai game Blox Fruits langsung tanpa koordinat
def auto_join_blox_fruits(game_id):
    print(colored("Membuka game Blox Fruits...", 'green'))
    subprocess.run(['adb', 'shell', 'am', 'start', '-n', 'com.roblox.client/.ActivityProtocolLaunch', 
                    '-d', f'https://www.roblox.com/games/{game_id}'])
    time.sleep(8)  # Menunggu beberapa detik agar game dimulai
    ensure_game_started()

# Fungsi untuk menekan tombol Start di game Blox Fruits (menggunakan ADB) beberapa kali
def press_start_button_multiple_times():
    print(colored("Menekan tombol Start di Blox Fruits secara bergantian di 2 koordinat...", 'green'))
    
    # Koordinat pertama
    x1, y1 = 550, 481
    # Koordinat kedua
    x2, y2 = 550, 380

    for _ in range(5):  # Menekan tombol sebanyak 5 kali
        # Klik di koordinat pertama
        subprocess.run(['adb', 'shell', 'input', 'tap', str(x1), str(y1)])
        time.sleep(1)  # Jeda 1 detik
        
        # Klik di koordinat kedua
        subprocess.run(['adb', 'shell', 'input', 'tap', str(x2), str(y2)])
        time.sleep(1)  # Jeda 1 detik

# Fungsi untuk memastikan game Blox Fruits sudah mulai dan siap dimainkan
def ensure_game_started():
    print(colored("Memastikan game Blox Fruits sudah dimulai...", 'green'))
    for _ in range(5):  # Melakukan pengecekan 5 kali
        if is_roblox_running():
            press_start_button_multiple_times()  # Menekan tombol Start 5 kali
            return True
        time.sleep(5)
    print(colored("Game Blox Fruits tidak dimulai. Coba lagi.", 'red'))
    return False

# Fungsi untuk memastikan Roblox tetap berjalan dan restart sesuai interval waktu yang ditentukan
def ensure_roblox_running_with_interval(interval_minutes):
    interval_seconds = interval_minutes * 60
    start_time = time.time()

    while True:
        elapsed_time = time.time() - start_time

        if elapsed_time >= interval_seconds or not is_roblox_running():
            print(colored(f"Memulai ulang Roblox...", 'yellow'))
            close_roblox()
            run_roblox()
            auto_join_blox_fruits(game_id)
            ensure_game_started()
            start_time = time.time()  # Reset waktu mulai

        time.sleep(10)  # Cek setiap 10 detik

# Fungsi utama untuk menjalankan aplikasi
def menu():
    global user_id, game_id

    user_id, game_id = load_config()

    if user_id and game_id:
        print(colored(f"User ID: {user_id}, Game ID: {game_id} telah dimuat dari konfigurasi.", 'green'))
    else:
        print(colored("User ID dan Game ID belum diset. Silakan set terlebih dahulu.", 'yellow'))

    while True:
        print("\nMenu:")
        print("1. Atur interval restart dan jalankan ulang Roblox")
        print("2. Set User ID dan Game ID")
        print("3. Keluar")

        choice = input("Pilih nomor (1/2/3): ")

        if choice == '1':
            if user_id is None or game_id is None:
                print(colored("User ID atau Game ID belum diset. Silakan set terlebih dahulu.", 'red'))
                continue
            interval_minutes = int(input("Masukkan interval waktu (dalam menit): "))
            ensure_roblox_running_with_interval(interval_minutes)
        elif choice == '2':
            user_id = input("Masukkan User ID: ")
            game_id = input("Masukkan Game ID: ")
            save_config(user_id, game_id)
        elif choice == '3':
            print("Keluar dari program...")
            break
        else:
            print("Pilihan tidak valid!")

# Eksekusi utama
menu()
