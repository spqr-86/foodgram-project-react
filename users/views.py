from django.contrib.auth import authenticate, get_user_model, login
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

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


def page_not_found(request, exception):
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500)
