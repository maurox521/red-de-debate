# -*- coding: utf-8 -*-

from django import forms
from django.core.exceptions import ValidationError
from perfil.models import Profile, List, UsersList

class updateAlias(forms.ModelForm):
    error_css_class = 'has-error'
    user = forms.CharField(widget=forms.TextInput(
        attrs={
            'type': 'hidden',
        }))
    alias = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
        }))
    class Meta:
        model = Profile
        fields = ('user', 'alias')

class updateImage(forms.Form):
    img = forms.FileField(label='Añadir imagen', required=False,
        widget=forms.FileInput(
            attrs={'id': 'debImgForm'}
            ))

class newList(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        self.user = kwargs.pop('actual_user')
        super(newList,self).__init__(*args,**kwargs)
        if self.user:
            self.fields['owner_id'].widget=forms.TextInput(
                attrs={
                    'value': self.user,
                    'type': 'hidden',
                })
    name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Escribe un nombre...',
            'maxlength': 100,
        }))
    owner_id = forms.CharField(widget=forms.TextInput())
    class Meta:
        model = List
        fields = ('id','name', 'owner_id')

    def clean_name(self):
        name = self.cleaned_data.get('name')
        user = self['owner_id'].value()
        if List.objects.filter(name=name, owner_id=user).exists():
            raise forms.ValidationError(("Ya existe una lista con ese nombre"))
        return name

class selectUsers(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        self.usuarios = kwargs.pop('usuarios')
        self.list = kwargs.pop('list')
        super(selectUsers,self).__init__(*args,**kwargs)
        if self.usuarios:
            self.fields['user'].choices = [(x['object'], x['name']) for x in self.usuarios]
        if self.list:
            self.fields['list_id'].widget=forms.TextInput(
                attrs={
                    'value': self.list,
                    'type': 'hidden',
                })
    list_id = forms.CharField(widget=forms.TextInput())
    user = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(
            attrs={'id': 'usuarioListadoForm'}
        ),
        label="Usuarios")
    class Meta:
        model = UsersList
        fields = ('id', 'user', 'list_id')

class selectList(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        self.listas = kwargs.pop('listas')
        self.user = kwargs.pop('user')
        super(selectList,self).__init__(*args,**kwargs)
        if self.listas:
            self.fields['list_id'].choices = [(x['id'], x['name']) for x in self.listas]
        if self.user:
            self.fields['user'].widget=forms.TextInput(
                attrs={
                    'value': self.user,
                    'type': 'hidden',
                })
    user = forms.CharField(widget=forms.TextInput())
    list_id = forms.MultipleChoiceField(required=True,
        widget=forms.CheckboxSelectMultiple(
            attrs={'id': 'ListadoForm'}
        ),
        label="Listas")
    class Meta:
        model = UsersList
        fields = ('id', 'user', 'list_id')
