from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponseRedirect
from django.views.generic import CreateView
from django.urls import reverse_lazy

from .forms import CustomUserCreationForm


User = get_user_model()


class SignUp(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/reg.html'

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(self.request, username=username, password=password)
        if user:
            login(self.request, user)
        return HttpResponseRedirect(reverse_lazy('index'))
