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
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            except subprocess.CalledProcessError:
                print(f"{red}Error: Gagal menginstall {package}. Silakan install manual.{reset}")
                sys.exit(1)
        print(f"\n{green}Instalasi berhasil. Silakan jalankan kembali script ini.{reset}")
        sys.exit(0)
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
    GRAY = '\033[90m'
    LIGHT_GREEN = '\033[92m'
    DARK_GREEN = '\033[32m'

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
{Colors.RESET}{Colors.CYAN}{'versi 12.3.24'.center(88)}
{'dibuat oleh rkhnatthaya'.center(88)}{Colors.RESET}
"""

# --- ANIMASI MATRIX ---
def run_matrix_animation():
    try:
        term_width, term_height = os.get_terminal_size()
        title_height = TITLE_ART.count('\n') + 2
        animation_height = max(1, term_height - title_height)
        chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        columns = [random.randint(0, animation_height) for _ in range(term_width)]
        
        for _ in range(100):
            output_buffer = []
            title_color = random.choice(COLOR_PALETTE)
            output_buffer.append(title_color + TITLE_ART)

            frame = [[' ' for _ in range(term_width)] for _ in range(animation_height)]
            for i in range(term_width):
                char = random.choice(chars)
                head_y = columns[i]
                if 0 <= head_y < animation_height: frame[head_y][i] = f"{Colors.WHITE}{char}{Colors.RESET}"
                trail_y, dark_trail_y = head_y - 1, head_y - 6
                if 0 <= trail_y < animation_height: frame[trail_y][i] = f"{Colors.LIGHT_GREEN}{random.choice(chars)}{Colors.RESET}"
                if 0 <= dark_trail_y < animation_height: frame[dark_trail_y][i] = f"{Colors.DARK_GREEN}{random.choice(chars)}{Colors.RESET}"
                columns[i] = (columns[i] + 1) % animation_height if animation_height > 0 else 0
                if columns[i] == 0 and random.random() < 0.02: columns[i] = random.randint(0, animation_height) if animation_height > 0 else 0
            
            output_buffer.append("\n".join("".join(row) for row in frame))
            output_buffer.append("\n" + "="*80)
            output_buffer.append(f"{Colors.BOLD}{Colors.YELLOW}Tekan [Ctrl+C] untuk membuka menu script".center(90))
            output_buffer.append("="*80)
            
            clear_screen()
            print("\n".join(output_buffer))
            
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

def animated_text(text):
    for char in text: sys.stdout.write(char); sys.stdout.flush(); time.sleep(0.03)
    print()

# --- HELPER & SIMULASI PROSES ---
STEP_LIBRARY = {
    'INIT': ["Menginisialisasi koneksi", "Memverifikasi target", "Memuat payload primer", "Mengautentikasi sesi", "Menyiapkan environment", "Membaca konfigurasi", "Resolving domain ke IP"],
    'SCAN': ["Memindai port terbuka", "Mencari kerentanan umum", "Enumerasi subdomain", "Mendeteksi versi layanan", "Memeriksa header HTTP", "Mencari file sensitif", "Mendeteksi proteksi CDN"],
    'EXPLOIT': ["Mengeksploitasi buffer overflow", "Mengirim paket berbahaya", "Mem-bypass firewall", "Menginjeksi SQL payload", "Mencoba XSS payload", "Mendapatkan remote shell", "Membanjiri server dengan request HTTP"],
    'DATA': ["Mengekstrak hash password", "Mendekripsi file konfigurasi", "Mengompresi log server", "Mencari data kredensial", "Mengunduh database", "Menganalisis traffic jaringan"],
    'CLEANUP': ["Menghapus jejak dari log", "Memutus koneksi aman", "Mengembalikan state sistem", "Menghapus file sementara", "Mematikan remote shell"],
    'GAME': ["Mencari process ID game", "Menginjeksi DLL ke memori", "Mem-bypass anti-cheat", "Hooking ke renderer D3D11", "Mencari pointer statis ammo", "Mengunci nilai memori"],
    'WIFI': ["Mengaktifkan mode monitor", "Menunggu WPA2 handshake", "Mengirim paket Deauth", "Memulai dictionary attack", "Mengeksploitasi WPS Pixie Dust", "Mendapatkan PSK dari AP"]
}
DELAY_MESSAGES = {
    'GENERIC': ["LATENSI TINGGI...", "MENSTABILKAN KONEKSI...", "MENUNGGU RESPON...", "MEMPROSES DATA..."],
    'SCAN': ["TARGET MENGGANTI IP...", "WAF TERDETEKSI, MENCARI JALUR LAIN...", "RESPON TIDAK DIHARAPKAN...", "MEMPERLAMBAT SCAN UNTUK MENGHINDARI DETEKSI..."],
    'EXPLOIT': ["PAYLOAD DITOLAK...", "SISTEM KEAMANAN AKTIF...", "MENGKALIBRASI ULANG PAYLOAD...", "MENCARI ALAMAT MEMORI BARU..."],
    'DATA': ["DEKRIPSI GAGAL, MENCOBA KUNCI LAIN...", "KONEKSI DATABASE TERPUTUS...", "INTEGRITAS DATA KORUP...", "TRANSFER DATA LAMBAT..."]
}

def generate_steps(categories):
    all_steps = []
    for category, count in categories:
        choices = random.choices(STEP_LIBRARY[category], k=count) if count > len(STEP_LIBRARY[category]) else random.sample(STEP_LIBRARY[category], k=count)
        for choice in choices:
            all_steps.append((random.uniform(0.8, 2.5), choice, category))
    return all_steps

def run_simulation_steps(steps_config):
    actual_steps = generate_steps(steps_config)
    for duration, text, category in actual_steps:
        spinner = ['-', '\\', '|', '/']
        start_time = time.time()
        tick_speed = random.uniform(0.02, 0.1)
        
        delay_events = sorted([{'percent': random.randint(20, 90), 'duration': random.uniform(1.5, 4.0), 'triggered': False, 'silent': random.random() < 0.5} for _ in range(random.randint(0, 5))], key=lambda x: x['percent'])

        while True:
            elapsed = time.time() - start_time
            if elapsed >= duration:
                progress = 100
                bar = '█' * 50
                sys.stdout.write(f"\r{Colors.GREEN}✓ {text}... [{Colors.GREEN}{bar}{Colors.RESET}] {progress}%{Colors.RESET}{' ' * 10}\n")
                sys.stdout.flush()
                break
            
            progress = int((elapsed / duration) * 100)

            for event in delay_events:
                if not event['triggered'] and progress >= event['percent']:
                    event['triggered'] = True
                    bar = '█' * int(event['percent'] / 2) + ' ' * (50 - int(event['percent'] / 2))
                    sys.stdout.write(f"\r{Colors.YELLOW}> {text}... [{Colors.GREEN}{bar}{Colors.RESET}] {event['percent']}% ")
                    sys.stdout.flush()
                    if not event['silent']:
                        possible_messages = DELAY_MESSAGES.get(category, DELAY_MESSAGES['GENERIC'])
                        sys.stdout.write(f"\n{Colors.YELLOW}[!] {random.choice(possible_messages)}{Colors.RESET}")
                        sys.stdout.flush()
                    
                    time.sleep(event['duration'])
                    
                    if not event['silent']:
                        sys.stdout.write("\033[F\033[K")
                        sys.stdout.flush()
                    
                    start_time += event['duration']
            
            bar = '█' * int(progress / 2) + ' ' * (50 - int(progress / 2))
            spin_char = spinner[int(time.time() * 10) % 4]
            sys.stdout.write(f"\r{Colors.CYAN}{spin_char} {text}... [{Colors.GREEN}{bar}{Colors.RESET}] {progress}% ")
            sys.stdout.flush()
            time.sleep(tick_speed)
        time.sleep(0.3)

# --- FUNGSI HASIL AKHIR ---
def display_final_output(script_name, target_info):
    print(f"\n{Colors.BOLD}{Colors.MAGENTA}--- HASIL OPERASI ---{Colors.RESET}")
    if "Bot Follower" in script_name:
        count = target_info.get('count', 'Banyak')
        print(f"  {Colors.GREEN}BERHASIL:{Colors.RESET} {Colors.WHITE}{count} followers telah ditambahkan ke akun {Colors.CYAN}{target_info['target']}{Colors.RESET}.")
    elif "Web Deface" in script_name:
        print(f"  {Colors.GREEN}BERHASIL:{Colors.RESET} {Colors.WHITE}Website {Colors.CYAN}{target_info['target']}{Colors.RESET} telah berhasil di-deface.")
        print(f"  {Colors.GRAY}Jejak telah dihapus dari server log.{Colors.RESET}")
    elif "Database" in script_name:
        print(f"  {Colors.GREEN}BERHASIL:{Colors.RESET} {Colors.WHITE}Akses ke database {Colors.CYAN}{target_info['target']}{Colors.RESET} diperoleh.")
        print(f"  {Colors.WHITE}Menampilkan sampel data dari tabel 'users':{Colors.RESET}")
        print(f"  {Colors.GRAY}+----+------------------+----------------------------+------------------------------------------------------------------+")
        print(f"  {Colors.GRAY}| ID | Username         | Email                      | Password Hash (SHA-256)                                          |")
        print(f"  {Colors.GRAY}+----+------------------+----------------------------+------------------------------------------------------------------+")
        for i in range(5):
            user_id = str(random.randint(1000, 9999))
            username = ''.join(random.choices("abcdefghijklmnopqrstuvwxyz1234567890", k=random.randint(8, 12)))
            email = f"{username}@{random.choice(['gmail.com', 'yahoo.com', 'proton.me'])}"
            p_hash = ''.join(random.choices("abcdef1234567890", k=64))
            print(f"  {Colors.CYAN}| {user_id.ljust(2)} | {username.ljust(16)} | {email.ljust(26)} | {p_hash} |")
        print(f"  {Colors.GRAY}+----+------------------+----------------------------+------------------------------------------------------------------+")
    elif "Password Cracker" in script_name:
        print(f"  {Colors.GREEN}BERHASIL:{Colors.RESET} {Colors.WHITE}Beberapa akun berhasil dibobol dari {Colors.CYAN}{target_info['target']}{Colors.RESET}.")
        print(f"  {Colors.WHITE}Menampilkan akun yang berhasil di-crack:{Colors.RESET}")
        for _ in range(3):
            email = f"{''.join(random.choices('abcdefgh', k=5))}_admin@{random.choice(['corporate.com', 'gov.id', 'secure.net'])}"
            password = ''.join(random.choices("abcdefghijklmnopqrstuvwxyz1234567890!@#", k=random.randint(8,12)))
            print(f"    {Colors.GRAY}-> Email: {Colors.CYAN}{email.ljust(30)}{Colors.RESET} Password: {Colors.RED}{password}{Colors.RESET}")
    else:
        animated_text(f"\n{Colors.GREEN}{Colors.BOLD}[+] SCRIPT DIEKSEKUSI DENGAN SUKSES!{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.MAGENTA}--------------------{Colors.RESET}")

# --- FUNGSI-FUNGSI SIMULASI ---
def simulate_bot_follower(script_name):
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name}...{Colors.RESET}\n")
    target = get_validated_input(f"{Colors.WHITE}Username Target: {Colors.RESET}", validate_username, "Format salah!")
    count = get_validated_input(f"{Colors.WHITE}Jumlah Followers: {Colors.RESET}", validate_number, "Jumlah tidak valid!")
    print("-" * 50); run_simulation_steps([('INIT', 3), ('EXPLOIT', 4), ('CLEANUP', 1)])
    display_final_output(script_name, {'target': target, 'count': count})

def simulate_web_deface(script_name):
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name}...{Colors.RESET}\n")
    target = get_validated_input(f"{Colors.WHITE}URL Target: {Colors.RESET}", validate_url, "Format URL salah!")
    print("-" * 50); run_simulation_steps([('INIT', 4), ('SCAN', 20), ('EXPLOIT', 15), ('DATA', 3), ('CLEANUP', 3)])
    display_final_output(script_name, {'target': target})

def simulate_ddos_ip(script_name):
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name} (IP Attack)...{Colors.RESET}\n")
    get_validated_input(f"{Colors.WHITE}Target IP Address: {Colors.RESET}", validate_ip, "Format IP salah!")
    get_validated_input(f"{Colors.WHITE}Target Port: {Colors.RESET}", validate_number, "Port tidak valid!")
    print("-" * 50); run_simulation_steps([('INIT', 10), ('EXPLOIT', 60)])
    animated_text(f"\n{Colors.GREEN}{Colors.BOLD}[+] SERANGAN LAYER 4 DIMULAI!{Colors.RESET}")

def simulate_ddos_website(script_name):
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name} (Website Attack)...{Colors.RESET}\n")
    target = get_validated_input(f"{Colors.WHITE}URL Target Website: {Colors.RESET}", validate_url, "Format URL salah!")
    print("-" * 50); run_simulation_steps([('INIT', 5), ('SCAN', 10), ('EXPLOIT', 50), ('CLEANUP', 1)])
    animated_text(f"\n{Colors.GREEN}{Colors.BOLD}[+] SERANGAN LAYER 7 DIMULAI! Website target diperkirakan akan lumpuh.{Colors.RESET}")
    
def simulate_wifi_hack(script_name):
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name}...{Colors.RESET}\n")
    target = get_validated_input(f"{Colors.WHITE}Target BSSID: {Colors.RESET}", validate_bssid, "Format BSSID salah!")
    print("-" * 50); run_simulation_steps([('INIT', 2), ('WIFI', 30), ('DATA', 5), ('CLEANUP', 1)])
    display_final_output(script_name, {'target': target, 'password': 'Password12345'})

def simulate_game_hack(script_name):
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name}...{Colors.RESET}\n")
    get_validated_input(f"{Colors.WHITE}Game Process Name: {Colors.RESET}", validate_process_name, "Format salah!")
    print("-" * 50); run_simulation_steps([('INIT', 2), ('GAME', 15), ('CLEANUP', 2)])
    animated_text(f"\n{Colors.GREEN}{Colors.BOLD}[+] SUKSES! Cheat diaktifkan.{Colors.RESET}")

def simulate_database_access(script_name):
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name}...{Colors.RESET}\n")
    target = get_validated_input(f"{Colors.WHITE}Target IP/Domain Database: {Colors.RESET}", validate_not_empty, "Target tidak boleh kosong!")
    print("-" * 50); run_simulation_steps([('INIT', 5), ('SCAN', 10), ('EXPLOIT', 12), ('DATA', 8), ('CLEANUP', 2)])
    display_final_output(script_name, {'target': target})

def simulate_password_cracker(script_name):
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name}...{Colors.RESET}\n")
    target = get_validated_input(f"{Colors.WHITE}Target File Hash (.txt): {Colors.RESET}", validate_not_empty, "Target tidak boleh kosong!")
    print("-" * 50); run_simulation_steps([('INIT', 2), ('DATA', 40), ('CLEANUP', 1)])
    display_final_output(script_name, {'target': target})
    
def simulate_generic_script(script_name):
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name}...{Colors.RESET}\n")
    target = input(f"{Colors.WHITE}Masukkan Target (IP/Domain/User): {Colors.RESET}")
    total_steps = random.randint(10, 80)
    print("-" * 50); run_simulation_steps([(random.choice(['INIT', 'SCAN', 'EXPLOIT', 'DATA']), total_steps)])
    display_final_output(script_name, {'target': target})

# --- DATA UNTUK SCRIPT & OPSI-OPSINYA ---
script_options = {
    1: {'func': simulate_bot_follower}, 3: {'func': simulate_web_deface},
    5: {'func': simulate_database_access}, 11: {'func': simulate_ddos_ip},
    12: {'func': simulate_password_cracker}, 15: {'func': simulate_wifi_hack},
    51: {'func': simulate_game_hack}, 75: {'func': simulate_ddos_website},
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
        ("10", "Port Scanner (Nmap)"), ("11", "DDoS L4 (IP Attack)"), ("12", "Password Cracker (Brute)"),
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
        ("75", "DDoS L7 (Website Attack)")
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
    # --- PERBAIKAN: Pindahkan semua fungsi helper info sistem ke sini agar tidak ada NameError ---
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
        if not data: return ""
        max_len = max(len(key) for key, val in data) + 2
        lines = []
        try: term_width = os.get_terminal_size().columns
        except OSError: term_width = 80
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
        try:
            uname = platform.uname(); cpu_info_data = cpuinfo.get_cpu_info()
            os_details = get_os_details(uname); partitions = psutil.disk_partitions()
            while True:
                output_buffer = []
                svmem = psutil.virtual_memory(); swap = psutil.swap_memory()
                boot_time = timedelta(seconds=int(time.time() - psutil.boot_time()))
                cpu_percents = psutil.cpu_percent(percpu=True, interval=0.1)
                device_os = [("Pabrikan", cpu_info_data.get('vendor_id_raw', 'N/A')), ("Model Internal", uname.node), ("Versi OS", os_details), ("Arsitektur", cpu_info_data.get('arch', 'N/A')), ("Versi Kernel", uname.release), ("Waktu Aktif (Uptime)", str(boot_time))]
                cpu_data = [("Nama Chipset", cpu_info_data.get('brand_raw', 'N/A')), ("Core Fisik", psutil.cpu_count(logical=False)), ("Total Core", psutil.cpu_count(logical=True)), ("L2 Cache", f"{cpu_info_data.get('l2_cache_size', 0) // 1024} KB"), ("L3 Cache", f"{cpu_info_data.get('l3_cache_size', 0) // 1024} KB"), ("Fitur", ', '.join([f for f in ['aes', 'sha'] if f in cpu_info_data.get('flags', [])]))]
                mem_data = [("Total RAM", bytes_to_gb(svmem.total)), ("RAM Tersedia", bytes_to_gb(svmem.available)), ("RAM Terpakai", f"{bytes_to_gb(svmem.used)} ({svmem.percent}%)"), ("Total Swap", bytes_to_gb(swap.total)), ("Swap Terpakai", f"{bytes_to_gb(swap.used)} ({swap.percent}%)")]
                unavail_mobile = [("Nama Pemasaran", "[Data Ponsel]"), ("Kode Perangkat", "[Data Ponsel]"), ("Level Patch Keamanan", "[Data Ponsel]"), ("Versi Baseband", "[Data Ponsel]")]
                output_buffer.append(f"{Colors.BOLD}{Colors.MAGENTA}--- Perangkat & OS ---{Colors.RESET}\n{format_info(device_os, 2)}")
                output_buffer.append(f"\n{Colors.BOLD}{Colors.MAGENTA}--- CPU ---{Colors.RESET}\n{format_info(cpu_data, 2)}")
                cpu_bars = [f"    {Colors.WHITE}Core {i}  [{Colors.GREEN}{'█' * int(p / 10)}{' ' * (10 - int(p / 10))}{Colors.RESET}] {p:5.1f}%{Colors.RESET}" for i, p in enumerate(cpu_percents)]
                output_buffer.append("\n".join(cpu_bars))
                output_buffer.append(f"\n{Colors.BOLD}{Colors.MAGENTA}--- Memori ---{Colors.RESET}\n{format_info(mem_data, 2)}")
                storage_buffer = [f"\n{Colors.BOLD}{Colors.MAGENTA}--- Penyimpanan ---{Colors.RESET}"]
                for p in partitions:
                    try: storage_buffer.append(f"  {Colors.WHITE}{p.device} @ {p.mountpoint}{Colors.RESET} | {Colors.GRAY}Total: {bytes_to_gb(psutil.disk_usage(p.mountpoint).total)}, Terpakai: {bytes_to_gb(psutil.disk_usage(p.mountpoint).used)} ({psutil.disk_usage(p.mountpoint).percent}%){Colors.RESET}")
                    except (PermissionError, FileNotFoundError): continue
                output_buffer.append("\n".join(storage_buffer))
                output_buffer.append(f"\n{Colors.BOLD}{Colors.MAGENTA}--- Informasi Lain (Spesifik Ponsel) ---{Colors.RESET}\n{format_info(unavail_mobile, 2)}")
                output_buffer.append(f"\n{Colors.GRAY}Dashboard refresh otomatis. Tekan [Ctrl+C] untuk kembali...{Colors.RESET}")
                clear_screen()
                print("\n".join(output_buffer))
                time.sleep(2)
        except KeyboardInterrupt: return
        except Exception as e:
            clear_screen()
            print(f"\n{Colors.RED}Terjadi error saat mengambil data sistem: {e}{Colors.RESET}")
            input("Tekan [Enter] untuk kembali...")
            return

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
            
            script_info = script_options.get(choice_int)
            if script_info:
                script_info['func'](script_name)
            else:
                simulate_generic_script(script_name)

        except (ValueError, IndexError):
            print(f"{Colors.RED}Input tidak valid.{Colors.RESET}"); time.sleep(2)
        except Exception as e:
            print(f"{Colors.RED}Terjadi error tak terduga: {e}{Colors.RESET}"); time.sleep(3)
        input(f"\n{Colors.YELLOW}Tekan [Enter] untuk kembali ke menu utama...{Colors.RESET}")

if __name__ == "__main__":
    missing = []
    try: import psutil
    except ImportError: missing.append('psutil')
    try: import cpuinfo
    except ImportError: missing.append('py-cpuinfo')
    if platform.system() == "Windows":
        try: import wmi
        except ImportError: missing.append('WMI')

    if missing:
        check_and_install_dependencies(missing)
    
    import psutil; import cpuinfo
    if platform.system() == "Windows": import wmi
    
    main()

