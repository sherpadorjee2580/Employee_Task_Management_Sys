from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.contrib import messages


def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            if user.groups.filter(name="Manager").exists():
                return redirect("manager_dashboard")

            elif user.groups.filter(name="Employee").exists():
                return redirect("employee_dashboard")

            else:
                messages.error(request, "No role assigned to this account.")
                logout(request)
                return redirect("login")

        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "accounts/login.html")


@login_required
def logout_view(request):

    logout(request)

    return redirect("login")


@login_required
def manager_dashboard(request):

    if not request.user.groups.filter(name="Manager").exists():
        messages.error(request, "You are not authorized to access this page.")
        return redirect("employee_dashboard")

    return render(request, "accounts/manager_dashboard.html")


@login_required
def employee_dashboard(request):

    if not request.user.groups.filter(name="Employee").exists():
        messages.error(request, "You are not authorized to access this page.")
        return redirect("manager_dashboard")

    return render(request, "accounts/employee_dashboard.html")