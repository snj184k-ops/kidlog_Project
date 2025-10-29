from django.core.management.base import BaseCommand

from kidlog.models import HtmtRecord,MilkRecord, SleepRecord, PoopRecord, PeeRecord, TemperatureRecord, FoodRecord

class Command(BaseCommand):
    help = "指定したchild_idのHtmtRecordを一括削除"

    def add_arguments(self, parser):
        parser.add_argument("child_id", type=int)

    def handle(self, *args, **options):
        child_id = options["child_id"]
        deleted, _ = HtmtRecord.objects.filter(child_id=child_id).delete()
        deleted, _ = MilkRecord.objects.filter(child_id=child_id).delete()
        deleted, _ = SleepRecord.objects.filter(child_id=child_id).delete()
        deleted, _ = PoopRecord.objects.filter(child_id=child_id).delete()
        deleted, _ = PeeRecord.objects.filter(child_id=child_id).delete()
        deleted, _ = TemperatureRecord.objects.filter(child_id=child_id).delete()
        deleted, _ = FoodRecord.objects.filter(child_id=child_id).delete()
        self.stdout.write(self.style.SUCCESS(f"{deleted} 件削除しました"))
