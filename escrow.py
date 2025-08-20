import requests
import json
import base64
import argparse
import os
import sys
from colorama import Fore, init
from Crypto.Cipher import ChaCha20

MASTER_KEY = [0xb3, 0xcb, 0x2e, 0x04, 0x87, 0x94, 0xd6, 0x73, 0x08, 0x23, 0xc4, 0x93, 0x7a, 0xbd, 0x18, 0xad, 0x6b, 0xe6, 0xdc, 0xb3, 0x91, 0x43, 0x0d, 0x28, 0xf9, 0x40, 0x9d, 0x48, 0x37, 0xb9, 0x38, 0xfb]
DECRYPT_FILES_COUNT = 0
SKIPPED_FILES_COUNT = 0
DB_PATH = "grant_cache.json"

class Grants:
    def __init__(self, server_key=None):
        self.server_key = server_key

    def _decode_jwt(self, jwt_token):
        parts = jwt_token.split('.')
        if len(parts) != 3:
            raise ValueError(f"{Fore.LIGHTRED_EX}[!] Invalid JWT format")

        payload_b64 = parts[1] + '=' * (-len(parts[1]) % 4)
        payload_json = base64.urlsafe_b64decode(payload_b64.encode()).decode()
        return json.loads(payload_json)

    def _load_cache(self):
        if os.path.exists(DB_PATH):
            try:
                with open(DB_PATH, "r") as f:
                    content = f.read().strip()
                    if not content:
                        return {} 
                    return json.loads(content)
            except json.JSONDecodeError:
                return {}
        return {}

    def _save_cache(self, cache):
        with open(DB_PATH, "w") as f:
            json.dump(cache, f, indent=2)

    def _update_cache_with_key(self, key, cache):
        url = f"https://keymaster.fivem.net/api/validate/{key}"
        resp = requests.get(url)

        if resp.status_code != 200:
            return []

        data = resp.json()
        grants_token = data.get("grants_token")
        if not grants_token:
            return []

        payload = self._decode_jwt(grants_token)
        grants = payload.get("grants", {})

        new_ids = []
        for rid, val in grants.items():
            if rid not in cache:
                cache[rid] = val
                new_ids.append(rid)

        return new_ids

    def get_all(self):
        cache = self._load_cache()
        new_ids = self._update_cache_with_key(self.server_key, cache)

        if new_ids:
            self._save_cache(cache)

    def get_hash(self, resource_id, server_key=None):
        resource_id = str(resource_id)
        cache = self._load_cache()

        if resource_id in cache:
            return cache[resource_id]

        key_to_use = server_key or self.server_key
        if not key_to_use:
            return None

        self._update_cache_with_key(key_to_use, cache)

        if resource_id in cache:
            self._save_cache(cache)
            return cache[resource_id]

        return None

class Escrow:
    def __init__(self, fx_base, fx_file, server_key):
        self.fx_base = fx_base
        self.fx_file = fx_file
        self.server_key = server_key
        self.resource_key = None

    def is_valid(self):
        fxapContent = None
        with open(self.fx_file, "rb") as f:
            fxapContent = f.read()

        return fxapContent[:4] == b'FXAP'

    def get_resource_id(self):
        if not self.is_valid():
            return

        file = None
        with open(self.fx_base, "rb") as f:
            file = f.read()
        
        iv = file[0x4a:0x4a + 0xc]
        cipher = ChaCha20.new(key=bytes(MASTER_KEY), nonce=iv)
        decrypted = cipher.decrypt(file[0x56:])
        resource_id = int.from_bytes(decrypted[0x4a:0x4a + 4], byteorder="big")

        return resource_id

    def get_key(self):
        resource_id = self.get_resource_id()

        grants = Grants(server_key=self.server_key)
        key = grants.get_hash(resource_id)
        
        if key is None and self.server_key is None:
            sys.exit(1)

        if key is None:
            key = grants.get_hash(resource_id, server_key=self.server_key)

        if key is None:
            sys.exit(1)

        self.resource_key = key

    def save_decrypted(self, decrypted, base_input_dir, resource_name=None):
        import os

        rel_path = os.path.relpath(self.fx_file, base_input_dir)
        output_dir = os.path.join("./out", resource_name)
        output_path = os.path.join(output_dir, rel_path)

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        content = decrypted
        if self.fx_file.endswith("fxmanifest.lua"):
            text = decrypted.decode("utf-8", errors="ignore")
            lines = text.splitlines()

            filtered_lines = [line for line in lines if line.strip() != "dependency '/assetpacks'"]
            header = ["-- Decrypted by https://discord.gg/fivecommunity2" for _ in range(5)]
            new_lines = header + filtered_lines

            content = "\n".join(new_lines).encode("utf-8")

        with open(output_path, "wb") as f:
            f.write(content)

        fxap_path = os.path.join(output_dir, ".fxap")
        if os.path.isfile(fxap_path):
            try:
                os.remove(fxap_path)
            except:
                pass

    def decrypt(self):
        global DECRYPT_FILES_COUNT
        global SKIPPED_FILES_COUNT

        if not self.is_valid():
            # print(f"{Fore.LIGHTRED_EX}[!] Skipping file: {self.fx_file}")
            SKIPPED_FILES_COUNT += 1
            return False

        self.get_key()

        file = None
        with open(self.fx_file, "rb") as f:
            file = f.read()

        iv = file[0x4a:0x4a + 0xc]
        encrypted = file[0x56:]

        cipher = ChaCha20.new(key=bytes(MASTER_KEY), nonce=iv)
        first_round = cipher.decrypt(encrypted)
        real_iv = first_round[:0x5c][-16:][-12:]
        
        header = first_round[:0x5c]
        content = first_round[0x5c:]

        cipher = ChaCha20.new(key=bytes.fromhex(self.resource_key), nonce=real_iv)
        decrypted = cipher.decrypt(content)

        # print(f"{Fore.GREEN}[+] Decrypted: {self.fx_file}")
        DECRYPT_FILES_COUNT += 1

        return decrypted


def get_all_keys(server_key):
    g = Grants(server_key)
    g.get_all()

def banner():
    os.system("cls || clear")
    os.system(f'title Five Community decrypt')


def main():
    banner()
    parser = argparse.ArgumentParser(
        description="FXAP Decryptor v1",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('-f', '--file', help='Path to the encrypted .sv file to decrypt')
    parser.add_argument('-d', '--dir', help='Path to a directory to decrypt all stream files recursively')
    parser.add_argument('-k', '--server_key', help='Server key used to retrieve new grants')
    parser.add_argument('-s', '--only_keys', action='store_true', help='Only fetch and list all known resource IDs for a given server key')
    parser.add_argument('-r', '--recursive', help='Path to a directory to decrypt all RESOURCES')

    args = parser.parse_args()

    if args.server_key and args.only_keys:
        get_all_keys(args.server_key)
        return

    if args.file:
        escrow_parser = Escrow(args.fxap, args.file, args.server_key)
        des = escrow_parser.decrypt()
        escrow_parser.save_decrypted(des, args.file)
    elif args.dir:
        fxap_path = os.path.join(args.dir, ".fxap")
        resource_name = os.path.basename(os.path.normpath(args.dir))

        for root, dirs, files in os.walk(args.dir):
            for file in files:
                file_path = os.path.join(root, file)
                escrow_parser = Escrow(fxap_path, file_path, args.server_key)
                des = escrow_parser.decrypt()

                if des:
                    escrow_parser.save_decrypted(des, args.dir, resource_name)
                else:
                    with open(file_path, "rb") as f:
                        original_data  = f.read()

                    escrow_parser.save_decrypted(original_data, args.dir, resource_name)


        #input(f"\n\n{Fore.LIGHTMAGENTA_EX}Press Enter to exit...")

    else:
        parser.error(
            "You must provide either -f/--file to decrypt a single file or -d/--dir to decrypt all files in a directory.\n"
            "Or use -k/--server_key with -s/--only_keys to fetch all known decrypt keys."
        )



if __name__ == "__main__":
    main()