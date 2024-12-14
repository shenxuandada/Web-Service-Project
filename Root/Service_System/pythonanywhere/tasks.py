from django.utils.timezone import now, timedelta
from django.db.models import Sum
from .models import DetectionRecord, Post

def push_hourly_person_count():
    # 获取上一个整点的时间范围
    current_time = now()
    start_time = current_time.replace(minute=0, second=0, microsecond=0) - timedelta(hours=1)
    end_time = start_time + timedelta(hours=1)

    # 统计上一小时的 "人" 流量总和
    person_count = DetectionRecord.objects.filter(
        detected_hour__gte=start_time,
        detected_hour__lt=end_time
    ).aggregate(total=Sum('count'))['total'] or 0

    # 推送到博客（创建一条新的 Post 记录）
    Post.objects.create(
        title=f"人流量统计 - {start_time.strftime('%Y-%m-%d %H:00')}",
        text=f"在 {start_time.strftime('%Y-%m-%d %H:00')} 到 {end_time.strftime('%Y-%m-%d %H:00')} 之间，共检测到 {person_count} 人。"
    )
