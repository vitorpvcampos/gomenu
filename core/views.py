from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect

from core.forms import ProfileForm, SignUpForm
from core.models import UserProfile


def index(request):
    return render(request, 'base.html')


def dashboard(request):
    return render(request, 'base.html')


@login_required
def profile(request):
    profile_inline_formset = inlineformset_factory(User, UserProfile,
                                                   fields=('avatar',))
    if request.method == 'POST':
        form = ProfileForm(data=request.POST, instance=request.user)
        formset = profile_inline_formset(request.POST, request.FILES,
                                         instance=request.user)

        if form.is_valid():
            perfil = form.save(commit=False)
            formset = profile_inline_formset(request.POST, request.FILES,
                                             instance=perfil)

            if formset.is_valid():
                perfil.save()
                formset.save()
                return redirect('dashboard')

    else:
        form = ProfileForm(instance=request.user)
        formset = profile_inline_formset(instance=request.user)

    context = {'form': form, 'formset': formset, }

    return render(request, 'profile.html', context)


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            user = User.objects.get(username=username)
            group = Group.objects.get_or_create(name="Restaurant Manager")
            user.groups.add(group)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html',
                  {'form': form})
