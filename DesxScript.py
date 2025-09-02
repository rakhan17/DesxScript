import os
import time
import random
import sys
import platform
import subprocess
import importlib.util
from datetime import timedelta

# --- FUNGSI BARU UNTUK CEK & INSTALASI DEPENDENSI ---
def check_and_install_dependencies(missing_packages):
    """Menawarkan untuk menginstall dependensi yang hilang."""
    yellow, reset, cyan, green, red = '\033[93m', '\033[0m', '\033[96m', '\033[92m', '\033[91m'
    print(f"{yellow}Peringatan: Script ini memerlukan paket Python tambahan.{reset}")
    print(f"Paket yang hilang: {cyan}{', '.join(missing_packages)}{reset}")
    
    try:
        choice = input("Apakah Anda ingin menginstallnya sekarang? (Y/n): ").lower().strip()
    except KeyboardInterrupt:
        print("\nInstalasi dibatalkan oleh pengguna.")
        sys.exit(1)

    if choice == 'y':
        print(f"Memulai instalasi {', '.join(missing_packages)}...")
        for package in missing_packages:
            try:
                # Menggunakan sys.executable memastikan pip yang benar yang digunakan
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            except subprocess.CalledProcessError:
                print(f"{red}Error: Gagal menginstall {package}. Silakan install manual.{reset}")
                sys.exit(1)
        print(f"\n{green}Instalasi berhasil. Silakan jalankan kembali script ini.{reset}")
        sys.exit(0) # Keluar agar user menjalankan ulang dengan environment yang bersih
    else:
        print("Instalasi dibatalkan. Program akan keluar.")
        sys.exit(1)


