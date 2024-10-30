from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Dog, Toy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .forms import FeedingForm

# Create your views here.


def associate_toy(request, dog_id, toy_id):
    # Adds the row with dog_id and toy_id to the join table in psql
    Dog.objects.get(id=dog_id).toys.add(toy_id)
    return redirect("dog-detail", dog_id=dog_id)


def remove_toy(request, dog_id, toy_id):
    dog = Dog.objects.get(id=dog_id)
    toy = Toy.objects.get(id=toy_id)
    dog.toys.remove(toy)
    return redirect("dog-detail", dog_id=dog.id)


class ToyCreate(CreateView):
    model = Toy
    fields = "__all__"


class ToyList(ListView):
    model = Toy


class ToyDetail(DetailView):
    model = Toy


class ToyUpdate(UpdateView):
    model = Toy
    fields = ["name", "color"]


class ToyDelete(DeleteView):
    model = Toy
    success_url = "/toys/"


def home(request):
    return render(request, "home.html")


def about(request):
    return render(request, "about.html")


def dog_index(request):
    dogs = Dog.objects.all()
    return render(request, "dogs/index.html", {"dogs": dogs})


def dog_detail(request, dog_id):
    dog_from_db = Dog.objects.get(id=dog_id)
    toys_dog_doesnt_have = Toy.objects.exclude(
        id__in=dog_from_db.toys.all().values_list("id")
    )
    feeding_form = FeedingForm()
    return render(
        request,
        "dogs/detail.html",
        {
            "dog": dog_from_db,
            "feeding_form": feeding_form,
            "toys": toys_dog_doesnt_have,
        },
    )


# This expects a template in the format of
# templates/<app-name>/<model_name>_form.html
# templates/my_app/dog_form.html
class DogCreate(CreateView):
    model = Dog
    fields = ["name", "breed", "description", "age"]
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
    return redirect("dog-detail", dog_id=dog_id)
