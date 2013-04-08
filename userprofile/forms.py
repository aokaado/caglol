# -*- coding: utf-8 -*-

from django import forms

from studlan.userprofile.models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('username', 'date_of_birth', 'city',)
