from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from auth_.models import MainUser


class MainUserCreationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(MainUserCreationForm, self).__init__(*args, **kwargs)
        # If one field gets autocompleted but not the other, our 'neither
        # password or both password' validation will be triggered.
        self.fields['password1'].widget.attrs['autocomplete'] = 'off'
        self.fields['password2'].widget.attrs['autocomplete'] = 'off'

    class Meta(UserCreationForm.Meta):
        model = MainUser
        fields = '__all__'


class MainUserChangeForm(UserChangeForm):

    def __init__(self, *args, **kwargs):
        super(MainUserChangeForm, self).__init__(*args, **kwargs)

    class Meta(UserChangeForm.Meta):
        model = MainUser
        fields = '__all__'
