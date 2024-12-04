from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .database import add_user, add_worker, user_exists, worker_exists, users_db, workers_db
from .forms import UserRegistrationForm, WorkerRegistrationForm
from .models import User, Worker, JobCategory, SubJobCategory, Transaction, Service, Discount, Order
from datetime import datetime
from django.contrib import messages
from django.http import JsonResponse

def choose_role(request):
    return render(request, 'choose_role.html')

from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
import datetime

def register_user(request):
    """Menangani pendaftaran pengguna baru."""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            password = form.cleaned_data['password']
            gender = form.cleaned_data['gender']
            phone = form.cleaned_data['phone']
            dob = request.POST.get('dob')
            address = form.cleaned_data['address']

            dob_date = datetime.datetime.strptime(dob, '%Y-%m-%d').date()

            try:
                # Simpan ke database
                user_profile = User(
                    name=name,
                    password=password,
                    # gender=gender,
                    phone=phone,
                    # dob=dob_date,
                    address=address
                )
                user_profile.save() 
                return redirect('login')
            except ValueError as e:
                form.add_error(None, str(e))
                return render(request, 'register_user.html', {'form': form})
    else:
        form = UserRegistrationForm()

    return render(request, 'register_user.html', {'form': form})

def register_worker(request):
    """Menangani pendaftaran pekerja baru."""
    if request.method == 'POST':
        form = WorkerRegistrationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            password = form.cleaned_data['password']
            gender = form.cleaned_data['gender']
            phone = form.cleaned_data['phone']
            dob = form.cleaned_data['dob']
            address = form.cleaned_data['address']
            account_number = form.cleaned_data['account_number']
            npwp = form.cleaned_data['npwp']
            photo_url = form.cleaned_data['photo_url']
            bank_name = form.cleaned_data['bank_name']
            
            try:
                Worker.objects.create(
                    name=name,
                    password=password,
                    gender=gender,
                    phone=phone,
                    dob=dob,
                    address=address,
                    account_number=account_number,
                    npwp=npwp,
                    photo_url=photo_url,
                    bank_name=bank_name
                )
                return redirect('login')
            except ValueError as e:
                form.add_error(None, str(e))
                return render(request, 'register_worker.html', {'form': form})
    else:
        form = WorkerRegistrationForm()
    
    return render(request, 'register_worker.html', {'form': form})

def profile(request):
    return render(request, "profile.html")

