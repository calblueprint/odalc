from django.conf import settings

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


class MissingTokenException(Exception):
    pass


def handle_stripe_course_registration(user, course, token):
    # Get the credit card details submitted by the form
    if not token:
        raise MissingTokenException()
    # May raise a stripe.CardError
    charge = stripe.Charge.create(
        amount=course.get_cost_in_cents(), # amount in cents
        currency="usd",
        card=token,
        description='This is a payment for ' + course.title,
        metadata={
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'course':course.title,
            'teacher_first_name':course.teacher.first_name,
            'teacher_last_name':course.teacher.last_name,
            'teacher_email':course.teacher.email,
            'odalc_funds': course.odalc_cost_split
        }
    )
    return charge


def handle_stripe_donation(amount, token):
    if not token or not amount:
        raise MissingTokenException()
    charge = stripe.Charge.create(
        amount=parse_amount_to_cents(amount), # amount in cents, again
        currency="usd",
        card=token
    )
    return charge


def parse_amount_to_cents(amount):
    return int(float(amount) * 100)
