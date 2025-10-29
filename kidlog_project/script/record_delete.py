
from kidlog.models import HtmtRecord,MilkRecord, SleepRecord, PoopRecord, PeeRecord, TemperatureRecord, FoodRecord, Child

HtmtRecord.objects.filter(child_id=1).delete()
MilkRecord.objects.filter(child_id=1).delete()
SleepRecord.objects.filter(child_id=1).delete()
PoopRecord.objects.filter(child_id=1).delete()
PeeRecord.objects.filter(child_id=1).delete()
TemperatureRecord.objects.filter(child_id=1).delete()
FoodRecord.objects.filter(child_id=1).delete()
