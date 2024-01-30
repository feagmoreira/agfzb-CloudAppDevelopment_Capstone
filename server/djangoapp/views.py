from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarDealer, DealerReview
from .restapis import get_request, get_dealers_from_cf, get_dealer_reviews_from_cf, analyze_review_sentiments, post_request, get_dealer_by_id_from_cf
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST 
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provided credentials are valid
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect('djangoapp:index')
        else:
            # If not authorized reload page
            return redirect('djangoapp:index')
    else:
        return render(request, 'djangoapp/index.html', context)


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to dearlership review
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        # Get user information from request.POST
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            # Login the user and redirect to dealer reviews page
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/registration.html', context)


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context ={}
    if request.method == "GET":
        url = "https://feagmoreira-3000.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        #Append list to the dictionary
        context["dealerships"] = dealerships
        # Render index with the dealerships
        return render(request, 'djangoapp/index.html', context)

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context ={}
    if request.method == "GET":
        url = "https://feagmoreira-5000.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/get_reviews"
        url_dealer = "https://feagmoreira-3000.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
        # Get reviews from the URL
        reviews = get_dealer_reviews_from_cf(url, dealer_id)
        # Get dealer from the URL
        dealer = get_dealer_by_id_from_cf(url_dealer, dealer_id)
        # Append reviews list to context
        context["reviews"] = reviews
        #Append list to the dictionary
        context["dealer"] = dealer
        # Return a list of reviews
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    # Handles POST request
    if request.method == "POST" and request.body:
        url = "https://feagmoreira-5000.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/post_review"
        # Post will be executed only if user is logged
        #if request.user.is_authenticated:
        json_body = json.loads(request.body)
            # If user is valid, create post body
        review = {}
        review["id"] = json_body["id"]
        review["name"] = json_body["name"]
        review["dealership"] = dealer_id
        review["review"] = json_body["review"]
        review["purchase"] = json_body["purchase"]
        review["purchase_date"] = json_body["purchase_date"]
        review["car_make"] = json_body["car_make"]
        review["car_model"] = json_body["car_model"]
        review["car_year"] = json_body["car_year"]
            # Encapsulate body
        json_payload = {}
        json_payload["review"] = review
            # Execute POST request to Backend
        response = post_request(url, json_payload)
            # Return reponse
        return HttpResponse(response)
    else:
        return HttpResponseForbidden("User not logged in!")


