from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from django.views.generic import FormView, View
from django.urls import reverse_lazy

from .forms import UserRegistrationForm
from .utils import send_activation_email


class RegisterView(FormView):
    """"Create User"""
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')
    template_name = 'account/registration.html'

    def form_valid(self, form):
        user = form.save()
        send_activation_email(user)
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class ActivationView(View):
    """Activation user by email"""
    def get(self, request, activation_code):
        user = get_object_or_404(get_user_model(), activation_code=activation_code)
        user.is_active = True
        user.activation_code = ''
        user.save()
        return render(request, 'account/activation.html')
        