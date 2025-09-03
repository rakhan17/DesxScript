import os
import time
import random
import sys
import platform
import subprocess
import importlib.util
from datetime import timedelta
import socket
import re
from urllib.parse import urljoin, urlparse
import string
import hashlib
import base64
import binascii

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
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', pip_name])
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
    return f"""{color}{Colors.BOLD}
██████╗ ███████╗███████╗██╗  ██╗███████╗ ██████╗██████╗ ██╗██████╗ ████████╗
██╔══██╗██╔════╝██╔════╝╚██╗██╔╝██╔════╝██╔════╝██╔══██╗██║██╔══██╗╚══██╔══╝
██║  ██║█████╗  ███████╗ ╚███╔╝ ███████╗██║     ██████╔╝██║██████╔╝   ██║   
██║  ██║██╔══╝  ╚════██║ ██╔██╗ ╚════██║██║     ██══██╗██║██╔═══╝    ██║   
██████╔╝███████╗███████║██╔╝ ██╗███████║╚██████╗██║  ██║██║██║        ██║   
╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝╚═╝        ╚═╝   
{Colors.RESET}{Colors.CYAN}{'DesxScript Ultimate Toolkit v7.0'.center(88)}
{'created by rkhnatthyascrpter'.center(88)}{Colors.RESET}
"""

def get_validated_input(prompt, validation_func, error_message):
    while True:
        user_input = input(prompt)
        if validation_func(user_input): return user_input
        else: print(f"{Colors.RED}{error_message}{Colors.RESET}")

validate_url = lambda u: u.startswith('http://') or u.startswith('https://')
validate_not_empty = lambda s: len(s.strip()) > 0
validate_numeric = lambda n: n.isdigit() and int(n) > 0
validate_username = lambda u: u.startswith('@') and len(u) > 1
validate_ip = lambda ip: len(ip.split('.')) == 4 and all(p.isdigit() and 0 <= int(p) <= 255 for p in ip.split('.'))

# --- SIMULATION ENGINE ---
STEP_LIBRARY = {
    'SOCIAL_INIT': ["Connecting to Social Media API", "Bypassing SSL Pinning", "Authenticating session"],
    'SOCIAL_EXPLOIT': ["Injecting follower packets", "Finding vulnerable endpoint", "Bypassing rate limits"],
    'WEB_SCAN': ["Scanning for common directories", "Checking server headers", "Testing for SQLi vulnerabilities"],
    'WEB_EXPLOIT': ["Uploading PHP shell", "Executing command injection", "Escalating privileges to root"],
    'CLEANUP': ["Erasing tracks from logs", "Closing secure connection", "Deleting temporary files"],
}
DELAY_MESSAGES = {
    'SOCIAL': ["API IS RESPONDING SLOWLY...", "RATE LIMIT REACHED, WAITING...", "CAPTCHA DETECTED, ATTEMPTING BYPASS..."],
    'WEB': ["WAF DETECTED, FINDING ALTERNATE ROUTE...", "UNEXPECTED RESPONSE...", "SLOWING SCAN TO AVOID DETECTION..."],
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
                        possible_messages = DELAY_MESSAGES.get(category, ["GENERIC DELAY..."])
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

# --- SIMULATED SCRIPTS ---
def simulate_bot_follower(script_name):
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name}...{Colors.RESET}\n")
    target = get_validated_input(f"{Colors.WHITE}Enter target username (e.g., @username): {Colors.RESET}", validate_username, "Invalid username format! Must start with '@'.")
    count = get_validated_input(f"{Colors.WHITE}Enter amount of followers: {Colors.RESET}", validate_numeric, "Amount must be a number!")
    print("-" * 50); run_simulation_steps([('SOCIAL_INIT', 3), ('SOCIAL_EXPLOIT', 5), ('CLEANUP', 1)])
    print(f"\n{Colors.BOLD}{Colors.GREEN}SUCCESS! {count} followers have been sent to {target}.{Colors.RESET}")

def simulate_web_deface(script_name):
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name}...{Colors.RESET}\n")
    target = get_validated_input(f"{Colors.WHITE}Enter target URL (e.g., http://example.com): {Colors.RESET}", validate_url, "Invalid URL format!")
    print("-" * 50); run_simulation_steps([('WEB_SCAN', 8), ('WEB_EXPLOIT', 5), ('CLEANUP', 2)])
    print(f"\n{Colors.BOLD}{Colors.GREEN}SUCCESS! Website {target} has been defaced.{Colors.RESET}")

