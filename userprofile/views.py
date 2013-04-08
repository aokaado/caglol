from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404

from caglols.userprofile.models import UserProfile

@login_required
def my_profile(request):
    profile = request.user.get_profile()

    return render(request, 'userprofile/profile.html', {'quser': request.user, 'profile': profile})	