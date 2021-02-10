from audioop import reverse
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import logout, authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from accounts.models import Profile, Submit
from eventing.models import Event
from accounts.forms import RegisterForm, UserEdit, ProfileEdit, CreatEvent, EditEvent, VerifyEvent


def register_user(request):
    """
    method for the client can register
    """
    context = {}
    reg_form = RegisterForm(request.POST)
    if request.method == 'POST':
        if reg_form.is_valid():
            new_user = reg_form.save()
            profile = Profile.objects.create(user=new_user, organ_name='بدون سازمان')
            login(request, new_user)
            return HttpResponseRedirect(reverse('accounts:profile'))
        else:
            context = {
                'reg_form': reg_form,
            }
    return render(request, 'accounts/register.html', context)


def login_operation(request):
    """
    login method
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if request.GET.get('next'):
                return HttpResponseRedirect(request.GET.get('next'))
            return HttpResponseRedirect(reverse('eventing:home_loader'))
        else:
            context = {
                'username': username,
                'error': 'کاربر یافت نشد'
            }
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('eventing:home_loader'))

        context = {}

    return render(request, 'accounts/login_page.html', context)


def logout_operation(request):
    """
    logout method
    """
    logout(request)
    return HttpResponseRedirect(reverse('accounts:login'))


def only_admin(view_func):
    """
    this method allowed to admin to access special task and templates
    """
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'admin':
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('eventing:home_loader'))
    return wrapper_function


@login_required
@only_admin
def admin_panel(request):
    """
    render admin panel
    """
    verified = Event.objects.filter(Q(cancel=False) and Q(verify=True)).order_by('-made_time')
    not_verified = Event.objects.filter(Q(cancel=False) and Q(verify=False)).order_by('-made_time')
    context = {
        'verified': verified,
        'not_verified': not_verified,
    }
    return render(request, 'accounts/admin_panel.html', context)


@login_required
@only_admin
def verify_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    organizer = event.organizer
    if request.method == 'POST':
        v_event = VerifyEvent(request.POST, files=request.FILES, instance=event)
        if v_event.is_valid():
            v_event.save()
            if v_event.cleaned_data['verify']:
                event.situation = Event.EVENT_NOT_STARTED
                event.save()
            if v_event.cleaned_data['cancel']:
                event.situation = Event.EVENT_CANCELED
                event.save()
            return HttpResponseRedirect((reverse('accounts:admin_panel')))
    else:
        v_event = VerifyEvent(instance=event)
        context = {
            'v_event': v_event,
            'event': event,
            'organizer': organizer,
        }
        return render(request, 'accounts/event_verify.html', context)


@login_required
def change_password(request):
    """
    user can change username and password
    """
    if request.method == 'POST':
        change_form = PasswordChangeForm(request.user, request.POST)
        if change_form.is_valid():
            user = change_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'گذر واژه با موفقیت تغییر کرد')
            return HttpResponseRedirect(reverse('accounts:change_password'))
        else:
            messages.error(request, 'لطفا خطا های زیر را بررسی کنید')
    else:
        change_form = PasswordChangeForm(request.user)
    context = {
        'change_form': change_form
    }
    return render(request, 'accounts/change_password.html', context)


@login_required
def profile_view(request):
    """
    user profile loader

    """
    if request.method == 'POST':
        user_field = UserEdit(request.POST, instance=request.user)
        profile_field = ProfileEdit(request.POST, files=request.FILES, instance=request.user.profile)
        if user_field.is_valid() and profile_field.is_valid():
            user_field.save()
            profile_field.save()
            return HttpResponseRedirect((reverse('accounts:profile')))
    else:
        user_field = UserEdit(instance=request.user)
        profile_field = ProfileEdit(instance=request.user.profile)

    profile = request.user.profile
    context = {
        'profile': profile,
        'user_field': user_field,
        'profile_filed': profile_field,
    }
    return render(request, 'accounts/profile_page.html', context)


@login_required
def my_events(request):
    """
    user can show own events
    """
    i_submitted = Submit.objects.filter\
        (Q(submitted_user=request.user.profile) & Q(cancel=False)).order_by('-submit_time')
    i_added = Event.objects.filter\
        (Q(organizer=request.user.profile)).order_by('-made_time')
    context = {
            'i_submitted': i_submitted,
            'i_added': i_added,
    }
    return render(request, 'accounts/profile_myevent.html', context)


@login_required
def event_submitted(request, event_id):
    """
    user can cancel submitted event
    """
    event = Event.objects.get(pk=event_id)
    user = request.user.profile
    context = {
        'event': event
    }
    '#Unsubmit event'
    if request.method == 'POST':
        try:
            assert not check_submitted(user, event), 'شما در این رویداد ثبت نام نکرده اید'
            submit = Submit.objects.get(submitted_user=user, submitted_event=event, cancel=False)
            submit.cancel = True
            submit.save()
            return HttpResponseRedirect(reverse('accounts:my_event'))
        except Exception as e:
            context['error'] = str(e)
        # ----
    return render(request, 'accounts/event_submitted.html', context)


def check_submitted(user, event):
    """
    check user are submitted specific event
    """
    if Submit.objects.filter(submitted_user=user, submitted_event=event, cancel=False).exists():
        return False
    else:
        return True


@login_required
def add_new_event(request):
    """
    user can add new event
    """
    context = {}
    if request.method == "POST":
        new_event = CreatEvent(request.POST, files=request.FILES)
        if new_event.is_valid():
            b = new_event.save(commit=False)
            b.organizer = request.user.profile
            b.save()
            return HttpResponseRedirect(reverse('accounts:my_event'))
    else:
        new_event = CreatEvent()
        context = {
            'new_event': new_event
        }
    return render(request, 'accounts/add_new_event.html', context)


@login_required
def edit_own_event(request, event_id):
    """
    user can edit or cancel own event
    """
    event = Event.objects.get(pk=event_id)
    user = request.user.profile
    subscribed = Submit.objects.filter(Q(submitted_event=event) and Q(cancel=False))

    if check_event_owner(user, event):
        if request.method == 'POST':
            edit_event = EditEvent(request.POST, files=request.FILES, instance=event)
            if edit_event.is_valid():
                edit_event.save()
                if edit_event.cleaned_data['cancel']:
                    event.situation = Event.EVENT_CANCELED
                    event.save()
                return HttpResponseRedirect((reverse('accounts:my_event')))
        else:
            edit_event = EditEvent(instance=event)
            context = {
                'edit_event': edit_event,
                'event': event,
                'subscribed': subscribed
            }
            return render(request, 'accounts/edit_event.html', context)
    else:
        raise Http404('شما اجازه دسترسی به این صفحه را ندارید')


def check_event_owner(user, event):
    if event.organizer == user:
        return True
    else:
        return False

