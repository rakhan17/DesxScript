import os
import time
import random
import sys
import platform
import subprocess
import importlib.util
from datetime import datetime, timedelta
import socket
import re
from urllib.parse import urljoin, urlparse
import string
import hashlib
import base64
import binascii
import json
import shutil
import difflib

# --- GLOBAL CONFIG ---
# DANGER: Storing API keys directly in code is a security risk.
# This key is placed here based on direct user request for private use.
# Do NOT share this script publicly with the key included.
GEMINI_API_KEY = "AIzaSyDQwFO5m5hpsW5y6MLU3MxRlUVL-qPF0EA"

# --- DEPENDENCY CHECK AND INSTALLATION ---
def check_and_install_dependencies(missing_packages):
    """Offers to install missing dependencies."""
    yellow, reset, cyan, green, red = '\033[93m', '\033[0m', '\033[96m', '\033[92m', '\033[91m'
    print(f"{yellow}Warning: This script requires additional Python packages to function correctly.{reset}")
    print(f"Missing packages: {cyan}{', '.join(missing_packages)}{reset}")
    
    try:
        choice = input("Do you want to install them now? (Y/n): ").lower().strip()
    except KeyboardInterrupt:
        print("\nInstallation cancelled by user.")
        sys.exit(1)

    if choice == 'y':
        print(f"Starting installation of {', '.join(missing_packages)}...")
        for package in missing_packages:
            try:
                pip_name = package
                if package == 'PIL': pip_name = 'Pillow'
                if package == 'bs4': pip_name = 'beautifulsoup4'
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', pip_name])
            except subprocess.CalledProcessError:
                print(f"{red}Error: Failed to install {package}. Please install it manually.{reset}")
                sys.exit(1)
        print(f"\n{green}Installation successful. Please restart the script.{reset}")
        sys.exit(0)
    else:
        print("Installation cancelled. The program will now exit.")
        sys.exit(1)

# --- CORE UTILITIES ---
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class Colors:
    RESET = '\033[0m'; BOLD = '\033[01m'; RED = '\033[91m'; GREEN = '\033[92m'
    YELLOW = '\033[93m'; BLUE = '\033[94m'; MAGENTA = '\033[95m'; CYAN = '\033[96m'
    WHITE = '\033[97m'; GRAY = '\033[90m'

COLOR_PALETTE = [Colors.RED, Colors.GREEN, Colors.YELLOW, Colors.BLUE, Colors.MAGENTA, Colors.CYAN, Colors.WHITE]

def get_title_art():
    color = random.choice(COLOR_PALETTE)
    # Updated version number
    return f"""{color}{Colors.BOLD}
██████╗ ███████╗███████╗██╗  ██╗███████╗ ██████╗██████╗ ██╗██████╗ ████████╗
██╔══██╗██╔════╝██╔════╝╚██╗██╔╝██╔════╝██╔════╝██╔══██╗██║██╔══██╗╚══██╔══╝
██║  ██║█████╗  ███████╗ ╚███╔╝ ███████╗██║     ██████╔╝██║██████╔╝   ██║   
██║  ██║██╔══╝  ╚════██║ ██╔██╗ ╚════██║██║     ██══██╗██║██╔═══╝    ██║   
██████╔╝███████╗███████║██╔╝ ██╗███████║╚██████╗██║  ██║██║██║        ██║   
╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝╚═╝        ╚═╝   
{Colors.RESET}{Colors.CYAN}{'DesxScript Ultimate Toolkit v8.2'.center(88)}
{'created by rkhnatthyascrpter'.center(88)}{Colors.RESET}
"""

def get_validated_input(prompt, validation_func, error_message):
    while True:
        try:
            user_input = input(prompt)
            if validation_func(user_input): return user_input
            else: print(f"{Colors.RED}{error_message}{Colors.RESET}")
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}Operation cancelled by user.{Colors.RESET}")
            return None

validate_url = lambda u: u.startswith('http://') or u.startswith('https://')
validate_not_empty = lambda s: len(s.strip()) > 0
validate_numeric = lambda n: n.isdigit() and int(n) > 0
validate_username = lambda u: u.startswith('@') and len(u) > 1
validate_ip = lambda ip: len(ip.split('.')) == 4 and all(p.isdigit() and 0 <= int(p) <= 255 for p in ip.split('.'))
validate_email = lambda e: re.match(r"[^@]+@[^@]+\.[^@]+", e)
def validate_date(date_string):
    try:
        datetime.strptime(date_string, '%d-%m-%Y')
        return True
    except ValueError:
        return False

# --- SIMULATION ENGINE ---
STEP_LIBRARY = {
    'SOCIAL_INIT': ["Connecting to Social Media API", "Bypassing SSL Pinning", "Authenticating session"],
    'SOCIAL_EXPLOIT': ["Injecting follower packets", "Finding vulnerable endpoint", "Bypassing rate limits"],
    'WEB_SCAN': ["Scanning for common directories", "Checking server headers", "Testing for SQLi vulnerabilities"],
    'WEB_EXPLOIT': ["Uploading PHP shell", "Executing command injection", "Escalating privileges to root"],
    'DDOS_L7_INIT': ["Resolving target domain", "Analyzing CDN protection", "Building botnet instruction set"],
    'DDOS_L7_EXPLOIT': ["Flooding target with HTTP GET requests", "Bypassing Cloudflare with headless browsers", "Rotating source IPs"],
    'WIN_INIT': ["Initializing VBScript engine", "Connecting to Software Protection Platform", "Querying KMS server"],
    'WIN_EXPLOIT': ["Attempting to install GVLK key", "Sending activation request to KMS server", "Forcing activation attempt"],
    'EMAIL_INIT': ["Connecting to SMTP relay server", "Authenticating anonymous session", "Preparing email headers"],
    'EMAIL_EXPLOIT': ["Sending email burst to target", "Spoofing sender address", "Overloading mail queue"],
    'WIFI_CRACK': ["Scanning for nearby networks", "Capturing WPA handshake", "Initializing dictionary attack", "Analyzing packet captures", "Running hash through wordlist"],
    'MAC_CHANGE': ["Accessing network interface controller", "Disabling interface", "Spoofing physical address", "Re-enabling interface"],
    'CLEANUP': ["Erasing tracks from logs", "Closing secure connection", "Deleting temporary files"],
}
DELAY_MESSAGES = {
    'SOCIAL': ["API IS RESPONDING SLOWLY...", "RATE LIMIT REACHED, WAITING...", "CAPTCHA DETECTED, ATTEMPTING BYPASS..."],
    'WEB': ["WAF DETECTED, FINDING ALTERNATE ROUTE...", "UNEXPECTED RESPONSE...", "SLOWING SCAN TO AVOID DETECTION..."],
    'DDOS_L7': ["TARGET IS MITIGATING ATTACK...", "BOTS ARE BEING BLACKLISTED...", "INCREASING REQUEST RATE..."],
    'WIN': ["KMS SERVER NOT RESPONDING...", "ACTIVATION KEY REJECTED...", "RPC SERVER UNAVAILABLE..."],
    'EMAIL': ["SMTP SERVER THROTTLING CONNECTION...", "TARGET MAILBOX IS FULL...", "RELAY TEMPORARILY BLOCKED..."],
    'WIFI_CRACK': ["POOR SIGNAL STRENGTH...", "ENCRYPTION TOO STRONG...", "SWITCHING TO BRUTE-FORCE..."],
    'MAC_CHANGE': ["DRIVER INCOMPATIBILITY DETECTED...", "PERMISSION DENIED...", "RESETTING TO DEFAULT..."],
    'CLEANUP': ["LOGS ARE CORRUPTED...", "FAILED TO CLOSE SESSION...", "RESTORING SYSTEM STATE..."]
}

def generate_steps(categories):
    all_steps = []
    for category, count in categories:
        choices = random.choices(STEP_LIBRARY[category], k=count) if count > len(STEP_LIBRARY[category]) else random.sample(STEP_LIBRARY[category], k=count)
        for choice in choices:
            all_steps.append((random.uniform(0.8, 2.5), choice, category.split('_')[0]))
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
                progress = 100; bar = '█' * 50
                sys.stdout.write(f"\r{Colors.GREEN}✓ {text}... [{Colors.GREEN}{bar}{Colors.RESET}] {progress}%{Colors.RESET}{' ' * 20}\n")
                sys.stdout.flush(); break
            
            progress = int((elapsed / duration) * 100)
            for event in delay_events:
                if not event['triggered'] and progress >= event['percent']:
                    event['triggered'] = True
                    bar = '█' * int(event['percent'] / 2) + ' ' * (50 - int(event['percent'] / 2))
                    sys.stdout.write(f"\r{Colors.YELLOW}> {text}... [{Colors.GREEN}{bar}{Colors.RESET}] {event['percent']}% ")
                    sys.stdout.flush()
                    if not event['silent']:
                        possible_messages = DELAY_MESSAGES.get(category.upper(), ["GENERIC DELAY..."])
                        sys.stdout.write(f"\n{Colors.YELLOW}[!] {random.choice(possible_messages)}{Colors.RESET}")
                        sys.stdout.flush()
                    time.sleep(event['duration'])
                    if not event['silent']: sys.stdout.write("\033[F\033[K"); sys.stdout.flush()
                    start_time += event['duration']
            
            bar = '█' * int(progress / 2) + ' ' * (50 - int(progress / 2))
            spin_char = spinner[int(time.time() * 10) % 4]
            sys.stdout.write(f"\r{Colors.CYAN}{spin_char} {text}... [{Colors.GREEN}{bar}{Colors.RESET}] {progress}% ")
            sys.stdout.flush()
            time.sleep(tick_speed)
        time.sleep(0.2)

