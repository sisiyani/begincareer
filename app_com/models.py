from django.db import models

# Create your models here.
class Appointment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    date = models.DateField()
    time_slot = models.TimeField()
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.date} {self.time_slot}"

class Contact(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom / Prénom")
    phone = models.CharField(max_length=15, verbose_name="Téléphone")
    email = models.EmailField(verbose_name="E-mail")
    budget = models.CharField(max_length=50, blank=True, null=True, verbose_name="Budget estimé")
    message = models.TextField(verbose_name="Message")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date d'envoi")

    def __str__(self):
        return f"{self.name} - {self.phone} - {self.email} - {self.budget} - {self.message}"