from django import forms
from django.contrib.auth.models import User
from .models import MyUser 
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.bootstrap import TabHolder, Tab


"""class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    helper = FormHelper()
    helper.form_tag = False
    helper.layout = Layout(
		TabHolder(

			Tab(
				'User info',
				'username',
				'email',
				'password'
			)
		)
	)	
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):

    helper = FormHelper()
    helper.form_tag = False
    helper.layout = Layout(
        TabHolder(

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
            )

        )
    )

    class Meta:
        model = UserProfile
        fields = ('website', 'picture', 'info', 'age', 'gender', 'hobbies', 'height', 'weight', 'birthday')"""



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
            )

        )
    )

    class Meta:
        model = MyUser
        fields = ('first_name', 'last_name', 'email', 'password',
		  'website', 'picture', 'info', 'age', 
		  'gender', 'hobbies', 'height', 'weight',
                  'birthday')
