from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Event
from accounts.models import Submit
from .forms import EventSearchForm


def home_loader(request):
    """
    Load landing page
    """
    return render(request, 'eventing/base_page.html')


def event_list(request):
    """
    method for query from db to return all or searched events object and sent to client
    """
    events = Event.objects.filter(Q(cancel=False) and Q(verify=True))
    search_form = EventSearchForm(request.GET)
    if search_form.is_valid():
        if search_form.cleaned_data['event_title']:
            events = events.filter(title__contains=search_form.cleaned_data['event_title'])
        if search_form.cleaned_data['event_subject']:
            events = events.filter(subject=search_form.cleaned_data['event_subject'])
        if search_form.cleaned_data['event_NOT_START']:
            events = events.filter(situation=Event.EVENT_NOT_STARTED)
    events = events.order_by('-start_date')
    context = {
        'events': events,
        'search_form': search_form
    }
    return render(request, 'eventing/event_list.html', context)


def event_details(request, event_id):
    """
    method for query from db to return event details
    """
    event = Event.objects.get(pk=event_id)
    context = {
        'event': event
    }
    if request.user.is_authenticated:
        user = request.user.profile
        '#submit event'
        if request.method == 'POST':
            try:
                assert event.situation != event.EVENT_STARTED, 'رویداد درحال برگزاری میباشد'
                assert event.situation != event.EVENT_CANCELED, 'رویداد لغو شده است'
                assert event.situation != event.EVENT_DONE, 'رویداد به پایان رسیده است'
                assert event.situation != event.NOT_VERIFY, 'این رویداد تایید نشده است'
                assert check_submitted(user, event), 'شما قبلا ثبت نام کرده اید'
                Submit.objects.create(submitted_user=user, submitted_event=event)
                return HttpResponseRedirect(reverse('accounts:my_event'))
            except Exception as e:
                context['error'] = str(e)

    return render(request, 'eventing/event_details.html', context)


def check_submitted(user, event):
    """
    check user are submitted specific event
    """
    if Submit.objects.filter(submitted_user=user, submitted_event=event, cancel=False).exists():
        return False
    else:
        return True

