from django.shortcuts import render

def upload_trades(request):
    """
    View voor de uploadpagina.
    Straks komt hier de logica voor het uploaden en inlezen van IBKR/DeGiro bestanden.
    """
    return render(request, "trades/upload.html")


def dashboard(request):
    """
    View voor het dashboard.
    Straks halen we hier Trade-data op en maken we grafieken.
    """
    return render(request, "trades/dashboard.html")
