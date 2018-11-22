from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Profile
from .forms import PostForm, UserForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
#from django.views.generic import TemplateView
########################################POST###################################
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blogs/post_list.html', {'posts': posts})
    #path('post/<int:pk>/', views.post_detail, name='post_detail')
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blogs/post_detail.html', {'post': post})
#@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            #post.published_date = timezone.now()#review post uncomment for no review
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blogs/post_edit.html', {'form': form})
@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            #post.published_date = timezone.now()#review post uncomment for no review
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blogs/post_edit.html', {'form': form})
@login_required
def post_draft_list(request):#post approvals(#review post uncomment for no review)
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blogs/post_draft_list.html', {'posts': posts})
@login_required
def post_publish(request, pk):#adding publish button(#review post uncomment for no review)
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)
@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

############################################################
#####################PROFILE###################################################
###############################################################################
@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profileForm = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profileForm.is_valid():
            user_form.save(commit=False)
            profileForm.save(commit=False)
            profileForm.published_date = timezone.now()
            profileForm.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserForm(instance=request.user)
        profileForm = ProfileForm(instance=request.user.profile)
    return render(request, 'blogs/profile.html', {
        'user_form': user_form,
        'profileForm': profileForm
    })

###############################################################################
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .forms import SignUpForm
from .tokens import account_activation_token

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.is_active = False#waiting for comfirmation####################
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your: MySite Account'
            message = render_to_string('blogs/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')#########################
            #login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            #return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})
def account_activation_sent(request):
    return render(request, 'blogs/account_activation_sent.html')

from django.contrib.auth import login
from django.contrib.auth.models import User
#from django.shortcuts import render, redirect
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
#from .tokens import account_activation_token

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'blogs/account_activation_invalid.html')#
        
from django.core.mail import send_mail

send_mail('noreply', 'body of the message', 'adeolaolalekan1431@yahoo.com', ['adeolaolalekan01831@gmail.com', 'adeolaolalekan1831@outlook.com'])

###############################################################################
from django.contrib.admin import helpers
from django.contrib import auth
#...

def logins(request):
    if request.user.is_authenticated:
        return redirect('admin_page')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            # correct username and password login the user
            auth.login(request, user)
            return redirect('admin_page')
        else:
            return redirect('home')
    return render(request, 'registration/logins.html')
def logout(request):
    auth.logout(request)
    return render(request,'registration/logout.html')
def admin_page(request):
    if not request.user.is_authenticated:
        return redirect('blog_login')
    return render(request, 'registration/admin.html')
def home(request):
    """
    Home page
    """
    # If a user is authenticated then redirect them to the user page
    if request.user.is_authenticated:#user page
        posts = Post.objects.filter(author=User.objects.get(username=request.user.username)).order_by('published_date')
        return render(request, 'blogs/post_list.html', {'posts': posts})
    else:#general page
        return render(request, 'blogs/account_update.html')
##############################################################################
#SEARCHING
from django.contrib.auth.models import User
from django.shortcuts import render
from .forms import UserFilter

def search(request):
    user_list = User.objects.all()
    user_filter = UserFilter(request.GET, queryset=user_list)
    return render(request, 'registration/user_list.html', {'filter': user_filter})
from .models import Students
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
def index(request):
    next = request.GET.get('next', '/admin_page')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                data = Students.objects.all()
                stu = {"student_number": data}
                return render(request, 'blogs/profiles.html', {'data': stu})
            else:
                HttpResponse("Inactive User.")
        else:
            print("User Not Found!", next)
            return HttpResponseRedirect(settings.LOGIN_URL)
    
    return render(request, 'blogs/profiles.html', {'redirect_to':next})
###############################################################################

################################################################################
#ACCOUNT MANAGMENT
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from social_django.models import UserSocialAuth
@login_required
def settings(request):
    user = request.user

    try:
        github_login = user.social_auth.get(provider='github')
    except UserSocialAuth.DoesNotExist:
                github_login = None
    try:
        twitter_login = user.social_auth.get(provider='twitter')
    except UserSocialAuth.DoesNotExist:
                twitter_login = None

    try:
        facebook_login = user.social_auth.get(provider='facebook')
    except UserSocialAuth.DoesNotExist:
                facebook_login = None

    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

    return render(request, 'registration/settings.html', {
        'github_login': github_login,
        'twitter_login': twitter_login,
        'facebook_login': facebook_login,
        'can_disconnect': can_disconnect
    })

@login_required
def password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('post_list')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'registration/password.html', {'form': form})
###############################################################################

from .forms import DocumentForm
def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'blogs/model_form_upload.html', {
        'form': form
    })

from .forms import StudentForm

def StudentReg(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = StudentForm()
    return render(request, 'blogs/student_reg.html', {'form': form})