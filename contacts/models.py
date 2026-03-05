from django.db import models

class Contact(models.Model):

    CATEGORY_CHOICES = [
        ('Friends', 'Friends'),
        ('Work', 'Work'),
        ('Family', 'Family'),
        ('Other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='Other'
    )
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

