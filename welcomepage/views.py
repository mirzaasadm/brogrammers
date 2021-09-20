from django.shortcuts import render
from django.http import HttpResponse , HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from welcomepage.models import Document
from welcomepage.functions import RandomURLgenerator , DocumentFunctions
from welcomepage.threads import UpdateDocumentContentThread
import threading

from three_merge import merge

# Create your views here.


merge_queue = {}


def WelcomePage(request):
    code = RandomURLgenerator.id_generator()
    while(RandomURLgenerator.URLalreadyexists(code)):
        code = RandomURLgenerator.id_generator()
    print("code:   ", code)
    doc_entry = Document(doc_id=code, title="title", content="File data", colabs="")
    doc_entry.save()
    return render(request, 'welcome.html', {'nextpageurl':code})
    
    
def document(request, pk):
    if(RandomURLgenerator.URLalreadyexists(pk)):        
        usern = request.POST.get("username","")
        
        doc = Document.objects.get(doc_id=pk)
        if(DocumentFunctions.checkcolabname(doc.colabs, usern)):
            doc.colabs += usern + "\n"
            doc.save()

        merge_queue[pk] = []
        resp = render(request, 'document.html', {'user':doc.colabs, 'idofdoc':pk, 'content':doc.content, 'filename':doc.title})
        doc_thread = UpdateDocumentContentThread(doc.doc_id)
        doc_thread.daemon = True
        doc_thread.start()
        return resp
    else:
        return render(request, 'errorpage.html')


@csrf_exempt
def editcontent(request):
    if request.method == 'POST':
        print("in POST")
        doc = Document.objects.get(doc_id=request.POST['documentid'])        
        merge_queue[request.POST['documentid']].append(request.POST['content'])

        print("Length doc items :   ",len(merge_queue[request.POST['documentid']]))

        thread = DocumentFunctions.getthreadbyname(request.POST['documentid']) 
        thread.array.append(request.POST['content'])

        return HttpResponse()
        
        
@csrf_exempt
def editfilename(request):
    if request.method == 'POST':
        doc = Document.objects.get(doc_id=request.POST['documentid'])
        doc.title = request.POST['filename']
        doc.save()
        
        success = doc.title
        return HttpResponse(success)
        
        
@csrf_exempt
def refreshdata(request):
    if request.method == 'POST':
        doc = Document.objects.get(doc_id=request.POST['documentid'])

        return HttpResponse(doc.content)

        
@csrf_exempt
def downloadfile(request):
    if request.method == 'POST':
        filetitle = "C:\\Users\\masad\\Downloads\\"+request.POST['filename']+".txt"
        filedata = request.POST['content']
        file1 = open(filetitle, "w")
        file1.write(filedata)
        file1.close()
        
        success =  "Done"
        return HttpResponse(success)