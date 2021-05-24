from django.db import models
from django.contrib.auth import get_user_model
from matir_bank.core.upload_path_maker import upload_path_maker
User = get_user_model()



def image_upload_path(instance, filename):
    return upload_path_maker('photo', instance, filename)


class Photo(models.Model):
    image = models.ImageField(upload_to=image_upload_path)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'PHOTO of '+str(self.user.id)
