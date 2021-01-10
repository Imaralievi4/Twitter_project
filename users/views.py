from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.views.generic import FormView, View
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import CustomUserCreationForm, ProfileUpdateForm
from .utils import send_activation_email
# from django.contrib import messages
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User


class RegisterView(FormView):
    """"Create User"""
    form_class = CustomUserCreationForm
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


@login_required
def profile(request):
    if request.method == 'POST':
        uform = UserUpdateForm(request.POST, instance=request.user)
        pform = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if uform.is_valid() and pform.is_valid():
            uform.save()
            pform.save()
            messages.success(request, f'Account has been updated.')
            return redirect('profile')
    else:
        uform = UserUpdateForm(instance=request.user)
        pform = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'account/profile.html', {'uform': uform, 'pform': pform})


@login_required
def SearchView(request):
    if request.method == 'POST':
        kerko = request.POST.get('search')
        print(kerko)
        results = User.objects.filter(username__contains=kerko)
        context = {
            'results':results
        }
        return render(request, 'account/search_result.html', context)
