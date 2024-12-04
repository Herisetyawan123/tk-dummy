from django.urls import path
from .views import choose_role, register_user, register_worker, login, home_user, home_worker, logout, landing, profile, subkategori, daftar_diskon, my_pay, kelola_pesanan, transaksi_mypay_view, view_pemesanan, get_user_pending_orders, beli_diskon
from .views import choose_role, get_subkategori, register_user, register_worker, login, home_user, home_worker, logout, landing, profile, subkategori, daftar_diskon, my_pay, kelola_pesanan, transaksi_mypay_view, view_pemesanan, get_user_pending_orders, kelola_pekerjaan_worker, get_subkategori, kelola_status_pekerjaan, profile_worker

urlpatterns = [
    path('', landing, name='landing'),
    path('register/user/', register_user, name='register_user'),
    path('register/worker/', register_worker, name='register_worker'),
    path('login/', login, name='login'),
    path('choose_role/', choose_role, name='choose_role'),
    
    path('home/profile/', profile, name='profile'),
    # user
    path('home/user/', home_user, name='home_user'),
    path('home/myapp/', my_pay, name='my_app'),
    path('home/transaksi-user-mypay/', transaksi_mypay_view, name='transaksi_user_mypay'),
    path('home/pemesanan/<str:id>', view_pemesanan, name='pesanan'),
    path('user/pending-orders', get_user_pending_orders, name='api_pesanan'),
    path('home/kelola-pesanan/', kelola_pesanan, name='kelola_pesanan'),
    path('home/daftar-diskon/', daftar_diskon, name='daftar_diskon'),
    path('home/beli-diskon/<str:diskon_id>', beli_diskon, name='beli_diskon'),

    # jenis pekerjaan
    path('home/subkategori/<str:subcategory_id>/', subkategori, name='sub_category'),
    path('worker/mypay', my_app, name="my_pay_worker")

    # worker
    path('home/worker/', home_worker, name='home_worker'),
    path('home/worker/kelola-pekerjaan', kelola_pekerjaan_worker, name='kelola_pekerjaan_worker'),
    path('home/worker/kelola-status-pekerjaan', kelola_status_pekerjaan, name='kelola_status_pekerjaan'),
    path('api/subkategori/<str:kategori_id>', get_subkategori, name='get_subkategori'),
    path('home/worker/profile', profile_worker, name='worker_profile'),
    path('logout/', logout, name='logout'),
]