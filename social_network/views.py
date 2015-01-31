from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.shortcuts import render_to_response
from social_network.forms import UserForm, UserProfileForm
from social_network.models import job
import json
import os
import math

pathToHtml = "social_network/html/"
pathToCss = "social_network/css/"

pathToHtml = ""


def index(request):    
    return render_to_response(pathToHtml+"homepage.html", {}, RequestContext(request))

def log_in(request):
    return render_to_response("login.html", {}, RequestContext(request))

def authentication(request):
    if request.method == "POST":
        if request.POST['username'] is not None and request.POST['password'] is not None:
            username = request.POST['username']
            password = request.POST['password']

            # # combination is valid - a User object is returned if it is.
            user = authenticate(username=username, password=password)

            # If we have a User object, the details are correct.
            # If None (Python's way of representing the absence of a value), no user
            # with matching credentials was found.
            if user:
                # Is the account active? It could have been disabled.
                if user.is_active:
                    # If the account is valid and active, we can log the user in.
                    # We'll send the user back to the homepage.
                    login(request, user)
                    return HttpResponseRedirect('../')
                else:
                    # An inactive account was used - no logging in!
                    return HttpResponseRedirect("../login/")

            else:
                return HttpResponseRedirect("../login/")
        else:
            return HttpResponseRedirect("../login/")

    else:
        return HttpResponseRedirect("../login/")

def create_account(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    username = request.POST['username']
    password = request.POST['password']


    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)


        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()


            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True


        else:
            return(HttpResponseRedirect("/social/new_account_failure/"))

        user_logged = authenticate(username=username, password=password)
        login(request, user_logged)

        return(HttpResponseRedirect("/social/new_account_success/"))



    # # Not a HTTP POST, so we render our form using two ModelForm instances.
    # # These forms will be blank, ready for user input.
    # else:
    #     user_form = UserForm()
    #     profile_form = UserProfileForm()

    # Render the template depending on the context.
    return(HttpResponseRedirect("/social/"))






    # context = RequestContext(request)
    # if request.method == 'POST':
        
    # return HttpResponseRedirect("/social/")


def log_out(request):
    logout(request)
    return HttpResponseRedirect('/social/')


def profile(request):
    if request.user.is_authenticated():
        return render_to_response("profile.html", {}, RequestContext(request))
    else:
        return HttpResponseRedirect("/social/login/")


def new_account_success(request):
    return render_to_response("new_account.html", {}, RequestContext(request))    


def job_search(request):
    return render_to_response("search.html", {}, RequestContext(request))



def job_search_backend(request):

    if request.method != 'GET':
        return HttpResponse("Error!")
        
    page = request.GET['page']
    search_vals = request.GET['search_vals']
    per_page = request.GET['per_page']

    
    firstEntry = int(page) * int(per_page)
    lastEntry = (int(page)+1) * int(per_page)
    print(firstEntry)

    retJson = []
    if search_vals=="all":
        totalJobs = len(job.objects.all())
        numPages = math.ceil(float(totalJobs) / float(per_page))
        allJobs = job.objects.order_by('-posted_timestamp')[firstEntry:lastEntry]


        for jobObj in allJobs:
            retJson.append(
                {
                    "user" : str(jobObj.user.username),
                    "title" : str(jobObj.title),
                    "job_descr" : str(jobObj.job_descr),
                    "deadline_date" : str(jobObj.deadline_date),
                    "job_duration" : str(jobObj.job_duration),
                    "posted_timestamp" : str(jobObj.posted_timestamp),
                    "numPages" : int(numPages),
                }
                )
            print jobObj.user
            

    print (retJson)
    return HttpResponse(json.dumps(retJson))
