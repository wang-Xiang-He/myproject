from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
import braintree
from orders.models import Order


def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    # POST請求則處理支付
    if request.method == "POST":
        # 獲得最終生成的交易token
        # payment_method_nonce：Braintree JS 客戶端生成的交易token
        nonce = request.POST.get('payment_method_nonce', None)
        # 使用token和附加信息，建立並向Braintree提交交易信息
        result = braintree.Transaction.sale(
            {
                'amount': '{:2f}'.format(order.get_total_cost()),
                'payment_method_nonce': nonce,
                'options': {
                    'submit_for_settlement': True,
                }
            }
        )
        # 如果提交交易信息成功,將已支付和交易id記錄到Order表中
        if result.is_success:
            order.paid = True
            order.braintree_id = result.transaction.id
            order.save()
            return redirect('payment:done')
        else:
            return redirect('payment:canceled')

    # GET請求則生成臨時token交給前端頁面以生成支付表單供用戶填寫
    else:
        client_token = braintree.ClientToken.generate()
        return render(request,
                      'payment/process.html',
                      {'order': order,
                       'client_token': client_token})

def payment_done(request):
    return render(request, 'payment/done.html')
def payment_canceled(request):
    return render(request, 'payment/canceled.html')