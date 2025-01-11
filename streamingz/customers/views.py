from django.http import FileResponse, HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse
import os
from .forms import UserSignupForm
from movies.models import Video
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .khalti import get_khalti,verify_khalti
from .esewa_payment import send_esewa_payment, generate_transaction_uuid


def user_signup(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            if "HX-Request" in request.headers:
                return render(request, 'myapp/signup_success.html', {'user': user})
            return redirect('login')
        
        else:
            if "HX-Request" in request.headers:
                return render(request, 'signup.html', {'form': form})
            return render(request, 'signup.html', {'form': form})
    
    else:
        form = UserSignupForm()

    return render(request, 'signup.html', {'form': form})


def serve_hls_playlist(request, video_id):
    try:
        video = get_object_or_404(Video, pk=video_id)
        hls_playlist_path = os.path.join(settings.MEDIA_ROOT, video.hls)
        hls_playlist_path = os.path.normpath(hls_playlist_path)
        with open(hls_playlist_path, 'r') as m3u8_file:
            m3u8_content = m3u8_file.read()
        base_url = request.build_absolute_uri('/') 
        serve_hls_segment_url = base_url + "serve_hls_segment/" + str(video_id)
        m3u8_content = m3u8_content.replace('{{ dynamic_path }}', serve_hls_segment_url)

        return HttpResponse(m3u8_content, content_type='application/vnd.apple.mpegurl')
    except (Video.DoesNotExist, FileNotFoundError):
        return HttpResponse("Video or HLS playlist not found", status=404)

def serve_hls_segment(request, video_id, segment_name):
    try:
        video = get_object_or_404(Video, pk=video_id)
        hls_directory = os.path.join(os.path.dirname(video.video.path), 'hls_output')
        segment_path = os.path.join(hls_directory, segment_name)
        return FileResponse(open(segment_path, 'rb'))
    except (Video.DoesNotExist, FileNotFoundError):
        return HttpResponse("Video or HLS segment not found", status=404)


def hls_video_player(request, video_id):
    video = Video.objects.filter(slug=video_id).first()
    hls_playlist_url = reverse('serve_hls_playlist', args=[video.id])
    context = {
        'hls_url': hls_playlist_url,
        'video': video,
    }
    return render(request, 'index2.html', context)



def all_videos(request):
    videos = Video.objects.filter(status='Completed')
    context = {
        'videos': videos,
    }
    return render(request, 'index.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('all_videos') 

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('all_videos')
        else:
            if not username or not password:
                error_message = 'Please fill in both fields.'
            else:
                error_message = 'Invalid username or password.'

            return render(request, 'login.html', {
                'error': error_message
            })
        
    return render(request, 'login.html')

@login_required 
def logout_view(request):
    logout(request) 
    return redirect('all_videos')


@csrf_protect
@login_required
def choose_plan(request):
    if request.method == "POST":
        package_id = request.POST.get("package_id")
        package_name = request.POST.get("package_name")
        gateway = request.POST.get("gateway")

        if gateway == "khalti":
            url = get_khalti(package_id, package_name)
            return redirect(url)
        elif gateway == "esewa":
            total_amount = 100
            transaction_uuid = generate_transaction_uuid()
            response = send_esewa_payment(total_amount, transaction_uuid)

            if response.status_code == 302:
                redirect_url = response.headers.get("Location")
                return redirect(redirect_url)
            else:
                return HttpResponse(f"eSewa Payment Failed: {response.text}", status=response.status_code)
        else:
            return HttpResponse("Invalid payment gateway selected", status=400)
    else:
        return render(request, 'plans.html')


@login_required
def user_dashboard(request):
    return render(request, 'dashboard.html')



@csrf_protect
def subscribe_plan(request):
    if request.method == "POST":
        package_id = request.POST.get("package_id")
        package_name = request.POST.get("package_name")
        return HttpResponse(f"Subscribed to {package_name} (ID: {package_id}) successfully!")
    else:
        return redirect("home")


def process_payment(request):
    pidx = request.GET.get('pidx', 'N/A')
    transaction_id = request.GET.get('transaction_id', 'N/A')
    tidx = request.GET.get('tidx', 'N/A')
    amount = request.GET.get('amount', 'N/A')
    total_amount = request.GET.get('total_amount', 'N/A')
    mobile = request.GET.get('mobile', 'N/A')
    status = request.GET.get('status', 'N/A')
    purchase_order_id = request.GET.get('purchase_order_id', 'N/A')
    purchase_order_name = request.GET.get('purchase_order_name', 'N/A')
    verification = verify_khalti(pidx)

    if verification:
        return render(request, 'payment_success.html', {
            'pidx': pidx,
            'transaction_id': transaction_id,
            'tidx': tidx,
            'amount': amount,
            'total_amount': total_amount,
            'mobile': mobile,
            'status': status,
            'purchase_order_id': purchase_order_id,
            'purchase_order_name': purchase_order_name,
        })
    else:
        return render(request, 'payment_failed.html', {
            'pidx': pidx,
            'transaction_id': transaction_id,
            'tidx': tidx,
            'amount': amount,
            'total_amount': total_amount,
            'mobile': mobile,
            'status': status,
            'purchase_order_id': purchase_order_id,
            'purchase_order_name': purchase_order_name,
        })
    
def poor_users(request):
    return render(request, 'poor.html')