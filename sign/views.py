from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from .models import BasicSignupForm
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required


class BaseRegisterView(CreateView):
    model = User
    form_class = BasicSignupForm
    success_url = '/news/'


@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='author')
    if not request.user.groups.filter(name='author').exists():
        premium_group.user_set.add(user)
    return redirect('/news/')