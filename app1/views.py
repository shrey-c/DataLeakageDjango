from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect	
from .forms import ChangepwdForm, DocumentForm, DetectorUploadForm
from login.models import LoginDetails
from app1.models import Document as doc, DetectorUpload
from django.views.decorators.cache import cache_control
import cv2
from PyPDF2 import PdfFileReader,PdfFileWriter
from reportlab.pdfgen import canvas
import subprocess
import codecs
from Crypto.Cipher import AES
from django.db.models import Q
# Create your views here.

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def userhome(request):
	try:
		username = request.session['username']
		designation = request.session['access']
		clientid = request.session['clientid']
		levels = ['public','private','confidential','topsecret']
		context = {
		'username' : username,
		'designation' : levels[designation%4 - 1],
		'nbar' : 'home',
		}
	except:
		return HttpResponseRedirect('/')
	if designation == 5:
		del request.session['username']
		return HttpResponseRedirect('/')
	return render(request, 'app1/userHome.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def detectorhome(request):
	try:
		username = request.session['username']
		designation = request.session['access']
		clientid = request.session['clientid']
		context = {
		'username' : username,
		'nbar' : 'home',
		}
	except:
		return HttpResponseRedirect('/')
	if designation != 5:
		del request.session['username'] #end the session
		return HttpResponseRedirect('/') #redirect to login page	
	return render(request, 'app1/detectorHome.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def changepassword(request):
	try:
		username = request.session['username']
		designation = request.session['access']
		clientid = request.session['clientid']
	except:
		return HttpResponseRedirect('/')
	levels = ['public','private','confidential','topsecret']	
	if request.method == 'POST':
		form = ChangepwdForm(request.POST)
		if form.is_valid():
			current = form.cleaned_data['current']
			new = form.cleaned_data['new']
			reenter = form.cleaned_data['reenter']

			q = LoginDetails.objects.get(clientid=clientid)
			if q.password == current:
				if new == reenter:
					q.password = new
					q.save()
				else:
					return HttpResponse("new and reentered password doesn't match")
			else:
				return HttpResponse("incorrect password")
	else:
		form = ChangepwdForm()

	context = {
		'form' : form,
		'username' : username,
		'designation' : levels[designation%4 -1],
		'nbar' : 'changepass'
	}
	if designation == 5:
		return render(request, 'app1/detector_changePassword.html', context)
	else:
		return render(request, 'app1/user_changePassword.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def modelformupload(request):
	try:
		username = request.session['username']
		designation = request.session['access']
		clientid = request.session['clientid']
	except:
		return HttpResponseRedirect('/')
	if request.method == 'POST':
		form = DocumentForm(request.POST, request.FILES)
		if form.is_valid():
			if request.POST['accesslevel'] > str(designation):
				return HttpResponse("Access level not allowed")
			else:
				form.save()
				q = doc.objects.last()
				q.author = clientid
				q.save()

			return HttpResponseRedirect('/user/userhome')
	else:
		form = DocumentForm()
	levels = ['public', 'private', 'confidential', 'topsecret']
	context = {
		'form' : form,
		'designation': levels[designation%4 -1],
		'nbar':'uploaddoc',
		'username' : username,
	}
	if designation == 5:
		del request.session['username']
		return HttpResponseRedirect('/')
	return render(request, 'app1/user_uploadDocument.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def displayfiles(request):
	try:
		username = request.session['username']
		clientid = request.session['clientid']
		designation = request.session['access']
	except:
		return HttpResponseRedirect('/')
	q = doc.objects.filter(accesslevel__lte=designation)
	levels = ['public', 'private', 'confidential', 'topsecret']
	context = {
		'data': q,
		'nbar': 'displaydoc',
		'designation': levels[designation%4 -1],
		'username': username,
	}
	if request.method == 'POST':
		if request.POST.get('filename'): #filename is name attribute of the button clicked in template
			name = request.POST.get('filename')
			out = "documents/document-output.pdf"
			val = modify_file(name, clientid)
			if val == "success":
				return HttpResponseRedirect("/media/" + out)
			else:
				return HttpResponse("Embed failure")
	if designation == 5:
		del request.session['username']
		return HttpResponseRedirect('/')
	return render(request, "app1/user_searchDocument.html", context)

def modify_file(filename, clientid):
    q = LoginDetails.objects.filter(clientid=clientid)[0]
    cipher = q.cipher_text
    hash1 = q.hash_text

    #cipher embedding
    pixel_array = [ord(c) for c in cipher]
    del pixel_array[-1]
    img = cv2.imread('/home/t3/projtest/actual/new/mysite/media/documents/image_small.png')
    for i in range(0, len(pixel_array), 1):
        img.itemset((55, i + 10, 0), pixel_array[i])

    #hash embedding
    pixel_array1 = [ord(c) for c in hash1]
    x = 58
    y = 10
    for i in range(len(pixel_array1) - 1, -1, -1):
        if (y >= img.shape[1]):
            y = 0
            x = x + 1

        img.itemset((x, y, 0), pixel_array1[i])
        y = y + 1
    cv2.imwrite('/home/t3/projtest/actual/new/mysite/media/documents/image_small_hash.png', img)

    #embedding process
    c = canvas.Canvas("/home/t3/projtest/actual/new/mysite/media/documents/watermark.pdf")
    c.drawImage("/home/t3/projtest/actual/new/mysite/media/documents/image_small_hash.png", 0, 0, preserveAspectRatio=True)
    c.save()

    output = PdfFileWriter()
    newurl = "/home/t3/projtest/actual/new/mysite/media/" + filename
    input1 = PdfFileReader(open(newurl, "r+b"))
    num_pages = input1.getNumPages()
    watermark = PdfFileReader(open("/home/t3/projtest/actual/new/mysite/media/documents/watermark.pdf", "r+b"))

    for pg in range(0, num_pages):
        page = input1.getPage(pg)
        page.mergePage(watermark.getPage(0))
        output.addPage(page)

    # finally, write "output" to document-output.pdf
    outputStream = open("/home/t3/projtest/actual/new/mysite/media/documents/document-output.pdf", "w+b")
    output.write(outputStream)
    outputStream.close()
    return ("success")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def checkdocument(request):
    try:
        username = request.session['username']
        designation = request.session['access']
    except:
        return HttpResponseRedirect('/')
    if designation != 5:
        del request.session['username']  # end the session
        return HttpResponseRedirect('/')  # redirect to login page
    if request.method=='POST':
        form = DetectorUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            extraction()
        return HttpResponseRedirect('/user/history')

    else:
        form = DetectorUploadForm()

    context = {
        'username': username,
        'nbar': 'checkdoc',
        'form': form,
    }
    return render(request, "app1/detector_checkDocument.html", context)

def extraction():
	q = DetectorUpload.objects.last()
	name = str(q.document)
	document_location = "/home/t3/projtest/actual/new/mysite/media/"
	file_loc = document_location + name
	logo_loc = document_location + "detector/./z"

	#logo extraction from document
	subprocess.call(["pdfimages", "-png", "-p", "-l", "1", file_loc, logo_loc])

	#cipher extraction from logo
	im = cv2.imread(document_location + 'detector/z-001-000.png')
	cipher = []
	for i in range(0,24,1):
		cipher.append(im[55,i+10,0])
	cipher = ''.join(chr(c) for c in cipher)
	cipher=cipher + '\n'

    #decryption of cipher
	base64_data = cipher.encode('utf-8')
	cipher_text = codecs.decode(base64_data, 'base64')
	decryption_suite = AES.new('this is a key123', AES.MODE_CBC, 'This is an IV456')
	plain = decryption_suite.decrypt(cipher_text)
	plain = plain.decode('utf-8')
    #extaction of hash from logo
	x=58
	y=10
	reverse_hash=[]
	for i in range(0,128,1):
		if(y>=im.shape[1]):
			y=0
			x=x+1
		reverse_hash.append(im[x,y,0])
		y=y+1
	hash=reverse_hash[::-1]
	hash = ''.join(chr(c) for c in hash)  # join characters
	try:
		culprit = LoginDetails.objects.filter(Q(cipher_text=cipher) | Q(hash_text=hash))[0]
		print(culprit.clientid, culprit.username, culprit.hash_text)
		if culprit.hash_text == hash:
			print("Culprit's name is: {}".format(culprit.username))
			q.username = culprit.username
			q.designation = culprit.designation
			q.m = hash
			q.mdash = culprit.hash_text
			q.clientid = culprit.clientid
			q.status = 'Yes'
			q.save()

	except:
		print("Not detected")
		q.status = 'No'
		q.save()


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def history(request):
	try:
		username = request.session['username']
		designation = request.session['access']
	except:
		return HttpResponseRedirect('/')
	if designation != 5:
		del request.session['username']  # end the session
		return HttpResponseRedirect('/')  # redirect to login page

	q = DetectorUpload.objects.exclude(status='Not Viewed').order_by("-uploaded_at")
	context = {
		'nbar': 'history',
		'data': q,
		'designation': designation,
		'username': username,
	}

	return render(request, 'app1/detector_history.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deletefile(request):
	try:
		username = request.session['username']
		clientid = request.session['clientid']
		designation = request.session['access']
	except:
		return HttpResponseRedirect('/')
	q = doc.objects.filter(author=clientid) #make it author
	levels = ['public', 'private', 'confidential', 'topsecret']
	context = {
		'data': q,
		'nbar': 'deletedoc',
		'designation': levels[designation%4 -1],
		'username': username,
	}
	document_location = "/home/t3/projtest/actual/new/mysite/media/"
	if request.method == 'POST':
		if request.POST.get('filename'): #filename is name attribute of the button clicked in template
			name = request.POST.get('filename')
			del_location = document_location + name
			print(del_location)
			doc.objects.get(document=name).delete()
			subprocess.call(["rm", del_location])

	if designation == 5:
		del request.session['username']
		return HttpResponseRedirect('/')
	return render(request, 'app1/user_deleteDocument.html',context)