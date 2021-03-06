from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import credentials
from institute.models import Blocks, Institutestd, Officials
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from students.models import attendance, details
from django.core.mail import send_mail
from hosteldb.settings import EMAIL_HOST_USER


# Create your views here.

def login(request):
    
    if request.method == 'POST':
        user = request.POST["username"]
        password1 = request.POST["password"]
        if credentials.objects.filter(regd_no=user, password=password1).exists():
            response = redirect('students:student_home')
            response.set_cookie('username_std',user)
            return response

        elif credentials.objects.filter(emp_id=user, password=password1).exists():
            response = redirect('officials:official_home')
            response.set_cookie('username_off',user)
            return response

        else:
            messages.error(request, 'Invalid Username or Password')
            return redirect('authenticate:login')
            

    return render(request, 'authenticate/login.html')

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        regno = request.POST["regno"]
        password1 = request.POST["pass"]
        mode = request.POST["type"]
    
        if(mode == 'student'):
            if credentials.objects.filter(regd_no=regno).exists():
                messages.error(request, 'Student already exists. Please Login!')
                return redirect('authenticate:signup')
            
            else:
                if Institutestd.objects.filter(regd_no = regno).exists():
                    newStudent = Institutestd.objects.get(regd_no = regno)

                    newCred = credentials(regd_no= Institutestd.objects.get(regd_no = regno), password=password1)
                    

                    if(newStudent.year == 1):
                        blocks = Blocks.objects.filter(room_type='3S')
                        for block in blocks:
                            if block.gender == newStudent.gender:
                                for floor in ['Ground','First','Second']:
                                    for room in range(1,block.capacity+1):
                                        if(details.objects.filter(block_id=block.block_id,floor=floor,room_no=room).count() < 3):
                                            addStudent = details(regd_no=newStudent,block_id=Blocks.objects.get(block_id=block.block_id),floor=floor,room_no=room)
                                            addStudent.save()

                                            addAttendance = attendance(regd_no=newStudent)
                                            addAttendance.save()

                                            newCred.save()
                                            
                                            messages.success(request, 'User added to hostels successfully!')
                                            return redirect('authenticate:signup')
                        else:
                            messages.success(request, 'No Vacancies!')
                            return redirect('authenticate:signup')                            

                    elif(newStudent.year == 2 or newStudent.year== 3):
                        blocks = Blocks.objects.filter(room_type='2S')
                        for block in blocks:
                            if block.gender == newStudent.gender:
                                for floor in ['Ground','First','Second']:
                                    for room in range(1,block.capacity+1):
                                        if(details.objects.filter(block_id=block.block_id,floor=floor,room_no=room).count() < 2):
                                            addStudent = details(regd_no=newStudent,block_id=Blocks.objects.get(block_id=block.block_id),floor=floor,room_no=room)
                                            addStudent.save()

                                            addAttendance = attendance(regd_no=newStudent)
                                            addAttendance.save()

                                            newCred.save()
                                            messages.success(request, 'User added to hostels successfully!')
                                            return redirect('authenticate:signup')
                        else:
                            messages.success(request, 'No Vacancies!')
                            return redirect('authenticate:signup') 

                    else:
                        blocks = Blocks.objects.filter(room_type='1S')
                        for block in blocks:
                            if block.gender == newStudent.gender:
                                for floor in ['Ground','First','Second']:
                                    for room in range(1,block.capacity+1):
                                        if(details.objects.filter(block_id=block.block_id,floor=floor,room_no=room).count() < 1):
                                            addStudent = details(regd_no=newStudent,block_id=Blocks.objects.get(block_id=block.block_id),floor=floor,room_no=room)
                                            addStudent.save()

                                            addAttendance = attendance(regd_no=newStudent)
                                            addAttendance.save()                                        

                                            newCred.save()
                                            messages.success(request, 'User added to hostels successfully!')
                                            return redirect('authenticate:signup')
                        else:
                            messages.success(request, 'No Vacancies!')
                            return redirect('authenticate:signup') 

                else:
                    messages.error(request, 'No student with given Registration no.')
                    return redirect('authenticate:signup')

        elif(mode == 'official'):
            if credentials.objects.filter(emp_id=regno).exists():
                messages.error(request, 'Official already exists. Please Login!')
                return redirect('authenticate:signup')
            
            else:
                if Officials.objects.filter(emp_id = regno).exists():
                    newCred = credentials(emp_id= Officials.objects.get(emp_id = regno), password=password1)
                    newCred.save()
                    messages.success(request, 'User added to hostels successfully!')
                    return redirect('authenticate:signup')
                else:
                    messages.error(request, 'No Official with given Registration no.')
                    return redirect('authenticate:signup')
    
    
    return render(request, 'authenticate/SignUp1.html')



def forgot(request):
    if request.method == 'POST':
        user = request.POST["username"]
        if credentials.objects.filter(regd_no=user).exists():
            newPass = credentials.objects.get(regd_no_id=str(user))
            use=Institutestd.objects.get(regd_no=user)
            email=use.email_id
            subject="NIT AP Hostel Management System-Forgot Password request!"
            message="The password for the username \n"+str(user)+" is "+"\n Password : "+str(newPass.password)+"\nThis is a computer generated message dont reply to this !This is from Hostel Management System NIT AP .If it is not you please report to admin of the website "
            recepient=str(email)
            send_mail(subject,message,EMAIL_HOST_USER,[recepient],fail_silently=False)
            messages.success(request, 'Password is sent to your mail id!')
            return redirect('authenticate:login')

        elif credentials.objects.filter(emp_id=user).exists():
            newPass = credentials.objects.get(emp_id_id=str(user))
            use=Officials.objects.get(emp_id=user)
            email=use.email_id
            subject="NIT AP Hostel Management System-Forgot Password request!"
            message="The password for the username \n"+str(user)+" is "+"\n Password : "+str(newPass.password)+"\nThis is a computer generated message dont reply to this !This is from Hostel Management System NIT AP .If it is not you please report to admin of the website "
            recepient=str(email)
            send_mail(subject,message,EMAIL_HOST_USER,[recepient],fail_silently=False)
            messages.success(request, 'Password is sent to your mail id!')
            return redirect('authenticate:login')

        else:
            messages.error(request, 'Invalid Username')
            return redirect('authenticate:forgot')    

    return render(request, 'authenticate/forgot.html')