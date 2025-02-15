# shop/cart.py

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, quantity=1):
        product_id = str(product.id)  # Ensure product id is a string
        product_type = str(product.__class__.__name__)  # Get product type dynamically

        if product_id not in self.cart:
            self.cart[product_id] = {
                'type': product_type,
                'name': product.name,
                'price': product.price,
                'quantity': 0,
            }
        
        self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session['cart'] = self.cart
        self.session.modified = True

    def get_total_price(self):
        return sum(item['price'] * item['quantity'] for item in self.cart.values())
