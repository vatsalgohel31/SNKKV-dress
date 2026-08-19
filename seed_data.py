import os
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_dress.settings')
django.setup()

from django.contrib.auth.models import User
from dress_app.models import StandardPrice, StudentDressEntry

def seed():
    print("Setting up Admin Superusers (vatsal, sunilbhai)...")
    admin_users = [
        ('vatsal', 'vatsal@example.com', 'jayshreekrishna'),
        ('sunilbhai', 'sunilbhai@example.com', 'jayshreekrishna'),
        ('admin', 'admin@example.com', 'admin123'),
    ]
    for username, email, pwd in admin_users:
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, email, pwd)
            print(f"Admin user created ({username} / {pwd})")
        else:
            u = User.objects.get(username=username)
            u.set_password(pwd)
            u.is_staff = True
            u.is_superuser = True
            u.save()
            print(f"Admin user updated ({username} / {pwd})")

    print("\nSetting up View-Only User (user1)...")
    if not User.objects.filter(username='user1').exists():
        u1 = User.objects.create_user('user1', 'user1@example.com', 'jayshreeram')
        u1.is_staff = False
        u1.is_superuser = False
        u1.save()
        print("View-only user created (user1 / jayshreeram)")
    else:
        u1 = User.objects.get(username='user1')
        u1.set_password('jayshreeram')
        u1.is_staff = False
        u1.is_superuser = False
        u1.save()
        print("View-only user updated (user1 / jayshreeram)")


    print("\nSeeding Standard-wise Pricing (Std 1 - 12)...")
    # Tiered pricing for school standards
    pricing_matrix = {
        1: (300, 260, 100, 80),
        2: (320, 280, 100, 80),
        3: (340, 300, 110, 90),
        4: (360, 320, 110, 90),
        5: (380, 340, 120, 100),
        6: (400, 360, 120, 100),
        7: (420, 380, 130, 110),
        8: (450, 400, 130, 110),
        9: (480, 430, 140, 120),
        10: (500, 450, 140, 120),
        11: (540, 480, 150, 130),
        12: (580, 520, 150, 130),
    }

    for std, (d, ed, dup, edup) in pricing_matrix.items():
        sp, created = StandardPrice.objects.update_or_create(
            standard=std,
            defaults={
                'dress_price': Decimal(str(d)),
                'extra_dress_price': Decimal(str(ed)),
                'dupatta_price': Decimal(str(dup)),
                'extra_dupatta_price': Decimal(str(edup)),
            }
        )
        status = "Created" if created else "Updated"
        print(f"[{status}] Std {std}: Dress=Rs.{d}, Extra=Rs.{ed}, Dupatta=Rs.{dup}, Extra Dup=Rs.{edup}")

    print("\nSeeding Sample Student Dress Entries...")
    sample_students = [
        # (Name, Std, Medium, has_dress, has_dupatta, has_extra_dress, has_extra_dupatta, notes)
        ("Aarav Rajesh Patel", 1, "GUJARATI", True, False, False, False, "Chest: 22, Length: 24"),
        ("Diya Mukesh Shah", 2, "GUJARATI", True, True, False, False, "Length: 26, Dupatta: White"),
        ("Krish Hardik Mehta", 3, "ENGLISH", True, False, True, False, "2 Dresses set, Chest: 25"),
        ("Ananya Bhavin Joshi", 4, "ENGLISH", True, True, True, True, "Full Set (2 Dress + 2 Dupatta)"),
        ("Dev Sanjay Parmar", 5, "GUJARATI", True, False, False, False, "Standard 1 Dress"),
        ("Pooja Dinesh Solanki", 6, "GUJARATI", True, True, False, False, "Dupatta Color: Navy Blue"),
        ("Rohan Kirit Rathod", 7, "ENGLISH", True, False, True, False, "Length: 34, Waist: 28"),
        ("Khushi Jignesh Trivedi", 8, "GUJARATI", True, True, True, True, "Full Set with extra dupatta"),
        ("Kavya Nilesh Dave", 9, "GUJARATI", True, True, False, False, "Std 9 Gujarati Medium"),
        ("Harsh Jayesh Vaghela", 10, "ENGLISH", True, False, True, False, "Std 10 English Medium"),
        ("Tanvi Kamlesh Prajapati", 11, "GUJARATI", True, True, True, True, "Complete Uniform Set"),
        ("Yash Arvindbhai Chauhan", 12, "ENGLISH", True, False, False, False, "Standard Final Year Dress"),
    ]

    if StudentDressEntry.objects.count() == 0:
        for name, std, med, hd, hdup, hed, hedup, notes in sample_students:
            entry = StudentDressEntry(
                name=name,
                standard=std,
                medium=med,
                has_dress=hd,
                has_dupatta=hdup,
                has_extra_dress=hed,
                has_extra_dupatta=hedup,
                notes=notes
            )
            entry.total_price = entry.compute_price_from_standard()
            entry.save()
            print(f"Created student record: {name} (Std {std} - {med}) => Rs.{entry.total_price}")
    else:
        print(f"Existing {StudentDressEntry.objects.count()} student records found.")

    print("\nSeed completed successfully!")

if __name__ == '__main__':
    seed()