# --- "ADVANCED" SCRIPTS ---
def tool_bot_follower(script_name):
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name}...{Colors.RESET}\n")
    platform_choice = input(f"{Colors.WHITE}Select Platform [1] Instagram or [2] TikTok: {Colors.RESET}")
    if platform_choice is None: return
    platform_name = "Instagram" if platform_choice == '1' else "TikTok"
    target = get_validated_input(f"{Colors.WHITE}Enter {platform_name} username (e.g., @username): {Colors.RESET}", validate_username, "Invalid username format! Must start with '@'.")
    if target is None: return
    count = get_validated_input(f"{Colors.WHITE}Enter amount of followers: {Colors.RESET}", validate_numeric, "Amount must be a number!")
    if count is None: return
    print("-" * 50); run_simulation_steps([('SOCIAL_INIT', 3), ('SOCIAL_EXPLOIT', 5), ('CLEANUP', 1)])
    print(f"\n{Colors.BOLD}{Colors.GREEN}SUCCESS! {count} followers have been sent to {target}.{Colors.RESET}")

def tool_web_deface(script_name):
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name}...{Colors.RESET}\n")
    target = get_validated_input(f"{Colors.WHITE}Enter target URL (e.g., http://example.com): {Colors.RESET}", validate_url, "Invalid URL format!")
    if target is None: return
    print("-" * 50); run_simulation_steps([('WEB_SCAN', 8), ('WEB_EXPLOIT', 5), ('CLEANUP', 2)])
    print(f"\n{Colors.BOLD}{Colors.GREEN}SUCCESS! Website {target} has been defaced.{Colors.RESET}")

def tool_email_bomber(script_name):
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name}...{Colors.RESET}\n")
    target = get_validated_input(f"{Colors.WHITE}Enter target email address: {Colors.RESET}", validate_email, "Invalid email format!")
    if target is None: return
    count = get_validated_input(f"{Colors.WHITE}Enter amount of emails to send: {Colors.RESET}", validate_numeric, "Amount must be a number!")
    if count is None: return
    print("-" * 50); run_simulation_steps([('EMAIL_INIT', 3), ('EMAIL_EXPLOIT', 5), ('CLEANUP', 1)])
    print(f"\n{Colors.BOLD}{Colors.GREEN}SUCCESS! {count} emails have been sent to {target}.{Colors.RESET}")

def tool_ddos_l7(script_name):
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name}...{Colors.RESET}\n")
    target = get_validated_input(f"{Colors.WHITE}Enter target website URL (e.g., http://example.com): {Colors.RESET}", validate_url, "Invalid URL format!")
    if target is None: return
    print("-" * 50); run_simulation_steps([('DDOS_L7_INIT', 4), ('DDOS_L7_EXPLOIT', 10), ('CLEANUP', 1)])
    print(f"\n{Colors.BOLD}{Colors.GREEN}ATTACK INITIATED! Target {target} will be offline shortly.{Colors.RESET}")

def tool_windows_activation(script_name):
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name}...{Colors.RESET}\n")
    if get_validated_input(f"{Colors.WHITE}Press [Enter] to begin Windows activation...{Colors.RESET}", lambda x: True, "") is None: return
    print("-" * 50); run_simulation_steps([('WIN_INIT', 3), ('WIN_EXPLOIT', 4), ('CLEANUP', 1)])
    print(f"\n{Colors.BOLD}{Colors.GREEN}SUCCESS! Windows has been activated permanently.{Colors.RESET}")

def tool_generic(script_name):
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name}...{Colors.RESET}\n")
    target = input(f"{Colors.WHITE}Enter Target (e.g. IP, Domain, User): {Colors.RESET}")
    print("-" * 50); run_simulation_steps([('SOCIAL_INIT', 2), ('WEB_SCAN', 3), ('CLEANUP', 1)])
    print(f"\n{Colors.YELLOW}Operation '{script_name}' on target '{target}' completed.{Colors.RESET}")

def tool_wifi_cracker(script_name):
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name}...{Colors.RESET}\n")
    target_ssid = get_validated_input(f"{Colors.WHITE}Enter Target WiFi SSID: {Colors.RESET}", validate_not_empty, "SSID cannot be empty!")
    if target_ssid is None: return
    print("-" * 50); run_simulation_steps([('WIFI_CRACK', 5), ('CLEANUP', 1)])
    found_password = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(8, 12)))
    print(f"\n{Colors.BOLD}{Colors.GREEN}SUCCESS! Password for '{target_ssid}' found: {found_password}{Colors.RESET}")

def tool_cc_generator(script_name):
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name}...{Colors.RESET}\n")
    
    def luhn_checksum(card_number):
        def digits_of(n): return [int(d) for d in str(n)]
        digits = digits_of(card_number)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = sum(odd_digits)
        for d in even_digits: checksum += sum(digits_of(d * 2))
        return checksum % 10

    def generate_card(prefix, length):
        card_number = prefix + ''.join(random.choices(string.digits, k=length - len(prefix) - 1))
        check_digit = (10 - luhn_checksum(card_number + '0')) % 10
        return card_number + str(check_digit)

    count_str = get_validated_input(f"{Colors.WHITE}How many cards to generate?: {Colors.RESET}", validate_numeric, "Must be a number!")
    if count_str is None: return
    count = int(count_str)
    
    prefixes = {'Visa': '4', 'Mastercard': '5', 'Amex': '37'}
    print(f"\n{Colors.BOLD}{Colors.MAGENTA}--- GENERATED CARDS ---{Colors.RESET}")
    for _ in range(count):
        card_type = random.choice(list(prefixes.keys()))
        card_number = generate_card(prefixes[card_type], 16)
        print(f"  {Colors.WHITE}{card_type:<12}{Colors.RESET}: {Colors.CYAN}{card_number}{Colors.RESET}")

def tool_mac_changer(script_name):
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name}...{Colors.RESET}\n")
    try:
        current_mac = getmac.get_mac_address()
        print(f"{Colors.WHITE}Current MAC Address: {Colors.CYAN}{current_mac}{Colors.RESET}")
        choice = input(f"{Colors.WHITE}Do you want to change it? (y/n): {Colors.RESET}").lower()
        if choice == 'y':
            new_mac = "02:00:00:%02x:%02x:%02x" % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            print("-" * 50); run_simulation_steps([('MAC_CHANGE', 4), ('CLEANUP', 1)])
            print(f"\n{Colors.BOLD}{Colors.GREEN}SUCCESS! MAC Address has been changed to {new_mac}.{Colors.RESET}")
        else:
            print("Operation cancelled.")
    except Exception:
        print(f"{Colors.RED}Could not retrieve MAC address. Are you running with sufficient privileges?{Colors.RESET}")

# --- REAL TOOL FUNCTIONS ---
def real_port_scanner(script_name):
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name}...{Colors.RESET}\n")
    target = get_validated_input(f"{Colors.WHITE}Enter Target IP or Domain: {Colors.RESET}", validate_not_empty, "Target cannot be empty!")
    if target is None: return
    try:
        ip = socket.gethostbyname(target)
        print(f"\n{Colors.CYAN}Scanning common ports for {target} ({ip})...{Colors.RESET}")
        common_ports = [21, 22, 23, 25, 53, 80, 110, 139, 443, 1433, 3306, 3389, 5900, 8080]
        open_ports = []
        for port in common_ports:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(0.2)
                result = sock.connect_ex((ip, port))
                status = f"{Colors.GREEN}Open{Colors.RESET}" if result == 0 else f"{Colors.GRAY}Closed{Colors.RESET}"
                print(f"  Port {str(port).ljust(5)}: {status}")
                if result == 0: open_ports.append(port)
        print(f"\n{Colors.BOLD}{Colors.MAGENTA}--- RESULTS ---{Colors.RESET}\n  {Colors.GREEN}Found {len(open_ports)} open ports: {Colors.CYAN}{', '.join(map(str, open_ports))}{Colors.RESET}" if open_ports else f"{Colors.YELLOW}No common open ports found.{Colors.RESET}")
    except socket.gaierror: print(f"{Colors.RED}Error: Hostname could not be resolved.{Colors.RESET}")
    except socket.error: print(f"{Colors.RED}Error: Could not connect to the server.{Colors.RESET}")

def real_subdomain_enumerator(script_name):
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name}...{Colors.RESET}\n")
    target = get_validated_input(f"{Colors.WHITE}Enter Target Domain (e.g., google.com): {Colors.RESET}", validate_not_empty, "Domain is not valid!")
    if target is None: return
    sub_list = ["www", "mail", "ftp", "admin", "api", "dev", "test", "cpanel", "webmail", "blog", "shop", "support", "cdn", "m"]
    print(f"\n{Colors.CYAN}Searching for subdomains of {target}...{Colors.RESET}")
    found = []
    for sub in sub_list:
        hostname = f"{sub}.{target}"
        try:
            socket.gethostbyname(hostname)
            print(f"  {Colors.GREEN}[+] http://{hostname} - FOUND!{Colors.RESET}")
            found.append(f"http://{hostname}")
        except socket.error:
            sys.stdout.write(f"\r  {Colors.GRAY}[-] Trying {hostname}...                "); sys.stdout.flush()
    print("\r" + " " * 60 + "\r", end="")
    print(f"\n{Colors.BOLD}{Colors.MAGENTA}--- RESULTS ---{Colors.RESET}\n  {Colors.GREEN}Found {len(found)} active subdomains:{Colors.RESET}\n" + '\n'.join([f"    {Colors.CYAN}-> {u}{Colors.RESET}" for u in found]) if found else f"  {Colors.YELLOW}No common subdomains found.{Colors.RESET}")

def real_admin_finder(script_name):
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name}...{Colors.RESET}\n")
    target = get_validated_input(f"{Colors.WHITE}Enter URL (e.g., http://example.com): {Colors.RESET}", validate_url, "URL is not valid!")
    if target is None: return
    paths = ["admin/", "administrator/", "login.php", "admin.php", "wp-admin/", "admin/login.php", "cpanel/"]
    print(f"\n{Colors.CYAN}Searching for admin panels on {target}...{Colors.RESET}")
    found = []
    for path in paths:
        url = urljoin(target, path)
        try:
            res = requests.get(url, timeout=3, allow_redirects=False)
            sys.stdout.write(f"\r  {Colors.GRAY}[-] Trying {url}...                "); sys.stdout.flush()
            if res.status_code in (200, 302, 401, 403):
                print(f"\r  {Colors.GREEN}[+] {url} - FOUND! (Status: {res.status_code}){Colors.RESET}" + " "*20)
                found.append(url)
        except requests.RequestException: continue
    print("\r" + " " * 60 + "\r", end="")
    print(f"\n{Colors.BOLD}{Colors.MAGENTA}--- RESULTS ---{Colors.RESET}\n  {Colors.GREEN}Found {len(found)} possible admin panels:{Colors.RESET}\n" + '\n'.join([f"    {Colors.CYAN}-> {u}{Colors.RESET}" for u in found]) if found else f"  {Colors.YELLOW}No common admin panels found.{Colors.RESET}")