# Fungsi untuk membersihkan layar terminal
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Kelas untuk menyimpan kode warna ANSI
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[01m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    LIGHT_GREEN = '\033[92m'
    DARK_GREEN = '\033[32m'
    GRAY = '\033[90m'

COLOR_PALETTE = [Colors.RED, Colors.GREEN, Colors.YELLOW, Colors.BLUE, Colors.MAGENTA, Colors.CYAN, Colors.WHITE]

# ASCII Art untuk judul "DesxScript"
TITLE_ART = f"""
{Colors.BOLD}
██████╗ ███████╗███████╗██╗  ██╗███████╗ ██████╗██████╗ ██╗██████╗ ████████╗
██╔══██╗██╔════╝██╔════╝╚██╗██╔╝██╔════╝██╔════╝██╔══██╗██║██╔══██╗╚══██╔══╝
██║  ██║█████╗  ███████╗ ╚███╔╝ ███████╗██║     ██████╔╝██║██████╔╝   ██║   
██║  ██║██╔══╝  ╚════██║ ██╔██╗ ╚════██║██║     ██══██╗██║██╔═══╝    ██║   
██████╔╝███████╗███████║██╔╝ ██╗███████║╚██████╗██║  ██║██║██║        ██║   
╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝╚═╝        ╚═╝   
{Colors.RESET}
"""

# --- ANIMASI MATRIX ---
def run_matrix_animation():
    try:
        term_width, term_height = os.get_terminal_size()
        title_height = TITLE_ART.count('\n') + 2
        animation_height = max(1, term_height - title_height)
        chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        columns = [random.randint(0, animation_height) for _ in range(term_width)]
        
        for _ in range(100): # Batasi iterasi agar tidak berjalan selamanya
            clear_screen()
            title_color = random.choice(COLOR_PALETTE)
            print(title_color + TITLE_ART + Colors.RESET)
            frame = [[' ' for _ in range(term_width)] for _ in range(animation_height)]
            for i in range(term_width):
                char = random.choice(chars)
                head_y = columns[i]
                if 0 <= head_y < animation_height: frame[head_y][i] = f"{Colors.WHITE}{char}{Colors.RESET}"
                for j in range(1, 10):
                    trail_y, dark_trail_y = head_y - j, head_y - j - 5
                    if 0 <= trail_y < animation_height: frame[trail_y][i] = f"{Colors.LIGHT_GREEN}{random.choice(chars)}{Colors.RESET}"
                    if 0 <= dark_trail_y < animation_height: frame[dark_trail_y][i] = f"{Colors.DARK_GREEN}{random.choice(chars)}{Colors.RESET}"
                columns[i] = (columns[i] + 1) % animation_height if animation_height > 0 else 0
                if columns[i] == 0 and random.random() < 0.02: columns[i] = random.randint(0, animation_height) if animation_height > 0 else 0
            print("\n".join("".join(row) for row in frame))
            print("\n" + "="*80); print(f"{Colors.BOLD}{Colors.YELLOW}Tekan [Ctrl+C] untuk membuka menu script".center(90)); print("="*80)
            time.sleep(0.05)
    except (KeyboardInterrupt, OSError): return

# --- FUNGSI VALIDASI INPUT ---
def get_validated_input(prompt, validation_func, error_message):
    while True:
        user_input = input(prompt)
        if validation_func(user_input): return user_input
        else: print(f"{Colors.RED}{error_message}{Colors.RESET}")

validate_username = lambda u: u.startswith('@') and len(u) > 1
validate_number = lambda n: n.isdigit() and int(n) > 0
validate_url = lambda u: u.startswith('http://') or u.startswith('https://')
validate_process_name = lambda p: p.endswith('.exe') and len(p) > 4
validate_wallet_address = lambda a: a.startswith('0x') and len(a) == 42
validate_audio_file = lambda f: f.endswith(('.mp3', '.wav', '.flac'))
validate_ip = lambda ip: len(ip.split('.')) == 4 and all(p.isdigit() and 0 <= int(p) <= 255 for p in ip.split('.'))
validate_not_empty = lambda s: len(s.strip()) > 0
validate_bssid = lambda b: len(b) == 17 and b.count(':') == 5

def bytes_to_gb(b): return f"{b / (1024**3):.2f} GB"

# --- HELPER & SIMULASI PROSES (DIROMBAK TOTAL) ---
STEP_LIBRARY = {
    'INIT': ["Menginisialisasi koneksi", "Memverifikasi target", "Memuat payload primer", "Mengautentikasi sesi", "Menyiapkan environment", "Membaca konfigurasi"],
    'SCAN': ["Memindai port terbuka", "Mencari kerentanan umum", "Enumerasi subdomain", "Mendeteksi versi layanan", "Memeriksa header HTTP", "Mencari file sensitif"],
    'EXPLOIT': ["Mengeksploitasi buffer overflow", "Mengirim paket berbahaya", "Mem-bypass firewall", "Menginjeksi SQL payload", "Mencoba XSS payload", "Mendapatkan remote shell"],
    'DATA': ["Mengekstrak hash password", "Mendekripsi file konfigurasi", "Mengompresi log server", "Mencari data kredensial", "Mengunduh database", "Menganalisis traffic jaringan"],
    'CLEANUP': ["Menghapus jejak dari log", "Memutus koneksi aman", "Mengembalikan state sistem", "Menghapus file sementara", "Mematikan remote shell"],
    'GAME': ["Mencari process ID game", "Menginjeksi DLL ke memori", "Mem-bypass anti-cheat", "Hooking ke renderer D3D11", "Mencari pointer statis ammo", "Mengunci nilai memori"],
    'WIFI': ["Mengaktifkan mode monitor", "Menunggu WPA2 handshake", "Mengirim paket Deauth", "Memulai dictionary attack", "Mengeksploitasi WPS Pixie Dust", "Mendapatkan PSK dari AP"]
}

def generate_steps(categories):
    """Membangun daftar langkah simulasi yang bervariasi."""
    all_steps = []
    for category, count in categories:
        # Ambil 'count' langkah acak dari kategori yang sesuai
        if count > len(STEP_LIBRARY[category]):
            # Jika butuh lebih banyak dari yang tersedia, ulangi saja
            choices = random.choices(STEP_LIBRARY[category], k=count)
        else:
            choices = random.sample(STEP_LIBRARY[category], k=count)
        
        # Tambahkan durasi acak untuk setiap langkah
        for choice in choices:
            duration = random.uniform(0.8, 2.5)
            all_steps.append((duration, choice))
    return all_steps

def run_simulation_steps(steps_config):
    """Menjalankan simulasi dengan langkah, durasi, dan delay yang sangat acak."""
    actual_steps = generate_steps(steps_config)
    for duration, text in actual_steps:
        spinner = ['-', '\\', '|', '/']
        start_time = time.time()
        
        # Tentukan berapa kali proses ini akan 'stuck'
        num_delays = random.randint(0, 5) 
        delay_events = []
        if num_delays > 0:
            for _ in range(num_delays):
                delay_events.append({
                    'percent': random.randint(20, 90),
                    'duration': random.uniform(1.5, 4.0),
                    'triggered': False,
                    'silent': random.random() < 0.5 # 50% kemungkinan delay senyap
                })
        delay_events.sort(key=lambda x: x['percent']) # Pastikan delay terjadi berurutan

        while True:
            elapsed = time.time() - start_time
            if elapsed >= duration:
                progress = 100
                bar = '█' * 50
                sys.stdout.write(f"\r{Colors.GREEN}✓ {text}... [{Colors.GREEN}{bar}{Colors.RESET}] {progress}%{Colors.RESET}{' ' * 10}\n")
                sys.stdout.flush()
                break
            
            progress = int((elapsed / duration) * 100)

            # Cek apakah ada event delay yang harus ditangani
            for event in delay_events:
                if not event['triggered'] and progress >= event['percent']:
                    event['triggered'] = True
                    progress = event['percent']
                    bar = '█' * int(progress / 2) + ' ' * (50 - int(progress / 2))
                    # PERUBAHAN: Spinner menjadi kuning, tapi progress bar tetap hijau saat delay
                    sys.stdout.write(f"\r{Colors.YELLOW}> {text}... [{Colors.GREEN}{bar}{Colors.RESET}] {progress}% ")
                    sys.stdout.flush()

                    if not event['silent']:
                        messages = ["KONEKSI TIMEOUT...", "PAYLOAD DITOLAK...", "MENUNGGU RESPON...", "LATENSI TINGGI...", "MENSTABILKAN KONEKSI..."]
                        sys.stdout.write(f"\n{Colors.YELLOW}[!] {random.choice(messages)}{Colors.RESET}")
                        sys.stdout.flush()
                    
                    time.sleep(event['duration'])
                    
                    if not event['silent']:
                        sys.stdout.write("\033[F\033[K")
                        sys.stdout.flush()
                    
                    duration += event['duration'] # Tambahkan durasi delay ke total durasi proses
            
            bar = '█' * int(progress / 2) + ' ' * (50 - int(progress / 2))
            spin_char = spinner[int(time.time() * 10) % 4]
            sys.stdout.write(f"\r{Colors.CYAN}{spin_char} {text}... [{Colors.GREEN}{bar}{Colors.RESET}] {progress}% ")
            sys.stdout.flush()
            time.sleep(0.05)
        time.sleep(0.3)

# --- FUNGSI UNTUK STATISTIK SISTEM (DIROMBAK) ---
def get_os_details(uname):
    system = uname.system
    if system == "Windows": return f"Windows {uname.release}"
    elif system == "Darwin":
        ver = platform.mac_ver()
        try:
            name_bytes = subprocess.check_output(['sw_vers', '-productName'])
            name = name_bytes.decode('utf-8').strip()
            return f"{name} {ver[0]}"
        except Exception: return f"macOS {ver[0]}"
    elif system == "Linux":
        try:
            with open("/etc/os-release") as f:
                for line in f:
                    if line.startswith("PRETTY_NAME="): return line.split('"')[1]
        except Exception: return f"{uname.system} {uname.release}"
    return f"{uname.system} {uname.release}"

def format_info(data, cols=2):
    """Format data menjadi beberapa kolom yang rapi."""
    if not data: return ""
    max_len = max(len(key) for key, val in data) + 2
    lines = []
    
    # Coba dapatkan lebar terminal, fallback jika gagal
    try:
        term_width = os.get_terminal_size().columns
    except OSError:
        term_width = 80 # Default
        
    col_width = (term_width // cols) - 2
    
    for i in range(0, len(data), cols):
        row_items = data[i:i+cols]
        line = ""
        for key, val in row_items:
            formatted_key = f"{Colors.WHITE}{key.ljust(max_len)}{Colors.RESET}: "
            formatted_val = f"{Colors.CYAN}{str(val)}{Colors.RESET}"
            line += (formatted_key + formatted_val).ljust(col_width)
        lines.append(line)
    return "\n".join(lines)

def display_system_info_screen():
    clear_screen()
    print(f"{Colors.BOLD}{Colors.YELLOW}Mengumpulkan informasi sistem, harap tunggu...{Colors.RESET}")
    
    uname = platform.uname()
    cpu_info = cpuinfo.get_cpu_info()
    svmem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    
    device_os = [
        ("Pabrikan", cpu_info.get('vendor_id_raw', 'N/A')),
        ("Model Internal", uname.node),
        ("Versi OS", get_os_details(uname)),
        ("Arsitektur", cpu_info.get('arch', 'N/A')),
        ("ID Build OS", uname.version.split(' ')[0]),
        ("Versi Kernel", uname.release),
        ("Waktu Aktif (Uptime)", str(timedelta(seconds=int(time.time() - psutil.boot_time())))),
        ("Status Root/Jailbreak", "[Tidak Berlaku di PC]"),
    ]
    cpu_data = [
        ("Nama Chipset", cpu_info.get('brand_raw', 'N/A')),
        ("Core Fisik", psutil.cpu_count(logical=False)),
        ("Total Core", psutil.cpu_count(logical=True)),
        ("Set Instruksi", cpu_info.get('isa', 'N/A')),
        ("L1 Cache", cpu_info.get('l1_data_cache_size', 'N/A')),
        ("L2 Cache", f"{cpu_info.get('l2_cache_size', 0) // 1024} KB"),
        ("L3 Cache", f"{cpu_info.get('l3_cache_size', 0) // 1024} KB"),
        ("Fitur CPU", ', '.join([f for f in ['aes', 'neon', 'sha'] if f in cpu_info.get('flags', [])])),
    ]
    mem_data = [
        ("Total RAM", bytes_to_gb(svmem.total)),
        ("RAM Tersedia", bytes_to_gb(svmem.available)),
        ("RAM Terpakai", f"{bytes_to_gb(svmem.used)} ({svmem.percent}%)"),
        ("Total Z-RAM (Swap)", bytes_to_gb(swap.total)),
        ("Z-RAM Terpakai", f"{bytes_to_gb(swap.used)} ({swap.percent}%)"),
        ("Tipe RAM", "[Tidak Tersedia di PC]"),
    ]
    unavail_mobile = [
        ("Nama Pemasaran", "[Data Ponsel]"), ("Kode Perangkat", "[Data Ponsel]"),
        ("Nama Kode OS", "[Data Ponsel]"), ("Level Patch Keamanan", "[Data Ponsel]"),
        ("Versi Bootloader", "[Data Ponsel]"), ("Versi Baseband", "[Data Ponsel]"),
        ("Status Enkripsi", "[Data Ponsel]"), ("Platform Keamanan", "[Data Ponsel]"),
    ]

    clear_screen()
    print(f"{Colors.BOLD}{Colors.MAGENTA}--- Perangkat & OS ---{Colors.RESET}\n{format_info(device_os)}")
    print(f"\n{Colors.BOLD}{Colors.MAGENTA}--- CPU ---{Colors.RESET}\n{format_info(cpu_data)}")
    print(f"\n{Colors.BOLD}{Colors.MAGENTA}--- Memori ---{Colors.RESET}\n{format_info(mem_data)}")
    print(f"\n{Colors.BOLD}{Colors.MAGENTA}--- Penyimpanan ---{Colors.RESET}")
    partitions = psutil.disk_partitions()
    for p in partitions:
        try:
            usage = psutil.disk_usage(p.mountpoint)
            print(f"  {Colors.WHITE}{p.device} ({p.fstype}) @ {p.mountpoint}{Colors.RESET} | {Colors.GRAY}Total: {bytes_to_gb(usage.total)}, Terpakai: {bytes_to_gb(usage.used)} ({usage.percent}%){Colors.RESET}")
        except (PermissionError, FileNotFoundError): continue
    print(f"\n{Colors.BOLD}{Colors.MAGENTA}--- Jaringan ---{Colors.RESET}")
    if_addrs = psutil.net_if_addrs()
    for interface, addrs in if_addrs.items():
        print(f"  {Colors.WHITE}Interface: {interface}{Colors.RESET}")
        for addr in addrs:
            if str(addr.family) == 'AddressFamily.AF_INET': print(f"    {Colors.GRAY}IP Address: {addr.address}")
            elif str(addr.family) == 'AddressFamily.AF_PACKET': print(f"    {Colors.GRAY}MAC Address: {addr.address}")
    print(f"\n{Colors.BOLD}{Colors.MAGENTA}--- Informasi Lain (Spesifik Ponsel) ---{Colors.RESET}\n{format_info(unavail_mobile)}")
    input(f"\n{Colors.YELLOW}Tekan [Enter] untuk kembali ke menu utama...{Colors.RESET}")

# --- FUNGSI-FUNGSI SIMULASI ---
def simulate_bot_follower(script_name, option_name):
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name} ({option_name})...{Colors.RESET}\n")
    get_validated_input(f"{Colors.WHITE}Username Target: {Colors.RESET}", validate_username, "Format salah!")
    get_validated_input(f"{Colors.WHITE}Jumlah Followers: {Colors.RESET}", validate_number, "Jumlah tidak valid!")
    print("-" * 50)
    run_simulation_steps([('INIT', 3), ('EXPLOIT', 4), ('CLEANUP', 1)])
    print("-" * 50); animated_text(f"\n{Colors.GREEN}{Colors.BOLD}[+] SUKSES!{Colors.RESET}")

def simulate_web_deface(script_name, option_name):
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name} ({option_name})...{Colors.RESET}\n")
    get_validated_input(f"{Colors.WHITE}URL Target: {Colors.RESET}", validate_url, "Format URL salah!")
    print("-" * 50)
    if "Otomatis" in option_name:
        run_simulation_steps([('INIT', 4), ('SCAN', 20), ('EXPLOIT', 15), ('DATA', 3), ('CLEANUP', 3)])
    else:
        get_validated_input(f"{Colors.WHITE}Path ke file deface: {Colors.RESET}", validate_not_empty, "Path kosong!")
        run_simulation_steps([('INIT', 5), ('EXPLOIT', 10), ('CLEANUP', 2)])
    print("-" * 50); animated_text(f"\n{Colors.GREEN}{Colors.BOLD}[+] BERHASIL! Website di-deface.{Colors.RESET}")

