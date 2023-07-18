from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator

# Create your models here.
STATE_CHOICES= (
('Dhaka,Bangladesh' , 'Dhaka Bangladesh'),
('Banani,Bangladesh' , 'Banani Bangladesh'),
('Jatrabari,Bangladesh' , 'Jatrabari Bangladesh'),
('Motijheel,Bangladesh' , 'Motijheel Bangladesh'),
('Mohammadpur,Bangladesh' , 'Mohammadpur Bangladesh'),
('Gulshan,Bangladesh' , 'Gulshan Bangladesh'),
('Badda,Bangladesh' , 'Badda Bangladesh'),
('Khilgaon,Bangladesh' , 'Khilgaon Bangladesh'),
('Tejgaon,Bangladesh' , 'Tejgaon Bangladesh'),
('Rampura,Bangladesh' , 'Rampura Bangladesh'),
('Banasree,Bangladesh' , 'Banasree Bangladesh'),
('Malibagh,Bangladesh' , 'Malibagh Bangladesh'),
('Mouchak,Bangladesh' , 'Mouchak Bangladesh'),
('Shahbag,Bangladesh' , 'Shahbag Bangladesh'),
('Paltan,Bangladesh' , 'Paltan Bangladesh'),
('Mohakhali,Bangladesh' , 'Mohakhali Bangladesh'),
('Mirpur,Bangladesh' , 'Mirpur Bangladesh'),
('Kalabagan,Bangladesh' , 'Kalabagan Bangladesh'),
('Kathalbagan,Bangladesh' , 'Kathalbagan Bangladesh'),
('Dhanmandi,Bangladesh' , 'Dhanmandi Bangladesh'),
('Uttara,Bangladesh' , 'Uttara Bangladesh'),
('Azimpur,Bangladesh' , 'Azimpur Bangladesh'),
('Aminbazar,Bangladesh' , 'Aminbazar Bangladesh'),
('Nikunja,Bangladesh' , 'Nikunja Bangladesh'),
('Wari,Bangladesh' , 'Wari Bangladesh'),
('Shyamoli,Bangladesh' , 'Shyamoli Bangladesh'),
('Lalmatia,Bangladesh' , 'Lalmatia Bangladesh'),
('Gabtoli,Bangladesh' , 'Gabtoli Bangladesh'),
('Khilkhet,Bangladesh' , 'Khilkhet Bangladesh'),
('Demra,Bangladesh' , 'Demra Bangladesh'),
('Bashabo,Bangladesh' , 'Bashabo Bangladesh'),
('Bailyroad,Bangladesh' , 'Bailyroad Bangladesh'),
('Zigatola,Bangladesh' , 'Zigatola Bangladesh'),
('Modhubag,Bangladesh' , 'Modhubag Bangladesh'),
('Mugda,Bangladesh' , 'Mugda Bangladesh'),

)

class Customer(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    locality=models.CharField(max_length=200)
    city=models.CharField(max_length=50)
    zipcode=models.IntegerField()
    state=models.CharField(choices=STATE_CHOICES, max_length=50)
    
    def _str_ (self):
     return str(self.id)

CATEGORY_CHOICES=(
    ('L','Luxury'),
    ('CD','Cheap Deals'),
    ('C','Car Rentals'),
    ('B','Bike Rentals'),
    ('P','Popular Attractions'),
)
class Product(models.Model):
    title=models.CharField(max_length=100)
    selling_price=models.FloatField()
    discounted_price=models.TextField()
    description=models.TextField()
    ratings=models.CharField(max_length=100)
    category=models.CharField(choices=CATEGORY_CHOICES,max_length=3)
    product_image=models.ImageField(upload_to='productimg')
    
    
    def _str_ (self):
         return str(self.id)
     


class Cart(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.PositiveBigIntegerField(default=1)
    
    def _str_ (self):
         return str(self.id)
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

STATUS_CHOICES=(
    ('Confirmed','Confirmed'),
    ('Cancel','Cancel'),
)

class BookingsPlaced(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveBigIntegerField(default=1)
    confirmation_date=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=50,choices=STATUS_CHOICES,default='Pending')
    
    @property
    def total_cost(self):
         return self.quantity * self.product.discounted_price
    