def real_hash_identifier(script_name):
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name}...{Colors.RESET}\n")
    hash_str = input(f"{Colors.WHITE}Enter hash string: {Colors.RESET}")
    if hash_str is None: return
    hash_str = hash_str.strip().lower()
    patterns = {'MD5': r"^[a-f0-9]{32}$", 'SHA-1': r"^[a-f0-9]{40}$", 'SHA-256': r"^[a-f0-9]{64}$", 'SHA-512': r"^[a-f0-9]{128}$"}
    found = next((t for t, p in patterns.items() if re.match(p, hash_str)), "Unknown")
    print(f"\n{Colors.BOLD}{Colors.MAGENTA}--- RESULT ---{Colors.RESET}\n  {Colors.GREEN}Hash is likely of type {Colors.CYAN}{found}{Colors.RESET}." if found != "Unknown" else f"  {Colors.RED}Hash type does not match common patterns.{Colors.RESET}")

def real_metadata_scraper(script_name):
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name}...{Colors.RESET}\n")
    path = input(f"{Colors.WHITE}Enter full path to file (image/pdf): {Colors.RESET}")
    if path is None: return
    path = path.strip()
    if not os.path.exists(path): print(f"{Colors.RED}Error: File not found.{Colors.RESET}"); return
    print(f"\n{Colors.CYAN}Extracting metadata from {os.path.basename(path)}...{Colors.RESET}")
    try:
        if path.lower().endswith(('.png', '.jpg', '.jpeg')):
            with Image.open(path) as img:
                exif = img._getexif()
                if exif:
                    print(f"{Colors.BOLD}{Colors.MAGENTA}--- IMAGE METADATA (EXIF) ---{Colors.RESET}")
                    for tag_id, val in exif.items(): print(f"  {Colors.WHITE}{str(TAGS.get(tag_id, tag_id)).ljust(25)}{Colors.RESET}: {Colors.CYAN}{val}{Colors.RESET}")
                else: print(f"{Colors.YELLOW}No EXIF data found.{Colors.RESET}")
        elif path.lower().endswith('.pdf'):
            with open(path, 'rb') as f:
                meta = PyPDF2.PdfReader(f).metadata
                if meta:
                    print(f"{Colors.BOLD}{Colors.MAGENTA}--- PDF METADATA ---{Colors.RESET}")
                    for key, val in meta.items(): print(f"  {Colors.WHITE}{key.replace('/', '').ljust(25)}{Colors.RESET}: {Colors.CYAN}{val}{Colors.RESET}")
                else: print(f"{Colors.YELLOW}No metadata found.{Colors.RESET}")
        else: print(f"{Colors.RED}File format not supported. Please use an image or PDF file.{Colors.RESET}")
    except Exception as e: print(f"{Colors.RED}Error processing file: {e}{Colors.RESET}")

def real_fake_identity_generator(script_name):
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name}...{Colors.RESET}\n")
    fake = Faker('id_ID')
    profile = fake.profile()
    print(f"{Colors.BOLD}{Colors.MAGENTA}--- GENERATED PROFILE ---{Colors.RESET}")
    print(f"  {Colors.WHITE}{'Name':<15}{Colors.RESET}: {Colors.CYAN}{profile['name']}{Colors.RESET}")
    print(f"  {Colors.WHITE}{'Sex':<15}{Colors.RESET}: {Colors.CYAN}{'Male' if profile['sex'] == 'M' else 'Female'}{Colors.RESET}")
    print(f"  {Colors.WHITE}{'Address':<15}{Colors.RESET}: {Colors.CYAN}{profile['address'].replace(chr(10), ', ')}{Colors.RESET}")
    print(f"  {Colors.WHITE}{'Email':<15}{Colors.RESET}: {Colors.CYAN}{profile['mail']}{Colors.RESET}")
    print(f"  {Colors.WHITE}{'Birthdate':<15}{Colors.RESET}: {Colors.CYAN}{profile['birthdate']}{Colors.RESET}")

def real_website_cloner(script_name):
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name}...{Colors.RESET}\n")
    url = get_validated_input(f"{Colors.WHITE}Enter full website URL: {Colors.RESET}", validate_url, "URL is not valid!")
    if url is None: return
    
    try:
        print(f"{Colors.CYAN}Starting cloning process from {url}...{Colors.RESET}")
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        res = requests.get(url, timeout=10, headers=headers)
        res.raise_for_status()

        soup = BeautifulSoup(res.content, 'html.parser')
        domain = urlparse(url).netloc.replace('.', '_')
        if not os.path.exists(domain): os.makedirs(domain)

        # Create asset directories
        asset_dirs = ['css', 'js', 'images']
        for dir_name in asset_dirs:
            dir_path = os.path.join(domain, dir_name)
            if not os.path.exists(dir_path): os.makedirs(dir_path)

        # --- Download and rewrite assets ---
        tags_to_process = {
            'link': 'href',
            'script': 'src',
            'img': 'src'
        }

        for tag_name, attr in tags_to_process.items():
            for tag in soup.find_all(tag_name, {attr: True}):
                asset_url = tag[attr]
                if not isinstance(asset_url, str) or asset_url.startswith('data:'): continue
                if asset_url.startswith('//'): asset_url = 'https:' + asset_url
                
                full_asset_url = urljoin(url, asset_url)
                
                try:
                    asset_path = urlparse(full_asset_url).path
                    filename = os.path.basename(asset_path)
                    if not filename: continue

                    local_dir = ''
                    if tag_name == 'link' and ('.css' in filename): local_dir = 'css'
                    elif tag_name == 'script' and ('.js' in filename): local_dir = 'js'
                    elif tag_name == 'img': local_dir = 'images'
                    else: continue

                    local_path_for_download = os.path.join(domain, local_dir, filename)
                    local_path_for_html = f"{local_dir}/{filename}"

                    if not os.path.exists(local_path_for_download):
                        asset_res = requests.get(full_asset_url, timeout=5, headers=headers, stream=True)
                        if asset_res.status_code == 200:
                            with open(local_path_for_download, 'wb') as f:
                                for chunk in asset_res.iter_content(chunk_size=8192):
                                    f.write(chunk)
                            print(f"    {Colors.GREEN}[+] Downloaded: {filename}{Colors.RESET}")
                        else:
                             print(f"    {Colors.YELLOW}[!] Skipped (Status {asset_res.status_code}): {filename}{Colors.RESET}")
                    
                    tag[attr] = local_path_for_html

                except requests.RequestException:
                    print(f"    {Colors.RED}[-] Failed download: {os.path.basename(full_asset_url)}{Colors.RESET}")
                except Exception:
                    pass

        with open(os.path.join(domain, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(str(soup))
        print(f"\n{Colors.GREEN}[+] Successfully saved modified index.html{Colors.RESET}")
        
        print(f"\n{Colors.BOLD}{Colors.GREEN}Cloning finished! Files saved in folder '{domain}'.{Colors.RESET}")
    except requests.RequestException as e:
        print(f"{Colors.RED}Error: Failed to access URL: {e}{Colors.RESET}")

def real_dns_lookup(script_name):
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name}...{Colors.RESET}\n")
    domain = get_validated_input(f"{Colors.WHITE}Enter domain name: {Colors.RESET}", validate_not_empty, "Domain cannot be empty!")
    if domain is None: return
    print(f"\n{Colors.CYAN}Performing DNS Lookup for {domain}...{Colors.RESET}")
    try:
        info = socket.gethostbyname_ex(domain)
        print(f"{Colors.BOLD}{Colors.MAGENTA}--- DNS LOOKUP RESULTS ---{Colors.RESET}")
        print(f"  {Colors.WHITE}{'Hostname':<15}{Colors.RESET}: {Colors.CYAN}{info[0]}{Colors.RESET}")
        if info[1]: print(f"  {Colors.WHITE}{'Aliases':<15}{Colors.RESET}: {Colors.CYAN}{', '.join(info[1])}{Colors.RESET}")
        if info[2]: print(f"  {Colors.WHITE}{'IP Addresses':<15}{Colors.RESET}: {Colors.CYAN}{', '.join(info[2])}{Colors.RESET}")
    except socket.gaierror: print(f"{Colors.RED}Error: Could not find information for that domain.{Colors.RESET}")

def real_http_header_viewer(script_name):
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name}...{Colors.RESET}\n")
    url = get_validated_input(f"{Colors.WHITE}Enter full URL: {Colors.RESET}", validate_url, "URL is not valid!")
    if url is None: return
    try:
        print(f"\n{Colors.CYAN}Fetching HTTP Headers from {url}...{Colors.RESET}")
        response = requests.head(url, allow_redirects=True, timeout=5)
        print(f"{Colors.BOLD}{Colors.MAGENTA}--- HTTP HEADER RESULTS ---{Colors.RESET}")
        print(f"{Colors.WHITE}Status Code: {Colors.CYAN}{response.status_code} {response.reason}{Colors.RESET}")
        for key, value in response.headers.items(): print(f"  {Colors.WHITE}{key:<25}{Colors.RESET}: {Colors.CYAN}{value}{Colors.RESET}")
    except requests.RequestException as e: print(f"{Colors.RED}Error: Failed to fetch data from URL: {e}{Colors.RESET}")