def simulate_generic_script(script_name):
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name}...{Colors.RESET}\n")
    target = input(f"{Colors.WHITE}Enter Simulation Target (e.g. IP, Domain, User): {Colors.RESET}")
    print("-" * 50); run_simulation_steps([('SOCIAL_INIT', 3), ('WEB_SCAN', 5), ('CLEANUP', 2)])
    print(f"\n{Colors.YELLOW}Simulation for '{script_name}' on target '{target}' completed.{Colors.RESET}")

# --- REAL TOOL FUNCTIONS ---
def real_port_scanner(script_name):
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name}...{Colors.RESET}\n")
    target = get_validated_input(f"{Colors.WHITE}Enter Target IP or Domain: {Colors.RESET}", validate_not_empty, "Target cannot be empty!")
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
    hash_str = input(f"{Colors.WHITE}Enter hash string: {Colors.RESET}").strip().lower()
    patterns = {'MD5': r"^[a-f0-9]{32}$", 'SHA-1': r"^[a-f0-9]{40}$", 'SHA-256': r"^[a-f0-9]{64}$", 'SHA-512': r"^[a-f0-9]{128}$"}
    found = next((t for t, p in patterns.items() if re.match(p, hash_str)), "Unknown")
    print(f"\n{Colors.BOLD}{Colors.MAGENTA}--- RESULT ---{Colors.RESET}\n  {Colors.GREEN}Hash is likely of type {Colors.CYAN}{found}{Colors.RESET}." if found != "Unknown" else f"  {Colors.RED}Hash type does not match common patterns.{Colors.RESET}")

def real_metadata_scraper(script_name):
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name}...{Colors.RESET}\n")
    path = input(f"{Colors.WHITE}Enter full path to file (image/pdf): {Colors.RESET}").strip()
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
    try:
        print(f"{Colors.CYAN}Starting cloning process from {url}...{Colors.RESET}")
        res = requests.get(url, timeout=5); res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')
        domain = urlparse(url).netloc.replace('.', '_')
        if not os.path.exists(domain): os.makedirs(domain)
        with open(os.path.join(domain, 'index.html'), 'w', encoding='utf-8') as f: f.write(soup.prettify())
        print(f"  {Colors.GREEN}[+] Successfully saved index.html{Colors.RESET}")
        print(f"{Colors.CYAN}Downloading assets (CSS, JS)...{Colors.RESET}")
        for tag in soup.find_all(['link', 'script']):
            attr = 'href' if tag.name == 'link' else 'src'
            if tag.has_attr(attr) and tag[attr]:
                asset_url = urljoin(url, tag[attr])
                if urlparse(asset_url).netloc == urlparse(url).netloc:
                    try:
                        asset_res = requests.get(asset_url, timeout=3)
                        if asset_res.status_code == 200:
                            filename = os.path.basename(urlparse(asset_url).path)
                            if filename:
                                with open(os.path.join(domain, filename), 'wb') as f: f.write(asset_res.content)
                                print(f"    {Colors.GREEN}[+] Downloaded: {filename}{Colors.RESET}")
                    except requests.RequestException: print(f"    {Colors.RED}[-] Failed download: {os.path.basename(asset_url)}{Colors.RESET}")
        print(f"\n{Colors.BOLD}{Colors.GREEN}Cloning finished! Files saved in folder '{domain}'.{Colors.RESET}")
    except requests.RequestException as e: print(f"{Colors.RED}Error: Failed to access URL: {e}{Colors.RESET}")

def real_dns_lookup(script_name):
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name}...{Colors.RESET}\n")
    domain = get_validated_input(f"{Colors.WHITE}Enter domain name: {Colors.RESET}", validate_not_empty, "Domain cannot be empty!")
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
    length = int(get_validated_input(f"{Colors.WHITE}Password length (e.g., 16): {Colors.RESET}", validate_numeric, "Must be a number!"))
    include_symbols = input(f"{Colors.WHITE}Include symbols? (y/n): {Colors.RESET}").lower() == 'y'
    chars = string.ascii_letters + string.digits
    if include_symbols: chars += string.punctuation
    password = ''.join(random.choice(chars) for _ in range(length))
    print(f"\n{Colors.BOLD}{Colors.MAGENTA}--- GENERATED PASSWORD ---{Colors.RESET}\n  {Colors.GREEN}{password}{Colors.RESET}")

