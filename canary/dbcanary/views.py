import logging

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from dbcanary.forms import AdvertForm, CarForm, CarFiltersForm
from dbcanary.models import Car, Advert
from dbcanary.queries import filter_cars

logger = logging.getLogger(__name__)


def create_advert(request, *args, **kwargs):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = AdvertForm(request.POST, request.FILES)
            form_car = CarForm(request.POST, )
            if form_car.is_valid():
                car = Car.objects.create(**form_car.cleaned_data)
                if form.is_valid():
                    logger.info(form.cleaned_data)
                    advert = Advert.objects.create(car=car, owner=request.user, **form.cleaned_data)
                    advert.save()
                return redirect(
                    "/",
                )
        else:
            form = AdvertForm()
            form_car = CarForm()
            return render(request, "create_advert.html", {"form": form, "form_car": form_car})
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
