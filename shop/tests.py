from django.test import TestCase

"""
----- Tests to carry out -----

1. Create a sample new user
2. Log in and confirm creation of session
3. Change password and confirm new password
4. Logout and confirm end of session
5. Log in of the same user
6. Addition of product to cart and check product exists in cart (retrieve product)
7. Remove product from cart and ensure it has been removed
8. Add 2 more products to cart and ensure they can be retrieved when user views cart
9. Add and remove quantity of existing products and ensure they reflect
10. Simulate sample shipping location and ensure that the correct price reflects
11. Confirm sub-total of the cart
12. Simulate payment and creation of an order

"""
# Create your tests here.
