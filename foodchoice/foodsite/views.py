from django.shortcuts import render
from django.http import HttpResponse
from .forms import RequestForm
from .models import Restaurant
import random
import json

# Create your views here.
def index(request):
    return render(request, "foodsite/index.html", {"form": RequestForm()})

def request(request):
    """
    Request a location for food.
    """
    if request.method == "POST":
        form = RequestForm(request.POST)
        if not form.is_valid():
            return HttpResponse("Data was not properly submitted.")
        # check database for Restaurant where name == form.name
        name = form.cleaned_data["location"]
        restaurants = Restaurant.objects.filter(name=name)
        if not restaurants:
            # create restaurant
            restaurant = Restaurant()
            restaurant.name = name
            restaurant.number_requests = 1
            restaurant.save()
        else:
            # if we found one, increment number_requests
            restaurants[0].number_requests += 1
            restaurants[0].save()
        return render(request, "foodsite/request.html", {"restaurant": name})
    else:
        return HttpResponse("Data was not properly submitted.")

def result(request):
    """
    Make a decision for a meal.
    """
    def weighted_choice(choices):
        total = sum(c.number_requests for c in choices)
        r = random.uniform(0, total)
        upto = 0
        for c in choices:
            if upto + c.number_requests >= r:
                return c
            upto += c.number_requests
        assert False, "Shouldn't get here"
    restaurants = Restaurant.objects.exclude(number_requests=0)
    lenr = len(restaurants)
    if not restaurants:
        return HttpResponse("No restaurants have been requested")
    # select random restaurant from the database
    restaurant = weighted_choice(restaurants)
    name = restaurant.name
    # set number_requests to 0
    restaurant.number_requests = 0
    restaurant.save()

    # render it to the screen
    return render(request, "foodsite/result.html", {"restaurant": name})

def show_restaurants(request):
    restaurants = Restaurant.objects.exclude(number_requests=0)
    lenr = len(restaurants)
    restaurant_hash = {}
    for restaurant in restaurants:
        restaurant_hash[str(restaurant.name)] = str(restaurant.number_requests)
    return HttpResponse(json.dumps(restaurant_hash))
