# -*- coding: utf-8 -*-

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, ButtonHolder
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

class LoginForm(forms.Form):
    sps = forms.ChoiceField(
        label=u'Kirjautumispalvelu', 
        help_text=u'Muutamia yleisimpiä kirjautumispalvelimia.')
    openid_identifier = forms.URLField(
        widget=forms.TextInput(), 
        max_length=255, 
        required=True, 
        label=u'Osoite', 
        help_text=u'Kirjautumispalvelun osoite. Voit joko valita ylläolevasta valikosta tunnetun, tai käyttää omaasi.')
    next = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        # Init
        self.next = kwargs.pop('next', "")
        super(LoginForm, self).__init__(*args, **kwargs)
        
        # Build form
        self.helper = FormHelper()
        self.helper.form_action = reverse('openid-login')
        self.helper.layout = Layout(
            Fieldset(
                u'',
                'sps',
                'openid_identifier',
                'next',
                ButtonHolder (
                    Submit('submit-login', u'Kirjaudu')
                )
            )
        )
        
        # Initial values
        self.fields['next'].initial = self.next
        self.fields['sps'].choices = [
            ('https://www.google.com/accounts/o8/id', 'Google'),
            ('https://korppi.jyu.fi/openid/', 'Korppi'),
            ('https://me.yahoo.com', 'Yahoo'),
        ]
        self.fields['sps'].initial = 0
        self.fields['openid_identifier'].initial = 'https://www.google.com/accounts/o8/id'

class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                u'',
                'first_name',
                'last_name',
                'email',
                ButtonHolder (
                    Submit('submit', u'Tallenna')
                )
            )
        )
        
    class Meta:
        model = User
        fields = ('first_name','last_name','email')
