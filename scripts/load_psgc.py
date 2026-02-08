import os
import sys
import csv
import logging
import django

# --- Django setup ---
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from src.location.models import Region, Province, Municipality, Barangay

# --- Logging setup ---
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_dir = os.path.join(project_root, "logs")
os.makedirs(log_dir, exist_ok=True)   # ensure logs/ exists
log_file = os.path.join(log_dir, "psgc_import.log")

# Configure logging to both file and console
logger = logging.getLogger("psgc_import")
logger.setLevel(logging.INFO)

# File handler
fh = logging.FileHandler(log_file, mode="w", encoding="utf-8")
fh.setLevel(logging.INFO)

# Console handler
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# Attach handlers
logger.addHandler(fh)
logger.addHandler(ch)

def log_and_print(message, level="info"):
    getattr(logger, level)(message)

# --- Loaders ---
def load_regions(path):
    loaded = 0
    with open(path, newline="", encoding="latin-1") as f:
        reader = csv.DictReader(f)
        for row in reader:
            Region.objects.get_or_create(
                region_id=int(row["region_id"]),
                code=row["code"],
                name=row["description"]
            )
            loaded += 1
    log_and_print(f"Regions loaded: {loaded}")


def load_provinces(path):
    loaded, skipped = 0, 0
    with open(path, newline="", encoding="latin-1") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                region = Region.objects.get(region_id=int(row["region_id"]))
                Province.objects.get_or_create(
                    province_id=int(row["province_id"]),
                    code=row["code"],
                    name=row["description"],
                    region=region
                )
                loaded += 1
            except Region.DoesNotExist:
                skipped += 1
                log_and_print(f"Skipped province {row['description']} (region_id {row['region_id']} not found)", "warning")
    log_and_print(f"Provinces loaded: {loaded}, skipped: {skipped}")


def load_muncities(path):
    loaded, skipped = 0, 0
    with open(path, newline="", encoding="latin-1") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                province = Province.objects.get(province_id=int(row["province_id"]))
                Municipality.objects.get_or_create(
                    muncity_id=int(row["muncity_id"]),
                    code=row["code"],
                    name=row["description"],
                    province=province
                )
                loaded += 1
            except Province.DoesNotExist:
                skipped += 1
                log_and_print(f"Skipped municipality {row['description']} (province_id {row['province_id']} not found)", "warning")
    log_and_print(f"Municipalities loaded: {loaded}, skipped: {skipped}")


def load_barangays(path):
    loaded, skipped = 0, 0
    with open(path, newline="", encoding="latin-1") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                municipality = Municipality.objects.get(muncity_id=int(row["muncity_id"]))
                Barangay.objects.get_or_create(
                    barangay_id=int(row["barangay_id"]),
                    code=row["code"],
                    name=row["description"],
                    municipality=municipality
                )
                loaded += 1
            except Municipality.DoesNotExist:
                skipped += 1
                log_and_print(f"Skipped barangay {row['description']} (muncity_id {row['muncity_id']} not found)", "warning")
    log_and_print(f"Barangays loaded: {loaded}, skipped: {skipped}")


# --- Main ---
if __name__ == "__main__":
    log_and_print("Starting PSGC import...")
    load_regions("data/region.csv")
    load_provinces("data/province.csv")
    load_muncities("data/muncity.csv")
    load_barangays("data/barangay.csv")
    log_and_print("✅ PSGC data import complete.")