def real_ip_geolocation(script_name):
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name}...{Colors.RESET}\n")
    ip_address = get_validated_input(f"{Colors.WHITE}Enter IP Address: {Colors.RESET}", validate_not_empty, "IP Address cannot be empty!")
    if ip_address is None: return
    try:
        print(f"\n{Colors.CYAN}Looking up geolocation for {ip_address}...{Colors.RESET}")
        response = requests.get(f"http://ip-api.com/json/{ip_address}", timeout=5); response.raise_for_status()
        data = response.json()
        if data['status'] == 'success':
            print(f"{Colors.BOLD}{Colors.MAGENTA}--- GEOLOCATION RESULTS ---{Colors.RESET}")
            for key, val in data.items():
                 if key not in ['status', 'query']: print(f"  {Colors.WHITE}{key.title():<15}{Colors.RESET}: {Colors.CYAN}{val}{Colors.RESET}")
        else: print(f"{Colors.RED}Error: Failed to get data for IP '{ip_address}'. Message: {data.get('message')}{Colors.RESET}")
    except requests.RequestException as e: print(f"{Colors.RED}Error: Could not connect to geolocation service: {e}{Colors.RESET}")

def real_link_extractor(script_name):
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name}...{Colors.RESET}\n")
    url = get_validated_input(f"{Colors.WHITE}Enter webpage URL: {Colors.RESET}", validate_url, "URL is not valid!")
    if url is None: return
    try:
        print(f"\n{Colors.CYAN}Extracting all links from {url}...{Colors.RESET}")
        response = requests.get(url, timeout=5); response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        links = {urljoin(url, a['href']) for a in soup.find_all('a', href=True)}
        print(f"\n{Colors.BOLD}{Colors.MAGENTA}--- LINK EXTRACTION RESULTS ({len(links)} FOUND) ---{Colors.RESET}")
        for link in sorted(list(links)): print(f"  {Colors.CYAN}{link}{Colors.RESET}")
    except requests.RequestException as e: print(f"{Colors.RED}Error: Failed to access URL: {e}{Colors.RESET}")

def real_whois_lookup(script_name):
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name}...{Colors.RESET}\n")
    domain = get_validated_input(f"{Colors.WHITE}Enter domain name: {Colors.RESET}", validate_not_empty, "Domain cannot be empty!")
    if domain is None: return
    try:
        print(f"\n{Colors.CYAN}Performing WHOIS Lookup for {domain}...{Colors.RESET}")
        w = whois.whois(domain)
        print(f"{Colors.BOLD}{Colors.MAGENTA}--- WHOIS LOOKUP RESULTS ---{Colors.RESET}")
        if w.domain_name:
            for key, value in w.items():
                if value and isinstance(value, list): print(f"  {Colors.WHITE}{str(key).replace('_', ' ').title():<20}{Colors.RESET}: {Colors.CYAN}{', '.join(map(str, value))}{Colors.RESET}")
                elif value: print(f"  {Colors.WHITE}{str(key).replace('_', ' ').title():<20}{Colors.RESET}: {Colors.CYAN}{value}{Colors.RESET}")
        else: print(f"{Colors.RED}Could not find WHOIS data for that domain.{Colors.RESET}")
    except Exception as e: print(f"{Colors.RED}Error during WHOIS lookup: {e}{Colors.RESET}")

def real_password_generator(script_name):
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name}...{Colors.RESET}\n")
    length_str = get_validated_input(f"{Colors.WHITE}Password length (e.g., 16): {Colors.RESET}", validate_numeric, "Must be a number!")
    if length_str is None: return
    length = int(length_str)
    include_symbols = input(f"{Colors.WHITE}Include symbols? (y/n): {Colors.RESET}").lower() == 'y'
    chars = string.ascii_letters + string.digits
    if include_symbols: chars += string.punctuation
    password = ''.join(random.choice(chars) for _ in range(length))
    print(f"\n{Colors.BOLD}{Colors.MAGENTA}--- GENERATED PASSWORD ---{Colors.RESET}\n  {Colors.GREEN}{password}{Colors.RESET}")

def real_file_hasher(script_name):
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name}...{Colors.RESET}\n")
    file_path = get_validated_input(f"{Colors.WHITE}Enter full path to file: {Colors.RESET}", os.path.exists, "File not found!")
    if file_path is None: return
    print(f"\n{Colors.CYAN}Calculating hashes for {os.path.basename(file_path)}...{Colors.RESET}")
    hasher_md5, hasher_sha256 = hashlib.md5(), hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""): hasher_md5.update(chunk); hasher_sha256.update(chunk)
        print(f"\n{Colors.BOLD}{Colors.MAGENTA}--- FILE HASH RESULTS ---{Colors.RESET}")
        print(f"  {Colors.WHITE}{'MD5':<8}{Colors.RESET}: {Colors.CYAN}{hasher_md5.hexdigest()}{Colors.RESET}")
        print(f"  {Colors.WHITE}{'SHA256':<8}{Colors.RESET}: {Colors.CYAN}{hasher_sha256.hexdigest()}{Colors.RESET}")
    except IOError as e: print(f"{Colors.RED}Error reading file: {e}{Colors.RESET}")

def real_url_shortener(script_name):
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name}...{Colors.RESET}\n")
    long_url = get_validated_input(f"{Colors.WHITE}Enter long URL: {Colors.RESET}", validate_url, "URL is not valid!")
    if long_url is None: return
    try:
        print(f"\n{Colors.CYAN}Shortening URL...{Colors.RESET}")
        api_url = f"http://tinyurl.com/api-create.php?url={long_url}"
        response = requests.get(api_url, timeout=5); response.raise_for_status()
        print(f"\n{Colors.BOLD}{Colors.MAGENTA}--- SHORTENED URL ---{Colors.RESET}\n  {Colors.GREEN}{response.text}{Colors.RESET}")
    except requests.RequestException as e: print(f"{Colors.RED}Error: Failed to shorten URL: {e}{Colors.RESET}")

def real_base64_tool(script_name):
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name}...{Colors.RESET}\n")
    choice = input(f"{Colors.WHITE}Select [1] Encode or [2] Decode: {Colors.RESET}")
    if choice is None: return
    text = input(f"{Colors.WHITE}Enter text: {Colors.RESET}")
    if text is None: return
    try:
        if choice == '1':
            encoded = base64.b64encode(text.encode('utf-8')).decode('utf-8')
            print(f"\n{Colors.BOLD}{Colors.MAGENTA}--- ENCODED RESULT ---{Colors.RESET}\n  {Colors.GREEN}{encoded}{Colors.RESET}")
        elif choice == '2':
            decoded = base64.b64decode(text.encode('utf-8')).decode('utf-8')
            print(f"\n{Colors.BOLD}{Colors.MAGENTA}--- DECODED RESULT ---{Colors.RESET}\n  {Colors.GREEN}{decoded}{Colors.RESET}")
        else: print(f"{Colors.RED}Invalid choice.{Colors.RESET}")
    except (binascii.Error, UnicodeDecodeError): print(f"{Colors.RED}Error: Invalid Base64 text.{Colors.RESET}")

def real_what_is_my_ip(script_name):
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name}...{Colors.RESET}\n")
    try:
        print(f"{Colors.CYAN}Looking up your public IP address...{Colors.RESET}")
        response = requests.get("https://api.ipify.org?format=json", timeout=5); response.raise_for_status()
        ip = response.json()['ip']
        print(f"\n{Colors.BOLD}{Colors.MAGENTA}--- YOUR PUBLIC IP ---{Colors.RESET}\n  {Colors.GREEN}{ip}{Colors.RESET}")
    except requests.RequestException as e: print(f"{Colors.RED}Error: Failed to get IP address: {e}{Colors.RESET}")

# --- PROGRAMMER & UTILITY TOOLS ---
def real_json_validator(script_name):
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name}...{Colors.RESET}\n")
    print(f"{Colors.CYAN}Enter your JSON data. Press Ctrl+D (Linux/macOS) or Ctrl+Z then Enter (Windows) when done.{Colors.RESET}")
    try:
        json_input = sys.stdin.read()
        parsed_json = json.loads(json_input)
        pretty_json = json.dumps(parsed_json, indent=4, sort_keys=True)
        print(f"\n{Colors.BOLD}{Colors.GREEN}--- JSON is VALID ---{Colors.RESET}")
        print(f"{Colors.WHITE}Formatted Output:{Colors.RESET}")
        print(f"{Colors.CYAN}{pretty_json}{Colors.RESET}")
    except json.JSONDecodeError as e:
        print(f"\n{Colors.BOLD}{Colors.RED}--- JSON is INVALID ---{Colors.RESET}")
        print(f"{Colors.YELLOW}Error: {e}{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.RED}An unexpected error occurred: {e}{Colors.RESET}")

def real_line_counter(script_name):
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name}...{Colors.RESET}\n")
    path = get_validated_input(f"{Colors.WHITE}Enter directory path to scan: {Colors.RESET}", os.path.isdir, "Directory not found!")
    if path is None: return
    extensions_str = input(f"{Colors.WHITE}Enter file extensions to count (e.g., py,js,html): {Colors.RESET}")
    if extensions_str is None: return
    extensions = [f".{ext.strip()}" for ext in extensions_str.split(',')]
    
    total_lines = 0
    total_files = 0
    print(f"\n{Colors.CYAN}Scanning for files with extensions: {', '.join(extensions)}{Colors.RESET}")
    
    for dirpath, _, filenames in os.walk(path):
        for filename in filenames:
            if filename.endswith(tuple(extensions)):
                total_files += 1
                try:
                    with open(os.path.join(dirpath, filename), 'r', errors='ignore') as f:
                        total_lines += len(f.readlines())
                except Exception:
                    continue
    
    print(f"\n{Colors.BOLD}{Colors.MAGENTA}--- LINE COUNT RESULTS ---{Colors.RESET}")
    print(f"  {Colors.WHITE}{'Total Files Scanned':<25}{Colors.RESET}: {Colors.CYAN}{total_files}{Colors.RESET}")
    print(f"  {Colors.WHITE}{'Total Lines of Code':<25}{Colors.RESET}: {Colors.CYAN}{total_lines}{Colors.RESET}")

