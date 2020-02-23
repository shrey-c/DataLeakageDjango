from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import LoginDetailsForm
from .models import LoginDetails
from django.contrib.auth.decorators import login_required
from Crypto.Cipher import AES
import uuid #for generation of client id
import codecs
import hashlib
# Create your views here.

def login_form(request):
	if request.method == 'POST':
		form = LoginDetailsForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']

			try:
				q = LoginDetails.objects.get(username=username)
				if(q.password == password):
					request.session['username'] = username
					request.session['access'] = q.designation
					request.session['clientid'] = q.clientid
					if q.designation != 5:
						return HttpResponseRedirect("/user/userhome/")
					else:
						return HttpResponseRedirect("/user/detectorhome/")
					#return HttpResponse("access granted")
				else:
					return HttpResponse("<h1> Access Denied </h1>")
			except:
				return HttpResponse("<h1> Access Denied </h1>")
	else:
		form = LoginDetailsForm()
	return render(request, 'login/index.html', {'form':form})

@login_required
def login_assign(request):
	clientid = uuid.uuid4().hex[:16].upper()

	encryption_suite = AES.new('this is a key123',AES.MODE_CBC,'this is an IV456')
	cipher_text = encryption_suite.encrypt(clientid)
	base64_data = codecs.encode(cipher_text,'base64')
	asc = base64_data.decode('utf-8') #cipher text to readable string format

	clientid1 = clientid.encode('utf-8')
	print(clientid1)
	hash_object = hashlib.sha512(clientid1)
	hex_dig = hash_object.hexdigest() #hash

	#to update the last record with the above values
	q = LoginDetails.objects.last()
	if q.clientid == "xyz":
		q.clientid = clientid
		q.cipher_text = asc
		q.hash_text = hex_dig
		q.save()
	else:
		pass
	return HttpResponse("client id, ciphertext, and hash generated")

def logout(request):
	try:
		del request.session['username']
	except:
		pass
	return HttpResponseRedirect("/")
