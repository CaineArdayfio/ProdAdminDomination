import stripe

# Set your secret key: remember to change this to your live secret key in production
# See your keys here: https://dashboard.stripe.com/account/apikeys
stripe.api_key = "sk_test_51MIgTvG1tFaoV4hYH8agk5RkYiJvWTyTLRUYrBMubA7hBCIvsMf1I1JHfvIhXevYT4gH6BMAbrLhtbkRjMpQY5CG00cR0VVSRx"

# Create a token representing a credit card
token = stripe.Token.create(
    card = {
        "number": "4242424242424242",
        "exp_month": 12,
        "exp_year": 2030,
        "cvc": "123"
    }
)

if token:
    # Credit card is valid

    # Create a new customer with the credit card token 
    customer = stripe.Customer.create(
        email = "customer@example.com",
        source = token.id,
        phone = "1234567890",
        type = "express",
        description = "a test user"
        # return_url = 
        # refresh_url = 
    )

    # Charge the customer's card
    charge = stripe.Charge.create(
        amount = 1000, # Amount in cents
        currency = "usd",
        customer = customer.id,
        description = "Charge for customer@example.com",
        receipt_email = "customer@example.com"
    )

else:
    # Credit card is invalid, raise exception
    raise Exception("Invalid card:", token.error.message)
