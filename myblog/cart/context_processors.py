# 將cart 設定為全局變量
from .cart import Cart



def cart(request):
    return {'mycart': Cart(request)}


# django规定的上下文处理器，就是一个函数，
# 接受request请求作为参数，然后返回一个键值对。键的名称就是未来在模板中可以使用的request.XXX名称。