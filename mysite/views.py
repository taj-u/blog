from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect

def home_view(request):
    user = request.user
    return render(request, 'home_view.html', {'user':user})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the new user
            login(request, user)  # Log the user in
            return redirect('blog:post_list')  # Redirect to the home page or artile list
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})