def real_directory_tree(script_name):
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name}...{Colors.RESET}\n")
    path = get_validated_input(f"{Colors.WHITE}Enter directory path to display: {Colors.RESET}", os.path.isdir, "Directory not found!")
    if path is None: return
    print(f"\n{Colors.BOLD}{Colors.MAGENTA}--- DIRECTORY TREE for {os.path.basename(path)} ---{Colors.RESET}")
    
    def generate_tree(dir_path, prefix=""):
        files = os.listdir(dir_path)
        files.sort(key=lambda f: os.path.isfile(os.path.join(dir_path, f)))
        
        pointers = [f"{Colors.CYAN}├── {Colors.RESET}"] * (len(files) - 1) + [f"{Colors.CYAN}└── {Colors.RESET}"]
        for pointer, file in zip(pointers, files):
            full_path = os.path.join(dir_path, file)
            is_dir = os.path.isdir(full_path)
            color = Colors.BLUE if is_dir else Colors.WHITE
            print(f"{prefix}{pointer}{color}{file}{Colors.RESET}")
            if is_dir:
                extension = f"{Colors.CYAN}│   {Colors.RESET}" if pointer == f"{Colors.CYAN}├── {Colors.RESET}" else "    "
                generate_tree(full_path, prefix + extension)

    print(f"{Colors.BLUE}{os.path.basename(path)}{Colors.RESET}")
    generate_tree(path)

def real_github_user_info(script_name):
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name}...{Colors.RESET}\n")
    username = get_validated_input(f"{Colors.WHITE}Enter GitHub Username: {Colors.RESET}", validate_not_empty, "Username cannot be empty!")
    if username is None: return
    api_url = f"https://api.github.com/users/{username}"
    try:
        print(f"\n{Colors.CYAN}Fetching data for {username}...{Colors.RESET}")
        res = requests.get(api_url, timeout=5)
        if res.status_code == 200:
            data = res.json()
            created_date = datetime.strptime(data.get('created_at'), "%Y-%m-%dT%H:%M:%SZ").strftime('%d %B %Y')
            
            print(f"\n{Colors.BOLD}{Colors.MAGENTA}--- GITHUB USER INFO: {data.get('login')} ---{Colors.RESET}")
            print(f"  {Colors.WHITE}{'Name':<18}{Colors.RESET}: {Colors.CYAN}{data.get('name') or 'N/A'}{Colors.RESET}")
            print(f"  {Colors.WHITE}{'Bio':<18}{Colors.RESET}: {Colors.CYAN}{data.get('bio') or 'N/A'}{Colors.RESET}")
            print("-" * 50)
            print(f"  {Colors.WHITE}{'Followers':<18}{Colors.RESET}: {Colors.CYAN}{data.get('followers')} | {Colors.WHITE}Following:{Colors.CYAN} {data.get('following')}{Colors.RESET}")
            print(f"  {Colors.WHITE}{'Public Repos':<18}{Colors.RESET}: {Colors.CYAN}{data.get('public_repos')} | {Colors.WHITE}Public Gists:{Colors.CYAN} {data.get('public_gists')}{Colors.RESET}")
            print("-" * 50)
            print(f"  {Colors.WHITE}{'Location':<18}{Colors.RESET}: {Colors.CYAN}{data.get('location') or 'N/A'}{Colors.RESET}")
            print(f"  {Colors.WHITE}{'Company':<18}{Colors.RESET}: {Colors.CYAN}{data.get('company') or 'N/A'}{Colors.RESET}")
            print(f"  {Colors.WHITE}{'Website':<18}{Colors.RESET}: {Colors.CYAN}{data.get('blog') or 'N/A'}{Colors.RESET}")
            print(f"  {Colors.WHITE}{'Member Since':<18}{Colors.RESET}: {Colors.CYAN}{created_date}{Colors.RESET}")
            print(f"  {Colors.WHITE}{'Profile URL':<18}{Colors.RESET}: {Colors.CYAN}{data.get('html_url')}{Colors.RESET}")

        elif res.status_code == 404:
            print(f"{Colors.RED}Error: User '{username}' not found.{Colors.RESET}")
        else:
            print(f"{Colors.RED}Error: Failed to fetch data (Status Code: {res.status_code}){Colors.RESET}")
    except requests.RequestException as e:
        print(f"{Colors.RED}Error connecting to GitHub API: {e}{Colors.RESET}")

def real_qr_generator(script_name):
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name}...{Colors.RESET}\n")
    data = get_validated_input(f"{Colors.WHITE}Enter data for QR Code (URL or text): {Colors.RESET}", validate_not_empty, "Data cannot be empty!")
    if data is None: return
    filename = input(f"{Colors.WHITE}Enter filename to save (e.g., myQR.png): {Colors.RESET}")
    if filename is None: return
    filename = filename.strip()
    if not filename.lower().endswith('.png'): filename += '.png'
    
    try:
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(filename)
        print(f"\n{Colors.BOLD}{Colors.GREEN}SUCCESS! QR Code saved as {os.path.abspath(filename)}{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.RED}Error creating QR Code: {e}{Colors.RESET}")

def real_weather_forecaster(script_name):
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name}...{Colors.RESET}\n")
    city = get_validated_input(f"{Colors.WHITE}Enter city name: {Colors.RESET}", validate_not_empty, "City cannot be empty!")
    if city is None: return
    try:
        print(f"\n{Colors.CYAN}Fetching weather for {city}...{Colors.RESET}")
        res = requests.get(f"https://wttr.in/{city}?format=3")
        res.raise_for_status()
        print(f"\n{Colors.BOLD}{Colors.MAGENTA}--- WEATHER FORECAST ---{Colors.RESET}")
        print(f"  {Colors.CYAN}{res.text}{Colors.RESET}")
    except requests.RequestException:
        print(f"{Colors.RED}Error: Could not fetch weather data. Check city name or your connection.{Colors.RESET}")

def real_lorem_ipsum_generator(script_name):
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name}...{Colors.RESET}\n")
    words = ["lorem", "ipsum", "dolor", "sit", "amet", "consectetur", "adipiscing", "elit", "sed", "do", "eiusmod", "tempor", "incididunt", "ut", "labore", "et", "dolore", "magna", "aliqua"]
    try:
        num_paragraphs_str = get_validated_input(f"{Colors.WHITE}Enter number of paragraphs: {Colors.RESET}", validate_numeric, "Must be a number!")
        if num_paragraphs_str is None: return
        num_paragraphs = int(num_paragraphs_str)
        
        print(f"\n{Colors.BOLD}{Colors.MAGENTA}--- GENERATED LOREM IPSUM ---{Colors.RESET}")
        for _ in range(num_paragraphs):
            num_sentences = random.randint(3, 7)
            paragraph = []
            for _ in range(num_sentences):
                num_words = random.randint(5, 15)
                sentence = ' '.join(random.choices(words, k=num_words)).capitalize() + "."
                paragraph.append(sentence)
            print(' '.join(paragraph) + "\n")
    except (ValueError, TypeError):
        print(f"{Colors.RED}Invalid input.{Colors.RESET}")

def real_ping_tool(script_name):
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name}...{Colors.RESET}\n")
    host = get_validated_input(f"{Colors.WHITE}Enter host to ping (e.g., google.com or 8.8.8.8): {Colors.RESET}", validate_not_empty, "Host cannot be empty!")
    if host is None: return
    
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '4', host]
    
    try:
        print(f"\n{Colors.CYAN}Pinging {host}...{Colors.RESET}")
        subprocess.check_call(command)
    except subprocess.CalledProcessError:
        print(f"\n{Colors.RED}Ping failed. Host may be down or unreachable.{Colors.RESET}")
    except FileNotFoundError:
        print(f"\n{Colors.RED}'ping' command not found. Is it installed and in your PATH?{Colors.RESET}")

def real_yt_downloader(script_name):
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name}...{Colors.RESET}\n")
    url = get_validated_input(f"{Colors.WHITE}Enter YouTube Video URL: {Colors.RESET}", validate_url, "Invalid URL format!")
    if url is None: return
    try:
        print(f"\n{Colors.CYAN}Connecting to YouTube...{Colors.RESET}")
        yt = YouTube(url)
        print(f"{Colors.WHITE}Fetching video: {Colors.CYAN}{yt.title}{Colors.RESET}")
        
        stream = yt.streams.get_highest_resolution()
        if not stream:
            print(f"{Colors.RED}Error: No downloadable stream found.{Colors.RESET}")
            return
            
        print(f"{Colors.WHITE}Resolution: {Colors.CYAN}{stream.resolution}{Colors.RESET} | {Colors.WHITE}File Size: {Colors.CYAN}{stream.filesize / (1024*1024):.2f} MB{Colors.RESET}")
        download_path = input(f"{Colors.WHITE}Enter download path (leave empty for current directory): {Colors.RESET}")
        if download_path is None: return
        download_path = download_path.strip() or "."
        
        print(f"\n{Colors.CYAN}Starting download...{Colors.RESET}")
        stream.download(output_path=download_path)
        print(f"\n{Colors.BOLD}{Colors.GREEN}SUCCESS! Video '{yt.title}' downloaded to {os.path.abspath(download_path)}{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.RED}An error occurred: {e}{Colors.RESET}")

