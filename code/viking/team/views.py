from django.views.generic import DetailView
from .models import Group, Profile


class GroupDetailView(DetailView):
    model = Group


class ProfileDetailView(DetailView):
    queryset = Profile.objects.filter(published=True, visible_profile=True)
