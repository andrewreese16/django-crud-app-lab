from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Dog
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import FeedingForm

# Create your views here.


def home(request):
    return render(request, "home.html")


def about(request):
    return render(request, "about.html")


def dog_index(request):
    dogs = Dog.objects.all()
    return render(request, "dogs/index.html", {"dogs": dogs})


def dog_detail(request, dog_id):
    dog_from_db = Dog.objects.get(id=dog_id)
    feeding_form = FeedingForm()
    return render(
        request, "dogs/detail.html", {"dog": dog_from_db, "feeding_form": feeding_form}
    )


# This expects a template in the format of
# templates/<app-name>/<model_name>_form.html
# templates/my_app/dog_form.html
class DogCreate(CreateView):
    model = Dog
    fields = "__all__"
    # Go to the models.py file for the Dog model
    # to see where the DogCreate redirects to, after
    # a POST request


class DogUpdate(UpdateView):
    model = Dog
    fields = ["breed", "description", "age"]


class DogDelete(DeleteView):
    model = Dog
    success_url = "/dogs/"


def add_feeding(request, dog_id):
    form = FeedingForm(request.POST)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.dog_id = dog_id
        new_feeding.save()
    return redirect('dog-detail', dog_id=dog_id)