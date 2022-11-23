from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from shareRes.models import *


# Create your views here.
def sendEmail(request):
	checked_res_list = request.POST.getlist('checks') # checks라는 이름을 가진 태그의 값을 다 가져옴
	inputReceiver = request.POST['inputReceiver']
	inputTitle = request.POST['inputTitle']
	inputContent = request.POST['inputContent']
	print(checked_res_list, '/', inputReceiver, '/', inputTitle, '/', inputContent)
	
	mail_html = '<html><body>'
	mail_html += '<h1> 맛집공유 </h1>'
	mail_html += '<p>'+inputContent+ '<br>'
	mail_html += '발신자님께서 공유하신 맛집은 다음과 같습니다.</p>'
	
	for checked_res_id in checked_res_list:
		
		restaurant = Restaurant.objects.get(id = checked_res_id)
		mail_html += '<h2>' + restaurant.restaurant_name + '</h2>'
		mail_html += '<h4>* 관련 링크</h4>' + '<p>'+restaurant.restaurant_link +'</p>'
		mail_html += '<h4>* 상세 내용</h4>' + '<p>'+restaurant.restaurant_content +'</p>'
		mail_html += '<h4>* 장소 키워드</h4>' + '<p>'+restaurant.restaurant_keyword +'</p>'
		mail_html += '<br>'
		mail_html += '</body></html>'
	print(mail_html)
	
	# json 파일 읽어서 아이디 비밀번호 가져오기
	import json
	with open('/Users/iseongmin/workspaces/RestaurantShare-with-Django/RestaurantShare/sendEmail/email.json', 'r') as f:
		json_data = json.load(f)
	email = json_data['email']
	password = json_data['password']
	# smtp using
	server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
	server.login(email, password)
	
	msg = MIMEMultipart('alternative')
	msg['Subject'] = inputTitle
	msg['From'] = email
	msg['To'] = inputReceiver
	mail_html = MIMEText(mail_html, 'html')
	msg.attach(mail_html)
	print(msg['To'], type(msg['To']))
	server.sendmail(msg['From'], msg['To'].split(','), msg.as_string())
	server.quit()
	return HttpResponseRedirect(reverse('index'))