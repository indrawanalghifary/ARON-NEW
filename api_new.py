import requests
from split import convert_config

# def get_hardware_id():
#     # Implementasi untuk mendapatkan hardware ID
#     # Contoh: menggunakan UUID sebagai hardware ID
#     import uuid
#     return str(uuid.uuid4())

import os
import json
import uuid
import hashlib
import subprocess
from pathlib import Path


class PersistentHWID:
    def __init__(self):
        self.storage = Path.home() / ".device_identity"

    def _run(self, command):
        try:
            result = subprocess.check_output(
                command,
                shell=True,
                stderr=subprocess.DEVNULL
            ).decode(errors="ignore")

            lines = [x.strip() for x in result.splitlines() if x.strip()]

            if len(lines) >= 2:
                return lines[1]

        except:
            pass

        return "UNKNOWN"

    def _get_hardware_fingerprint(self):
        """
        Hardware fingerprint relatif stabil
        """

        bios_uuid = self._run("wmic csproduct get uuid")

        board_serial = self._run(
            "wmic baseboard get serialnumber"
        )

        bios_serial = self._run(
            "wmic bios get serialnumber"
        )

        cpu_id = self._run(
            "wmic cpu get processorid"
        )

        raw = "|".join([
            bios_uuid,
            board_serial,
            bios_serial,
            cpu_id
        ])

        return hashlib.sha256(
            raw.encode()
        ).hexdigest()

    def get_hwid(self):
        """
        Menghasilkan HWID:
        - persistent
        - unik
        - stabil
        - sulit duplikat
        """

        # Kalau sudah ada -> pakai yang lama
        if self.storage.exists():
            try:
                with open(self.storage, "r") as f:
                    data = json.load(f)

                return data["hwid"]

            except:
                pass

        # Fingerprint hardware
        hardware_hash = self._get_hardware_fingerprint()

        # UUID random unik
        random_uuid = str(uuid.uuid4())

        # Gabungkan
        combined = f"{hardware_hash}|{random_uuid}"

        # Final HWID
        hwid = hashlib.sha256(
            combined.encode()
        ).hexdigest()

        # Simpan supaya persistent
        data = {
            "hwid": hwid
        }

        with open(self.storage, "w") as f:
            json.dump(data, f)

        return hwid


# ==========================
# Penggunaan
# ==========================


def get_hardware_id():
    hw = PersistentHWID()
    return hw.get_hwid()


def post_request(url, data):
    headers = {
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'
    }
    response = requests.post(url, data=data, headers=headers)
    return response.json()


def get_user_info(token):
    url = "https://duadev.xyz/api/token"
    # token = "VTOX-S4YS-BK08-LXQD"
    app_code = "ARON"
    device_id = get_hardware_id()
    # device_id = "12345"

    data = {
        "token": token,
        "app_code": app_code,
        "device_id": device_id
    }
    hasil = post_request(url, data)
    # print(hasil)
    return hasil
# response 
# {'status': 'success', 'data': {'token': 'VTOX-S4YS-BK08-LXQD', 'is_expired': False, 'remaining_days': 9, 'app_code': 'ARON', 'expired_at': '2026-05-22', 'package_title': 'Trial', 'codename': 'AGS', 'max_devices': 1, 'used_devices': 1, 'remaining_devices': 0, 'profile_name': 'Agis Maulana', 'account_email': 'kangagis02@gmail.com', 'website_url': 'https://duadev.xyz'}, 'config': [{'sku': 'SQUWNT', 'items': ['SQU', 'WNT']}]}

if __name__ == "__main__":
    
    user = get_user_info("VTOX-S4YS-BK08-LXQD")
    print(json.dumps(user, indent=4))
    split_map = convert_config(user)
    print(split_map)