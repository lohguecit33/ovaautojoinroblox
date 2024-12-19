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

# Fungsi untuk memeriksa apakah game Blox Fruits sudah dimulai
def is_blox_fruits_running():
    result = subprocess.run(['adb', 'shell', 'pidof', 'com.roblox.client'], stdout=subprocess.PIPE)
    return result.stdout.strip() != b''

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
        if is_blox_fruits_running():
            press_start_button_multiple_times()  # Menekan tombol Start 5 kali
            return True
        time.sleep(5)
    print(colored("Game Blox Fruits tidak dimulai. Coba lagi.", 'red'))
    return False

# Fungsi untuk menampilkan tabel status Roblox dan Blox Fruits (disatukan)
def display_process_table(user_id, game_id):
    roblox_status = "Berjalan" if is_roblox_running() else "Tidak Berjalan"
    blox_fruits_status = "Dalam Game Blox Fruits" if is_blox_fruits_running() else "Tidak Di Dalam Game"

    table = [
        ["Proses Roblox (Blox Fruits)", f"{roblox_status}, {blox_fruits_status}"],
        ["User ID", user_id if user_id else "Tidak Ditemukan"],
        ["Game ID", game_id if game_id else "Tidak Ditemukan"]
    ]

    os.system('cls' if os.name == 'nt' else 'clear')
    print(tabulate(table, headers=["Proses", "Status"], tablefmt="grid"))

# Fungsi untuk mengecek dan menyiapkan User ID dan Game ID
def set_user_and_game_id():
    global user_id, game_id
    user_id = input("Masukkan User ID (username Roblox): ")
    print(f"User ID telah diatur ke: {user_id}")

    game_id = input("Masukkan Game ID untuk Blox Fruits: ")
    print(f"Game ID telah diatur ke: {game_id}")

    save_config(user_id, game_id)

# Fungsi untuk memastikan Roblox tetap berjalan dan restart sesuai interval waktu yang ditentukan
def ensure_roblox_running_with_interval(interval_minutes):
    interval_seconds = interval_minutes * 60
    start_time = time.time()

    while True:
        elapsed_time = time.time() - start_time

        # Cek apakah sudah waktunya untuk restart
        if elapsed_time >= interval_seconds:
            print(colored(f"Interval {interval_minutes} menit telah berlalu. Memulai ulang Roblox...", 'yellow'))
            run_roblox()
            auto_join_blox_fruits(game_id)
            ensure_game_started()
            press_start_button_multiple_times()  # Tekan Start beberapa kali setelah restart
            start_time = time.time()  # Reset waktu mulai

        # Cek apakah Roblox keluar atau force close
        if not is_roblox_running():
            print(colored("Roblox terdeteksi keluar atau force close. Memulai ulang...", 'red'))
            run_roblox()
            auto_join_blox_fruits(game_id)
            ensure_game_started()
            press_start_button_multiple_times()  # Tekan Start beberapa kali setelah restart
            start_time = time.time()  # Reset waktu mulai

        time.sleep(10)  # Cek setiap 10 detik

# Fungsi utama untuk menjalankan aplikasi
def menu():
    global user_id, game_id

    user_id, game_id = load_config()

    if user_id and game_id:
        print(colored(f"User ID: {user_id}, Game ID: {game_id} telah dimuat dari konfigurasi.", 'green'))
    else:
        print(colored("User ID dan Game ID belum diset. Silakan pilih 2 untuk menyetelnya.", 'yellow'))

    while True:
        display_process_table(user_id, game_id)

        print(colored("\nMenu Utama:", 'blue'))
        print("1. Set Interval Restart Roblox dan Auto Join ke Blox Fruits")
        print("2. Set User ID dan Game ID")
        print("3. Exit")

        choice = input("Pilih nomor (1/2/3): ")

        if choice == '1':
            # Menambahkan menu untuk memilih waktu restart sebelum memulai Roblox
            while True:
                try:
                    interval_minutes = int(input("Masukkan waktu restart Roblox dalam menit (misalnya 5): "))
                    print(colored(f"Roblox akan restart setiap {interval_minutes} menit.", 'green'))
                    break
                except ValueError:
                    print(colored("Input tidak valid. Harap masukkan angka.", 'red'))

            if user_id is None or game_id is None:
                print(colored("User ID atau Game ID belum diset. Silakan pilih 2 untuk menyetelnya.", 'red'))
            else:
                print(colored("Memulai Roblox dan Blox Fruits...", 'green'))
                run_roblox()
                auto_join_blox_fruits(game_id)
                ensure_game_started()
                press_start_button_multiple_times()  # Tekan Start beberapa kali setelah game dimulai

                # Menjalankan fungsi untuk memastikan Roblox berjalan dan restart sesuai interval
                ensure_roblox_running_with_interval(interval_minutes)

        elif choice == '2':
            set_user_and_game_id()

        elif choice == '3':
            print(colored("Keluar...", 'red'))
            exit(0)

        else:
            print(colored("Pilihan tidak valid, kembali ke menu...", 'yellow'))

# Main execution
menu()
