import openpyxl
from django.core.mail import send_mail
from django.db.models import Q
from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from agents.mixins import OrganisorAndLoginRequiredMixin
from .models import Tracker
from .forms import TrackerModelForm, CustomUserCreationForm

class TrackerListView(LoginRequiredMixin, generic.ListView):
    template_name = "tracker/tracker_list.html"
    context_object_name = "tracker"

    def get_queryset(self):
        queryset = Tracker.objects.all()

        if self.request.user.is_agent:
            queryset = queryset.filter(agent__user=self.request.user)

        search_query = self.request.GET.get("search", "")

        if search_query:
            queryset = queryset.filter(
                 Q(month__icontains=search_query) |
                 Q(agent__user__username__icontains=search_query)
            )
            

        return queryset.order_by("-created_at")

class TrackerCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "tracker/tracker_create.html"
    form_class = TrackerModelForm

    def get_success_url(self):
        return reverse("tracker:tracker-list")

class TrackerUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "tracker/tracker_update.html"
    queryset = Tracker.objects.all()
    form_class = TrackerModelForm

    def get_success_url(self):
        return reverse("tracker:tracker-list")

class TrackerDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name= "tracker/tracker_delete.html"
    queryset = Tracker.objects.all()

    def get_success_url(self):
        return reverse("tracker:tracker-list")

