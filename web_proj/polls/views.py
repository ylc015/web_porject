from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from .models import MyUser 
from .forms import UserForm, UpdateUserForm
from django.contrib.auth.models import User
from registration.backends.simple.views import RegistrationView

import logging
logger = logging.getLogger(__name__)


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_user_list'

    """def get_queryset(self):
        Return the last five published questions (not including those set to be
        published in the future).
        return Question.objects.filter(
        pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]"""

    def get_queryset(self):

	    #return the 10 latest user (in registration order) 

	    return MyUser.objects.all()

    def user(self):

        return self.request.user

def index(request):

    all_users = MyUser.objects.all()

class DetailView(generic.DetailView):

	#def get_queryset(self):
    	#return Question.objects.filter(pub_date__lte=timezone.now())
	#	return UserProfile.objects.all()
	model = MyUser 
	template_name = 'polls/detail.html'

def detail(request, user_key):
    user_obj = get_object_or_404(MyUser, pk=user_key)
    current_user = request.user
    return render(request, 'polls/detail_overview.html', {'user_prof': user_obj, 'user_id': current_user})






def register(request):

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        #profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        #if user_form.is_valid() and profile_form.is_valid():
        if user_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save(commit=False)

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            #user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            #profile = profile_form.save(commit=False)
            #profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                user.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            user.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors
            #print profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        #profile_form = UserProfileForm()

    # Render the template depending on the context.
    # send userprofile instance if needed
    return render(request,
            'polls/register.html',
            {'user_form': user_form,'registered': registered} )


def user_login(request):

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
                # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
                # because the request.POST.get('<variable>') returns None, if the value does not exist,
                # while the request.POST['<variable>'] will raise key error exception
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(email=email, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)

                request.session['user_id'] = user.id
                return HttpResponseRedirect('/polls/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(email, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'polls/login.html', {})

@login_required
def logout(request):

    logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("polls/logout.html")


@login_required
def invite_user(request):

    user_ids = None
    if request.method == 'GET':

        user_id = request.GET['user_id']

        if user_id is None:
            logger.debug("retrieve user id from frontend failed")
            return HttpResponse("invite failed")

        target_usr = get_object_or_404(MyUser, id=user_id)
        req_user = request.user

        req_user.add_relationship(target_usr)
        target_usr.add_follower(req_user)

        logger.debug("user %s has followed user %s" % (req_user, target_usr))


    return HttpResponse("successfully invited user")

@login_required
def aboutView(request):
    rel = request.user.get_admirers()
    return render(request, 'polls/about_overview.html', {'user_name': request.user, 'rel': rel })

@login_required
def updateUser(request):


    if request.method == 'POST':
        instance = request.user

        update_form = UserForm(data=request.POST, instance=instance)


        if update_form.is_valid():

            user = update_form.save(commit=False)
            user.set_password(user.password)
            if 'picture' in request.FILES:
                user.picture = request.FILES['picture']
            user.save()

        else:
            print update_form.errors

        print "*********************"
        print "user section name is %s" % (request.user.get_full_name())

        rel = request.user.get_admirers()
        return render(request, 'polls/about_overview.html', {'user_name': request.user, 'rel': rel, 'user_id':request.user })


    else:
        update_form = UserForm()

    # Render the template depending on the context.
    # send userprofile instance if needed
    return render(request,
            'polls/about_edit.html',
            {'update_form':update_form, 'user_id':request.user} )

