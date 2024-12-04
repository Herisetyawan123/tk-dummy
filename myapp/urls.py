from django.urls import path
from .views import choose_role, register_user, register_worker, login, home_user, home_worker, logout, landing, profile, subkategori, daftar_diskon, my_pay, kelola_pesanan, transaksi_mypay_view, view_pemesanan, get_user_pending_orders

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

    # jenis pekerjaan
    path('home/subkategori/<str:subcategory_id>/', subkategori, name='sub_category'),

    # worker
    path('home/worker/', home_worker, name='home_worker'),
    path('logout/', logout, name='logout'),
]