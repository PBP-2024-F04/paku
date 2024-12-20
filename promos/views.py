from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from promos.models import Promo
from .forms import PromoForm
from django.urls import reverse
import json
from django.contrib.auth.models import User
import logging

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
    promo = get_object_or_404(Promo, id=promo_id, user=request.user)  # Ensure only the merchant can update their promo
    if request.method == 'GET':
        # Return the existing promo data in JSON format for editing
        promo_data = {
            'id': str(promo.id),
            'judul_promo': promo.judul_promo,
            'deskripsi_promo': promo.deskripsi_promo,
            'tanggal_batas': promo.tanggal_batas,
        }
        return JsonResponse(promo_data)

    if request.method == 'POST':
        # Update promo with the new data
        data = json.loads(request.body)
        form = PromoForm(data, instance=promo)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Promo berhasil diperbarui.'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})

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

@login_required(login_url='/accounts/login')
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

@csrf_exempt
@require_POST
@login_required(login_url='/accounts/login')
def create_promo_json(request):
    try:
        data = json.loads(request.body)
        
        # Menggunakan PromoForm untuk validasi
        promo_form = PromoForm(data)
        
        if promo_form.is_valid():
            promo = promo_form.save(commit=False)
            promo.user = request.user  # Menetapkan user dari request.user
            promo.save()
            return JsonResponse({"status": "success", "message": "Promo berhasil dibuat!"}, status=201)
        else:
            return JsonResponse({"status": "error", "errors": promo_form.errors}, status=400)
    
    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)
    except KeyError as e:
        return JsonResponse({"status": "error", "message": f"Missing parameter: {str(e)}"}, status=400)
    
@csrf_exempt
@require_POST
@login_required(login_url='/accounts/login')
def edit_promo_json(request, promo_id):
    try:
        data = json.loads(request.body)
        
        promo = get_object_or_404(Promo, pk=promo_id, user=request.user)
        
        promo_form = PromoForm(data, instance=promo)
        
        if promo_form.is_valid():
            promo = promo_form.save()
            return JsonResponse({"success": True, "message": "Promo berhasil diperbarui!"}, status=200)
        else:
            return JsonResponse({"success": False, "errors": promo_form.errors}, status=400)
    
    except json.JSONDecodeError:
        return JsonResponse({"success": False, "message": "Invalid JSON"}, status=400)

@csrf_exempt
@require_POST
@login_required(login_url='/accounts/login')
def delete_promo_json(request, promo_id):
    promo = get_object_or_404(Promo, pk=promo_id, user=request.user)
    promo.delete()
    return JsonResponse({"success": True, "message": "Promo berhasil dihapus!"}, status=200)
