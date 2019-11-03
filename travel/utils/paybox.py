from django.conf import settings
import hashlib
from urllib.parse import parse_qs


def parse_body(body):
    body = body.decode('utf-8')
    body = parse_qs(body)
    for k, v in body.items():
        body[k] = v[0]
    return body


def get_sig(mydict, url='payment.php', pb_secret=settings.PB_SECRET):
    new_list = list()
    for key in sorted(mydict.keys()):
        new_list.append(str(mydict[key]))
    res = url + ';' + ';'.join(new_list) + ';' + pb_secret
    hashed = hashlib.md5(res.encode('utf-8')).hexdigest()
    return hashed


def verify_sig(request, url=''):
    if request.method == 'GET':
        sig = request.GET.get('pg_sig')
        my_dict = request.GET.dict()
    else:
        # sig = request.POST.get('pg_sig')
        # my_dict = request.POST.dict()
        my_dict = parse_body(request.body)
        sig = my_dict.pop('pg_sig', None)
    if sig != get_sig(my_dict, url=url):
        return False
    return True


"""
100	'Некорректная подпись запроса *'
101	'Неверный номер магазина''
110	'Отсутствует или не действует контракт с магазином'
120	'Запрошенное действие отключено в настройках магазина''
200	'Не хватает или некорректный параметр запроса'
340	'Транзакция не найдена'
350	'Транзакция заблокирована'
360	'Транзакция просрочена'
365	'Срок жизни рекуррентного профиля истек'
400	'Платеж отменен покупателем или платежной системой'
420	'Платеж отменен по причине превышения лимита'
465	'Ошибка связи с платежной системой'
466	'Истек SSL сертификат'
470	'Ошибка на стороне платежной системы'
475	'Общий сбой платежной системы'
490	'Отмена платежа невозможна'
600	'Общая ошибка'
700	'Ошибка в данных введенных покупателем'
701	'Некорректный номер телефона'
711	'Номер телефона неприемлем для выбранной ПС'
850	'Ни одна из платежных систем не готова принять запрос'
1000 'Внутренняя ошибка сервиса (может не повториться при повторном обращении)'
"""
