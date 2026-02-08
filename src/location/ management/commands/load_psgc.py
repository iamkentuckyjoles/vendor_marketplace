import csv
from django.core.management.base import BaseCommand
from location.models import Region, Province, Municipality, Barangay

class Command(BaseCommand):
    help = "Load PSGC data from CSV files into Region, Province, Municipality, and Barangay models"

    def add_arguments(self, parser):
        parser.add_argument("--region", type=str, help="Path to region.csv")
        parser.add_argument("--province", type=str, help="Path to province.csv")
        parser.add_argument("--muncity", type=str, help="Path to muncity.csv")
        parser.add_argument("--barangay", type=str, help="Path to barangay.csv")

    def handle(self, *args, **options):
        # Load Regions
        if options["region"]:
            with open(options["region"], newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    Region.objects.get_or_create(
                        code=row["region_code"], name=row["region_name"]
                    )
            self.stdout.write(self.style.SUCCESS("Regions loaded."))

        # Load Provinces
        if options["province"]:
            with open(options["province"], newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    region = Region.objects.get(code=row["region_code"])
                    Province.objects.get_or_create(
                        code=row["province_code"], name=row["province_name"], region=region
                    )
            self.stdout.write(self.style.SUCCESS("Provinces loaded."))

        # Load Municipalities
        if options["muncity"]:
            with open(options["muncity"], newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    province = Province.objects.get(code=row["province_code"])
                    Municipality.objects.get_or_create(
                        code=row["muncity_code"], name=row["muncity_name"], province=province
                    )
            self.stdout.write(self.style.SUCCESS("Municipalities loaded."))

        # Load Barangays
        if options["barangay"]:
            with open(options["barangay"], newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    municipality = Municipality.objects.get(code=row["muncity_code"])
                    Barangay.objects.get_or_create(
                        code=row["barangay_code"], name=row["barangay_name"], municipality=municipality
                    )
            self.stdout.write(self.style.SUCCESS("Barangays loaded."))
