from .cart import Cart

#Cria um Context processor para que o carrinho funcione em toda a aplicaçao
def cart(request):

    return {'cart': Cart(request)}