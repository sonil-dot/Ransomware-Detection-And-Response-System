
import os
import shutil
from datetime import datetime

from config import config


def quarantine_file(file_path):
    """Copy a suspicious file as evidence without deleting the original."""

    if not os.path.isfile(file_path):
        print(f"[ERROR] File not found: {file_path}")
        return False

    quarantine_dir = "./quarantine"
    os.makedirs(quarantine_dir, exist_ok=True)

    filename = os.path.basename(file_path)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    destination = os.path.join(
        quarantine_dir,
        f"{timestamp}_{filename}"
    )

    try:
        if config["response"]["simulation_mode"]:
            print("[SIMULATION] Copying evidence. Original remains unchanged.")
        else:
            print(
                "[COPY ONLY] Creating an evidence copy. "
                "The original is not isolated or deleted."
            )

        shutil.copy2(file_path, destination)

        print(f"[SUCCESS] Evidence copy saved to: {destination}")
        return True

    except OSError as error:
        print(f"[ERROR] Could not copy file: {error}")
        return False


if __name__ == "__main__":
    test_file = "./test_data/entropy_test.txt"
    quarantine_file(test_file)
