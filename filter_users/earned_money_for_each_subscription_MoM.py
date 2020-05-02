from main.models import UserSubscription, Visit, Subscription
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from payments.models import CPTransaction


t = timezone.now()
t += relativedelta(days=1)
t -= relativedelta(years=1)

print(t)

visit_count_by_users = dict()

for sub in Subscription.objects.filter(is_active=True):
    for i in range(12):
        from django.db.models import Sum
        cnt = len(CPTransaction.objects.filter(subscription_id=sub.id,
                                           confirm_date__gte=t + relativedelta(months=i),
                                           confirm_date__lte=t + relativedelta(months=i + 1)))
        money = CPTransaction.objects.filter(subscription_id=sub.id,
                                               confirm_date__gte=t + relativedelta(months=i),
                                               confirm_date__lte=t + relativedelta(months=i + 1)).aggregate(Sum('amount'))
        print('Sold {} months subscriptions in month number {}: {}; Earned money: {}'.format(sub.months, i+1, cnt, money['amount__sum']))
