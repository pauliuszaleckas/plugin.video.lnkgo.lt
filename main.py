#
#  Copyright (C) 2013  Paulius Zaleckas <paulius.zaleckas@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License along
#  with this program; if not, write to the Free Software Foundation, Inc.,
#  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

import urlparse
import urllib
import re

import xbmcgui
import xbmcplugin

BASE_URL = 'http://lnkgo.lt/'
CATEGORY_URL = BASE_URL + 'video-kategorija/'
VIDEO_URL = BASE_URL + 'video-perziura/'

def CATEGORY():
	response = urllib.urlopen(CATEGORY_URL)
	html = response.read()
	response.close()
	match = re.compile('<a href="/video-kategorija/(\d+?)/.+?">(.+?)&nbsp;<img src="img/arrow.link.png" alt="" /></a>').findall(html)
	for idx,name in match:
		link = PATH + '?prg_idx=' + str(idx) + '&page=1'
		item = xbmcgui.ListItem(name)
		xbmcplugin.addDirectoryItem(HANDLE, link, item, True)
	xbmcplugin.endOfDirectory(HANDLE)

def add_all_video(vidx):
	response = urllib.urlopen(VIDEO_URL + vidx)
	html = response.read()
	response.close()
	match = re.compile('<div class="image">\s*<div>\s*<a href="/video-perziura/(\d+?)/.+?"><img src="(.+?)\?.+?" alt=".*?" /><span class="videoPlay">&nbsp;</span></a>\s*</div>\s*</div>\s*<div class="info">\s*<div class="title">\s*<a href=".+?".*?>(.+?)&nbsp;<img src="img/arrow.link.png" alt="" /></a>').findall(html)
	for vidx,image,name in match:
		link = PATH + '?vidx=' + str(vidx)
		item = xbmcgui.ListItem(name, iconImage=image)
		item.setProperty('IsPlayable', 'true')
		xbmcplugin.addDirectoryItem(HANDLE, link, item)

def INDEX(idx):
	response = urllib.urlopen(CATEGORY_URL + idx)
	html = response.read()
	response.close()
	match = re.search('<div class="image">\s*<div>\s*<a href="/video-perziura/(\d+?)/.+?">', html)
	if match:
		add_all_video(match.group(1));
	xbmcplugin.endOfDirectory(HANDLE)

def play_video(video):
	response = urllib.urlopen(BASE_URL + video)
	html = response.read()
	response.close()
	vurl = re.compile('ipadUrl: \'(.*?)\'').findall(html)
	if len(vurl):
		item = xbmcgui.ListItem(path=vurl[0])
		xbmcplugin.setResolvedUrl(HANDLE, True, item)

def PLAY(vidx):
	response = urllib.urlopen(VIDEO_URL + vidx)
	html = response.read()
	response.close()
	vurl = re.compile('var url\s+= \'(.*?)\';').findall(html)
	if len(vurl):
		play_video(vurl[0])

if __name__ == '__main__':
	PATH = sys.argv[0]
	HANDLE = int(sys.argv[1])
	PARAMS = urlparse.parse_qs(sys.argv[2][1:])

	if 'prg_idx' in PARAMS:
		INDEX(PARAMS['prg_idx'][0])
	elif 'vidx' in PARAMS:
		PLAY(PARAMS['vidx'][0])
	else:
		CATEGORY()