def simulate_ddos(script_name, option_name):
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name} ({option_name})...{Colors.RESET}\n")
    get_validated_input(f"{Colors.WHITE}Target IP Address: {Colors.RESET}", validate_ip, "Format IP salah!")
    get_validated_input(f"{Colors.WHITE}Target Port: {Colors.RESET}", validate_number, "Port tidak valid!")
    print("-" * 50)
    run_simulation_steps([('INIT', 10), ('EXPLOIT', 60)])
    print("-" * 50); animated_text(f"\n{Colors.GREEN}{Colors.BOLD}[+] SERANGAN DIMULAI!{Colors.RESET}")
    
def simulate_wifi_hack(script_name, option_name):
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name} ({option_name})...{Colors.RESET}\n")
    get_validated_input(f"{Colors.WHITE}Target BSSID: {Colors.RESET}", validate_bssid, "Format BSSID salah!")
    print("-" * 50)
    run_simulation_steps([('INIT', 2), ('WIFI', 30), ('DATA', 5), ('CLEANUP', 1)])
    print("-" * 50); animated_text(f"\n{Colors.GREEN}{Colors.BOLD}[+] SUKSES! Password ditemukan.{Colors.RESET}")
    
def simulate_game_hack(script_name, option_name):
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name} ({option_name})...{Colors.RESET}\n")
    get_validated_input(f"{Colors.WHITE}Game Process Name: {Colors.RESET}", validate_process_name, "Format salah!")
    print("-" * 50)
    run_simulation_steps([('INIT', 2), ('GAME', 15), ('CLEANUP', 2)])
    print("-" * 50); animated_text(f"\n{Colors.GREEN}{Colors.BOLD}[+] SUKSES! Cheat diaktifkan.{Colors.RESET}")

