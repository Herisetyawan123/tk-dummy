from django.core.management.base import BaseCommand
from myapp.models import JobCategory, SubJobCategory, Service, User, Worker, Discount  # Ganti `myapp` dengan nama aplikasi Anda
from datetime import  datetime
import random
from decimal import Decimal

def run():
    # Data untuk di-seed
    categories_data = [
        {
            'name': 'IT',
            'subcategories': [
                {
                    'name': 'Desain Grafis',
                    'services': [
                        {'name': 'Desain Logo', 'description': 'Membuat logo profesional', 'amount': 150000},
                        {'name': 'Desain Poster', 'description': 'Membuat poster kreatif', 'amount': 150000},
                    ]
                },
                {
                    'name': 'Pengembangan Web',
                    'services': [
                        {'name': 'Frontend Development', 'description': 'Pengembangan tampilan depan website', 'amount': 150000},
                        {'name': 'Backend Development', 'description': 'Pengembangan server dan database', 'amount': 150000},
                    ]
                },
                {
                    'name': 'Data Science',
                    'services': [
                        {'name': 'Analisis Data', 'description': 'Menganalisis data untuk mengambil keputusan', 'amount': 150000},
                        {'name': 'Machine Learning', 'description': 'Membangun model machine learning', 'amount': 150000},
                    ]
                },
            ]
        },
        {
            'name': 'Kesehatan',
            'subcategories': [
                {
                    'name': 'Dokter Umum',
                    'services': [
                        {'name': 'Pemeriksaan Kesehatan', 'description': 'Pemeriksaan kesehatan umum', 'amount': 150000},
                        {'name': 'Rujukan Spesialis', 'description': 'Memberikan rujukan ke dokter spesialis', 'amount': 150000},
                    ]
                },
                {
                    'name': 'Perawat',
                    'services': [
                        {'name': 'Perawatan Pasien', 'description': 'Memberikan perawatan kepada pasien', 'amount': 150000},
                        {'name': 'Pemberian Obat', 'description': 'Memberikan obat sesuai resep', 'amount': 150000},
                    ]
                },
                {
                    'name': 'Fisioterapi',
                    'services': [
                        {'name': 'Rehabilitasi Fisik', 'description': 'Membantu pemulihan fisik pasien', 'amount': 150000},
                        {'name': 'Latihan Fisioterapi', 'description': 'Memberikan latihan untuk pasien', 'amount': 150000},
                    ]
                },
            ]
        },
        {
            'name': 'Konstruksi',
            'subcategories': [
                {
                    'name': 'Arsitek',
                    'services': [
                        {'name': 'Desain Bangunan', 'description': 'Merancang bangunan yang fungsional', 'amount': 150000},
                        {'name': 'Konsultasi Arsitektur', 'description': 'Memberikan konsultasi desain bangunan', 'amount': 150000},
                    ]
                },
                {
                    'name': 'Kontraktor',
                    'services': [
                        {'name': 'Pembangunan Gedung', 'description': 'Membangun gedung dari awal', 'amount': 150000},
                        {'name': 'Renovasi Bangunan', 'description': 'Melakukan renovasi bangunan', 'amount': 150000},
                    ]
                },
                {
                    'name': 'Insinyur Sipil',
                    'services': [
                        {'name': 'Perencanaan Konstruksi', 'description': 'Merencanakan proyek konstruksi', 'amount': 150000},
                        {'name': 'Pengawasan Konstruksi', 'description': 'Mengawasi proses konstruksi', 'amount': 150000},
                    ]
                },
            ]
        },
    ]

    user = {
        'name': 'Heri Setyawan',
        'password':  '083853797950',
        # 'gender':  'L',
        'phone':  '083853797950',
        'saldo': 1000000, 
        'address': 'Jln Rengganis'
    }    


    worker = {
        'name': 'Developer Setyawan',
        'password':  '083853797951',
        'gender':  'L',
        'phone':  '083853797951',
        'dob':  datetime.now(),
        'saldo': 1000000, 
        'address': 'Jln Rengganis',
        'account_number': '083853797951',
        'bank_name': 'BRI',
        'photo_url': 'htttp://example.com',
    }

    promo_codes = ['PROMO2024', 'SALE50', 'NEWYEAR10', 'DISCOUNT30', 'BLACKFRIDAY15']

    for promo_code in promo_codes:  # Menghasilkan 10 data diskon sebagai contoh
        code = promo_code
        percentage = random.randint(5, 50)  # Diskon antara 5% hingga 50%
        min_transaction = 150000  # Minimal transaksi antara 50 hingga 500
        max_usage = random.randint(1, 100)  # Maksimum penggunaan antara 1 hingga 100
        usage_quota = random.randint(0, max_usage)  # Kuota penggunaan diskon
        voucher_price = Decimal(random.randint(50000, 100000))  # Harga voucher antara 50,000 hingga 100,000

        # Buat dan simpan objek Discount
        discount = Discount.objects.create(
            code=code,
            percentage=Decimal(percentage),
            min_transaction=min_transaction,
            max_usage=max_usage,
            usage_quota=usage_quota,
            voucher_price=voucher_price
        )


    User.objects.create(
        name=user['name'],
        password=user['password'],
        # gender=user['gender'],
        phone=user['phone'],
        saldo=user['saldo'],
        address=user['address'],
    )

    Worker.objects.create(
        name=worker['name'],
        password=worker['password'],
        gender=worker['gender'],
        phone=worker['phone'],
        saldo=worker['saldo'],
        address=worker['address'],
        dob=worker['dob'],
        account_number=worker['account_number'],
        bank_name=worker['bank_name'],
        photo_url=worker['photo_url'],
    )


    # Menyimpan data ke dalam database
    for category_data in categories_data:
        category = JobCategory.objects.create(name=category_data['name'])
        for subcategory_data in category_data['subcategories']:
            subcategory = SubJobCategory.objects.create(
                category=category,
                name=subcategory_data['name']
            )
            for service_data in subcategory_data['services']:
                Service.objects.create(
                    sub_category=subcategory,
                    name=service_data['name'],
                    description=service_data['description'],
                    amount=service_data['amount']
                )

    print("data success di seeder")
