from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from django.shortcuts import render, redirect

from .serializers import TaskSerializer
from .models import MyTaskList
from rest_framework.parsers import JSONParser

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    else:
            inital_data = {'username':'', 'password':''}
            form = AuthenticationForm(initial=inital_data)
    return render(request, 'login.html',{'form':form})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
            inital_data = {'username':'', 'password1':'','password2':''}
            form = UserCreationForm(inital_data)
    return render(request, 'register.html',{'form':form})

class MyTaskView(viewsets.ModelViewSet):
    queryset = MyTaskList.objects.all()
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "mytask.html"
    parser_classes = (JSONParser,)
    serializer_class = TaskSerializer

    def list(self, request):
        if not request.user.is_authenticated:
             return redirect('/login')
        title=request.GET.get('title')
        due_date=request.GET.get('due_date')
        sort, order = request.GET.get('sort','due_date'), request.GET.get('order','asc')
        if sort not in ('title','due_date','category') and order not in ('asc','desc'):
            sort, order = 'due_date','asc'
        allTasks = MyTaskList.objects.all().order_by(f'-{sort}' if order =='desc' else sort)
        mytasks = list(allTasks.filter(user=request.user).order_by('title').values_list('title', flat= True))
        queryset, message, filters = None, None, {}
        if title and due_date:
            queryset = MyTaskList.objects.filter(title=title, due_date=due_date)
        elif title:
            queryset = MyTaskList.objects.filter(title=title)
        elif due_date:
            queryset = MyTaskList.objects.filter(due_date=due_date)
        if not queryset and allTasks:
            queryset = allTasks
            message = f'No task found by title, {title}' if title else None
        else:
            message = 'No tasks for you. Please add one.'
        serializer = TaskSerializer(queryset, many=True)
        filters['titles'] = list(allTasks.values_list('title', flat = True))
        filters['due_dates'] = list(allTasks.values_list('due_date', flat = True))
        filters['categories'] = list(allTasks.values_list('category', flat = True))
        search_query = title
        query = f'&title={title}' if title else f'&due_date={due_date}' if due_date else None
        return (Response({'data':serializer.data, 'mytasks': mytasks, "message":message, "filters":filters, "query": query, "search_query":search_query }))