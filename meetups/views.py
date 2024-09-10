from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import MeetupModel,Participant
from .forms import RegistrationForm

def index(request):
    meetups=MeetupModel.objects.all()
    return render(request,'meetups/index.html',{
        'show_meetups':True,
        'meetups':meetups
    })
def meetup_details(request,slug):
    try:
        selected_meetup=MeetupModel.objects.get(slug=slug)
        if request.method == 'GET':
            
            registration_form=RegistrationForm()
            return render(request,'meetups/meetup-details.html',{
                'meetup_found':True,
                'meetup':selected_meetup,
                'form':registration_form
            })
        else:
            registration_form=RegistrationForm(request.POST)
            if registration_form.is_valid():
                user_email=registration_form.cleaned_data['email']
                participant, _ =Participant.objects.get_or_create(email=user_email)
                selected_meetup.participants.add(participant)
                return redirect('confirm-registration',slug=slug)
        return render(request,'meetups/meetup-details.html',{
                'meetup_found':True,
                'meetup':selected_meetup,
                'form':registration_form
            })
    except Exception as exc:
        return render(request,'meetups/meetup-details.html',{
            'meetup_found':False,
            'meetup_title':'No meetup found',
            'meetup_description':'We could not find a meetup for the slug'
        })
def confirm_registration(request,slug):
    meetup=MeetupModel.objects.get(slug=slug)
    return render(request,'meetups/registration-success.html',{
        'organizer_email':meetup.organazier_email
    })