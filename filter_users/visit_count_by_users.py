from main.models import Visit, UserSubscription
from dateutil.relativedelta import relativedelta
from django.utils import timezone
t = timezone.now()
t += relativedelta(days=5)
t -= relativedelta(years=1)

visit_count_by_users = dict()
jiilik = set()

from main.models import Subscription

for sub in UserSubscription.objects.all():
    cnt = len(Visit.objects.filter(user=sub.user,
                                   status='APPROVED',
                                   timestamp__gte=t+relativedelta(months=11),
                                   timestamp__lte=t+relativedelta(months=12))
              )
    jiilik.add(cnt)
    try:
        visit_count_by_users[cnt] += 1
    except:
        visit_count_by_users[cnt] = 1

for i in jiilik:
    print(i, visit_count_by_users[i])
