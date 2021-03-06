'''
Created on Feb 15, 2014

@author: svalmiki
'''
from ds import DS
from html.parser import HTMLParser
from urllib.parse import urljoin
import re
import urllib.robotparser as rp

MAX_EXT_LENGTH = 5
HTTPS = "https:"
HTTP = "http:"
MAX_PROTO_LEN = 8
ROBOTS_TXT = "/robots.txt"
escapeExts = [
               #images
               ".jpeg",
               ".jpg",
               ".gif",
               ".png",
               ".bmp",
               ".raw",
               ".tiff",
               ".jfif",
               ".exif",
               ".ico",
               
               
               #videos
               ".mp4",
               ".wmv",
               ".3gp",
               ".ogg",
               ".flv",
               
               
               #audio
               ".mp3",
               ".wma",
               
               
               #text
               ".pdf",
               ".xlsx",
               ".xls",
               ".docx",
               ".doc",
               ".ppt",
               ".pptx",
               ".css",
               ".js",
               ".py",
               
               #executable
               ".exe",
               ".chm",
               ".sh"
               ]

class DataParser(HTMLParser):
    def __init__(self, strict=False):
        HTMLParser.__init__(self, strict)
        self.url = ""
        self.links = []
        self.record = 1
        self.data = ""
    
        
    def handle_starttag(self, tag, attrs):
        if tag == 'script' or tag == 'link' or tag == 'style' or tag == 'a':
            self.record = 0
        else:
            self.record = 1
        if tag == 'a':
            for attr, value in attrs:
                if attr == 'href':
                    link = self.filterlink(value)
                    if link != "":
                        if link not in DS.linkSet:
                            DS.linkSet.add(link)
                            self.links.append(link)
        
    def handle_data(self, data):
        if self.record:
            try:
                self.data = self.data + str(data)
            except:
                pass
        
    def handle_endtag(self, tag):
        self.record = 0
    
    
    def getlinks(self):
        return self.links
       
    def filterlink(self, link):
        proto = HTTP
        reFwdSlash = re.compile("^//.*")
        reStartPound = re.compile("^#.*")
        reRelLink1 = re.compile('^[/][a-zA-Z0-9].*')
        reRelLink2 = re.compile('^[a-zA-Z0-9].*')
        reHttps = re.compile("^https://.*")
        reJavascript = re.compile("^javascript:.*")
        reMailto = re.compile("^mailto:.*")

        
        # Makes sure the link has a protocol
        if reHttps.match(self.url):
            proto = HTTPS
        else:
            proto = HTTP
        
        # Removes all named anchors or fragments
        if reStartPound.match(link):
            return ""
        
        # Removes javascript links
        if reJavascript.match(link):
            return ""
        
        # Removes all mailto links
        if reMailto.match(link):
            return ""
        
        # Adds protocol to link
        if reFwdSlash.match(link):
            link = proto + link
            
        # Joins URL to relative link   
        if reRelLink1.match(link) or reRelLink2.match(link):
            link = urljoin(self.url, link)
        
        
        lcLink = link.lower()
        subLink = lcLink[-MAX_EXT_LENGTH:]
        
        # Removes unwanted extensions
        for ext in escapeExts:
            if subLink.find(ext) > -1:
                return ""
            
        # Checks if link is okay to crawl with robots.txt
        if self.checkrobot(link):
            return link
        else:
            return ""
    
    
    def get_data(self):
        return self.data
    
    
    def get_links(self):
        return self.links 
    
    # Checks robots.txt
    def checkrobot(self,u):
        try:
            robUrl = u if u.find("/", MAX_PROTO_LEN) == -1 else u[:u.find("/",MAX_PROTO_LEN)]
            robUrl = robUrl + ROBOTS_TXT
            rob = rp.RobotFileParser()
            rob.set_url(robUrl)
            return rob.can_fetch("*", u) 
        except:
            return True         