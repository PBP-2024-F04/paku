from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from promos.models import Promo
from .forms import PromoForm
from django.urls import reverse

@login_required(login_url='/accounts/login')
def my_promos(request):
    # Hanya menampilkan promo yang dibuat oleh pengguna yang sedang login
    promos = Promo.objects.filter(user=request.user) 
    return render(request, 'my_promos.html', {'promos': promos, 'user': request.user})

def main(request):
    # Menampilkan semua promo yang dapat dilihat oleh publik
    promos = Promo.objects.all()
    return render(request, 'promos.html', {'promos': promos, 'user': request.user})

@csrf_exempt
@login_required(login_url='/accounts/login/')
def add_promo(request):
    if request.method == 'POST':
        form = PromoForm(request.POST)
        if form.is_valid():
            promo = form.save(commit=False)
            promo.user = request.user  # Menetapkan pengguna saat ini
            promo.save()
            return JsonResponse({'success': True, 'redirect_url': '/promos/my_promos/'})  # Ubah redirect ke promos/my_promos/
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = PromoForm()
    
    return render(request, 'add_promo.html', {'form': form})

@csrf_exempt
@login_required(login_url='/accounts/login')
def update_promo(request, promo_id):
    promo = get_object_or_404(Promo, id=promo_id, user=request.user)  # Pastikan hanya merchant yang bisa mengupdate promo mereka
    if request.method == 'POST':
        promo.promo_title = request.POST.get('promo_title')
        promo.restaurant_name = request.POST.get('restaurant_name')
        promo.promo_description = request.POST.get('promo_description')
        promo.batas_penggunaan = request.POST.get('batas_penggunaan')
        promo.save()
        return JsonResponse({'success': True})

@csrf_exempt
@login_required(login_url='/accounts/login')
def delete_promo(request, promo_id):
    promo = get_object_or_404(Promo, id=promo_id, user=request.user)  # Pastikan hanya merchant yang bisa menghapus promo mereka
    if request.method == 'POST':
        promo.delete()
        return JsonResponse({'success': True})

@csrf_exempt
def get_promo(request, promo_id):
    promo = get_object_or_404(Promo, id=promo_id)
    return JsonResponse({
        'id': promo.id,
        'promo_title': promo.promo_title,
        'restaurant_name': promo.restaurant_name,
        'promo_description': promo.promo_description,
        'batas_penggunaan': promo.batas_penggunaan,
    })