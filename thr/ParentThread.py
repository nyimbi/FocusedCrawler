'''
Created on Feb 22, 2014

@author: svalmiki
'''
from thr import CrawlThread as CT
from threading import Thread

class ParentThread(Thread):
    def __init__(self, query, totalCount):
        Thread.__init__(self)
        self.totalCount = totalCount
        self.query = query
        
    def run(self):
        for i in range(self.totalCount):
            ct = CT.CrawlThread(self.query)
            ct.start()