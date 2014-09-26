from django.contrib import messages
from django.conf import settings
from django.shortcuts import redirect
from django.views.generic import TemplateView

from odalc.courses.models import Course
from odalc.users.views import UserDataMixin
from odalc.lib.payments import MissingTokenException, handle_stripe_donation

import stripe


class AboutPageView(UserDataMixin, TemplateView):
    template_name = 'base/about.html'


class DonatePageView(UserDataMixin, TemplateView):
    template_name = 'base/donate.html'

    def get_context_data(self, **kwargs):
        context = super(DonatePageView, self).get_context_data(**kwargs)
        context['stripe_public_key'] = settings.STRIPE_PUBLIC_KEY
        return context

    def post(self, request, *args, **kwargs):
        # Get the credit card details submitted by the form
        token = request.POST.get('stripeToken', False)
        amount = request.POST.get('quantity', False)
        try:
            handle_stripe_donation(amount, token)
            messages.success(request, "Thank you! Your donation has been processed.")
            return redirect('donate')
        except MissingTokenException:
            messages.error(request, "No payment information was included in your submission. Your card hasn't been charged")
            return redirect('donate')
        except stripe.CardError:
            # The card has been declined
            messages.error(request, "Your information was invalid or your card has been declined")
            return self.render_to_response(self.get_context_data())


class HomePageView(UserDataMixin, TemplateView):
    """Landing page for the website. Also displays the next three upcoming
    courses as "featured courses". If there are not enough, it will display past
    courses as well."""
    NUM_COURSES_SHOWN = 3
    template_name = 'base/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['featured_courses'] = Course.objects.get_featured(
            HomePageView.NUM_COURSES_SHOWN)
        return context

