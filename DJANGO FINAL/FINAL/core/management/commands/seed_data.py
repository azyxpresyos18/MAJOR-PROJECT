from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Client, Department, Product, Location, Schedule
from datetime import date, time

class Command(BaseCommand):
    help = 'Seed database with sample data'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@demopower.com', 'admin123')
            self.stdout.write('Created admin user: admin / admin123')

        c1, _ = Client.objects.get_or_create(name='Coca-Cola')
        c2, _ = Client.objects.get_or_create(name='Nivea')
        c3, _ = Client.objects.get_or_create(name='Monde')
        c4, _ = Client.objects.get_or_create(name='Century Pacific')
        c5, _ = Client.objects.get_or_create(name='BLK Cosmetics')

        d1, _ = Department.objects.get_or_create(name='Sales')
        d2, _ = Department.objects.get_or_create(name='Marketing')
        d3, _ = Department.objects.get_or_create(name='Operations')
        d4, _ = Department.objects.get_or_create(name='Logistics')

        p1, _ = Product.objects.get_or_create(client=c1, name='Coca-Cola 1.5L',      defaults={'category': 'Drinks'})
        p2, _ = Product.objects.get_or_create(client=c2, name='Nivea Face Wash',     defaults={'category': 'Face Products'})
        p3, _ = Product.objects.get_or_create(client=c2, name='Nivea Lotion',        defaults={'category': 'Body Care'})
        p4, _ = Product.objects.get_or_create(client=c3, name='Monde Butter Cookies',defaults={'category': 'Snacks'})
        p5, _ = Product.objects.get_or_create(client=c4, name='Century Tuna Classic',defaults={'category': 'Canned Goods'})
        p6, _ = Product.objects.get_or_create(client=c5, name='BLK Face Powder',     defaults={'category': 'Cosmetics'})

        l1, _ = Location.objects.get_or_create(name='Ayala Center Cebu',    defaults={'city':'Cebu City','address':'Cardinal Rosales Ave','open_hours':'10AM-9PM','is_available':True})
        l2, _ = Location.objects.get_or_create(name='SM City Cebu',         defaults={'city':'Cebu City','address':'North Reclamation Area','open_hours':'10AM-9PM','is_available':True})
        l3, _ = Location.objects.get_or_create(name='SM Seaside City',      defaults={'city':'Cebu City','address':'South Road Properties','open_hours':'10AM-9PM','is_available':False})
        l4, _ = Location.objects.get_or_create(name='Robinsons Galleria',   defaults={'city':'Cebu City','address':'Gen. Maxilom Ave','open_hours':'10AM-9PM','is_available':True})
        l5, _ = Location.objects.get_or_create(name='Gaisano Country Mall', defaults={'city':'Cebu City','address':'Gov. M. Cuenco Ave','open_hours':'9AM-8PM','is_available':True})

        admin = User.objects.get(username='admin')
        schedules = [
            dict(client=c2,product=p2,department=d2,location=l1,scheduled_date=date(2026,5,5), scheduled_time=time(15,30),quantity=200,assigned_to='Maria Santos', status='ongoing'),
            dict(client=c2,product=p3,department=d2,location=l2,scheduled_date=date(2026,4,28),scheduled_time=time(13,30),quantity=100,assigned_to='Pedro Reyes',  status='completed'),
            dict(client=c1,product=p1,department=d1,location=l4,scheduled_date=date(2026,5,10),scheduled_time=time(10,0), quantity=500,assigned_to='Juan Dela Cruz',status='confirmed'),
            dict(client=c3,product=p4,department=d3,location=l5,scheduled_date=date(2026,6,5), scheduled_time=time(9,0),  quantity=300,assigned_to='Ana Lim',      status='pending'),
            dict(client=c4,product=p5,department=d4,location=l3,scheduled_date=date(2026,5,15),scheduled_time=time(14,0), quantity=150,assigned_to='Carlo Cruz',   status='pending'),
        ]
        created = 0
        for s in schedules:
            obj, new = Schedule.objects.get_or_create(
                client=s['client'],product=s['product'],location=s['location'],
                scheduled_date=s['scheduled_date'],
                defaults={**s,'created_by':admin}
            )
            if new: created += 1

        self.stdout.write(self.style.SUCCESS(f'Done! 5 clients, 6 products, 5 locations, {created} new schedules.'))
