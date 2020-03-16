# from celery import task
from django.core.mail import send_mail
from .models import Order


# @task
def order_created(order_id):
    """
    當一個訂單創建完成後發送郵件通知給用戶
    :param order_id: 訂單編號
    :return: mail_sent
    """

    order = Order.objects.get(id=order_id)
    subject = 'Order {}'.format(order.id)
    message = 'Dear {},\n\nYou have successfully placed an order. Your order id is {}.'.format(order.first_name,
                                                                                               order_id)
    mail_sent = send_mail(subject, message, '<NBA news live>', [order.email])
    print(mail_sent, type(mail_sent))
    return mail_sent