from django.utils import timezone
import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from kidlog.models import HtmtRecord,MilkRecord, SleepRecord, PoopRecord, PeeRecord, TemperatureRecord, FoodRecord, Child

class Command(BaseCommand):
    help = "Import records from CSV files"

    def add_arguments(self, parser):
        parser.add_argument("model", type=str, help="Model name (milk/sleep/poop/pee/temp/food)")
        parser.add_argument("csv_file", type=str, help="Path to CSV file")

    def handle(self, *args, **options):
        model = options["model"]
        file_path = options["csv_file"]

        with open(file_path, newline='', encoding="utf-8") as f:
            reader = csv.DictReader(f)

            if model == "milk":
                for row in reader:
                    dt = datetime.strptime(row["time"], "%Y-%m-%d %H:%M")
                    aware_dt = timezone.make_aware(dt)
                    MilkRecord.objects.create(
                        child_id=row["child_id"],
                        time=aware_dt,
                        amount=row["amount"],
                        note=row.get("note")
                    )

            elif model == "sleep":
                for row in reader:
                    start_dt = datetime.strptime(row["start_time"], "%Y-%m-%d %H:%M")
                    start_aware_dt = timezone.make_aware(start_dt)
                    end_dt = datetime.strptime(row["end_time"], "%Y-%m-%d %H:%M")
                    end__aware_dt = timezone.make_aware(end_dt)
                    SleepRecord.objects.create(
                        child_id=row["child_id"],
                        start_time=start_aware_dt,
                        end_time=end__aware_dt,
                        note=row.get("note")
                    )

            elif model == "poop":
                for row in reader:
                    dt = datetime.strptime(row["time"], "%Y-%m-%d %H:%M")
                    aware_dt = timezone.make_aware(dt)
                    PoopRecord.objects.create(
                        child_id=row["child_id"],
                        time=aware_dt,
                        note=row.get("note")
                    )

            elif model == "pee":
                for row in reader:
                    dt = datetime.strptime(row["time"], "%Y-%m-%d %H:%M")
                    aware_dt = timezone.make_aware(dt)
                    PeeRecord.objects.create(
                        child_id=row["child_id"],
                        time=aware_dt,
                        note=row.get("note")
                    )

            elif model == "temp":
                for row in reader:
                    dt = datetime.strptime(row["time"], "%Y-%m-%d %H:%M")
                    aware_dt = timezone.make_aware(dt)
                    TemperatureRecord.objects.create(
                        child_id=row["child_id"],
                        time=aware_dt,
                        temperature=row["temperature"],
                        note=row.get("note")
                    )

            elif model == "food":
                for row in reader:
                    dt = datetime.strptime(row["time"], "%Y-%m-%d %H:%M")
                    aware_dt = timezone.make_aware(dt)
                    FoodRecord.objects.create(
                        child_id=row["child_id"],
                        time=aware_dt,
                        menu=row["menu"],
                        amount=row.get("amount"),
                        note=row.get("note")
                    )

            elif model == "htmt":
                for row in reader:
                    date = datetime.strptime(row["date"], "%Y-%m-%d").date()
                    HtmtRecord.objects.create(
                        child_id=row["child_id"],
                        height=row["height"],
                        weight=row["weight"],
                        date=date,
                    )

            else:
                self.stdout.write(self.style.ERROR("Unknown model"))
                return

        self.stdout.write(self.style.SUCCESS(f"Imported {model} records from {file_path}"))
