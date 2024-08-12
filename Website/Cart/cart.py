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
