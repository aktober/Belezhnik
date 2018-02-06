from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import TemplateView, CreateView

from users.forms import UserForm, UserProfileForm, CommonUserForm
from users.models import UserProfile
from users.tokens import account_activation_token


###############
# CBV version #
###############
class LoginPage(LoginView):
    """
    Login page with custom template
    """
    template_name = 'users/login.html'


class LogoutPage(LogoutView):
    """
    Logout with defining redirect page
    """
    def get_next_page(self):
        return reverse('home')


class RegisterPage(CreateView):
    """
    Register new user (with UserProfile)
    """
    template_name = 'users/register_new.html'
    form_class = CommonUserForm

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.set_password(user.password)
        user.save()

        profile = UserProfile()
        profile.user = user
        if 'picture' in self.request.FILES:
            profile.picture = self.request.FILES['picture']
        if 'bio' in self.request.POST:
            profile.bio = self.request.POST['bio']
        profile.save()

        send_account_confirmation_email(self.request, user)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('home')


class ProfilePage(TemplateView):
    """
    Display all user related info
    """
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        kwargs['profile'] = user_profile
        return kwargs


def send_account_confirmation_email(request, user):
    # send account confirmation email
    current_site = get_current_site(request)
    mail_subject = 'Activate your account.'
    message = render_to_string('users/acc_active_email.html', {
        'user': user,
        'domain': current_site.domain,
        'userid': user.pk,
        'token': account_activation_token.make_token(user),
    })
    to_email = user.email
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    email.send()


def activate(request, pk, token):
    user = User.objects.get(pk=pk)
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # login(request, user)
        return render(request, 'users/email_confirm_valid.html')
    else:
        return render(request, 'users/email_confirm_invalid.html')

###############
# FBV version #
###############


def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
            else:
                return render(request, 'users/login_not_active.html')
        else:
            return render(request, 'users/login_invalid.html')

    else:
        return render(request, 'users/login.html', {})


def user_register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.is_active = False
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            if 'bio' in request.POST:
                profile.bio = request.POST['bio']
            profile.save()

            registered = True

            # send account confirmation email
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('users/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'userid': user.pk,
                'token': account_activation_token.make_token(user),
            })
            to_email = user_form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'users/register.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


def profile_view(request):
    user = User.objects.get(pk=request.user.id)
    user_profile = UserProfile.objects.get(user=user)
    return render(request, 'users/profile.html', {'profile': user_profile})
