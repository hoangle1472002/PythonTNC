from django.db import models
from django.contrib.auth.models import User
class Users(models.Model):
    userid = models.AutoField(db_column='UserID', primary_key=True)  # Field name made lowercase.
    username = models.CharField(db_column='UserName', max_length=50)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=100)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=100)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'users'

class Customer(models.Model) :
    user  = models.OneToOneField(User,on_delete=models.CASCADE,null = True, blank=True)
    name = models.CharField(max_length=100,null = True)
    email = models.CharField(max_length=100,null= True)

    def __str__(self):
        return self.name
class Product(models.Model) :
    name = models.CharField(max_length=100,null = True)
    price = models.DecimalField(max_digits=7,decimal_places=2)
    digital = models.BooleanField(default=False,null=True,blank=False)
    image = models.ImageField(null = True, blank= True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try :
            url = self.image.url
        except :
            url = ''
        return url

class Order(models.Model) :
    customer = models.ForeignKey(Customer, on_delete= models.SET_NULL,blank=False,null = True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False,null = True,blank=False)
    transaction_id = models.CharField(max_length= 100, null = True)
    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderItems = self.orderitem_set.all()
        for i in orderItems:
            if i.product.digital == False :
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class OrderItem(models.Model) :
    product = models.ForeignKey(Product,on_delete = models.SET_NULL, blank = True, null = True)
    order   = models.ForeignKey(Order,on_delete= models.SET_NULL,blank= True, null = True)
    quantity = models.IntegerField(default= 0, null = True,blank= True)
    date_added = models.DateTimeField(auto_now_add= True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class ShippingAddress(models.Model) :
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order   = models.ForeignKey(Order,on_delete= models.SET_NULL,blank= True, null = True)
    address = models.CharField(max_length=100,null = True)
    city = models.CharField(max_length= 100, null= True)
    zipcode = models.CharField(max_length=100, null=True)
    date_added = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.address
