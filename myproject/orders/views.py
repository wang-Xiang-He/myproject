from django.shortcuts import render,redirect,reverse
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from django.contrib.auth.decorators import login_required
from .task import order_created

@login_required(login_url='/userprofile/login/')
def order_create(request):
    cart = Cart(request)
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        # 表單驗證通過就對購物車內每一條紀錄生成OrderItem中對應的一條紀錄
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'],
                                         quantity=item['quantity'])
            # 成功生成OrderItem之後清除購物車
            cart.clear()
            # 成功完成訂單後發送郵件
            # send_email
            order_created(order.id)
            # 在session中加入訂單id
            request.session['order_id'] = order.id
            # 重定向到支付頁面
            return redirect(reverse('payment:process'))

    else:
        form = OrderCreateForm()
    return render(request, 'orders/create.html', {'cart': cart, 'form': form})