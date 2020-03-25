from decimal import Decimal
from django.conf import settings
from shop.models import Product


class Cart(object):
    def __init__(self,request):
        """
        Initialize the cart.

        # session = {}
		# session = {'cart':{}}
		# cart = session.get(cart)
		# 將購物車內值命名為 cart 其值{}
		# #初始化購物車內值 cart 值
		# cart = {}
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            self.session[settings.CART_SESSION_ID] = {}
            cart = self.session[settings.CART_SESSION_ID]
        self.cart =cart

    def add(self, product, quantity=1, update_quantity=False):
        """
        向購物車中增加商品或者更新購物車中的數量
        :param product: Product實例對象
        :param quantity: 增加商品的數量，為整數，默認為1
        :param update_quantity: False 表示在原有數量上增加，True表示覆蓋原有數量
        :return: None
        """

        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

        # {'cart': {'product_id': {'quantity': quantity, 'price': price}}}

    def save(self):
        # 設置session.modified的值為True，中間件在看到這個屬性的時候，就會保存session
        self.session.modified = True

    def remove(self, product):
        """
        從購物車中刪除商品
        :param product: 要刪除的Product實例
        :return: None
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        疊代所有購物車內的商品
        :return: 疊代器對象
        """
        product_ids = self.cart.keys() #得到 product_id
        products = Product.objects.filter(id__in=product_ids)
        #__in 存在於一個list範圍內
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        購物車內一共有幾種商品
        :return: INT
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price'])*Decimal(item['quantity']) for item in self.cart.values())



    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()