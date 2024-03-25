from django.db import models

class Store(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=50)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    count = models.IntegerField()
    price = models.IntegerField()
    image = models.ImageField(blank=True, upload_to='item_images/')

    def __str__(self):
        return self.name