def simulate_generic_script(script_name):
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name}...{Colors.RESET}\n")
    input(f"{Colors.WHITE}Masukkan Target (IP/Domain/User): {Colors.RESET}")
    # Script generik punya jumlah langkah yang sangat acak
    total_steps = random.randint(10, 80)
    print("-" * 50)
    run_simulation_steps([(random.choice(['INIT', 'SCAN', 'EXPLOIT', 'DATA']), total_steps)])
    print("-" * 50); animated_text(f"\n{Colors.GREEN}{Colors.BOLD}[+] SCRIPT DIEKSEKUSI!{Colors.RESET}")

# --- DATA UNTUK SCRIPT & OPSI-OPSINYA ---
script_options = {
    1: {'title': "Bot Follower IG/TikTok", 'func': simulate_bot_follower},
    3: {'title': "Web Deface Tool v3.1", 'func': simulate_web_deface},
    11: {'title': "DDoS Script (Layer 4/7)", 'func': simulate_ddos},
    15: {'title': "WiFi Password Extractor", 'func': simulate_wifi_hack},
    51: {'title': "Aimbot/Wallhack Injector", 'func': simulate_game_hack},
}
LINUX_ONLY_SCRIPTS = [15, 32, 66, 67, 70]
WIN_ONLY_SCRIPTS = [16]