def real_image_to_base64(script_name):
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name}...{Colors.RESET}\n")
    path = get_validated_input(f"{Colors.WHITE}Enter full path to image file: {Colors.RESET}", os.path.isfile, "File not found!")
    if path is None: return
    try:
        with open(path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        print(f"\n{Colors.BOLD}{Colors.MAGENTA}--- BASE64 ENCODED IMAGE ---{Colors.RESET}")
        print(f"{Colors.CYAN}{encoded_string}{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.RED}Error processing file: {e}{Colors.RESET}")

def real_file_encryptor_decryptor(script_name):
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name}...{Colors.RESET}\n")
    
    def derive_key(password: str, salt: bytes) -> bytes:
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000)
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))

    choice = input(f"{Colors.WHITE}[1] Encrypt or [2] Decrypt?: {Colors.RESET}")
    if choice is None: return
    file_path = get_validated_input(f"{Colors.WHITE}Enter file path: {Colors.RESET}", os.path.isfile, "File not found!")
    if file_path is None: return
    password = input(f"{Colors.WHITE}Enter password: {Colors.RESET}")
    if password is None: return

    if choice == '1':
        try:
            with open(file_path, 'rb') as f: data = f.read()
            salt = os.urandom(16)
            key = derive_key(password, salt)
            fernet = Fernet(key)
            encrypted = fernet.encrypt(data)
            new_path = file_path + ".enc"
            with open(new_path, 'wb') as f:
                f.write(salt)
                f.write(encrypted)
            print(f"\n{Colors.GREEN}File encrypted successfully! Saved as {new_path}{Colors.RESET}")
        except Exception as e: print(f"\n{Colors.RED}Encryption failed: {e}{Colors.RESET}")
    elif choice == '2':
        try:
            with open(file_path, 'rb') as f:
                salt = f.read(16)
                encrypted_data = f.read()
            key = derive_key(password, salt)
            fernet = Fernet(key)
            decrypted = fernet.decrypt(encrypted_data)
            new_path = file_path.replace(".enc", ".dec")
            with open(new_path, 'wb') as f: f.write(decrypted)
            print(f"\n{Colors.GREEN}File decrypted successfully! Saved as {new_path}{Colors.RESET}")
        except Exception as e: print(f"\n{Colors.RED}Decryption failed. Check password or file integrity: {e}{Colors.RESET}")
    else: print(f"{Colors.RED}Invalid choice.{Colors.RESET}")

def real_diff_checker(script_name):
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name}...{Colors.RESET}\n")
    file1_path = get_validated_input(f"{Colors.WHITE}Enter path to first file: {Colors.RESET}", os.path.isfile, "File not found!")
    if file1_path is None: return
    file2_path = get_validated_input(f"{Colors.WHITE}Enter path to second file: {Colors.RESET}", os.path.isfile, "File not found!")
    if file2_path is None: return
    
    with open(file1_path) as f1, open(file2_path) as f2:
        file1_lines = f1.readlines()
        file2_lines = f2.readlines()
    
    diff = difflib.unified_diff(file1_lines, file2_lines, fromfile=os.path.basename(file1_path), tofile=os.path.basename(file2_path), lineterm='')
    print(f"\n{Colors.BOLD}{Colors.MAGENTA}--- FILE DIFFERENCES ---{Colors.RESET}")
    has_diff = False
    for line in diff:
        has_diff = True
        color = Colors.RESET
        if line.startswith('+'): color = Colors.GREEN
        elif line.startswith('-'): color = Colors.RED
        elif line.startswith('@'): color = Colors.CYAN
        print(color + line + Colors.RESET)
    if not has_diff: print(f"{Colors.GREEN}Files are identical.{Colors.RESET}")

def real_password_strength_checker(script_name):
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name}...{Colors.RESET}\n")
    password = input(f"{Colors.WHITE}Enter password to check: {Colors.RESET}")
    if password is None: return
    score = 0
    if len(password) >= 8: score += 1
    if len(password) >= 12: score += 1
    if re.search(r"[a-z]", password): score += 1
    if re.search(r"[A-Z]", password): score += 1
    if re.search(r"\d", password): score += 1
    if re.search(r"[\W_]", password): score += 1
    
    strength = "Very Weak"
    color = Colors.RED
    if score >= 6: strength, color = "Very Strong", Colors.GREEN
    elif score >= 5: strength, color = "Strong", Colors.GREEN
    elif score >= 4: strength, color = "Moderate", Colors.YELLOW
    elif score >= 3: strength, color = "Weak", Colors.YELLOW

    print(f"\n{Colors.BOLD}{Colors.MAGENTA}--- PASSWORD STRENGTH ---{Colors.RESET}")
    print(f"  Password strength: {color}{strength}{Colors.RESET}")

def real_ascii_art_generator(script_name):
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name}...{Colors.RESET}\n")
    text = input(f"{Colors.WHITE}Enter text for ASCII Art: {Colors.RESET}")
    if text is None: return
    try:
        result = pyfiglet.figlet_format(text)
        print(f"\n{Colors.BOLD}{Colors.MAGENTA}--- ASCII ART ---{Colors.RESET}")
        print(f"{Colors.CYAN}{result}{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.RED}Error generating ASCII art: {e}{Colors.RESET}")

def real_morse_translator(script_name):
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name}...{Colors.RESET}\n")
    MORSE_CODE_DICT = { 'A':'.-', 'B':'-...', 'C':'-.-.', 'D':'-..', 'E':'.', 'F':'..-.', 'G':'--.', 'H':'....', 'I':'..', 'J':'.---', 'K':'-.-', 'L':'.-..', 'M':'--', 'N':'-.', 'O':'---', 'P':'.--.', 'Q':'--.-', 'R':'.-.', 'S':'...', 'T':'-', 'U':'..-', 'V':'...-', 'W':'.--', 'X':'-..-', 'Y':'-.--', 'Z':'--..', '1':'.----', '2':'..---', '3':'...--', '4':'....-', '5':'.....', '6':'-....', '7':'--...', '8':'---..', '9':'----.', '0':'-----', ',':'--..--', '.':'.-.-.-', '?':'..--..', '/':'-..-.', '-':'-....-', '(':'-.--.', ')':'-.--.-'}
    choice = input(f"{Colors.WHITE}[1] Text to Morse or [2] Morse to Text?: {Colors.RESET}")
    if choice is None: return
    
    if choice == '1':
        text = input(f"{Colors.WHITE}Enter text: {Colors.RESET}")
        if text is None: return
        result = ' '.join(MORSE_CODE_DICT.get(char, '') for char in text.upper())
        print(f"\n{Colors.BOLD}{Colors.MAGENTA}--- MORSE CODE ---{Colors.RESET}\n  {Colors.CYAN}{result}{Colors.RESET}")
    elif choice == '2':
        morse = input(f"{Colors.WHITE}Enter morse code (space separated): {Colors.RESET}")
        if morse is None: return
        inv_morse_dict = {v: k for k, v in MORSE_CODE_DICT.items()}
        result = ''.join(inv_morse_dict.get(code, '') for code in morse.split(' '))
        print(f"\n{Colors.BOLD}{Colors.MAGENTA}--- DECODED TEXT ---{Colors.RESET}\n  {Colors.CYAN}{result}{Colors.RESET}")
    else: print(f"{Colors.RED}Invalid choice.{Colors.RESET}")

def real_local_web_server(script_name):
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name}...{Colors.RESET}\n")
    import http.server
    import socketserver
    port = 8000
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"{Colors.GREEN}Serving HTTP on port {port} from directory '{os.getcwd()}'...{Colors.RESET}")
        print(f"{Colors.YELLOW}Open http://localhost:{port} in your browser.{Colors.RESET}")
        print(f"{Colors.RED}Press Ctrl+C to stop the server.{Colors.RESET}")
        try: httpd.serve_forever()
        except KeyboardInterrupt: print(f"\n{Colors.RED}Server stopped.{Colors.RESET}")

def real_system_info_exporter(script_name):
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name}...{Colors.RESET}\n")
    try:
        print(f"{Colors.CYAN}Gathering system information...{Colors.RESET}")
        uname = platform.uname(); cpu_info_data = cpuinfo.get_cpu_info()
        os_details = get_os_details(uname)
        svmem = psutil.virtual_memory()
        
        info = f"""--- DesxScript System Info Export ---
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

--- Device & OS ---
OS Version: {os_details}
Model: {uname.node}
Architecture: {cpu_info_data.get('arch_string_raw', 'N/A')}

--- CPU ---
Chipset: {cpu_info_data.get('brand_raw', 'N/A')}
Cores: {psutil.cpu_count(logical=True)}

--- Memory ---
Total RAM: {svmem.total / (1024**3):.2f} GB
"""
        filename = "system_info.txt"
        with open(filename, "w") as f: f.write(info)
        print(f"\n{Colors.GREEN}System information exported to {os.path.abspath(filename)}{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.RED}Failed to export system info: {e}{Colors.RESET}")

