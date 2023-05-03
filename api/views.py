from django.shortcuts import render
from django.http import JsonResponse
from .models import Task

from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import serializers

@api_view(['GET'])
def apiOverView(request):
    api_urls = {
        'List' : '/task-list/', # list the tasks
        'Detail View' : '/task-detail/<str:pk>/', # return the a certain object
        'create' : '/task-create/', # create a task
        'Update' : '/task-update/<str:pk>/', # update a task based on primary key
        'Delete' : '/task-delete/<str:pk>/', # delete a task based on primary key
    }
    return Response(api_urls)


@api_view(['GET'])
def taskList(request):
    tasks = Task.objects.all().order_by('-id')
    # minus means descending order
    serializer = serializers.TaskSerializer(tasks, many = True)
    # do we want to serialize one object or have a list of them?
    # thats why many = True
    return Response(serializer.data)


@api_view(['GET'])
def taskDetail(request, pk):
    tasks = Task.objects.get(id = pk)
    serializer = serializers.TaskSerializer(tasks, many = False)
    return Response(serializer.data)


@api_view(['POST'])
def taskCreate(request):
    serializer = serializers.TaskSerializer(data = request.data)
    
    if serializer.is_valid() :
        serializer.save()

    return Response(serializer.data)


@api_view(['POST'])
def taskUpdate(request, pk):
    task = Task.objects.get(id = pk)
    # instance is needed so we can
    # point at what we need to update
    serializer = serializers.TaskSerializer(instance = task, data = request.data)
    if serializer.is_valid() :
        serializer.save()

    return Response(serializer.data)

@api_view(['DELETE'])
def taskDelete(request, pk):
    task = Task.objects.get(id = pk)
    task.delete()

    return Response("Deleted")

