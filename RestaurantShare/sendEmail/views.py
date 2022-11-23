from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from shareRes.models import *
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string


# Create your views here.
def sendEmail(request):
	checked_res_list = request.POST.getlist('checks') # checks라는 이름을 가진 태그의 값을 다 가져옴
	inputReceiver = request.POST['inputReceiver']
	inputTitle = request.POST['inputTitle']
	inputContent = request.POST['inputContent']
	print(checked_res_list, '/', inputReceiver, '/', inputTitle, '/', inputContent)
	restaurants = list()

	for checked_res_id in checked_res_list:
		restaurants.append(Restaurant.objects.get(id=checked_res_id))
		
	content = {'inputContent': inputContent, 'restaurants': restaurants}
	
	msg_html = render_to_string('sendEmail/email_format.html', content)
	# sendEmail/email_format.html의 html 형식으로 content를 변환할 것임
	
	# json 파일 읽어서 아이디 비밀번호 가져오기
	import json
	with open('/Users/iseongmin/workspaces/RestaurantShare-with-Django/RestaurantShare/sendEmail/email.json', 'r') as f:
		json_data = json.load(f)
	email = json_data['email']
	password = json_data['password']
	
	# django send_mail 라이브러리 사용
	msg = EmailMessage(subject = inputTitle, body=msg_html, from_email=email, bcc=inputReceiver.split(','))
	msg.content_subtype='html'
	msg.send()

	return HttpResponseRedirect(reverse('index'))