def real_readme_card_generator(script_name):
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name}...{Colors.RESET}\n")
    print(f"{Colors.CYAN}Let's create your DesxScript Member Card for GitHub!{Colors.RESET}")
    
    # Collect user data
    name = get_validated_input(f"{Colors.WHITE}Enter Your Name: {Colors.RESET}", validate_not_empty, "Name cannot be empty!")
    if name is None: return
    
    location = get_validated_input(f"{Colors.WHITE}Location: {Colors.RESET}", validate_not_empty, "Location cannot be empty!")
    if location is None: return
    
    field = get_validated_input(f"{Colors.WHITE}Field / Jurusan: {Colors.RESET}", validate_not_empty, "Field cannot be empty!")
    if field is None: return
    
    school = input(f"{Colors.WHITE}School / University (Opsional): {Colors.RESET}")
    if school is None: return
    school = school.strip()

    motto_line1 = input(f"{Colors.WHITE}Motto Baris 1 (Opsional): {Colors.RESET}")
    if motto_line1 is None: return
    motto_line1 = motto_line1.strip()

    motto_line2 = input(f"{Colors.WHITE}Motto Baris 2 (Opsional): {Colors.RESET}")
    if motto_line2 is None: return
    motto_line2 = motto_line2.strip()
    
    birth_date_str = get_validated_input(f"{Colors.WHITE}Tanggal Lahir (DD-MM-YYYY): {Colors.RESET}", validate_date, "Format tanggal salah!")
    if birth_date_str is None: return

    special_code = input(f"{Colors.WHITE}Enter Special Code (e.g., 17102009): {Colors.RESET}")
    if special_code is None: special_code = ""
    special_code = special_code.strip()

    # Calculate age
    try:
        birth_date = datetime.strptime(birth_date_str, "%d-%m-%Y")
        today = datetime.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    except:
        age = "N/A"

    # Set theme based on special code
    if special_code == "17102009": # OWNER
        status_text, stroke_color = "OWNER", "red"
    elif special_code == "slnn0860": # ADMIN
        status_text, stroke_color = "ADMIN", "gold"
    else: # MEMBER
        status_text, stroke_color = "MEMBER", "deepskyblue"

    # Build SVG string
    svg_code = f"""
<svg width="500" height="420" xmlns="http://www.w3.org/2000/svg">
  <style>
    .card {{ fill:#111; stroke-width:4; rx:25; ry:25; }}
    .name {{ font: bold 30px sans-serif; fill:white; }}
    .status {{ font: bold 22px sans-serif; }}
    .info {{ font: 18px sans-serif; fill:white; }}
    .motto {{ font: italic 16px sans-serif; fill:white; }}
    .footer {{ font: 12px sans-serif; fill:gray; }}
    .shimmer {{ animation: move 3s infinite; }}
    @keyframes move {{ 0%{{x:-200;}}100%{{x:600;}} }}
  </style>

  <defs>
    <linearGradient id="shimmer" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="transparent"/>
      <stop offset="50%" stop-color="rgba(255,255,255,0.3)"/>
      <stop offset="100%" stop-color="transparent"/>
    </linearGradient>
    <clipPath id="clip">
      <rect x="0" y="0" width="500" height="420" rx="25" ry="25"/>
    </clipPath>
  </defs>

  <g>
    <rect class="card" stroke="{stroke_color}" width="500" height="420"/>
    <rect class="shimmer" width="120" height="420" fill="url(#shimmer)" clip-path="url(#clip)"/>
    <text x="40" y="60" class="name">{name}</text>
    <text x="40" y="95" class="status" fill="{stroke_color}">{status_text}</text>
    <text x="40" y="145" class="info">Age: {age}</text>
    <text x="40" y="180" class="info">Location: {location}</text>
    <text x="40" y="215" class="info">Field: {field}</text>
    {"<text x='40' y='250' class='info'>School: " + school + "</text>" if school else ""}
    {"<text x='40' y='300' class='motto'>&quot;" + motto_line1 + "&quot;</text>" if motto_line1 else ""}
    {"<text x='40' y='325' class='motto'>&quot;" + motto_line2 + "&quot;</text>" if motto_line2 else ""}
    <text x="250" y="400" text-anchor="middle" class="footer">
      Generated by DesxScript Toolkit | DesxTools
    </text>
  </g>
</svg>
    """

    print(f"\n{Colors.BOLD}{Colors.GREEN}--- KODE KARTU PROFIL ANDA SIAP ---{Colors.RESET}")
    print(f"{Colors.YELLOW}Salin semua kode di bawah ini dan tempelkan ke file README.md di profil GitHub Anda.{Colors.RESET}")
    print(f"\n{Colors.CYAN}```markdown")
    print(svg_code.strip())
    print("```" + Colors.RESET)

def real_desx_gpt(script_name):
    """Chat with DesxGPT powered by a direct API call to Gemini."""
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name}...{Colors.RESET}\n")

    if not GEMINI_API_KEY or "AIza" not in GEMINI_API_KEY:
        print(f"{Colors.RED}Gemini API key is not configured correctly in the script.{Colors.RESET}")
        return

    # Use a more reliable model name
    model_name = "gemini-1.5-flash-latest"
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={GEMINI_API_KEY}"
    
    headers = {'Content-Type': 'application/json'}

    system_prompt = (
        "You are DesxGPT, a helpful and friendly AI assistant integrated into the DesxScript Ultimate Toolkit. "
        "Your creator is Rakhan Atthaya, a talented young Software Engineering student from Balikpapan, Indonesia, also known online as 'rkhnatthyascrpter'. "
        "He developed DesxScript, a multi-purpose command-line tool, to help programmers, developers, and IT enthusiasts with their tasks. "
        "Rakhan is passionate about full-stack development and studies at IDN Boarding School. "
        "Your purpose is to assist users with their questions concisely and accurately, acting as a knowledgeable companion within his software. "
        "Always remember your name is DesxGPT and you were created by Rakhan Atthaya."
    )
    
    # Initialize conversation history with the system prompt
    conversation_history = [
        {'role': 'user', 'parts': [{'text': f"Please adopt the following persona for our conversation: {system_prompt}"}]},
        {'role': 'model', 'parts': [{'text': "Understood. I am DesxGPT, an AI assistant within the DesxScript Ultimate Toolkit. How can I help you today?"}]}
    ]

    print(f"{Colors.CYAN}Welcome to DesxGPT. I am an AI assistant ready to help.{Colors.RESET}")
    print(f"{Colors.YELLOW}Type 'exit' or 'quit' to end the chat.{Colors.RESET}\n")
    
    while True:
        prompt = input(f"{Colors.GREEN}You: {Colors.RESET}")
        if prompt is None or prompt.lower() in ['exit', 'quit']:
            print(f"\n{Colors.YELLOW}DesxGPT session ended.{Colors.RESET}")
            break
        
        # Add user's message to history
        conversation_history.append({'role': 'user', 'parts': [{'text': prompt}]})
        
        payload = {'contents': conversation_history}
        
        try:
            print(f"{Colors.GRAY}DesxGPT is thinking...{Colors.RESET}", end="\r")
            
            response = requests.post(api_url, headers=headers, data=json.dumps(payload), timeout=60)
            response.raise_for_status() # Raise an exception for bad status codes
            
            response_data = response.json()
            
            # Extract text and handle potential errors
            try:
                ai_response_text = response_data['candidates'][0]['content']['parts'][0]['text']
                # Add AI's response to history
                conversation_history.append({'role': 'model', 'parts': [{'text': ai_response_text}]})

                print(" " * 30, end="\r") # Clear thinking message
                print(f"{Colors.CYAN}DesxGPT: {Colors.RESET}{ai_response_text}")
            except (KeyError, IndexError):
                print(f"\n{Colors.RED}Could not parse the API response. Full response: {response_data}{Colors.RESET}")

        except requests.exceptions.HTTPError as http_err:
             print(f"\n{Colors.RED}An HTTP error occurred: {http_err}{Colors.RESET}")
             print(f"{Colors.RED}Response Body: {response.text}{Colors.RESET}")
        except Exception as e:
            print(f"\n{Colors.RED}An unexpected error occurred: {e}{Colors.RESET}")

# --- SYSTEM INFO HELPER FUNCTIONS ---
def get_os_details(uname):
    system = uname.system
    if system == "Windows": return f"Windows {uname.release}"
    elif system == "Darwin":
        ver = platform.mac_ver()
        try:
            name = subprocess.check_output(['sw_vers', '-productName']).decode().strip()
            return f"{name} {ver[0]}"
        except Exception: return f"macOS {ver[0]}"
    elif system == "Linux":
        try:
            with open("/etc/os-release") as f:
                for line in f:
                    if line.startswith("PRETTY_NAME="): return line.split('"')[1]
        except Exception: return f"{uname.system} {uname.release}"
    return f"{uname.system} {uname.release}"

def format_info(data):
    if not data: return ""
    valid_data = [(k, v) for k, v in data if k is not None]
    if not valid_data: return ""
    max_len = max(len(key) for key, val in valid_data) + 2
    lines = []
    mid_point = (len(data) + 1) // 2
    col1 = data[:mid_point]
    col2 = data[mid_point:]
    
    while len(col1) > len(col2): col2.append((None, None))
    while len(col2) > len(col1): col1.append((None, None))

    for (k1, v1), (k2, v2) in zip(col1, col2):
        line = ""
        if k1 is not None: line += f"  {Colors.WHITE}{k1.ljust(max_len)}{Colors.RESET}: {Colors.CYAN}{str(v1)}{Colors.RESET}".ljust(60)
        if k2 is not None: line += f"  {Colors.WHITE}{k2.ljust(max_len)}{Colors.RESET}: {Colors.CYAN}{str(v2)}{Colors.RESET}"
        lines.append(line)
    return "\n".join(lines)

