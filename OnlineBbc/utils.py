def calculate_total_price(cart_items): 
    total_price = sum(item.product.price * item.stock for item in cart_items)
    return total_price


def count_cart_items(cart_items): 
    total_items = sum(item.stock for item in cart_items)
    return total_items

def apply_discount(total_price, discount_percentage):
    discount_amount = total_price * (discount_percentage / 100)
    discounted_price = total_price - discount_amount
    return discounted_price


