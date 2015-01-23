import logging

from django.contrib import messages
from django.conf import settings
from django.shortcuts import redirect
from django.views.generic import TemplateView

from odalc.courses.models import Course
from odalc.users.views import UserDataMixin
from odalc.lib.payments import MissingTokenException, handle_stripe_donation

import stripe


logger = logging.getLogger(settings.ODALC_LOGGER)


class AboutPageView(UserDataMixin, TemplateView):
    """Static page for general information about BRIDGE and ODALC."""
    template_name = 'base/about.html'

    def dispatch(self, request, *args, **kwargs):
        self.set_perms(request, *args, **kwargs)
        return super(AboutPageView, self).dispatch(request, *args, **kwargs)


class DonatePageView(UserDataMixin, TemplateView):
    """Static page for handling donations."""
    template_name = 'base/donate.html'

    def dispatch(self, request, *args, **kwargs):
        self.set_perms(request, *args, **kwargs)
        return super(DonatePageView, self).dispatch(request, *args, **kwargs)

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
            messages.error(request,
                    "No payment information was included in your submission. Your card hasn't been charged")
            return redirect('donate')
        except stripe.CardError:
            # The card has been declined
            messages.error(request, "Your information was invalid or your card has been declined")
            return self.render_to_response(self.get_context_data())
        except Exception as e:
            messages.error(request
                    "An unknown error occured. Please try again, or contact Oakland Digital if the problem persists.")
            return redirect('donate')


class FaqPageView(UserDataMixin, TemplateView):
    """ Static page for FAQ. The questions/answers are in the template file."""
    template_name = 'base/faq.html'

    def dispatch(self, request, *args, **kwargs):
        self.set_perms(request, *args, **kwargs)
        return super(FaqPageView, self).dispatch(request, *args, **kwargs)


class HomePageView(UserDataMixin, TemplateView):
    """Landing page for the website. Displays featured courses - if there aren't enough, upcoming and possibly past
    courses are also displayed.
    """
    NUM_COURSES_SHOWN = 3
    template_name = 'base/home.html'

    def dispatch(self, request, *args, **kwargs):
        self.set_perms(request, *args, **kwargs)
        return super(HomePageView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['featured_courses'] = Course.objects.get_featured(
            HomePageView.NUM_COURSES_SHOWN)
        return context


class WorkPageView(UserDataMixin, TemplateView):
    """Placeholder page for plans to make this platform open to people wanting to find partnerships for work
    opportunities - for potential employees."""
    template_name = 'base/work.html'

    def dispatch(self, request, *args, **kwargs):
        self.set_perms(request, *args, **kwargs)
        return super(WorkPageView, self).dispatch(request, *args, **kwargs)


class TalentPageView(UserDataMixin, TemplateView):
    """Placeholder page for plans to make this platform open to people wanting to find partnerships for work
    opportunities - for potential employees."""
    template_name = 'base/talent.html'

    def dispatch(self, request, *args, **kwargs):
        self.set_perms(request, *args, **kwargs)
        return super(TalentPageView, self).dispatch(request, *args, **kwargs)