# --- FUNGSI UTAMA & TAMPILAN MENU ---
def display_menu():
    clear_screen(); print(TITLE_ART)
    print(f"\n{Colors.BOLD}{Colors.YELLOW}AVAILABLE SCRIPTS MENU".center(90) + f"{Colors.RESET}"); print("="*80 + "\n")
    menu_items = [
        ("01", "Bot Follower IG/TikTok"), ("02", "Script Phising All Sosmed"), ("03", "Web Deface Tool v3.1"),
        ("04", "Spam OTP Call/SMS"), ("05", "VIP Access to Database"), ("06", "SQL Injection Scanner"),
        ("07", "XSS Payload Generator"), ("08", "Admin Panel Finder"), ("09", "Subdomain Enumerator"),
        ("10", "Port Scanner (Nmap)"), ("11", "DDoS Script (Layer 4/7)"), ("12", "Password Cracker (Brute)"),
        ("13", "Hash Identifier"), ("14", "Reverse Shell Generator"), ("15", "WiFi Password Extractor"),
        ("16", "Keylogger (Windows)"), ("17", "File Encryptor (Ransomware)"), ("18", "Steganography Tool"),
        ("19", "Metadata Scraper"), ("20", "Network Traffic Sniffer"), ("21", "MAC Address Spoofer"),
        ("22", "API Fuzzer"), ("23", "Directory Traversal Scan"), ("24", "Fake Identity Generator"),
        ("25", "Email Bomber"), 
        ("26", "Social Engineering Toolkit"), ("27", "RAT Builder (Remote Admin)"), ("28", "TOR Network Router"),
        ("29", "Blockchain Wallet Cracker"), ("30", "Cloud Bucket Scanner"), ("31", "Malware Sandbox Evasion"),
        ("32", "Rootkit Installer (Linux)"), ("33", "IoT Device Scanner"), ("34", "VoIP Call Interceptor"),
        ("35", "Bluetooth Skimmer"), ("36", "NFC Data Cloner"), ("37", "GPS Spoofing Tool"),
        ("38", "Drone Hijacker Script"), ("39", "Firmware Reverse Engineer"), ("40", "Credit Card Number Gen"),
        ("41", "Man-in-the-Middle Fmwk"), ("42", "Website Cloner"), ("43", "Code Obfuscator"),
        ("44", "VPN Killswitch Tester"), ("45", "DNS Cache Poisoning"), ("46", "HTTP Header Modifier"),
        ("47", "Cookie Editor/Injector"), ("48", "Automated Bug Bounty"), ("49", "AI Vulnerability Predictor"),
        ("50", "Quantum Enc Breaker(POC)"),
        ("51", "Aimbot/Wallhack Injector"), ("52", "Game Gold/Currency Hack"), ("53", "Server Lag Switcher"),
        ("54", "Anti-AFK Bot for MMO"), ("55", "Packet Editor for Games"), ("56", "Crypto Wallet Drainer"),
        ("57", "NFT Minting Bot"), ("58", "Smart Contract Exploiter"), ("59", "Blockchain Fork Tool"),
        ("60", "Mining Pool Hijacker"), ("61", "AI Voice Cloner (TTS)"), ("62", "DeepFake Video Generator"),
        ("63", "AI Model Poisoning"), ("64", "CAPTCHA Bypass w/ AI"), ("65", "Autonomous Drone Swarm"),
        ("66", "Satellite Uplink Intercept"), ("67", "Car ECU Flasher"), ("68", "Smart Lock Bypass"),
        ("69", "Power Grid Monitor"), ("70", "SCADA System Access"), ("71", "RFID Cloner"),
        ("72", "ATM Jackpotting Script"), ("73", "Social Credit Score Mod"), ("74", "Stock Market Predictor"),
        ("75", "Neuralink Interface (EXP)")
    ]
    current_os = platform.system()
    for i in range(25):
        line = ""
        for j in range(3):
            idx = i + j * 25
            if idx < len(menu_items):
                num, name = menu_items[idx]; num_int = int(num)
                color = Colors.WHITE
                if (current_os != "Linux" and num_int in LINUX_ONLY_SCRIPTS) or \
                   (current_os != "Windows" and num_int in WIN_ONLY_SCRIPTS):
                    color = Colors.RED
                prefix = "  " if j == 0 else ""
                line += f"{prefix}[{Colors.CYAN}{num}{Colors.RESET}] {color}{name.ljust(28)}{Colors.RESET}"
        print(line)
    print("\n" + "="*80)
    return menu_items

