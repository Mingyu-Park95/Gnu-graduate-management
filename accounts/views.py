from django.shortcuts import render
from .forms import CustomUserCreationForm, CustomUserChangeForm


def register(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'registration/register_done.html', {'new_user': new_user})
    else:
        user_form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': user_form})

def userChange(request):
    if request.method == 'POST':
        user_form = CustomUserChangeForm(request.POST, instance=request.user)
        if user_form.is_valid():
            new_user = user_form.save(commit=False) #commit은 뭘까 ..
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'registration/userChange_done.html', {'new_user': new_user})
    else:
        user_form = CustomUserChangeForm(instance=request.user)
    return render(request, 'registration/userChange.html', {'form': user_form})