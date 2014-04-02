# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.views.generic import DetailView
from cosinnus.models import CosinnusGroup
from cosinnus.models.group import MEMBERSHIP_ADMIN
from cosinnus.views.group import GroupListView, GroupUpdateView
from cosinnus.views.user import UserListView, UserDetailView
from cosinnus.views.profile import UserProfileUpdateView
from cosinnus.views.widget import DashboardMixin
from userprofiles.views import RegistrationView

from .forms import RegistrationMemberForm, RegistrationCommunityForm


class CommunityDetailView(DetailView):
    model = CosinnusGroup
    slug_url_kwarg = 'group'
    template_name = 'ecobasa/community_detail.html'

    def get_context_data(self, **kwargs):
        context = super(CommunityDetailView, self).get_context_data(**kwargs)
        context['profile'] = self.object.profile
        return context

community_detail = CommunityDetailView.as_view()


class CommunityDashboardView(DashboardMixin, DetailView):
    """Not really useful yet."""
    model = CosinnusGroup
    slug_url_kwarg = 'group'
    context_object_name = 'group'

    def get_filter(self):
        return {'group_id': self.object.pk}

community_dashboard = CommunityDashboardView.as_view()


class CommunityListView(GroupListView):
    template_name = 'ecobasa/community_list.html'

    def get_queryset(self):
        return self.model.objects.all()

community_list = CommunityListView.as_view()


class CommunityUpdateView(GroupUpdateView):
    template_name = 'ecobasa/community_form.html'

community_update = CommunityUpdateView.as_view()


class PioneerListView(UserListView):
    template_name = 'ecobasa/pioneer_list.html'

    def get_queryset(self):
       users = super(PioneerListView, self).get_queryset()
       pioneers = users.exclude(cosinnus_memberships__status=MEMBERSHIP_ADMIN)
       pioneers = pioneers.exclude(is_superuser=True, is_staff=True)
       return pioneers

pioneer_list = PioneerListView.as_view()


class PioneerDetailView(UserDetailView):
    template_name = 'ecobasa/pioneer_detail.html'

pioneer_detail = PioneerDetailView.as_view()


class BusListView(UserListView):
    template_name = 'ecobasa/bus_list.html'

    def get_context_data(self, **kwargs):
        context = super(BusListView, self).get_context_data(**kwargs)
        #import pdb; pdb.set_trace()
        context['user_list'] = context['user_list'].filter(cosinnus_profile__has_bus=True)
        #context['user_list'] = [user.name for user in context['user_list'] if user.has_bus == True]
        return context

bus_list = BusListView.as_view()


class BusAddView(UserProfileUpdateView):
    template_name = 'ecobasa/bus_add.html'

    def get_success_url(self):
        return reverse('bus-list')

bus_add = BusAddView.as_view()


#############################################################################
# registration overrides
#############################################################################

class RegistrationView(RegistrationView):
    template_name = 'userprofiles/registration.html'
register = RegistrationView.as_view()


class RegistrationMemberView(RegistrationView):
    template_name = 'userprofiles/registration_member.html'
    form_class = RegistrationMemberForm
register_member = RegistrationMemberView.as_view()


class RegistrationCommunityView(RegistrationView):
    template_name = 'userprofiles/registration_community.html'
    form_class = RegistrationCommunityForm
register_community = RegistrationCommunityView.as_view()
