from django_cron import CronJobBase, Schedule
from .models import DetectionRecord

class HourlyPersonCountCronJob(CronJobBase):
    RUN_EVERY_MINS = 60  # 每 60 分钟运行一次

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'blog.hourly_person_count'

    def do(self):
        person_count = DetectionRecord.objects.filter(category="person").count()
        print(f"1sum：{person_count}")
