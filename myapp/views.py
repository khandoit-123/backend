from django.shortcuts import render, redirect
from .models import Menu, Order, Track, Booking
from django.contrib.auth.decorators import login_required, permission_required
from .forms import UserProfileForm
from datetime import datetime

def home(request):
    return render(request, 'home.html')

@login_required(login_url='/accounts/login/')
def reservation(request):
    if request.method == "POST":
        date = request.POST.get("date")
        time = request.POST.get('time')
        people = request.POST.get('people')
        user = request.user
        reservation_date = datetime.strptime(date, "%Y-%m-%d").date()
        reservation_slot = datetime.strptime(time, "%H:%M").time()
        amt_people = int(people)
        reservation, created = Booking.objects.get_or_create(
                    name = user,
                    reservation_date = reservation_date,
                    reservation_slot = reservation_slot,
                    amt_people = amt_people
                    )
    return render(request, "reservation.html")

@login_required(login_url='/accounts/login/')
def order(request):
    orders = Order.objects.filter(user=request.user)
    items = Menu.objects.all()
    option = request.GET.get("type", "all")

    if option == "all":
        items = Menu.objects.all()
    elif option == "food":
        items = Menu.objects.filter(type="Food")
    elif option == "drink":
        items = Menu.objects.filter(type="Drink")
    else:
        items = Menu.objects.none()

    return render(request, "order.html", {"menu_items": items, "option": option, "orders": orders})

@login_required
def add_to_cart_all(request):
    if request.method == "POST":
        item_ids = request.POST.getlist("item_ids")
        table=request.POST.get('table')
        for item_id in item_ids:
            quantity = int(request.POST.get(f"q{item_id}"))
            if quantity > 0:
                item = Menu.objects.get(id=item_id)
                order, created = Order.objects.get_or_create(
                    user=request.user,
                    item=item,
                    table=table,
                    defaults={'quantity': quantity}
                )
                order, created = Track.objects.get_or_create(
                    item=item,
                    table=table,
                    defaults={'quantity': quantity},
                    status = False
                )
                if not created:
                    order.quantity += quantity
                    order.save()
    return redirect('order')

def register(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("accounts/login")
    else:
        form = UserProfileForm()

    return render(request, "register.html", {"form": form})

@permission_required(['myapp.add_track', 'myapp.change_track', 'myapp.add_track', 'myapp.change_track'], raise_exception=True)
def chef(request):
    items = Track.objects.filter(status=False)
    return render(request, "chef.html", {"items": items})

@permission_required(['myapp.add_track', 'myapp.change_track', 'myapp.add_track', 'myapp.change_track'], raise_exception=True)
def cooking(request):
    if request.method == "POST":
        item_id = request.POST.get("item_ids")
        status = request.POST.get(f"status_{item_id}")
        if status == 'True':
                track = Track.objects.get(id=item_id)
                track.status = (status == 'True')
                track.save()
    return redirect('chef')

@permission_required(['myapp.add_track', 'myapp.change_track', 'myapp.add_track', 'myapp.change_track'], raise_exception=True)
def checkout(request):
    orders = None
    table_number = None
    total = 0
    if "table" in request.POST and "paid" not in request.POST:
        table_number = request.POST.get("table")
        if table_number:
            try:
                table_number = int(table_number)
                orders = Order.objects.filter(table=table_number)
                for order in orders:
                    total +=  order.item.price * order.quantity
            except ValueError:
                orders = None
    elif "paid" in request.POST:
        table_number = request.POST.get("table")
        if table_number:
            Order.objects.filter(table=table_number).delete()
            Track.objects.filter(table=table_number).delete()
        return redirect("checkout")  # Reload page or redirect

    return render(request, "checkout.html", {"orders": orders,"table_number": table_number, "total": total})
