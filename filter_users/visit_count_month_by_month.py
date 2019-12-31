from main.models import Visit, UserSubscription
from dateutil.relativedelta import relativedelta
from django.utils import timezone
t = timezone.now()
t += relativedelta(days=5)
t -= relativedelta(years=1)

visit_count_by_users = dict()

for i in range(11):
    cnt = len(Visit.objects.filter(status='APPROVED',
                                   timestamp__gte=t+relativedelta(months=i),
                                   timestamp__lte=t+relativedelta(months=i+1))
              )
    print(cnt)