def main():
    while True:
        run_matrix_animation()
        menu_list = display_menu()
        try:
            choice = input(f"\n{Colors.YELLOW}Pilih nomor script (1-75), [S] untuk Info Sistem, atau [Q] untuk keluar: {Colors.RESET}")
            if choice.lower() == 'q':
                clear_screen(); print(f"\n{Colors.CYAN}{Colors.BOLD}Terima kasih telah menggunakan DesxScript.{Colors.RESET}\n"); break
            elif choice.lower() == 's':
                display_system_info_screen(); continue
            choice_int = int(choice)
            if not (1 <= choice_int <= len(menu_list)): raise IndexError("Pilihan di luar jangkauan")
            current_os = platform.system()
            script_name = menu_list[choice_int-1][1]
            if current_os != "Linux" and choice_int in LINUX_ONLY_SCRIPTS:
                print(f"{Colors.RED}Error: '{script_name}' hanya bisa di Linux.{Colors.RESET}"); time.sleep(3); continue
            if current_os != "Windows" and choice_int in WIN_ONLY_SCRIPTS:
                print(f"{Colors.RED}Error: '{script_name}' hanya bisa di Windows.{Colors.RESET}"); time.sleep(3); continue
            
            # Sederhanakan pemanggilan fungsi
            script_info = script_options.get(choice_int)
            if script_info and 'func' in script_info:
                # Untuk script dengan logika khusus, panggil fungsinya
                script_info['func'](script_name, "") # Opsi dikelola di dalam fungsi jika perlu
            else:
                # Untuk semua script lain, gunakan simulasi generik
                simulate_generic_script(script_name)

        except (ValueError, IndexError):
            print(f"{Colors.RED}Input tidak valid.{Colors.RESET}"); time.sleep(2)
        except Exception as e:
            print(f"{Colors.RED}Terjadi error tak terduga: {e}{Colors.RESET}"); time.sleep(3)
        input(f"\n{Colors.YELLOW}Tekan [Enter] untuk kembali ke menu utama...{Colors.RESET}")

if __name__ == "__main__":
    # Logika baru untuk memeriksa dependensi
    missing = []
    try:
        import psutil
    except ImportError:
        missing.append('psutil')
    try:
        import cpuinfo
    except ImportError:
        missing.append('py-cpuinfo')
    if platform.system() == "Windows":
        try:
            import wmi
        except ImportError:
            missing.append('WMI')

    if missing:
        check_and_install_dependencies(missing)
    
    main()


