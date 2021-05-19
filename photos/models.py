from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class Photo(models.Model):
    image = models.ImageField(upload_to='photo/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'PHOTO of '+str(self.user.id)
