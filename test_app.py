import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_dress.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from dress_app.models import StudentDressEntry, StandardPrice

def run_tests():
    c = Client()
    print("Testing unauthenticated access redirect...")
    resp = c.get('/')
    assert resp.status_code == 302, f"Expected 302, got {resp.status_code}"
    print("Unauthenticated redirect OK ->", resp.url)

    print("\nTesting Login page...")
    resp = c.get('/login/')
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
    print("Login page renders OK")

    # 1. Test Admin: vatsal
    print("\nTesting Admin Authentication: vatsal / jayshreekrishna...")
    logged_in = c.login(username='vatsal', password='jayshreekrishna')
    assert logged_in, "Failed to login vatsal"
    print("Admin vatsal logged in successfully!")

    resp = c.get('/')
    assert resp.status_code == 200
    assert "Student Dress Entry" in resp.content.decode('utf-8')
    print("Admin vatsal can access Entry page")

    resp = c.get('/pricing/')
    assert resp.status_code == 200
    print("Admin vatsal can access Pricing page")

    c.logout()

    # 2. Test Admin: sunilbhai
    print("\nTesting Admin Authentication: sunilbhai / jayshreekrishna...")
    logged_in = c.login(username='sunilbhai', password='jayshreekrishna')
    assert logged_in, "Failed to login sunilbhai"
    print("Admin sunilbhai logged in successfully!")

    resp = c.get('/')
    assert resp.status_code == 200
    print("Admin sunilbhai can access Entry page")

    c.logout()

    # 3. Test View-Only User: user1
    print("\nTesting View-Only User: user1 / jayshreeram...")
    logged_in = c.login(username='user1', password='jayshreeram')
    assert logged_in, "Failed to login user1"
    print("User user1 logged in successfully!")

    # user1 accessing viewer page
    resp = c.get('/viewer/')
    assert resp.status_code == 200
    content = resp.content.decode('utf-8')
    assert "School Dress Order Sheet" in content
    assert "New Student Entry" not in content  # Button hidden for user1
    assert "btn-delete" not in content  # Delete button hidden for user1
    print("user1 can view Excel Viewer without entry/edit/delete actions")

    # user1 trying to access entry page
    resp = c.get('/', follow=True)
    assert "Access restricted: View-only users cannot add student records" in resp.content.decode('utf-8')
    print("user1 blocked from Entry page (Redirected to viewer with error)")

    # user1 trying to access pricing page
    resp = c.get('/pricing/', follow=True)
    assert "Access restricted: View-only users cannot modify pricing" in resp.content.decode('utf-8')
    print("user1 blocked from Pricing page (Redirected to viewer with error)")

    # user1 trying to edit or delete
    entry = StudentDressEntry.objects.first()
    if entry:
        resp = c.get(f'/entry/edit/{entry.pk}/', follow=True)
        assert "Access restricted: View-only users cannot edit student records" in resp.content.decode('utf-8')
        print("user1 blocked from editing entries")

        resp = c.post(f'/entry/delete/{entry.pk}/', follow=True)
        assert "Access restricted: View-only users cannot delete records" in resp.content.decode('utf-8')
        print("user1 blocked from deleting entries")

    # 4. Test PDF & Excel Export for user1
    print("\nTesting PDF Export for user1 (Without measurements)...")
    resp = c.get('/export/pdf/?section=PRIMARY')
    assert resp.status_code == 200
    assert resp['Content-Type'] == 'application/pdf'
    assert len(resp.content) > 500
    print(f"PDF Export generated OK (Size: {len(resp.content)} bytes)")

    print("\nTesting Excel Export for user1 (Without measurements)...")
    resp = c.get('/export/excel/?section=PRIMARY')
    assert resp.status_code == 200
    assert 'spreadsheetml' in resp['Content-Type']
    assert len(resp.content) > 500
    print(f"Excel Export generated OK (Size: {len(resp.content)} bytes)")

    print("\nALL ROLE PERMISSIONS AND VIEW-ONLY TESTS PASSED SUCCESSFULLY!")

if __name__ == '__main__':
    run_tests()
