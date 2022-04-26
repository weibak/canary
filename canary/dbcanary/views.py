import logging

from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView

from dbcanary.forms import AdvertForm, CarFiltersForm
from dbcanary.models import Advert
from dbcanary.queries import filter_cars

logger = logging.getLogger(__name__)


def create_advert(request, *args, **kwargs):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = AdvertForm(request.POST, request.FILES)
            if form.is_valid():
                logger.info(form.cleaned_data)
                advert = Advert.objects.create(
                    owner=request.user,
                    honey=request.META.get(
                        'HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR')).split(',')[-1].strip(),
                    **form.cleaned_data)
                advert.save()
            return redirect(
                "/",
            )
        else:
            form = AdvertForm()
            return render(request, "create_advert.html", {"form": form})

    else:
        return redirect("auth")


class CarView(TemplateView):
    template_name = "car_list.html"

    def get_context_data(self, **kwargs, ):
        adverts = Advert.objects.all()
        filters_form = CarFiltersForm(self.request.GET)

        if filters_form.is_valid():
            price__gt = filters_form.cleaned_data["price__gt"]
            price__lt = filters_form.cleaned_data["price__lt"]
            order_by = filters_form.cleaned_data["order_by"]
            engine_type = filters_form.cleaned_data["engine_type"]
            gear_box = filters_form.cleaned_data["gear_box"]
            drive = filters_form.cleaned_data["drive"]
            adverts = filter_cars(adverts, price__gt, price__lt, order_by, engine_type, gear_box, drive)

        paginator = Paginator(adverts, 30)
        page_number = "page"
        adverts = paginator.get_page(page_number)
        return {"adverts": adverts, "filters_form": filters_form}


def advert_view(request, advert_id):
    advert = get_object_or_404(Advert, id=advert_id)
    if request.method == "POST":
        if request.user.is_authenticated and request.method == "POST":
            if request.POST["action"] == "add":
                advert.favorites.add(request.user)
                messages.info(request, "Product successfully added to favorites")
            elif request.POST["action"] == "remove":
                advert.favorites.remove(request.user)
                messages.info(request, "Product successfully removed to favorites")
            redirect("car_details", advert_id=advert.id)
    return render(
        request,
        "car_details.html",
        {
            "advert": advert,
            "is_advert_in_favorites": request.user in advert.favorites.all(),
        },
    )
