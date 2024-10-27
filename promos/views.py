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
        form = PromoForm(request.POST, instance=promo)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Promo berhasil diperbarui.'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = PromoForm(instance=promo)
    return render(request, 'update_promo.html', {'form': form})

@csrf_exempt
@login_required(login_url='/accounts/login')
def delete_promo(request, promo_id):
    if request.method == 'POST':
        try:
            promo = get_object_or_404(Promo, id=promo_id, user=request.user)  # Pastikan hanya merchant yang bisa menghapus promo mereka
            promo.delete()
            return JsonResponse({'status': 'success', 'message': 'Promo berhasil dihapus!'})
        except Promo.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Promo tidak ditemukan.'})
    return JsonResponse({'status': 'error', 'message': 'Permintaan tidak valid.'})

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
    
def promo_list_json(request):
    promos = Promo.objects.all()
    data = [{
        'id': promo.id,
        'promo_title': promo.promo_title,
        'restaurant_name': promo.restaurant_name,
        'promo_description': promo.promo_description,
        'batas_penggunaan': promo.batas_penggunaan.strftime('%d-%m-%Y') if promo.batas_penggunaan else "Tidak punya batas"
    } for promo in promos]
    return JsonResponse(data, safe=False)

def my_promo_list_json(request):
    promos = Promo.objects.filter(user=request.user) 
    data = [{
        'id': promo.id,
        'promo_title': promo.promo_title,
        'restaurant_name': promo.restaurant_name,
        'promo_description': promo.promo_description,
        'batas_penggunaan': promo.batas_penggunaan.strftime('%d-%m-%Y') if promo.batas_penggunaan else "Tidak punya batas"
    } for promo in promos]
    return JsonResponse(data, safe=False)