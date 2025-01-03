from django.shortcuts import render


from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response 
from .models import Message , Product_imges , Swapper_Imges , Address
from .serializers import MessageSerializer , Product_imgesSerializer , swapper_imgesSerializer










from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from employe.models import *
from users.models import *






class AttendanceAPIView(APIView):

    def post(self, request):
        card_tag = request.data.get('card_tag')
        user = CustomUser.objects.get(id=4)
        Address.objects.create(uid=card_tag)
        
        if not card_tag:
            return Response({'error': 'Card tag is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            employee = Employee.objects.get(rfid_address=card_tag)
        except Employee.DoesNotExist:
            return Response({'error': 'Invalid card tag.'}, status=status.HTTP_404_NOT_FOUND)
        Address.objects.create(uid=card_tag)
        # Get today's date for attendance checks
        today = timezone.now().date()
        
        # Check if the attendance list for today is empty
        attendance_today = Attendance.objects.filter(date=today)
        
        # If the employee is an admin
        if employee.isAdmin:
            if attendance_today.exists():
                return Response({'message': 'Attendance already started for today!'}, status=status.HTTP_400_BAD_REQUEST)

            # Add admin's attendance
            Attendance.objects.create(employee=employee, date=today, created_by=user)  # Assuming the admin records their own attendance
            return Response({'message': 'Admin attendance recorded successfully!'}, status=status.HTTP_201_CREATED)

        # If the employee is not an admin and attendance has not started
        if not attendance_today.exists():
            return Response({'error': 'Admin must activate the system first by scanning their card.'}, status=status.HTTP_403_FORBIDDEN)

        # Record attendance for normal employees
        Attendance.objects.create(employee=employee, date=today, created_by=user)  # Created by the employee who scanned
        return Response({'message': 'Attendance recorded successfully! '}, status=status.HTTP_201_CREATED)
    









@api_view(['GET', 'POST'])
def product_images(request):
    """
    List all product images or create a new product image.
    """
    if request.method == 'GET':
        product_images = Product_imges.objects.all()
        serializer = Product_imgesSerializer(product_images, many=True, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = Product_imgesSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET', 'POST'])
def swapper_images(request):
    """
    List all product images or create a new product image.
    """
    if request.method == 'GET':
        product_images = Swapper_Imges.objects.all()
        serializer = swapper_imgesSerializer(product_images, many=True, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = swapper_imgesSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)










@api_view(['GET', 'POST'])
def product_image_id(request , id):
    """
    List all product images or create a new product image.
    """
    if request.method == 'GET':
        product_images = Product_imges.objects.filter(product_ham=id)
        serializer = Product_imgesSerializer(product_images, many=True, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = Product_imgesSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)










@api_view(['GET', 'PUT', 'DELETE'])
def product_imge(request, pk):
    """
    Retrieve, update or delete a message instance.
    """
    try:
        Product_imges = Product_imges.objects.get(pk=pk)
    except Product_imges.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = Product_imgesSerializer(Product_imges)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = Product_imgesSerializer(Product_imges, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        Product_imges.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)









@api_view(['GET', 'POST'])
def message_list(request):
    """
    List all messages or create a new message.
    """
    if request.method == 'GET':
        messages = Message.objects.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





@api_view(['GET', 'PUT', 'DELETE'])
def message_detail(request, pk):
    """
    Retrieve, update or delete a message instance.
    """
    try:
        message = Message.objects.get(pk=pk)
    except Message.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MessageSerializer(message)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = MessageSerializer(message, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

