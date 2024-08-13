from Store.models import Product


class Cart():
    def __init__(self, request):
        self.session = request.session

        # GET The Current Session Key if it exists
        cart = self.session.get('session_key')


        # If The User is new , no Session Key ! Create one!
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        # Make Sure cart is available on all page of site
        self.cart = cart

    def add(self, product , quantity):
        product_id = str(product.id)
        product_qty = str(quantity)
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

    def __len__(self):
        return len(self.cart)

    def get_prods(self):
        # Get ids From Card
        product_ids = self.cart.keys()
        # Use ids to lookup product in database model
        product = Product.objects.filter(id__in=product_ids).all()
        # Return those looked up products
        return product

    def get_quants(self):
        quants = self.cart
        return quants

    def update(self, product_id , quantity):
        product_id = str(product_id)
        product_qty = str(quantity)
        if product_id in self.cart:
            # Get Cart
            ourcart = self.cart

            #Update Dictionary/cart

            ourcart[product_id] = product_qty

            self.session.modified = True

            thing = self.cart
            return thing