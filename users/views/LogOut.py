from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import logout

class LogOutView(View):
    def get(self, request):
        logout(request)
        return redirect('landing')