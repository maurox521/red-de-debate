# -*- coding: utf-8 -*-

from django import forms
from resumen.models import Debate
from django.contrib.auth import authenticate, login

counterarg_typeform = [('0', 'Ambas posturas'),
                ('1','Position contraria')]
members_typeform = [('0', 'Publico'),
                ('1','Privado a Usuarios Específicos'),
                ('2', 'Privado a Listas')]
owner=[('username','Nombre Real'),
         ('alias','Alias')]
order_deb_typeform= [('0', 'Fecha'),
                ('1','Visitas'),
                ('2', 'Nombre'),
                ('3', 'Participaciones')]
order_user_typeform= [('0', 'Nombre'),
                    ('1','Reputacion')]
participation_typeform = [('all', 'A elección del participante'),
                ('username','Nombre Real'),
                ('alias', 'Alias')]

class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, required=True, label="Usuario",
    widget=(forms.TextInput(attrs={"class":"input-login", 'name':"name", 'id':"name"})))
    password = forms.CharField(max_length=20, required=True, label="Contraseña",
    widget=(forms.PasswordInput(attrs={"class":"input-login", 'name':"pass", 'id':"pass"})))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Login incorrecto. Ingrese nuevamente.")
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user

class newDebateForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        self.owner = kwargs.pop('owner')
        self.usuarios = kwargs.pop('usuarios')
        self.listas = kwargs.pop('listado')
        super(newDebateForm,self).__init__(*args,**kwargs)
        if self.owner:
            self.fields['owner_type'].widget=forms.Select(
                    choices=self.owner,
                    attrs={'class': 'form-control', 'id': 'debAliasForm'}
                    )
        if self.usuarios:
            self.fields['members'].choices = [(x['object'], x['name']) for x in self.usuarios]
        if self.listas:
            self.fields['listado'].choices = [(x['id'], x['name']) for x in self.listas]
        self.fields['text'].required = False

    title = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Escribe un título...',
            'id': 'debTitleForm',
            'maxlength': 100,
        }))
    text = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'placeholder': 'Escribe una descripción...',
            'rows': 8,
            'id': 'debTextForm',
            'maxlength': 1000,
        }))
    end_date = forms.DateField(
        required=False,
        label='Fecha fin',
        widget=forms.TextInput(
            attrs={
                'type': 'date',
                'class': 'form-control',
                'id': 'debEndDateForm',
                # 'readonly': True,
            }))
    owner_type = forms.CharField(label='Publicar debate como')
    length = forms.CharField(
        label='Caracteres/argument',
        widget=forms.TextInput(
            # choices=caracteres,
            attrs={'class':'form-control', 'id': 'debLengthForm', 'value':'240','readonly': True}
            ))
    args_max = forms.CharField(
        label='Arguments/user',
        widget=forms.TextInput(
            # choices=rebates,
            attrs={'class': 'form-control', 'id': 'debArgsForm', 'value':'5','readonly': True}
            ))
    counterargs_max = forms.CharField(
        label='Rebates/user',
        widget=forms.TextInput(
            # choices=rebates,
            attrs={'class': 'form-control', 'id': 'debCounterArgForm', 'value':'5','readonly': True}
            ))
    position_max = forms.CharField(
        label='Cambio position/usr',
        widget=forms.TextInput(
            # choices=rebates,
            attrs={'class': 'form-control', 'id': 'debChangePositionForm', 'value':'5','readonly': True}
            ))
    counterargs_type = forms.CharField(
        label='Tipo Redebate',
        widget=forms.Select(
            choices=counterarg_typeform,
            attrs={'class': 'form-control', 'id': 'debCounterArgTypeForm'}
            ))
    members_type = forms.CharField(
        label='Tipo Debate',
        widget=forms.Select(
            choices=members_typeform,
            attrs={'class': 'form-control', 'id': 'debMemberTypeForm'}
            ))
    participation_type = forms.CharField(
        label='Tipo participación de usuarios en el debate',
        widget=forms.Select(
            choices=participation_typeform,
            attrs={'class': 'form-control', 'id': 'debParticipationTypeForm'}
            ))
    members = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(
            attrs={'id': 'debMembersForm'}
        ),
        label="Usuarios")
    listado = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(
            attrs={'id': 'debListForm'}
        ),
        label="Listas")
    class Meta:
        model = Debate
        fields = ('id_debate', 'title', 'text', 'end_date', 'owner_type',
                  'length', 'args_max', 'counterargs_max', 'position_max',
                  'counterargs_type', 'members_type')

class imageDebate(forms.Form):
    deb_img = forms.CharField(widget=forms.TextInput(
        attrs={
            'type': 'hidden',
            'id': 'id_deb_img'
        }))
    img = forms.FileField(label='Selecciona una imagen', required=False,
        widget=forms.FileInput(
            attrs={'id': 'debImgForm'}
            ))

class orderDebate(forms.Form):
    order_type = forms.CharField(
        label='Ordenar por',
        widget=forms.Select(
            choices=order_deb_typeform,
            attrs={'class': 'form-control', 'id': 'debOrderTypeForm', 'name': 'orderByForm'}
            ))

class orderUser(forms.Form):
    order_type = forms.CharField(
        label='Ordenar por',
        widget=forms.Select(
            choices=order_user_typeform,
            attrs={'class': 'form-control', 'id': 'userOrderTypeForm', 'name': 'userOrderByForm'}
            ))
