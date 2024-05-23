# views.py
from django.shortcuts import render
from .forms import CreatePollForm
from django.shortcuts import redirect, get_object_or_404
from .models import Poll
from django.http import HttpResponse
from django.contrib import messages
def home(request):
    polls = Poll.objects.all()
    context = {
        'polls' : polls
    }
    return render(request, 'poll_portal/home.html', context)

def create(request):
    context = {}
    return render(request, 'poll_portal/create.html', context)

def results(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)

    context = {
        'poll' : poll
    }
    return render(request, 'poll_portal/results.html', context)

def vote(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)
    
    if request.method == 'POST':
        selected_option = request.POST['poll']
        if selected_option == 'option1':
            poll.option_one_count += 1
        elif selected_option == 'option2':
            poll.option_two_count += 1
        elif selected_option == 'option3':
            poll.option_three_count += 1
        else:
            return HttpResponse(400, 'Invalid form option')

    poll.save()
        
    context = {
        'poll' : poll
    }
    return render(request, 'poll_portal/vote.html', context)

def create(request):
    if request.method == 'POST':
        form = CreatePollForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CreatePollForm()
        context = {'form' : form}
        return render(request, 'poll_portal/create.html', context)

def delete(request, poll_id):
    poll =get_object_or_404(Poll, pk=poll_id)
    poll.delete()
    messages.success(request, 'Poll deleted successfully.')
    return render(request, 'poll_portal/home.html')