def real_file_hasher(script_name):
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name}...{Colors.RESET}\n")
    file_path = get_validated_input(f"{Colors.WHITE}Enter full path to file: {Colors.RESET}", os.path.exists, "File not found!")
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
    try:
        print(f"\n{Colors.CYAN}Shortening URL...{Colors.RESET}")
        api_url = f"http://tinyurl.com/api-create.php?url={long_url}"
        response = requests.get(api_url, timeout=5); response.raise_for_status()
        print(f"\n{Colors.BOLD}{Colors.MAGENTA}--- SHORTENED URL ---{Colors.RESET}\n  {Colors.GREEN}{response.text}{Colors.RESET}")
    except requests.RequestException as e: print(f"{Colors.RED}Error: Failed to shorten URL: {e}{Colors.RESET}")

def real_base64_tool(script_name):
    clear_screen(); print(f"{Colors.YELLOW}[*] {script_name}...{Colors.RESET}\n")
    choice = input(f"{Colors.WHITE}Select [1] Encode or [2] Decode: {Colors.RESET}")
    text = input(f"{Colors.WHITE}Enter text: {Colors.RESET}")
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

# --- SCRIPT MAPPING ---
script_options = {
    1: {'func': simulate_bot_follower},
    3: {'func': simulate_web_deface},
    60: {'func': real_port_scanner}, 61: {'func': real_subdomain_enumerator},
    62: {'func': real_admin_finder}, 63: {'func': real_hash_identifier},
    64: {'func': real_metadata_scraper}, 65: {'func': real_fake_identity_generator},
    66: {'func': real_website_cloner}, 67: {'func': real_dns_lookup},
    68: {'func': real_http_header_viewer}, 69: {'func': real_ip_geolocation},
    70: {'func': real_link_extractor}, 71: {'func': real_whois_lookup},
    72: {'func': real_password_generator}, 73: {'func': real_file_hasher},
    74: {'func': real_url_shortener}, 75: {'func': real_base64_tool},
    76: {'func': real_what_is_my_ip},
}

WIN_ONLY_SCRIPTS = [16]
LINUX_ONLY_SCRIPTS = [32]

# --- MAIN APPLICATION ---
def display_menu():
    clear_screen(); print(get_title_art())
    print(f"\n{Colors.BOLD}{Colors.YELLOW}AVAILABLE SCRIPTS MENU".center(90) + f"{Colors.RESET}"); print("="*80 + "\n")
    
    simulated_scripts = [
        ("01", "Bot Follower IG/TikTok"), ("02", "Social Media Phishing"), ("03", "Web Deface Tool"),
        ("04", "Spam OTP Call/SMS"), ("05", "VIP Database Access"), ("06", "SQL Injection Scanner"),
        ("07", "XSS Payload Generator"), ("11", "DDoS L4 (IP Attack)"), ("12", "Password Cracker (Brute)"),
        ("14", "Reverse Shell Generator"), ("15", "WiFi Password Extractor"), ("16", "Keylogger (Windows)"), 
        ("17", "File Encryptor"), ("18", "Steganography Tool"), ("20", "Network Traffic Sniffer"), 
        ("21", "MAC Address Spoofer"), ("22", "API Fuzzer"), ("23", "Directory Traversal Scan"),
        ("25", "Email Bomber"), ("26", "Social Engineering Toolkit"), ("27", "RAT Builder (Remote Admin)"),
        ("28", "TOR Network Router"), ("29", "Blockchain Wallet Cracker"), ("30", "Cloud Bucket Scanner"),
        ("31", "Malware Sandbox Evasion"),("32", "Rootkit Installer (Linux)"), ("33", "IoT Device Scanner"),
        # Add more simulations here up to 59
    ]
    
    real_tools = [
        ("60", "Port Scanner"), ("61", "Subdomain Enumerator"), ("62", "Admin Panel Finder"),
        ("63", "Hash Identifier"), ("64", "Metadata Scraper"), ("65", "Fake Identity Generator"),
        ("66", "Website Cloner"), ("67", "DNS Lookup Tool"), ("68", "HTTP Header Viewer"),
        ("69", "IP Geolocation"), ("70", "Web Link Extractor"), ("71", "WHOIS Lookup"),
        ("72", "Password Generator"), ("73", "File Hasher"), ("74", "URL Shortener"),
        ("75", "Base64 Tool"), ("76", "What Is My IP"),
    ]

    menu_items = simulated_scripts + real_tools
    num_items = len(menu_items)
    num_cols = 3
    items_per_col = (num_items + num_cols - 1) // num_cols
    current_os = platform.system()

    for i in range(items_per_col):
        line = ""
        for j in range(num_cols):
            idx = i + j * items_per_col
            if idx < num_items:
                num, name = menu_items[idx]; num_int = int(num)
                color = Colors.WHITE
                if (current_os != "Windows" and num_int in WIN_ONLY_SCRIPTS) or \
                   (current_os != "Linux" and num_int in LINUX_ONLY_SCRIPTS):
                    color = Colors.RED
                prefix = "  " if j == 0 else ""
                line += f"{prefix}[{Colors.CYAN}{num}{Colors.RESET}] {color}{name.ljust(35)}{Colors.RESET}"
        print(line)
    print("\n" + "="*80)
    return menu_items
    
