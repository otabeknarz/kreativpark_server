from django.db import models


class People(models.Model):
    ID = models.CharField(max_length=40, primary_key=True, unique=True)
    name = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    passport_data = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class QrCode(models.Model):
    class Types(models.TextChoices):
        IN = "IN", "Kirish"
        OUT = "OUT", "Chiqish"

    ID = models.CharField(primary_key=True, unique=True, max_length=40)
    people = models.OneToOneField(
        People, on_delete=models.CASCADE, related_name="qrcode"
    )
    image_path = models.CharField(max_length=1024)
    type = models.CharField(max_length=3, choices=Types.choices)
    purpose = models.CharField(max_length=1024, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.created} - {self.people.name}"


class Data(models.Model):
    class Types(models.TextChoices):
        IN = "IN", "Kirish"
        OUT = "OUT", "Chiqish"

    people = models.ForeignKey(People, on_delete=models.CASCADE, related_name="data")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    purpose = models.CharField(max_length=1024)
    type = models.CharField(max_length=3, choices=Types.choices)

    def __str__(self):
        return f"{self.people.name} - {self.purpose} - {self.created}"
