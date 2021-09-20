import threading
import time
from welcomepage.models import Document
from welcomepage.cache import Cache , SynchronizedDocument
import requests
from three_merge import merge



class UpdateDocumentContentThread(threading.Thread):
    def __init__(self, doco):
        self.idoc = doco
        self.array = []
        threading.Thread.__init__(self)

    def run(self):
        try:
            threading.current_thread().name = self.idoc
            while True:
                doc = Document.objects.get(doc_id=self.idoc)
                while(len(self.array)>=2):
                    merged = merge(self.array[0], self.array[1], doc.content)
                    self.array.pop(0)
                    self.array.pop(0)
                    doc.content = merged
                    doc.save()
                    print("Saved in Database")                    

        except Exception as e:
            print(e)