def login(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        user = None
        error_message = "Invalid username or password"
      # Periksa di tabel User
        try:
            user = User.objects.get(phone=phone)
            # print(user)
            if password == user.password:
                # Simpan data User ke session
                request.session['user_id'] = user.id
                request.session['user_phone'] = user.phone
                request.session['role'] = 'User'  # Tandai role sebagai User
                return redirect('home_user')  # Ganti 'home' dengan URL tujuan
        except User.DoesNotExist:
            pass  # Lanjut ke tabel Worker

          # Periksa di tabel Worker
        try:
            worker = Worker.objects.get(phone=phone)
            if password == worker.password:
                # Simpan data Worker ke session
                request.session['worker_id'] = worker.id
                request.session['worker_phone'] = worker.phone
                request.session['role'] = 'Worker'  # Tandai role sebagai Worker
                print(worker.password == password)
                return redirect('home_worker')  # Ganti 'dashboard' dengan URL tujuan
        except Worker.DoesNotExist:
            pass

        # Jika tidak ditemukan di kedua tabel
        return render(request, 'login.html', {'error': error_message})
    return render(request, 'login.html')

def home(request):
    """Menampilkan halaman utama setelah login berhasil."""
    if 'user_phone' not in request.session:
        print(request.session)
        return
        return redirect('login') 
    
    phone = request.session['user_phone']
    if user_exists(phone):
        return render(request, 'home.html', {'user': users_db[phone]}) 
    return redirect('login')

def logout(request):
    """Menangani proses logout."""
    request.session.flush()  
    return redirect('login')

def landing(request):
    return render(request, 'landing.html')

def home_worker(request):
    # print(request.session['worker_phone'])
    """Menampilkan halaman untuk pekerja."""
    if 'worker_phone' not in request.session:
        return redirect('login') 

    phone = request.session['worker_phone']
    if Worker.objects.filter(phone=phone).exists():  
        worker = Worker.objects.get(phone=phone)
                # Retrieve categories, subcategories, and services
        categories = JobCategory.objects.all()

        return render(request, 'home_worker.html', {'user': worker , 'categories': categories})  
    return redirect('home_user')

subcategory_data = {
    "1-1": {
        "name": "Subkategori Jasa 1-1",
        "category": "Kategori Jasa 1",
        "description": "Deskripsi layanan untuk Subkategori Jasa 1-1.",
        "sessions": [
            {"name": "Sesi Layanan 1", "price": "Rp 150.000"},
            {"name": "Sesi Layanan 2", "price": "Rp 150.000"},
        ],
        "workers": [
            {"name": "Pekerja 1"},
            {"name": "Pekerja 2"},
        ],
        "testimonials": [
            {"user": "Pengguna A", "date": "2024-11-07", "text": "Sangat puas!", "worker": "Pekerja 1", "rating": 5},
        ],
    },
    "1-2": {
        "name": "Subkategori Jasa 1-2",
        "category": "Kategori Jasa 1",
        "description": "Deskripsi layanan untuk Subkategori Jasa 1-2.",
        "sessions": [
            {"name": "Sesi Layanan 1", "price": "Rp 150.000"},
            {"name": "Sesi Layanan 2", "price": "Rp 150.000"},
        ],
        "workers": [
            {"name": "Pekerja 3"},
            {"name": "Pekerja 4"},
        ],
        "testimonials": [
            {"user": "Pengguna B", "date": "2024-11-06", "text": "Layanan bagus", "worker": "Pekerja 3", "rating": 4},
        ],
    },
    "1-3": {
        "name": "Subkategori Jasa 1-3",
        "category": "Kategori Jasa 1",
        "description": "Deskripsi layanan untuk Subkategori Jasa 1-3.",
        "sessions": [
            {"name": "Sesi Layanan 1", "price": "Rp 150.000"},
            {"name": "Sesi Layanan 2", "price": "Rp 150.000"},
        ],
        "workers": [
            {"name": "Pekerja 5"},
            {"name": "Pekerja 6"},
        ],
        "testimonials": [
            {"user": "Pengguna C", "date": "2024-11-05", "text": "Sangat memuaskan!", "worker": "Pekerja 5", "rating": 5},
        ],
    },
    "2-1": {
        "name": "Subkategori Jasa 2-1",
        "category": "Kategori Jasa 2",
        "description": "Deskripsi layanan untuk Subkategori Jasa 2-1.",
        "sessions": [
            {"name": "Sesi Layanan 1", "price": "Rp 150.000"},
            {"name": "Sesi Layanan 2", "price": "Rp 150.000"},
        ],
        "workers": [
            {"name": "Pekerja 7"},
            {"name": "Pekerja 8"},
        ],
        "testimonials": [
            {"user": "Pengguna D", "date": "2024-11-04", "text": "Pengalaman yang menyenangkan.", "worker": "Pekerja 7", "rating": 4},
        ],
    },
    "2-2": {
        "name": "Subkategori Jasa 2-2",
        "category": "Kategori Jasa 2",
        "description": "Deskripsi layanan untuk Subkategori Jasa 2-2.",
        "sessions": [
            {"name": "Sesi Layanan 1", "price": "Rp 150.000"},
            {"name": "Sesi Layanan 2", "price": "Rp 150.000"},
        ],
        "workers": [
            {"name": "Pekerja 9"},
            {"name": "Pekerja 10"},
        ],
        "testimonials": [
            {"user": "Pengguna E", "date": "2024-11-03", "text": "Kualitas layanan baik.", "worker": "Pekerja 9", "rating": 3},
        ],
    },
    "2-3": {
        "name": "Subkategori Jasa 2-3",
        "category": "Kategori Jasa 2",
        "description": "Deskripsi layanan untuk Subkategori Jasa 2-3.",
        "sessions": [
            {"name": "Sesi Layanan 1", "price": "Rp 150.000"},
            {"name": "Sesi Layanan 2", "price": "Rp 150.000"},
        ],
        "workers": [
            {"name": "Pekerja 11"},
            {"name": "Pekerja 12"},
        ],
        "testimonials": [
            {"user": "Pengguna F", "date": "2024-11-02", "text": "Layanan yang ramah.", "worker": "Pekerja 11", "rating": 5},
        ],
    },
    "3-1": {
        "name": "Subkategori Jasa 3-1",
        "category": "Kategori Jasa 3",
        "description": "Deskripsi layanan untuk Subkategori Jasa 3-1.",
        "sessions": [
            {"name": "Sesi Layanan 1", "price": "Rp 150.000"},
            {"name": "Sesi Layanan 2", "price": "Rp 150.000"},
        ],
        "workers": [
            {"name": "Pekerja 13"},
            {"name": "Pekerja 14"},
        ],
        "testimonials": [
            {"user": "Pengguna G", "date": "2024-11-01", "text": "Harga sesuai kualitas.", "worker": "Pekerja 13", "rating": 4},
        ],
    },
    "3-2": {
        "name": "Subkategori Jasa 3-2",
        "category": "Kategori Jasa 3",
        "description": "Deskripsi layanan untuk Subkategori Jasa 3-2.",
        "sessions": [
            {"name": "Sesi Layanan 1", "price": "Rp 150.000"},
            {"name": "Sesi Layanan 2", "price": "Rp 150.000"},
        ],
        "workers": [
            {"name": "Pekerja 15"},
            {"name": "Pekerja 16"},
        ],
        "testimonials": [
            {"user": "Pengguna H", "date": "2024-10-31", "text": "Pekerjaan rapi dan cepat.", "worker": "Pekerja 15", "rating": 5},
        ],
    },
    "3-3": {
        "name": "Subkategori Jasa 3-3",
        "category": "Kategori Jasa 3",
        "description": "Deskripsi layanan untuk Subkategori Jasa 3-3.",
        "sessions": [
            {"name": "Sesi Layanan 1", "price": "Rp 150.000"},
            {"name": "Sesi Layanan 2", "price": "Rp 250.000"},
        ],
        "workers": [
            {"name": "Pekerja 17"},
            {"name": "Pekerja 18"},
        ],
        "testimonials": [
            {"user": "Pengguna I", "date": "2024-10-30", "text": "Akan menggunakan jasa lagi.", "worker": "Pekerja 17", "rating": 4},
        ],
    },
}

def subkategori(request, subcategory_id):
    # Gunakan subcategory_id langsung dari parameter
    subkategori_id = subcategory_id
    
    
    # Pastikan ID subkategori ada di data
    try:
        subkategori = SubJobCategory.objects.get(id=1)
        services = subkategori.services.all()

        testimonials = subkategori.testimonials.all()
        workers = subkategori.workers.all()
    
        return render(request, 'sub_category.html', {'subcategory': subkategori, 'services': services, 'testimonials': testimonials, 'workers': workers, "role": request.session['role']})
    except SubJobCategory.DoesNotExist:
        return render(request, '404.html', {'message': 'ID Subkategori tidak ditemukan atau tidak valid.'}, status=404)

def home_user(request):
  
    """Menampilkan halaman untuk pengguna."""
    if 'user_phone' not in request.session:
        return redirect('login')  

    phone = request.session['user_phone']
    if User.objects.filter(phone=phone).exists():
        user = User.objects.get(phone=phone)
        categories = JobCategory.objects.all()

        return render(request, 'home_user.html', {'user': user , 'categories': categories}) 
    return redirect('home_worker')


def daftar_diskon(request):
    return render(request, 'user/daftar_diskon.html')

def my_pay(request):
    phone = request.session['user_phone']
    penggunan = None
    if User.objects.filter(phone=phone).exists():
        pengguna = User.objects.get(phone=phone)
    transactions = pengguna.transactions.all()
    return render(request, 'user/mypay.html', {"pengguna": pengguna, "transactions": transactions})

def transaksi_mypay_view(request):
    # Ambil user_type dari sesi
    user_type = request.session.get('role', 'User')  # Default ke 'Pengguna' jika tidak diatur


    try:
        user_order = User.objects.get(phone=request.session['user_phone'])
    except User.DoesNotExist:
        return render(request, 'error.html', {'message': 'User not found'})

    # Ambil semua order yang statusnya "Menunggu Pembayaran"
    orders = Order.objects.filter(user=user_order, status="AWAITING_PAYMENT")
    if request.method == 'POST':
        # print(kategori)
        kategori = request.POST.get('kategori_transaksi')
        tanggal_transaksi = datetime.datetime.now().strftime('%Y-%m-%d')
        user = User.objects.get(phone=request.session['user_phone'])
        saldo_user = user.saldo
        if kategori == 'TOP UP MY PAY':
            nominal = int(request.POST.get('nominal', 0))
            if nominal > 0:
                # request.session['saldo'] += nominal
                user = User.objects.get(phone=request.session["user_phone"])
                print(user)
                user.saldo += nominal
                user.save()
                user = User.objects.get(phone=request.session['user_phone'])  # Atau gunakan ID jika lebih spesifik

                # Buat instance transaksi
                transaction = Transaction(
                    user=user,
                    category="TOPUP",
                    amount=nominal
                )

                # Simpan transaksi ke database
                transaction.save()
                messages.success(request, 'Top Up Berhasil!')
            else:
                messages.error(request, 'Nominal tidak valid.')

        elif kategori == 'MEMBAYAR TRANSAKSI':
            if user_type == 'User':
                pesanan_jasa = request.POST.get('pesanan_jasa')
                # Ekstrak jumlah dari pesanan_jasa (misalnya, "Jasa 1 - Rp 200.000")
                print(pesanan_jasa)
                try:
                  
                    order = Order.objects.get(id=pesanan_jasa)
                    print(order.total_price)
                    if saldo_user >= order.total_price:
                        # TODO: prosess
                        order.status = 'SEARCHING_WORKER'
                        user.saldo -= order.total_price
                         # Buat instance transaksi
                        transaction = Transaction(
                            user=user,
                            category="MEMBAYAR TRANSAKSI",
                            amount=order.total_price
                        )


                        # Simpan transaksi ke database
                        user.save()
                        order.save()
                        transaction.save()
                        print("success")
                        messages.success(request, 'Pembayaran Berhasil!')
                    else:
                        messages.error(request, 'Saldo tidak mencukupi.')
                except (IndexError, ValueError):
                    messages.error(request, 'Pesanan jasa tidak valid.')
            else:
                messages.error(request, 'MEMBAYAR TRANSAKSI tidak tersedia untuk Pekerja.')

        elif kategori == 'TRANSFER MYPAY':
            no_hp_tujuan = request.POST.get('no_hp')
            nominal_transfer = int(request.POST.get('nominal_transfer', 0))
            if Worker.objects.filter(phone=no_hp_tujuan).exists():
                worker = Worker.objects.get(phone=no_hp_tujuan)
                worker.saldo += nominal_transfer
                worker.save()

                user = User.objects.get(phone=request.session["user_phone"])
                if nominal_transfer > 0 and user.saldo >= nominal_transfer:
                    user.saldo -= nominal_transfer
                    user.save()
                    user = User.objects.get(phone=request.session['user_phone'])  # Atau gunakan ID jika lebih spesifik

                    # Buat instance transaksi
                    transaction = Transaction(
                        user=user,
                        category="TRANSFER MYPAY",
                        amount=nominal_transfer
                    )

                    # Simpan transaksi ke database
                    transaction.save()
                    messages.success(request, 'Transfer Berhasil!')
                else:
                    messages.error(request, 'Jumlah transfer tidak valid atau saldo tidak mencukupi.')
            else:
                messages.error(request, 'Nomor pekerja tidak ada.')

        elif kategori == 'WITHDRAWAL':
           
            nama_bank = request.POST.get('nama_bank')
            no_rekening = request.POST.get('no_rekening')
            nominal_withdrawal = int(request.POST.get('nominal_withdrawal', 0))
            user = User.objects.get(phone=request.session["user_phone"])
            if nominal_withdrawal > 0 and user.saldo >= nominal_withdrawal:
                user.saldo -= nominal_withdrawal
                user.save()
                user = User.objects.get(phone=request.session['user_phone'])  # Atau gunakan ID jika lebih spesifik

                # Buat instance transaksi
                transaction = Transaction(
                    user=user,
                    category="WITHDRAWAL",
                    amount=nominal_withdrawal
                )

                # Simpan transaksi ke database
                transaction.save()
                messages.success(request, 'Withdrawal Berhasil!')
            else:
                messages.error(request, 'Jumlah withdrawal tidak valid atau saldo tidak mencukupi.')

        else:
            messages.error(request, 'Kategori transaksi tidak valid.')

        return redirect('my_app')

    # Data dummy untuk form
    pengguna = None

    if User.objects.filter(phone=request.session['user_phone']).exists():
        pengguna = User.objects.get(phone=request.session['user_phone'])

    print(pengguna.name)

    dummy_form = {
        'nama_user': pengguna.name,
        'tanggal_transaksi': datetime.datetime.now().strftime('%Y-%m-%d'),
        'saldo_user': f"Rp {pengguna.saldo:,}".replace(',', '.'),
    }

    # Tentukan kategori transaksi dan pilih template berdasarkan user_type
    if user_type == 'User':
        dummy_form['kategori_transaksi'] = ['TOP UP MY PAY', 'MEMBAYAR TRANSAKSI', 'TRANSFER MYPAY', 'WITHDRAWAL']
        template_name = 'user/transaksi.html'
    else:  # Pekerja
        dummy_form['kategori_transaksi'] = ['TOP UP MY PAY', 'TRANSFER MYPAY', 'WITHDRAWAL']
        template_name = 'feat_4_red/transaksi_mypay_pekerja.html'

    return render(request, template_name, {'form': dummy_form, 'user_type': user_type, 'orders': orders})


def get_user_pending_orders(request):
    try:
        user = User.objects.get(phone=request.session['user_phone'])
        orders = Order.objects.filter(user=user, status="AWAITING_PAYMENT")
        
        # Buat response berupa JSON
        orders_data = [
            {
                'id': order.id,
                'service': order.service.name,
                'status': order.status,
                'total_price': order.total_price,
                'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
            for order in orders
        ]
        
        return JsonResponse({'orders': orders_data})
    
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

def kelola_pesanan(request):
        
    try:
        user = User.objects.get(phone=request.session['user_phone'])
    except User.DoesNotExist:
        return render(request, 'error.html', {'message': 'User not found'})

    # Ambil semua order yang terkait dengan pengguna
    orders = Order.objects.filter(user=user)
    return render(request, 'user/kelola_pesanan.html', { 'orders': orders})

def view_pemesanan(request, id):
    service = Service.objects.get(id=id)
    if request.method == 'POST':
        service_id = request.POST.get("id")
        tanggal = request.POST.get("tanggal")
        amount = request.POST.get("amount")
        diskon = request.POST.get("diskon")
        print(request.session)
        try:
            user = User.objects.get(phone=request.session['user_phone'])
            service = Service.objects.get(id=service_id)
            print(service)
        except (User.DoesNotExist, Service.DoesNotExist) as e:
            return render(request, "error.html", {"message": str(e)})

        discount = None
        try:
            discount = Discount.objects.get(code=diskon)
        except (Discount.DoesNotExist) as e:
            pass
        
        if discount != None:
            order = Order(
                user=user,
                service=service,
                status="AWAITING_PAYMENT",
                discount=discount,
            )
        else:
            order = Order(
                user=user,
                service=service,
                status="AWAITING_PAYMENT",
            )

        order.total_price = amount

        # Simpan data ke database
        order.save()
    return render(request, 'user/pemesanan.html', { 'service': service })