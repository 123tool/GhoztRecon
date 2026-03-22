import requests
import argparse
import re
import sys
import concurrent.futures
import urllib3
from colorama import Fore, Style, init

# Konfigurasi Global
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
init(autoreset=True)

class GhoztRecon:
    def __init__(self):
        self.found_urls = set()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
        }
        # Pola Regex untuk mendeteksi kebocoran data sensitif dalam URL
        self.secret_patterns = {
            "Firebase": r"firebaseio\.com",
            "Google_API": r"AIza[0-9A-Za-z-_]{35}",
            "Generic_Token": r"(?i)(api_key|token|auth|password|client_secret|access_token)([=:])",
            "S3_Bucket": r"s3\.amazonaws\.com",
            "IP_Address": r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
        }

    def banner(self):
        banner_text = f"""
{Fore.RED}      ::::::::  :::    :::  ::::::::  :::::::: ::::::::::: :::::::::  :::::::::: ::::::::  ::::::::  ::::    ::: 
{Fore.RED}    :+:    :+: :+:    :+: :+:    :+:      :+:      :+:     :+:    :+: :+:       :+:    :+: :+:    :+: :+:+:   :+: 
{Fore.WHITE}   +:+        +:+    +:+ +:+    +:+     +:+       +:+     +:+    +:+ +:+       +:+        +:+    +:+ :+:+:+  +:+ 
{Fore.WHITE}  :#:        +#++:++#++ +#+    +:+    +#+        +#+     +#++:++#:  +#++:++#  +#+        +#+    +:+ +#+ +:+ +#+ 
{Fore.CYAN} +#+   +#+# +#+    +#+ +#+    +#+   +#+         +#+     +#+    +#+ +#+       +#+        +#+    +#+ +#+  +#+#+# 
{Fore.CYAN}#+#    #+# #+#    #+# #+#    #+#  #+#          #+#     #+#    #+# #+#       #+#    #+# #+#    #+# #+#   #+#+# 
{Fore.BLUE}########  ###    ###  ########  ##########     ###     ###    ### ########## ########   ########  ###    #### 

{Fore.YELLOW}          >> Advanced Cyber Reconnaissance & Endpoint Discovery Tool <<
{Fore.CYAN}              [ Built for Bug Bounty Hunters & Security Pros ]
        """
        print(banner_text)

    def fetch_wayback(self, domain):
        try:
            url = f"http://web.archive.org/cdx/search/cdx?url=*.{domain}/*&output=txt&fl=original&collapse=urlkey"
            r = requests.get(url, headers=self.headers, timeout=30)
            urls = r.text.splitlines()
            self.found_urls.update(urls)
            print(f"{Fore.BLUE}[INFO] Wayback Machine: {len(urls)} endpoints found.")
        except Exception as e:
            print(f"{Fore.RED}[!] Error Wayback: {str(e)}")

    def fetch_otx(self, domain):
        try:
            url = f"https://otx.alienvault.com/api/v1/indicators/domain/{domain}/url_list?limit=100"
            r = requests.get(url, headers=self.headers, timeout=30)
            data = r.json()
            urls = [i['url'] for i in data.get('url_list', [])]
            self.found_urls.update(urls)
            print(f"{Fore.BLUE}[INFO] AlienVault OTX: {len(urls)} endpoints found.")
        except Exception as e:
            print(f"{Fore.RED}[!] Error OTX: {str(e)}")

    def check_live(self, url):
        try:
            r = requests.head(url, headers=self.headers, timeout=5, verify=False, allow_redirects=True)
            return r.status_code
        except:
            return None

    def scan_secrets(self, url):
        matches = []
        for name, pattern in self.secret_patterns.items():
            if re.search(pattern, url):
                matches.append(name)
        return matches

    def run(self, domain, js_only, param_only, live_check, output):
        self.banner()
        print(f"{Fore.GREEN}[*] Initializing scan for: {Fore.WHITE}{domain}")
        
        # Multithreading Fetching
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(lambda f: f(domain), [self.fetch_wayback, self.fetch_otx])

        all_results = list(self.found_urls)
        final_data = []
        
        print(f"\n{Fore.GREEN}[+] Processing and Filtering {len(all_results)} URLs...\n")

        for url in all_results:
            is_js = ".js" in url.split('?')[0]
            has_param = "?" in url and "=" in url
            
            # Apply Filters
            if js_only and not is_js: continue
            if param_only and not has_param: continue

            # Analyze URL
            secrets = self.scan_secrets(url)
            status_code = ""
            
            if live_check:
                sc = self.check_live(url)
                if sc: 
                    status_code = f" [{sc}]"
                else: 
                    continue # Skip dead links if live check is enabled

            # Color Coding
            color = Fore.WHITE
            if is_js: color = Fore.GREEN
            if has_param: color = Fore.YELLOW
            if secrets: color = Fore.RED

            secret_tag = f" {Fore.RED}[! {','.join(secrets)}]" if secrets else ""
            
            output_line = f"{color}{url}{Fore.CYAN}{status_code}{secret_tag}"
            print(output_line)
            final_data.append(url)

        if output:
            with open(output, "w") as f:
                f.write("\n".join(final_data))
            print(f"\n{Fore.CYAN}[+] Mission Complete. {len(final_data)} results saved to {output}")

def main():
    parser = argparse.ArgumentParser(description="GhoztRecon: High-speed endpoint discovery.")
    parser.add_argument("-d", "--domain", required=True, help="Domain target (ex: google.com)")
    parser.add_argument("-x", "--js", action="store_true", help="Extract only JavaScript files")
    parser.add_argument("--param", action="store_true", help="Extract only URLs with parameters")
    parser.add_argument("--live", action="store_true", help="Check HTTP status of each URL")
    parser.add_argument("-o", "--output", help="Save output to a text file")
    
    args = parser.parse_args()
    
    recon = GhoztRecon()
    try:
        recon.run(args.domain, args.js, args.param, args.live, args.output)
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] Aborted by user. Happy Hunting!")
        sys.exit()

if __name__ == "__main__":
    main()
