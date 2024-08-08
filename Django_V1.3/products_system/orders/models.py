from django.db import models
from products.models import Product

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('disapproved', 'Disapproved')
    ], default='pending')

    def __str__(self):
        return f"M-{str(self.id).zfill(3)}"  # Custom order number format

    def save(self, *args, **kwargs):
        if not self.id:
            saved = False
            while not saved:
                super(Order, self).save(*args, **kwargs)
                self.id = self.id  # Ensure order number is set after saving
                saved = True
        super(Order, self).save(*args, **kwargs)