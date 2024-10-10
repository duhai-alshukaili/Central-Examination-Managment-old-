from django.views import View
from django.shortcuts import render
from django.views.generic import TemplateView
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class HomeView(View):
    def get(self, request):
        
        print(request.get_host())
        
        host = request.get_host()
        islocal = host.find('localhost') >= 0 or host.find('127.0.0.1') >= 0

        context = {
            'installed': settings.INSTALLED_APPS,
            'islocal': islocal
        }

        if self.request.user.is_authenticated:
            return render(request, 'core/dashboard.html', context)
        else:
            return render(request, 'core/index.html', context)
    
# DashboardView using LoginRequiredMixin and TemplateView
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'core/dashboard.html'
    
    # Optionally, you can pass additional context if needed
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context
