from django.shortcuts import render, redirect
from . models import UserPersonalModel
from . forms import UserPersonalForm, UserRegisterForm
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
import numpy as np
import joblib

from .models import UserPredictModel
from .forms import UserPredictForm
import csv
from nltk.chat.util import Chat, reflections


def Landing_1(request):
    return render(request, '1_Landing.html')

def Register_2(request):
    form = UserRegisterForm()
    if request.method =='POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was successfully created. ' + user)
            return redirect('Login_3')

    context = {'form':form}
    return render(request, '2_Register.html', context)


def Login_3(request):
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('Home_4')
        else:
            messages.info(request, 'Username OR Password incorrect')

    context = {}
    return render(request,'3_Login.html', context)

def Home_4(request):
    return render(request, '4_Home.html')

def Teamates_5(request):
    return render(request,'5_Teamates.html')

def Domain_Result_6(request):
    return render(request,'6_Domain_Result.html')

def Problem_Statement_7(request):
    return render(request,'7_Problem_Statement.html')
    

def Per_Info_8(request):
    if request.method == 'POST':
        fieldss = ['firstname','lastname','age','address','phone','city','state','country']
        form = UserPersonalForm(request.POST)
        if form.is_valid():
            print('Saving data in Form')
            form.save()
        return render(request, '4_Home.html', {'form':form})
    else:
        print('Else working')
        form = UserPersonalForm(request.POST)    
        return render(request, '8_Per_Info.html', {'form':form})
    
    
Model1 = joblib.load('D:\PROJECT\STRESS_CHAT\CODE\DEPLOYMENT\PROJECT\APP\LR.pkl')  
  
def Deploy_9(request): 
    if request.method == "POST":
        int_features = [x for x in request.POST.values()]
        int_features = int_features[1:]
        
        print(int_features)
        final_features = [np.array(int_features, dtype=float)]
        print(final_features)
        prediction = Model1.predict(final_features)
        print(prediction)
        output = prediction[0]
        print(output)
        if output == 0:
            return render(request, '9_Deploy.html', {"prediction_text": "THE VERY LESS DEPRESSION MIGHT BE OCCUR IN THIS CONDITIONS"})
        elif output == 1:
            return render(request, '9_Deploy.html', {"prediction_text": "THE LESS DEPRESSION MIGHT BE OCCUR IN THIS CONDITIONS, THIS IS STAGE 1 DEPRESSION LEVEL."})
        elif output == 2:
            return render(request, '9_Deploy.html', {"prediction_text": "THE MODERATE DEPRESSION MIGHT BE OCCUR IN THIS CONDITIONS. THIS IS STAGE 2 DEPRESSION LEVEL."})
        elif output == 3:
            return render(request, '9_Deploy.html', {"prediction_text": "THE HIGH DEPRESSION MIGHT BE OCCUR IN THIS CONDITIONS. THIS IS STAGE 3 DEPRESSION LEVEL."})
        elif output == 4:
            return render(request, '9_Deploy.html', {"prediction_text": "THE VERY HIGH DEPRESSION MIGHT BE OCCUR IN THIS CONDITIONS. THIS IS STAGE 4 DEPRESSION LEVEL."})
    else:
        return render(request, '9_Deploy.html')
    
def Per_Database_10(request):
    models = UserPersonalModel.objects.all()
    return render(request, '10_Per_Database.html', {'models':models})

def chat_with_user(user_input):
    try:
        with open(csv_filepath, 'r', newline='') as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader)  
            patterns = [(row[0], row[1].split('|')) for row in csv_reader]
    except FileNotFoundError:
        patterns = []

    chatbot = Chat(patterns, reflections)
    return chatbot.respond(user_input)

csv_filepath = 'D:\PROJECT\STRESS_CHAT\CODE\DEPLOYMENT\PROJECT\APP\A.csv'

def Deploy_11(request):
    if request.method == 'POST':
        form = UserPredictForm(request.POST)

        if form.is_valid():
            form.save()
            user_input = form.cleaned_data.get('text')
            response = chat_with_user(user_input)
            print(response)

            data = UserPredictModel.objects.latest('id')
            data.label = response
            data.save()

            return render(request, '11_Deploy.html', {'form': form, 'prediction_text': response})

    else:
        print('Else working')
        form = UserPredictForm()
    return render(request, '11_Deploy.html', {'form': form})


def Database_12(request):
    models = UserPredictModel.objects.all()
    return render(request, '12_Database.html', {'models': models})


def Logout(request):
    logout(request)
    return redirect('Login_3')