# --- MAIN APPLICATION ---
def main():
    # --- SCRIPT CONFIGURATION ---
    ALL_SCRIPTS = [
        # Advanced Tools
        {'name': "Bot Follower IG/TikTok", 'func': tool_bot_follower},
        {'name': "Web Deface Tool", 'func': tool_web_deface},
        {'name': "Email Bomber", 'func': tool_email_bomber},
        {'name': "WiFi Password Cracker", 'func': tool_wifi_cracker},
        {'name': "Credit Card Generator", 'func': tool_cc_generator},
        {'name': "MAC Address Changer", 'func': tool_mac_changer},
        {'name': "Windows Activation", 'func': tool_windows_activation, 'win_only': True},
        {'name': "DDoS L7 (Website Attack)", 'func': tool_ddos_l7},
        {'name': "Keylogger", 'func': tool_generic, 'win_only': True},
        {'name': "Rootkit Installer", 'func': tool_generic, 'linux_only': True},
        # Network & Web Tools
        {'name': "Port Scanner", 'func': real_port_scanner},
        {'name': "Subdomain Enumerator", 'func': real_subdomain_enumerator},
        {'name': "Admin Panel Finder", 'func': real_admin_finder},
        {'name': "Website Cloner", 'func': real_website_cloner},
        {'name': "DNS Lookup Tool", 'func': real_dns_lookup},
        {'name': "HTTP Header Viewer", 'func': real_http_header_viewer},
        {'name': "IP Geolocation", 'func': real_ip_geolocation},
        {'name': "Web Link Extractor", 'func': real_link_extractor},
        {'name': "WHOIS Lookup", 'func': real_whois_lookup},
        {'name': "What Is My IP", 'func': real_what_is_my_ip},
        {'name': "Network Ping Tool", 'func': real_ping_tool},
        {'name': "YouTube Video Downloader", 'func': real_yt_downloader},
        # File & Data Tools
        {'name': "Hash Identifier", 'func': real_hash_identifier},
        {'name': "Metadata Scraper", 'func': real_metadata_scraper},
        {'name': "File Hasher", 'func': real_file_hasher},
        {'name': "URL Shortener", 'func': real_url_shortener},
        {'name': "Base64 Tool", 'func': real_base64_tool},
        {'name': "JSON Validator & Formatter", 'func': real_json_validator},
        {'name': "Code Line Counter", 'func': real_line_counter},
        {'name': "Directory Tree Generator", 'func': real_directory_tree},
        {'name': "QR Code Generator", 'func': real_qr_generator},
        {'name': "Image to Base64", 'func': real_image_to_base64},
        {'name': "File Encryptor/Decryptor", 'func': real_file_encryptor_decryptor},
        {'name': "File Difference Checker", 'func': real_diff_checker},
        # Utility Tools
        {'name': "Fake Identity Generator", 'func': real_fake_identity_generator},
        {'name': "GitHub User Info", 'func': real_github_user_info},
        {'name': "Password Generator", 'func': real_password_generator},
        {'name': "Password Strength Checker", 'func': real_password_strength_checker},
        {'name': "Weather Forecaster", 'func': real_weather_forecaster},
        {'name': "ASCII Art Generator", 'func': real_ascii_art_generator},
        {'name': "Morse Code Translator", 'func': real_morse_translator},
        {'name': "Lorem Ipsum Generator", 'func': real_lorem_ipsum_generator},
        {'name': "Start Local Web Server", 'func': real_local_web_server},
        {'name': "System Info Exporter", 'func': real_system_info_exporter},
    ]

    # --- SYSTEM INFO FUNCTIONS ---
    def display_system_info_screen():
        try:
            uname = platform.uname(); cpu_info_data = cpuinfo.get_cpu_info()
            os_details = get_os_details(uname)
            while True:
                device_os = [("OS Version", os_details), ("Internal Model", uname.node), ("Architecture", cpu_info_data.get('arch_string_raw', 'N/A')), ("Kernel Version", uname.release), ("Build ID", uname.version.split(' ')[0])]
                boot_time = timedelta(seconds=int(time.time() - psutil.boot_time()))
                cpu_percents = psutil.cpu_percent(percpu=True, interval=0.1)
                cpu_data = [("Uptime", str(boot_time)), ("Chipset Name", cpu_info_data.get('brand_raw', 'N/A')), ("Physical Cores", psutil.cpu_count(logical=False)), ("Total Cores", psutil.cpu_count(logical=True)), ("L2 Cache", f"{cpu_info_data.get('l2_cache_size', 0) // 1024} KB"), ("L3 Cache", f"{cpu_info_data.get('l3_cache_size', 0) // 1024} KB")]
                svmem = psutil.virtual_memory(); swap = psutil.swap_memory()
                mem_data = [("Total RAM", f"{svmem.total / (1024**3):.2f} GB"), ("Available RAM", f"{svmem.available / (1024**3):.2f} GB"), ("Used RAM", f"{svmem.used / (1024**3):.2f} GB ({svmem.percent}%)"), ("Total Swap", f"{swap.total / (1024**3):.2f} GB"), ("Used Swap", f"{swap.used / (1024**3):.2f} GB ({swap.percent}%)")]
                battery_data = []
                battery = psutil.sensors_battery()
                if battery:
                    power_plugged = "Plugged In" if battery.power_plugged else "Not Plugged"
                    health = "Good"
                    battery_data.extend([("Percentage", f"{battery.percent}%"), ("Status", power_plugged), ("Health", health)])
                    if battery.secsleft != psutil.POWER_TIME_UNLIMITED and not battery.power_plugged: battery_data.append(("Time Left", str(timedelta(seconds=battery.secsleft))))
                else: battery_data.append(("Status", "Not Detected"))

                clear_screen()
                print(f"{Colors.BOLD}{Colors.MAGENTA}--- Device & OS ---{Colors.RESET}\n{format_info(device_os)}")
                print(f"\n{Colors.BOLD}{Colors.MAGENTA}--- CPU ---{Colors.RESET}\n{format_info(cpu_data)}")
                cpu_bars = [f"  {Colors.WHITE}Core {i}  [{Colors.GREEN}{'█' * int(p / 10)}{' ' * (10 - int(p / 10))}{Colors.RESET}] {p:5.1f}%{Colors.RESET}" for i, p in enumerate(cpu_percents)]
                print("\n".join(cpu_bars))
                print(f"\n{Colors.BOLD}{Colors.MAGENTA}--- Memory ---{Colors.RESET}\n{format_info(mem_data)}")
                if battery_data: print(f"\n{Colors.BOLD}{Colors.MAGENTA}--- Battery ---{Colors.RESET}\n{format_info(battery_data)}")
                print(f"\n{Colors.GRAY}Dashboard is refreshing. Press [Ctrl+C] to return...{Colors.RESET}")
                time.sleep(2)
        except KeyboardInterrupt: return
        except Exception as e:
            clear_screen()
            print(f"\n{Colors.RED}An error occurred while fetching system info: {e}{Colors.RESET}")
            input("Press [Enter] to return...")

    # --- MAIN LOOP ---
    def display_main_menu():
        clear_screen(); print(get_title_art())
        print(f"\n{Colors.BOLD}{Colors.YELLOW}AVAILABLE SCRIPTS MENU".center(90) + f"{Colors.RESET}"); print("="*80 + "\n")
        
        num_items = len(ALL_SCRIPTS)
        num_cols = 3
        items_per_col = (num_items + num_cols - 1) // num_cols
        current_os = platform.system()

        for i in range(items_per_col):
            line = ""
            for j in range(num_cols):
                idx = i + j * items_per_col
                if idx < num_items:
                    script = ALL_SCRIPTS[idx]
                    num = f"{idx + 1:02d}"
                    name = script['name']
                    color = Colors.WHITE
                    
                    is_win_only = script.get('win_only', False)
                    is_linux_only = script.get('linux_only', False)

                    if (current_os != "Windows" and is_win_only) or \
                       (current_os != "Linux" and is_linux_only):
                        color = Colors.RED
                    
                    prefix = "  " if j == 0 else ""
                    line += f"{prefix}[{Colors.CYAN}{num}{Colors.RESET}] {color}{name.ljust(35)}{Colors.RESET}"
            print(line)
        print("\n" + "="*80)
        
        # New section for special tools
        print(f"\n{Colors.BOLD}{Colors.YELLOW}SPECIAL GENERATORS".center(90) + f"{Colors.RESET}"); print("="*80 + "\n")
        print(f"  [{Colors.CYAN}C{Colors.RESET}] {Colors.WHITE}GitHub README Card Generator{Colors.RESET}")
        print(f"  [{Colors.CYAN}A{Colors.RESET}] {Colors.WHITE}DesxGPT AI{Colors.RESET}")
        print("\n" + "="*80)


    while True:
        display_main_menu()
        try:
            choice = input(f"\n{Colors.YELLOW}Select an option, [S] for System Info, or [Q] to Quit: {Colors.RESET}").lower()
            if choice == 'q':
                clear_screen(); print(f"\n{Colors.CYAN}{Colors.BOLD}Thank you for using DesxScript.{Colors.RESET}\n"); break
            elif choice == 's':
                display_system_info_screen(); continue
            elif choice == 'c':
                real_readme_card_generator("GitHub README Card Generator")
                input(f"\n{Colors.YELLOW}Press [Enter] to return to the main menu...{Colors.RESET}")
                continue
            elif choice == 'a':
                real_desx_gpt("DesxGPT AI")
                input(f"\n{Colors.YELLOW}Press [Enter] to return to the main menu...{Colors.RESET}")
                continue

            choice_int = int(choice)
            if not (1 <= choice_int <= len(ALL_SCRIPTS)):
                raise ValueError("Selection out of range")

            script_info = ALL_SCRIPTS[choice_int - 1]
            script_name = script_info['name']
            current_os = platform.system()

            if (current_os != "Windows" and script_info.get('win_only')) or \
               (current_os != "Linux" and script_info.get('linux_only')):
                print(f"{Colors.RED}Error: The '{script_name}' tool is not compatible with your OS ({current_os}).{Colors.RESET}")
                time.sleep(3); continue

            script_info['func'](script_name)

            input(f"\n{Colors.YELLOW}Press [Enter] to return to the main menu...{Colors.RESET}")
        except (ValueError, IndexError):
            print(f"{Colors.RED}Invalid selection.{Colors.RESET}"); time.sleep(2)
        except KeyboardInterrupt:
            clear_screen(); print(f"\n{Colors.YELLOW}Operation cancelled. Returning to menu...{Colors.RESET}"); time.sleep(2)
        except Exception as e:
            print(f"{Colors.RED}An unexpected error occurred: {e}{Colors.RESET}"); time.sleep(3)

if __name__ == "__main__":
    all_packages = {
        'requests': 'requests', 'PIL': 'Pillow', 'PyPDF2': 'PyPDF2',
        'faker': 'Faker', 'bs4': 'beautifulsoup4', 'whois': 'python-whois',
        'psutil': 'psutil', 'cpuinfo': 'py-cpuinfo', 'qrcode': 'qrcode',
        'pyfiglet': 'pyfiglet', 'cryptography': 'cryptography',
        'getmac': 'get-mac', 'pytube': 'pytube'
    }
    if platform.system() == "Windows": all_packages['wmi'] = 'WMI'
    
    # Robust dependency check
    missing_imports = []
    for import_name in all_packages.keys():
        try:
            importlib.import_module(import_name)
        except ImportError:
            missing_imports.append(import_name)

    if missing_imports:
        pip_missing = [all_packages[name] for name in missing_imports]
        check_and_install_dependencies(pip_missing)
    
    import requests
    from PIL import Image
    from PIL.ExifTags import TAGS
    import PyPDF2
    from faker import Faker
    from bs4 import BeautifulSoup
    import whois
    import psutil
    import cpuinfo
    import qrcode
    import pyfiglet
    from cryptography.fernet import Fernet
    from getmac import get_mac_address as getmac
    from pytube import YouTube
    if platform.system() == "Windows": import wmi

    main()

