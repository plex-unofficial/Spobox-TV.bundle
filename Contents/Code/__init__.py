# -*- coding: utf-8 -*-
from PMS import *
import re 
import urllib

SPOBOXTV_PREFIX = '/video/SpoboxTV'

SPOBOXTV_CONTENT_URL	= 'http://system.medianac.de/spobox/player/78.html?autostart=true&dom_id=video_player&height=310&link_url=&mute=false&volume=20&width=792'

SPOBOXTV_PLAYER_BASEURL = 'http://www.plexapp.com/player/player.php?url='

CACHE_INTERVAL    = 3600

def Start():

  Plugin.AddPrefixHandler(SPOBOXTV_PREFIX, MainMenu, L('spobox.tv'), 'icon-default.png', 'art-default.png')
  Plugin.AddViewGroup('Details', viewMode='InfoList', mediaType='items')
  MediaContainer.content = 'Items'
  MediaContainer.art = R('art-default.png')
  MediaContainer.viewGroup = 'Details'
  MediaContainer.title1 = L('spobox.tv')
  HTTP.SetCacheTime(CACHE_INTERVAL)

def MainMenu():

  Log('(spobox.tv PLUG-IN) **==> ENTER Load spobox.tv Main Page')

  dir = MediaContainer()
 
  page = XML.ElementFromURL(SPOBOXTV_CONTENT_URL, isHTML=True)

  Log(page)

  scripts = page.xpath("/html/head/script")

  Log('(spobox.tv PLUG-IN) **==> retrieve spobox.tv Categories Script files')
  
  for script in scripts:
  
    content = re.findall('http://system.medianac.de/spobox/playlist/.*.js', script.text)
    categories = re.findall(' name: ".*",', script.text)

    if len(categories) != 0 :
            
        i=0
        
        Log('(spobox.tv PLUG-IN) **==> Load spobox.tv Categories')
        
        for category in categories:
            title = category[8:len(category)-2]
            contenturl= content[i]
            url = contenturl
            summary = ""
            thumb = "http://edge.download.newmedia.nacamar.net/medianac/spobox/download/default_asset_thumbnail.jpg"
            dir.Append(Function(DirectoryItem(ShowBrowser, title=title, thumb=thumb, summary=summary), showUrl=url, showName=title, showThumb=thumb))
            i = i + 1

  return dir

def ShowBrowser(sender, showUrl, showName, showThumb, pageNumber=1):

  dir = MediaContainer()

  Log('(spobox.tv PLUG-IN) **==> Load spobox.tv Category items from script')
 
  page = urllib.urlopen(showUrl)
  
  show = str(page.read())
  
  Log('(spobox.tv PLUG-IN) **==> regex Category items data from script')
  
  content = re.findall('"url":.*".*"', show)
  rtmps = re.findall('netConnectionUrl":.*".*"', show)
  titles = re.findall('description":.*".*"', show)
  categories = re.findall('category":.*".*"', show)
  thumbs = re.findall('preview_image_url":.*".*"', show)
  durations = re.findall('duration":.*".*"', show)
  
  if len(titles) != 0 :
             
    i=0
           
    for title in titles:
            
            contenttitle = title[15:len(title)-1]
            contenttitle = contenttitle.replace("<br/>"," ")
           
            contenturl = content[i]
            contenturl = contenturl[8:len(contenturl)-1]
            
            rtmpurl = rtmps[i]
            rtmpurl = rtmpurl[20:len(rtmpurl)-1]
            thumburl= thumbs[i]
            thumb = thumburl[21:len(thumburl)-1]
            category = categories[i]
            category = category[12:len(category)-1]
            titleduration = durations[i]
            titleduration = titleduration[11:len(titleduration)-1]
            contentart = ""
            
            Log('(spobox.tv PLUG-IN) **==> add item')
            
            dir.Append(RTMPVideoItem(url      = rtmpurl,clip     = contenturl,width    = 640,height   = 480,live     = False,title    = contenttitle,subtitle = category,summary  = contenttitle, duration = "0",thumb    = thumb,art      = contentart))
                       
            i = i + 1
  return dir