def main():
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

    def format_info(data, cols=2):
        if not data: return ""
        # Filter out None keys before finding max length
        valid_keys = [key for key, val in data if key is not None]
        if not valid_keys: return ""
        max_len = max(len(key) for key in valid_keys) + 2
        lines = []
        try: term_width = os.get_terminal_size().columns
        except OSError: term_width = 80
        col_width = (term_width // cols) - 2
        for i in range(0, len(data), cols):
            row_items = data[i:i+cols]
            line = ""
            for key, val in row_items:
                if key is None: continue
                line += f"{Colors.WHITE}{key.ljust(max_len)}{Colors.RESET}: {Colors.CYAN}{str(val)}{Colors.RESET}".ljust(col_width)
            lines.append(line)
        return "\n".join(lines)

    def display_system_info_screen():
        try:
            uname = platform.uname(); cpu_info_data = cpuinfo.get_cpu_info()
            os_details = get_os_details(uname)
            while True:
                output_buffer = []
                svmem = psutil.virtual_memory(); swap = psutil.swap_memory()
                boot_time = timedelta(seconds=int(time.time() - psutil.boot_time()))
                cpu_percents = psutil.cpu_percent(percpu=True, interval=0.1)
                
                # --- Build Data Sections ---
                device_os = [("OS Version", os_details), ("Architecture", cpu_info_data.get('arch', 'N/A')), ("Uptime", str(boot_time))]
                cpu_data = [("Model", cpu_info_data.get('brand_raw', 'N/A')), ("Physical Cores", psutil.cpu_count(logical=False)), ("Total Cores", psutil.cpu_count(logical=True))]
                mem_data = [("Total RAM", f"{svmem.total / (1024**3):.2f} GB"), ("Available", f"{svmem.available / (1024**3):.2f} GB"), ("Used", f"{svmem.percent}%")]
                
                # --- Mobile-only data section ---
                mobile_data = [
                    ("Marketing Name", "[Mobile Data Only]"), ("Internal Model", "[Mobile Data Only]"), ("Device Code", "[Mobile Data Only]"),
                    ("OS Codename", "[Mobile Data Only]"), ("Security Patch", "[Mobile Data Only]"), ("Root/Jailbreak", "[Mobile Data Only]"),
                    ("Thermal Throttling", "[Mobile Data Only]"), ("Chipset Mfg.", "[Mobile Data Only]"), ("CPU Governor", "[Mobile Data Only]"),
                    ("RAM Type", "[Mobile Data Only]"), ("Memory Bandwidth", "[Mobile Data Only]"), ("Storage Type", "[Mobile Data Only]"),
                    ("Sequential Read", "[Mobile Data Only]"), ("Sequential Write", "[Mobile Data Only]"), ("Bootloader Ver.", "[Mobile Data Only]"),
                    ("Baseband Ver.", "[Mobile Data Only]"), ("Storage Encryption", "[Mobile Data Only]"), ("Security Platform", "[Mobile Data Only]"),
                    ("Biometric Type", "[Mobile Data Only]"), ("Widevine DRM", "[Mobile Data Only]"), ("Wi-Fi Standard", "[Mobile Data Only]"),
                    ("IMEI", "[Mobile Data Only]"), ("ICCID", "[Mobile Data Only]"), ("IMSI", "[Mobile Data Only]"),
                    ("Network Operator", "[Mobile Data Only]"), ("GNSS Constellation", "[Mobile Data Only]"), ("Bluetooth Codecs", "[Mobile Data Only]"),
                    ("NFC Status", "[Mobile Data Only]"), ("USB Version", "[Mobile Data Only]"), ("Screen Resolution", "[Mobile Data Only]"),
                    ("Screen Panel", "[Mobile Data Only]"), ("Refresh Rate", "[Mobile Data Only]"), ("HDR Support", "[Mobile Data Only]"),
                    ("Audio Chip", "[Mobile Data Only]"), ("Speaker Config", "[Mobile Data Only]"), ("Camera Sensor", "[Mobile Data Only]"),
                    ("Battery Tech", "[Mobile Data Only]"), ("Charge Cycles", "[Mobile Data Only]"), ("Max Charge Wattage", "[Mobile Data Only]"),
                    ("Accelerometer", "[Mobile Data Only]"), ("Gyroscope", "[Mobile Data Only]"), ("Magnetometer", "[Mobile Data Only]"),
                ]


                # --- Render ---
                output_buffer.append(f"{Colors.BOLD}{Colors.MAGENTA}--- System & OS ---{Colors.RESET}\n{format_info(device_os, 3)}")
                output_buffer.append(f"\n{Colors.BOLD}{Colors.MAGENTA}--- CPU ---{Colors.RESET}\n{format_info(cpu_data, 3)}")
                cpu_bars = [f"    {Colors.WHITE}Core {i}  [{Colors.GREEN}{'█' * int(p / 10)}{' ' * (10 - int(p / 10))}{Colors.RESET}] {p:5.1f}%{Colors.RESET}" for i, p in enumerate(cpu_percents)]
                output_buffer.append("\n".join(cpu_bars))
                output_buffer.append(f"\n{Colors.BOLD}{Colors.MAGENTA}--- Memory ---{Colors.RESET}\n{format_info(mem_data, 3)}")
                output_buffer.append(f"\n{Colors.BOLD}{Colors.MAGENTA}--- Mobile-Specific Info (Not Applicable on PC) ---{Colors.RESET}\n{format_info(mobile_data, 3)}")
                output_buffer.append(f"\n{Colors.GRAY}Dashboard is refreshing. Press [Ctrl+C] to return...{Colors.RESET}")
                clear_screen(); print("\n".join(output_buffer)); time.sleep(2)
        except KeyboardInterrupt: return
        except Exception as e:
            clear_screen()
            print(f"\n{Colors.RED}An error occurred while fetching system info: {e}{Colors.RESET}")
            input("Press [Enter] to return...")
            return

    while True:
        menu_list = display_menu()
        try:
            choice = input(f"\n{Colors.YELLOW}Select script number, [S] for System Info, or [Q] to Quit: {Colors.RESET}")
            if choice.lower() == 'q':
                clear_screen(); print(f"\n{Colors.CYAN}{Colors.BOLD}Thank you for using DesxScript.{Colors.RESET}\n"); break
            elif choice.lower() == 's':
                display_system_info_screen(); continue
            
            choice_int = int(choice)
            script_name_from_list = next((item[1] for item in menu_list if int(item[0]) == choice_int), "Unknown Script")
            current_os = platform.system()

            if (current_os != "Windows" and choice_int in WIN_ONLY_SCRIPTS) or \
               (current_os != "Linux" and choice_int in LINUX_ONLY_SCRIPTS):
                print(f"{Colors.RED}Error: The '{script_name_from_list}' tool is not compatible with your OS ({current_os}).{Colors.RESET}")
                time.sleep(3); continue

            script_info = script_options.get(choice_int)
            if script_info:
                script_info['func'](script_name_from_list)
            else:
                simulate_generic_script(script_name_from_list)

            input(f"\n{Colors.YELLOW}Press [Enter] to return to the main menu...{Colors.RESET}")
        except (ValueError, IndexError):
            print(f"{Colors.RED}Invalid input.{Colors.RESET}"); time.sleep(2)
        except Exception as e:
            print(f"{Colors.RED}An unexpected error occurred: {e}{Colors.RESET}"); time.sleep(3)


if __name__ == "__main__":
    all_packages = {
        'requests': 'requests', 'PIL': 'Pillow', 'PyPDF2': 'PyPDF2',
        'faker': 'Faker', 'bs4': 'beautifulsoup4', 'whois': 'python-whois',
        'psutil': 'psutil', 'cpuinfo': 'py-cpuinfo'
    }
    if platform.system() == "Windows": all_packages['wmi'] = 'WMI'
    
    missing = [name for name, _ in all_packages.items() if importlib.util.find_spec(name) is None]
    if missing:
        pip_missing = [all_packages.get(m, m) for m in missing]
        check_and_install_dependencies(pip_missing)
    
    import requests; from PIL import Image, ExifTags; from PIL.ExifTags import TAGS
    import PyPDF2; from faker import Faker; from bs4 import BeautifulSoup
    import whois; import psutil; import cpuinfo
    if platform.system() == "Windows": import wmi

    main()

