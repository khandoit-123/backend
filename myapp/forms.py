from django.contrib.auth.forms import UserCreationForm
from .models import User
class UserProfileForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for fieldname in ["username", "password1", "password2"]:
            self.fields[fieldname].help_text = None