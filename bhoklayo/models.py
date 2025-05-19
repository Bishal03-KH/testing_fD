from django.db import models 

class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self): return self.name

class MenuItem(models.Model):
    name        = models.CharField(max_length=100)
    description = models.TextField()
    image       = models.ImageField(upload_to='menu_images/', blank=True, null=True)
    price       = models.DecimalField(max_digits=6, decimal_places=2)
    category    = models.ForeignKey(Category, on_delete=models.CASCADE)
    def __str__(self): return self.name

class Order(models.Model):
    items      = models.ManyToManyField(MenuItem)
    name       = models.CharField(max_length=50)
    email      = models.EmailField()
    address    = models.TextField()
    city       = models.CharField(max_length=50)
    zip_code   = models.CharField(max_length=10)
    is_paid    = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f'Order {self.id}'
