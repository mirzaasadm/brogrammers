import string
import random
from django.core import serializers
import threading
from welcomepage.models import Document
from welcomepage.threads import UpdateDocumentContentThread


class RandomURLgenerator():
    def URLalreadyexists(urlcode):
        object_list = serializers.serialize("python", Document.objects.all())
        for obj in object_list:
            if (urlcode == obj['fields']['doc_id']):
                return True
        return False

    def id_generator(size=11, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

class DocumentFunctions():

    def checkcolabname(colnames, name):
        if (colnames.find(name)):
            return True
        else:
            return False
            
            
    def getthreadbyname(tname):
        for thrd in threading.enumerate():
            if thrd.name == tname:
                return thrd
        nthread = UpdateDocumentContentThread(tname)
        nthread.daemon = True
        nthread.start()
        return nthread
        