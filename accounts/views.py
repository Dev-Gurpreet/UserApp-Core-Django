from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CreateUserForm
from .decorators import allowed_users, unauthenticated_user, admin_only
from django.contrib.auth.models import Group, User
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.urls import reverse
from .utils import account_activation_token


@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():

            user = form.save(commit=False)
            username = form.cleaned_data.get('username')
        
            user.is_active = False
            user.save()

            group = Group.objects.get(name='customer') #create user with customer group permissions
            user.groups.add(group)

            currentSite = get_current_site(request)

            emailSubject = 'Activate your account'

            emailBody = {
                    'user': user,
                    'domain': currentSite.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
            }

            link = reverse('activate', kwargs={
                               'uidb64': emailBody['uid'], 'token': emailBody['token']})

            activate_url = 'http://'+currentSite.domain+link
            
            emailTo = form.cleaned_data.get('email')

            email = EmailMessage(
                emailSubject,
                'Hi '+user.username + ', Please the link below to activate your account \n'+activate_url,
                'noreply@semycolon.com',
                [emailTo],
            )

            email.send(fail_silently=False)

            messages.success(request, 'Account successfully created for ' + username + '. Please the link send to your email address to activate your account.')
            return redirect('login')

    context = {'form':form}
    return render(request, 'accounts/register.html', context)


def VerificationView(request, uidb64, token):
    try:
        id = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=id)

        if not account_activation_token.check_token(user, token):
            return redirect('login'+'?message='+'User already activated')

        if user.is_active:
            return redirect('login')
        user.is_active = True
        user.save()

        messages.success(request, 'Account activated successfully')
        return redirect('login')

    except Exception as ex:
        pass

    return redirect('login')


@unauthenticated_user   # user define decorator
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user= authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request,"Username or Password is incorrect")

    context = {}
    return render(request, 'accounts/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login') #restrict to show home page and redirect to login page
#@allowed_users(allowed_roles=['admin']) # users have admin group permissions are allowed to veiw home page
@admin_only
def home(request):
    context = {}
    return render(request, 'accounts/home.html', context)

def customerPage(request):
    context = {}
    return render(request, 'accounts/customerPage.html', context)



# Create your views here.
