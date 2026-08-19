from django.db import models
from decimal import Decimal

STANDARD_CHOICES = [(i, f"Std {i}") for i in range(1, 13)]

MEDIUM_CHOICES = [
    ('GUJARATI', 'Gujarati'),
    ('ENGLISH', 'English'),
]

PACKAGE_CHOICES = [
    ('1_DRESS', '1 Dress'),
    ('1_DRESS_1_DUPATTA', '1 Dress + 1 Dupatta'),
    ('1_DRESS_1_EXTRA_1_DUPATTA', '1 Dress + 1 Extra Dress + 1 Dupatta'),
    ('1_DRESS_1_EXTRA_1_DUPATTA_1_EXTRA', '1 Dress + 1 Extra Dress + 1 Dupatta + 1 Extra Dupatta'),
    ('CUSTOM', 'Custom Selection'),
]

SECTION_CHOICES = [
    ('PRIMARY', 'Primary (Std 1 to 8)'),
    ('SECONDARY', 'Secondary (Std 9, 10)'),
    ('HIGHER_SECONDARY', 'Higher Secondary (Std 11, 12)'),
]



class StandardPrice(models.Model):
    standard = models.IntegerField(choices=STANDARD_CHOICES, unique=True, verbose_name="Standard (Std)")
    dress_price = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'), verbose_name="1 Dress Price (₹)")
    extra_dress_price = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'), verbose_name="1 Extra Dress Price (₹)")
    dupatta_price = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'), verbose_name="1 Dupatta Price (₹)")
    extra_dupatta_price = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'), verbose_name="1 Extra Dupatta Price (₹)")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['standard']
        verbose_name = "Standard Price"
        verbose_name_plural = "Standard Prices"

    def __str__(self):
        return f"Std {self.standard} - Dress: ₹{self.dress_price}, Extra: ₹{self.extra_dress_price}, Dupatta: ₹{self.dupatta_price}, Extra Dup: ₹{self.extra_dupatta_price}"

    def calculate_total(self, has_dress=True, has_extra_dress=False, has_dupatta=False, has_extra_dupatta=False):
        total = Decimal('0.00')
        if has_dress:
            total += self.dress_price
        if has_extra_dress:
            total += self.extra_dress_price
        if has_dupatta:
            total += self.dupatta_price
        if has_extra_dupatta:
            total += self.extra_dupatta_price
        return total


class StudentDressEntry(models.Model):
    name = models.CharField(max_length=150, verbose_name="Student Name")
    standard = models.IntegerField(choices=STANDARD_CHOICES, default=1, verbose_name="Standard")
    medium = models.CharField(max_length=20, choices=MEDIUM_CHOICES, default='GUJARATI', verbose_name="Medium")
    package_model = models.CharField(max_length=50, choices=PACKAGE_CHOICES, default='1_DRESS', verbose_name="Dress Model / Package")
    
    # Specific items selection
    has_dress = models.BooleanField(default=True, verbose_name="1 Dress")
    has_extra_dress = models.BooleanField(default=False, verbose_name="1 Extra Dress")
    has_dupatta = models.BooleanField(default=False, verbose_name="1 Dupatta")
    has_extra_dupatta = models.BooleanField(default=False, verbose_name="1 Extra Dupatta")
    
    dress_qty = models.PositiveIntegerField(default=1, verbose_name="Dress Quantity")
    dupatta_qty = models.PositiveIntegerField(default=0, verbose_name="Dupatta Quantity")
    
    notes = models.TextField(blank=True, default='', verbose_name="Measurements / Remarks")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), verbose_name="Total Price (₹)")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date Added")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Updated")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Student Dress Entry"
        verbose_name_plural = "Student Dress Entries"

    def __str__(self):
        return f"{self.name} - Std {self.standard} ({self.get_medium_display()}) - ₹{self.total_price}"

    @property
    def section_name(self):
        if 1 <= self.standard <= 8:
            return "Primary"
        elif 9 <= self.standard <= 10:
            return "Secondary"
        elif 11 <= self.standard <= 12:
            return "Higher Secondary"
        return ""

    @property
    def section_badge_class(self):
        if 1 <= self.standard <= 8:
            return "badge-primary-sec"
        elif 9 <= self.standard <= 10:
            return "badge-secondary-sec"
        elif 11 <= self.standard <= 12:
            return "badge-higher-sec"
        return "badge-secondary"


    def sync_quantities_and_package(self):
        """Derives counts and package name from boolean flags."""
        d_qty = 0
        if self.has_dress:
            d_qty += 1
        if self.has_extra_dress:
            d_qty += 1
            
        dup_qty = 0
        if self.has_dupatta:
            dup_qty += 1
        if self.has_extra_dupatta:
            dup_qty += 1
            
        self.dress_qty = d_qty
        self.dupatta_qty = dup_qty

        # Detect package
        if self.has_dress and not self.has_extra_dress and not self.has_dupatta and not self.has_extra_dupatta:
            self.package_model = '1_DRESS'
        elif self.has_dress and not self.has_extra_dress and self.has_dupatta and not self.has_extra_dupatta:
            self.package_model = '1_DRESS_1_DUPATTA'
        elif self.has_dress and self.has_extra_dress and self.has_dupatta and not self.has_extra_dupatta:
            self.package_model = '1_DRESS_1_EXTRA_1_DUPATTA'
        elif self.has_dress and self.has_extra_dress and self.has_dupatta and self.has_extra_dupatta:
            self.package_model = '1_DRESS_1_EXTRA_1_DUPATTA_1_EXTRA'
        else:
            self.package_model = 'CUSTOM'

    def compute_price_from_standard(self):
        try:
            sp = StandardPrice.objects.get(standard=self.standard)
            return sp.calculate_total(
                has_dress=self.has_dress,
                has_extra_dress=self.has_extra_dress,
                has_dupatta=self.has_dupatta,
                has_extra_dupatta=self.has_extra_dupatta
            )
        except StandardPrice.DoesNotExist:
            return self.total_price or Decimal('0.00')

    def save(self, *args, **kwargs):
        self.sync_quantities_and_package()
        if not self.total_price or self.total_price == Decimal('0.00'):
            self.total_price = self.compute_price_from_standard()
        super().save(*args, **kwargs)
