from django import forms
from django.contrib.auth.models import User
from .models import MyUser 
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.bootstrap import TabHolder, Tab
from django.views.generic.edit import UpdateView






class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    helper = FormHelper()
    helper.form_tag = False
    helper.layout = Layout(
        TabHolder(
			Tab(
				'User info',
				'first_name',
				'last_name',
				'email',
				'password'
			),

            Tab(
				'General info',
				'age',
				'gender',
				'height',
				'weight',
				'birthday',
            ),

            Tab(
				'More',
				'website',
				'picture',
				'info',
				'hobbies',
				'address',
				'city',
				'postal',
				'fav_food',
				'fav_sport',
            )

        )
    )

    class Meta:
        model = MyUser
        fields = ('first_name', 'last_name', 'email', 'password',
		  'website', 'picture', 'info', 'age', 
		  'gender', 'hobbies', 'height', 'weight',
                  'birthday', 'address', 'city', 'postal', 'fav_food', 'fav_sport')


class UpdateUserForm(UpdateView):
    model = MyUser
    fields = ['first_name', 'last_name', 'email', 'password',
		  		'website', 'picture', 'info', 'age',
		  		'gender', 'hobbies', 'height', 'weight',
                'birthday', 'address', 'city', 'postal', 'fav_food', 'fav_sport']
    template_name_suffix = '_update_form'