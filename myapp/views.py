import calendar

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import View

from .forms import InterestForm, ItemSearchForm, OrderItemForm
from .models import Item, Type, made_by


# Create your views here.
def index(request):
    type_list = Type.objects.all().order_by("id")[:10]
    return render(request, "myapp/index.html", {"type_list": type_list})


# Create your views here.


def about(request, year=None, month=None):
    if year is not None and month is not None:
        month_name = calendar.month_name[int(month)]

        welcome_message = "<p>" + f"This is an Online Grocery Store. You visited in {month_name} {year}." + "</p>"
    else:
        # If year and month are not provided, display a general welcome message
        welcome_message = "This is an Online Grocery Store."

    return render(request, "myapp/about.html", {"welcome_message": welcome_message})


def detail(request, type_no):
    # Retrieve the type object or raise a 404 error if not found
    type_obj = get_object_or_404(Type, pk=type_no)

    # Retrieve the items associated with the selected type
    items = Item.objects.filter(type=type_obj)

    # Pass necessary variables to the template
    context = {
        "type_obj": type_obj,
        "items": items,
    }

    # Render the detail.html template with the provided context
    return render(request, "myapp/detail.html", context)


class Detail(View):  # CBV for Part 3
    def get(self, request, type_no):
        response = HttpResponse()
        try:
            selected_type = Type.objects.get(pk=type_no)
            items = Item.objects.filter(type=selected_type)
            for i in items:
                para = "<p>" + str(i) + "</p>"
                response.write(para)
            return response
        except:
            return HttpResponse(status=404)


class made_bydetails(View):
    def get(self, request):
        details = made_by.objects.all().order_by("-first_name")
        return render(request, "myapp/made_by.html", {"details": details})


# class dummy(View):
#     def get(self,request):
#         dummy1 = 'dummy1'
#         dummy2 = 'dummy2'
#         context ={'dummy1':'dummy1','dummy2':'dummy2'}
#         return render(request, 'myapp/about.html',context)


def formTest(request):
    if request.method == "POST":
        order_item_form = OrderItemForm(request.POST)
        interest_form = InterestForm(request.POST)
        if order_item_form.is_valid() and interest_form.is_valid():
            order_item_form.save()

    else:
        order_item_form = OrderItemForm()
        interest_form = InterestForm()
    return render(request, "myapp/form.html", {"order_item_form": order_item_form, "interest_form": interest_form})


def items(request):
    itemlist = Item.objects.all().order_by("id")[:20]
    return render(request, "myapp/items.html", {"itemlist": itemlist})


def placeorder(request):
    msg = ""
    itemlist = Item.objects.all()

    if request.method == "POST":
        form = OrderItemForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if order.quantity <= order.item.stock:
                # order.save()
                order.item.stock -= order.quantity
                order.item.save()
                msg = "Your order has been placed successfully."
            else:
                msg = "We do not have sufficient stock to fill your order."
                return render(request, "myapp/order_response.html", {"msg": msg})
    else:
        form = OrderItemForm()
    return render(request, "myapp/placeorder.html", {"form": form, "msg": msg, "itemlist": itemlist})


def item_search(request):
    price = None
    if request.method == "POST":
        form = ItemSearchForm(request.POST)
        if form.is_valid():
            item = form.cleaned_data["item"]
            price = item.price
    else:
        form = ItemSearchForm()

    return render(request, "myapp/item_search.html", {"form": form, "price": price})


def itemdetail(request, item_id):
    # Retrieve the item based on item_id
    item = get_object_or_404(Item, pk=item_id)

    # Initialize message variable
    message = ""

    # Check if the item is available
    if not item.available:
        message = "This item is currently not available."

    # If a POST request, process the interest form
    if request.method == "POST":
        form = InterestForm(request.POST)
        if form.is_valid():
            # Save the form data (record user interest)
            form.save()
            # Update interested count for the item
            item.interested += 1
            item.save()
            # Redirect or display a success message
            return render(
                request,
                "myapp/itemdetail.html",
                {"item": item, "form": form, "message": "Thank you for showing your interest!"},
            )
    else:
        # Create a new instance of the interest form
        form = InterestForm()

    return render(request, "myapp/itemdetail.html", {"item": item, "form": form, "message": message})
