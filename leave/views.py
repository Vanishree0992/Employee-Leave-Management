from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import LeaveRequest
from .forms import LeaveRequestForm

class LeaveListView(LoginRequiredMixin, ListView):
    model = LeaveRequest
    template_name = "leave/leave_list.html"
    context_object_name = "leaves"
    paginate_by = 20

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return LeaveRequest.objects.all()
        return LeaveRequest.objects.filter(employee=user)

class LeaveDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = LeaveRequest
    template_name = "leave/leave_detail.html"

    def test_func(self):
        leave = self.get_object()
        user = self.request.user
        return user.is_superuser or user.is_staff or leave.employee == user

class LeaveCreateView(LoginRequiredMixin, CreateView):
    model = LeaveRequest
    form_class = LeaveRequestForm
    template_name = "leave/leave_form.html"
    success_url = reverse_lazy("leave:list")

    def form_valid(self, form):
        form.instance.employee = self.request.user
        messages.success(self.request, "Leave request submitted.")
        return super().form_valid(form)

class LeaveUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = LeaveRequest
    form_class = LeaveRequestForm
    template_name = "leave/leave_form.html"
    success_url = reverse_lazy("leave:list")

    def test_func(self):
        leave = self.get_object()
        return self.request.user.is_superuser or (leave.employee == self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Leave request updated.")
        return super().form_valid(form)

class LeaveDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = LeaveRequest
    template_name = "leave/leave_confirm_delete.html"
    success_url = reverse_lazy("leave:list")

    def test_func(self):
        leave = self.get_object()
        return self.request.user.is_superuser or (leave.employee == self.request.user)

class LeaveApproveRejectView(LoginRequiredMixin, UserPassesTestMixin, View):
    def post(self, request, pk):
        leave = get_object_or_404(LeaveRequest, pk=pk)
        action = request.POST.get("action")
        if action == "approve":
            leave.status = LeaveRequest.STATUS_APPROVED
            leave.save()
            messages.success(request, "Leave approved.")
        elif action == "reject":
            leave.status = LeaveRequest.STATUS_REJECTED
            leave.save()
            messages.success(request, "Leave rejected.")
        else:
            messages.error(request, "Unknown action.")
        return redirect("leave:detail", pk=leave.pk)

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser
