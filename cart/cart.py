from store.models import Product

class Cart():
    def __init__(self, request):
        self.session = request.session

        cart = self.session.get('session_key')

        #cria uma nova sessao para o usuário se ele nao tiver uma
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        self.cart = cart

    def add(self, product, quantity): #adiciona um produto ao carrinho na sessao
        product_id = str(product.id)
        product_qty = str(quantity)

        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id] = {'price': str(product.price)} # {id, {'price': preco}}
            self.cart[product_id] = int(product_qty)
        
        self.session.modified = True
        
    def total(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        quantities = self.cart
        total = 0
        for key, value in quantities.items():
            key = int(key)
            for product in products:
                if product.id == key:
                    total += product.price*value

        return total
    
    def __len__(self):
        return len(self.cart)
    
    def get_products(self):
        product_ids = self.cart.keys()

        products = Product.objects.filter(id__in=product_ids)

        return products

    def get_quants(self):
        quantities = self.cart
        return quantities
    
    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)

        ourcart = self.cart
        ourcart[product_id] = product_qty

        self.session.modified = True

        updated_cart = self.cart
        return updated_cart
    
    def delete(self, product):
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True
    
    
