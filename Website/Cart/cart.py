from Store.models import Product,Profile


class Cart():
    def __init__(self, request):
        self.session = request.session

        self.request = request

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

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Current User Profile
            current_user = Profile.objects.filter(user_id = self.request.user.id)
            carty = str(self.cart)
            # Convert {'3':2 , '2':4} to {"3" : 2 , "2":4}
            carty = carty.replace("\'" , "\"")
            # Save Carty To The Profile Model
            current_user.update(old_cart= str(carty))
    def db_add(self, product , quantity):
        product_id = str(product)
        product_qty = str(quantity)
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Current User Profile
            current_user = Profile.objects.filter(user_id = self.request.user.id)
            carty = str(self.cart)
            # Convert {'3':2 , '2':4} to {"3" : 2 , "2":4}
            carty = carty.replace("\'" , "\"")
            # Save Carty To The Profile Model
            current_user.update(old_cart= str(carty))

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


    def get_total(self):
        product_ids = self.cart.keys()

        products = Product.objects.filter(id__in=product_ids).all()

        quants = self.cart

        total = 0

        for key, value in quants.items():
            key = int(key)
            for product in products:
                if product.id == key:
                    price = int(product.price)
                    sale = int(product.Discountـpercentage) / 100
                    total_price = price - (price * sale)
                    total = total + (int(total_price) * int(value))
        return total

    def update(self, product_id , quantity):
        product_id = str(product_id)
        product_qty = str(quantity)
        if product_id in self.cart:
            # Get Cart
            ourcart = self.cart

            #Update Dictionary/cart

            ourcart[product_id] = product_qty

            self.session.modified = True

            # Deal with logged in user
            if self.request.user.is_authenticated:
                # Current User Profile
                current_user = Profile.objects.filter(user_id=self.request.user.id)
                carty = str(self.cart)
                # Convert {'3':2 , '2':4} to {"3" : 2 , "2":4}
                carty = carty.replace("\'", "\"")
                # Save Carty To The Profile Model
                current_user.update(old_cart=str(carty))

            thing = self.cart
            return thing

    def delete(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True


        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Current User Profile
            current_user = Profile.objects.filter(user_id = self.request.user.id)
            carty = str(self.cart)
            # Convert {'3':2 , '2':4} to {"3" : 2 , "2":4}
            carty = carty.replace("\'" , "\"")
            # Save Carty To The Profile Model
            current_user.update(old_cart= str(carty))