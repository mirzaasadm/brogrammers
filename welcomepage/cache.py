from queue import Queue, SimpleQueue
from collections import defaultdict
from three_merge import merge
from welcomepage.models import Document
from diff_match_patch import diff_match_patch

dmp = diff_match_patch()

class SynchronizedDocument:

    def __init__(self, initial_doc: str = "") -> None:
        self._shadow = initial_doc
        self._text = initial_doc
        self.shadow_version = 0
        self.patch = None
        
        
    def update_text(self, new_text):
        self._text = new_text
        
        
    def apply_patch(self, patch):
        patch = dmp.patch_fromText(patch)
        self._shadow = dmp.patch_apply(patch, self._shadow)[0]
        self.shadow_version += 1
        self._text = dmp.patch_apply(patch, self._text)[0]
    
    
    def get_patch(self):
        self.patch = dmp.patch_make(self._shadow, self._text)
        self._shadow = self._text
        return dmp.patch_toText(self.patch)



























class Cache:

    def __init__(self):
        self.work_queue = Queue()

    def insert_in_queue(self, contd):
        self.work_queue.put(contd)
        return True

    def merge_on_queue(self, base: str, queue: Queue):
        current_document = base

        while not queue.empty():
            left = queue.get_nowait()
            try:
                right = queue.get_nowait()
                print("111")
                merged = merge(left, right, current_document)
                print("222")
                #current_document = merged
            except  Exception as e:
                print("..Didn't come here..")
                merged = merge(current_document, current_document, left)
                #current_document = merged
            current_document = merged
        return current_document

    def process_work_queue(self, basecont):
        merged_document = basecont
        while not self.work_queue.empty():
            base = merged_document
            merged_document = self.merge_on_queue(base, self.work_queue)
        return merged_document    
            