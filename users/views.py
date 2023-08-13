from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Userprofile
from django.contrib.auth import login,authenticate
from django import forms
from .models import Userprofile

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields=('username',)
        
class UserprofileForm(forms.ModelForm):
    class Meta:
        model=Userprofile
        fields='__all__'
        

class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)

# Create your views here.
def vendor_deets(request,pk):
    user=User.objects.get(pk=pk)
    return render(request,'users/vendordetails.html',context={'user':user})

@login_required
def account(request):
    return render(request,'users/account.html')

def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request, user)
            return redirect('../')
    else:
        form = UserForm()
    
    return render(request, 'users/signin.html', {
        'form': form
    })