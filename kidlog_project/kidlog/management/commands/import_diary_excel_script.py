from django.core.management.base import BaseCommand
from django.utils import timezone
from kidlog.models import Child
from diary.models import DiaryRecord
import pandas as pd
from datetime import datetime


class Command(BaseCommand):
    help = "Import diary records from an Excel file into DiaryRecord model."

    def add_arguments(self, parser):
        parser.add_argument("excel_path", type=str, help="Path to Excel file")
        parser.add_argument("--child_id", type=int, default=1, help="Target child ID")

    def handle(self, *args, **options):
        excel_path = options["excel_path"]
        child_id = options["child_id"]

        # 対象の子どもを取得
        try:
            child = Child.objects.get(pk=child_id)
        except Child.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f"❌ Child with id={child_id} not found.")
            )
            return

        self.stdout.write(
            self.style.WARNING(
                f"📘 Importing diary for child id={child_id} from {excel_path}"
            )
        )

        # Excel読み込み
        df = pd.read_excel(excel_path)

        imported_count = 0
        for _, row in df.iterrows():
            try:
                dt = datetime.strptime(str(row["date"]), "%Y-%m-%d")
                aware_dt = timezone.make_aware(dt)
                DiaryRecord.objects.create(
                    child=child,
                    time=aware_dt,
                    summary=row.get("summary", "")[:100],
                    note=row.get("note", ""),
                )
                imported_count += 1
            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(f"⚠️ Skipped row due to error: {e}")
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"✅ Successfully imported {imported_count} diary records!"
            )
        )
