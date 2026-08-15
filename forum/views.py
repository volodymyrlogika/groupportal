from django.shortcuts import render


def menu(request):
    check_in = request.GET.get('check_in')
    check_out = request.GET.get('check_out')

    apartments = []
    if check_in and check_out:
        # Add real queryset logic here when an Apartment model is available.
        apartments = []

    return render(request, 'menu.html', {
        'apartments': apartments,
    })