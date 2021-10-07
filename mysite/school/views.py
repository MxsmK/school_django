from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseNotFound
from .models import Person
from django.utils import timezone


# получение данных из бд
def index(request):
    people = Person.objects.all()
    return render(request, "index.html", {"people": people})


def new(request):
    return render(request, "new.html")


# сохранение данных в бд
def create(request):
    if request.method == "POST":
        tom = Person()
        tom.name = request.POST.get("name")
        tom.surname = request.POST.get("surname")
        tom.sum = 0
        tom.is_free = request.POST.get("is_free")
        tom.is_weak = False
        tom.save()
    return HttpResponseRedirect("/")


def edit(request, id):
    try:
        person = Person.objects.get(id=id)

        if request.method == "POST":
            person.name = request.POST.get("name")
            person.surname = request.POST.get("surname")
            person.is_weak = request.POST.get("is_weak")
            person.is_free = request.POST.get("is_free")
            person.save()
            return HttpResponseRedirect("/")
        else:
            return render(request, "edit.html", {"person": person})
    except Person.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")


# удаление данных из бд
def delete(request, id):
    try:
        person = Person.objects.get(id=id)
        person.delete()
        return HttpResponseRedirect("/")
    except Person.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")


def status(request):
    people = Person.objects.all()
    stat_people = []
    for i in people:
        days = (timezone.now() - i.created_date).days
        if i.is_free:
            i.created_date = timezone.now()
            stat_people.append({"id": i.id, "name": i.name, "surname": i.surname, "sum": i.sum, "status": "ЕСТ, БЕСПЛАТНИК"})
        elif i.is_weak:
            i.created_date = timezone.now()
            stat_people.append({"id": i.id, "name": i.name, "surname": i.surname, "sum": i.sum, "status": "БОЛЕЕТ"})
        elif days >= 1:
            if i.sum >= (days + 5) * 70:
                i.sum -= days * 70
                i.created_date = timezone.now()
                stat_people.append({"id": i.id, "name": i.name, "surname": i.surname, "sum": i.sum, "status": "ЕСТ"})
            elif i.sum >= days * 70:
                i.sum -= days * 70
                i.created_date = timezone.now()
                stat_people.append(
                    {"id": i.id, "name": i.name, "surname": i.surname, "sum": i.sum, "status": "ЕСТ, ЗАКАНЧИВАЮТСЯ СРЕДСТВА"})
            else:
                i.created_date = timezone.now()
                stat_people.append({"id": i.id, "name": i.name, "surname": i.surname, "sum": i.sum, "status": "НЕ ЕСТ"})
        else:
            if i.sum >= (days + 5) * 70:
                stat_people.append({"id": i.id, "name": i.name, "surname": i.surname, "sum": i.sum, "status": "ЕСТ"})
            elif i.sum >= days * 70:
                stat_people.append(
                    {"id": i.id, "name": i.name, "surname": i.surname, "sum": i.sum, "status": "ЕСТ, ЗАКАНЧИВАЮТСЯ СРЕДСТВА"})
            else:
                stat_people.append({"id": i.id, "name": i.name, "surname": i.surname, "sum": i.sum, "status": "НЕ ЕСТ"})

    return render(request, "status.html", {"people": stat_people})


def add(request, id):
    try:
        person = Person.objects.get(id=id)
        if request.method == "POST":
            person.sum += int(request.POST.get("sum"))
            person.save()
            return HttpResponseRedirect("/status/")
        else:
            return render(request, "edit_sum.html", {"person": person})
    except Person.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")
