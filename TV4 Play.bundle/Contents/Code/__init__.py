# -*- coding: utf-8 -*-
import re
import urllib2
import urllib

PLUGIN_TITLE = 'TV4 Play'
PLUGIN_PREFIX = '/video/tv4play'

PROGRAMS_URL = 'http://mobapi.tv4play.se/video/program_formats/list.json?sorttype=name&premium_filter=free&category=%s'
CATEGORIES_URL = 'http://api.tv4play.se/video/categories/list'
EPISODES_URL = 'http://webapi.tv4play.se/video/programs/search.json?premium=false&rows=940&%s&startdate=197001010100&sorttype=name'
SWF_PLAYER_URL = 'http://embed.tv4play.se/tv4play/v0/tv4video.swf?vid=%s'

SMIL_URL="http://anytime.tv4.se/webtv/metafileFlash.smil?p=%s&bw=300000&emulate=true&sl=true"

CACHE_INTERVAL = CACHE_1HOUR
CACHE_INTERVAL_LONG = CACHE_1MONTH

# Default artwork and icon(s)
PLUGIN_ARTWORK = 'art-default.jpg'
PLUGIN_ICON_DEFAULT = 'icon-default.png'
PLUGIN_ICON_MORE = 'icon-more.png'

############################################################

def Start():
  Plugin.AddPrefixHandler(PLUGIN_PREFIX, MainMenu, PLUGIN_TITLE, PLUGIN_ICON_DEFAULT, PLUGIN_ARTWORK)
  Plugin.AddViewGroup('ListItems', viewMode='List', mediaType='items')

  ObjectContainer.title1 = PLUGIN_TITLE
  ObjectContainer.art = R(PLUGIN_ARTWORK)

def MainMenu():
	oc = ObjectContainer(no_cache = True)
	categories = JSON.ObjectFromURL(CATEGORIES_URL)
  	for category in categories:
		name = category["name"]
		oc.add(DirectoryObject(key = Callback(TV4Shows, categoryName = name), title = name, thumb=GetThumb(name=name)))

	return oc

def TV4Shows(categoryName):
	oc = ObjectContainer(title2=categoryName)

  	if '&' in categoryName:
  		categoryName = categoryName.replace(' ', '').replace('&', '-')
  
  	categoryName = urllib2.quote(categoryName.encode("utf8"))
  	programs = JSON.ObjectFromURL(PROGRAMS_URL % categoryName.lower())

  	for program in programs:
		name = program["name"]
		Log("Adding program: %s" % name)
		oc.add(DirectoryObject(key = Callback(TV4Episodes, showName = name), title = name, thumb=GetThumb(name=name)))

	return oc

def TV4Episodes(showName):
	oc =  ObjectContainer(title2 = showName)
  
	textVar = { 'text' : showName}
  	title = urllib.urlencode(textVar)

  	episodeurl = EPISODES_URL %  title
  	Log("EpisodeUrl is: %s" % episodeurl)
  	episodes = JSON.ObjectFromURL(EPISODES_URL %  title)
  	for episode in episodes['results']:
		name = episode['name']
		vmanid = episode['vmanprogid']
		date = episode['publishdate']
		#VideoUrl = SWF_PLAYER_URL % vmanid
		thumb = episode['thumbnail']
		summary = episode['lead']
		publishdate = episode['publishdate']
		oc.add(VideoClipObject(key=Callback(TV4Play, vmanid=vmanid), title=name, thumb=thumb, summary=summary, rating_key=vmanid))
	
	return oc

@indirect
def TV4Play(vmanid):
	#SmilXML = XML.ObjectFromURL(url=SMIL_URL % vmanid, encoding="latin-1")
	
	#metaTags = SmilXML.XPath("//smil//head")
	#for meta in metaTags:
	#	Log(meta)


	#Log("This is the player url: %s", PlayerUrl)
	#oc = ObjectContainer(title2="something")


	#Log("This is my SmilXML: %s", SmilXML)
	clipurl = "mp4:/mp4root/2012-11-21/pid3923685(2242502_T3MP4130).mp4?token=c3RhcnRfdGltZT0yMDEyMTEyNjE4NTAyNiZlbmRfdGltZT0yMDEyMTEyNjE4NTIyNiZkaWdlc3Q9ZWJiM2Q0YTQxNDc0ZmYwMTcyMmZkNDc0NmZmZDhhODg="
	return IndirectResponse(VideoClipObject, key=RTMPVideoURL(url="rtmpe://cp70051.edgefcs.net/tv4ondemand", clip=clipurl, swf_url="http://wwwb.tv4play.se/polopoly_fs/1.939636.1281635185!approot/tv4video.swf?swfvfy=true"))

def GetThumb(name=None, parent=None):
  if name == 'Aktualitet':
    return R('icon-Aktualitet.png')
  elif name == 'Hem & fritid':
    return R('icon-HemOchFritid.png')
  elif name == 'Nyheter':
    return R('icon-Nyheter.png')
  elif name == 'Nöje':
    return R('icon-NojeOchHumor.png')
  elif name == 'Sport':
    return R('icon-Sport.png')
  elif name == 'Fotbollskanalen':
    return R('icon-Fotbollskanalen.png')
  elif name == 'Hockeykanalen':
    return R('icon-Hockeykanalen.png')
  elif name == 'Lattjo lajban':
    return R('icon-LattjoLajban.png')
  elif name == 'Barn':
    return R(PLUGIN_ICON_DEFAULT)
  elif parent != None:
    return GetThumb(name=parent)
  else:
    return R(PLUGIN_ICON_DEFAULT)