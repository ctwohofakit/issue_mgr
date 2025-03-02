from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from accounts.models import Role, CustomUser
from .models import Issue, Status
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)



class IssueListView(LoginRequiredMixin,ListView):
    template_name="issues/list.html"
    model=Issue

    def get_context_data(self, **kwargs):
        context =super().get_context_data(**kwargs)
        user=self.request.user
        role=Role.objects.get(name="product owner")
        team_po=(
            CustomUser.objects
            .filter(team=user.team)
            .filter(role=role)
        )
        if team_po.exists():
            reporter = team_po[0]
            to_do=Status.objects.get(name="to do")
            context["to_do_list"]=(
                Issue.objects
                .filter(status=to_do)
                .filter(reporter=team_po[0])
                .order_by("created_on").reverse()
            )
            in_progress=Status.objects.get(name="in progress")
            context["in_progress_list"]=(
                Issue.objects
                .filter(status=in_progress)
                .filter(reporter=team_po[0])
                .order_by("created_on").reverse()       
            )

            done=Status.objects.get(name="done")
            context["done_list"] = (
                Issue.objects
                .filter(status=done)
                .filter(reporter=team_po[0])
                .order_by("created_on").reverse()
            )
        else:
            context["to_do_list"] = []
            context["in_progress_list"] = []
            context["done_list"] = []
        return context
    
class IssueDetailView(LoginRequiredMixin, DetailView):
    template_name="issues/detail.html"
    model=Issue

class IssueCreateView(LoginRequiredMixin, CreateView):
    model=Issue
    fields=["name","summary","description", "status", "assignee"]
    template_name="issues/new.html"
    success_url=reverse_lazy("list")

    def form_valid(self,form):
        form.instance.reporter=self.request.user
        return super().form_valid(form)
    


class IssueUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name="issues/edit.html"
    model=Issue
    fields=["name","summary","description", "status", "assignee"]

    def test_func(self):
        issue=self.get_object()
        return issue.reporter==self.request.user
    



class IssueDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    template_name="issues/delete.html"
    model=Issue
    success_url=reverse_lazy("list")

    def test_func(self):
        issue=self.get_object()
        return issue.reporter==self.request.user