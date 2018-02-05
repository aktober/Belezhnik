from django.shortcuts import render
from django.views import generic


class HomePage(generic.View):
    def get(self, request):
        return render(request, 'core/home.html')
