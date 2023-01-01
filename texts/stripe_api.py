import stripe
import sys


def isValidCard(card: str, cvc: str, exp_month: str, exp_year: str):
    # Set your secret key: remember to change this to your live secret key in production
    # See your keys here: https://dashboard.stripe.com/account/apikeys
    stripe.api_key = "sk_test_51MIgTvG1tFaoV4hYH8agk5RkYiJvWTyTLRUYrBMubA7hBCIvsMf1I1JHfvIhXevYT4gH6BMAbrLhtbkRjMpQY5CG00cR0VVSRx"

    try:
        # Create a token representing a credit card
        token = stripe.Token.create(
            card={
                "number": card,  # "4242424242424242",
                "exp_month": exp_month,  # 12,
                "exp_year": exp_year,  # 2030,
                "cvc": cvc  # "123"
            }
        )
        return "success", token

    except:
        # show which error was received
        # This means the card details aren't even valid... like totally wrong
        return "fail", sys.exc_info()[0]


def createCustomer(token, phone):
    if token:
        # Create a new customer with the credit card token
        customer = stripe.Customer.create(
            email="customer@example.com",
            source=token.id,
            phone=phone,  # "1234567890",
            type="express",
            description="a test user"
            # return_url =
            # refresh_url =
        )

        # Charge the customer's card
        charge = stripe.Charge.create(
            amount=1000,  # Amount in cents
            currency="usd",
            customer=customer.id,
            description="Charge for customer@example.com",
            receipt_email="customer@example.com"
        )

    else:
        # Credit card is invalid, raise exception
        raise Exception("Invalid card:", token.error.message)
