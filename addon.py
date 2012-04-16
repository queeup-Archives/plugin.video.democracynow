# -*- coding: utf-8 -*-

# Imports
from BeautifulSoup import SoupStrainer, BeautifulSoup as BS
import sys
import urllib
import xbmcgui
import xbmcplugin
import xbmcaddon

__addon__ = xbmcaddon.Addon(id='plugin.video.democracynow')
__info__ = __addon__.getAddonInfo
__icon__ = __info__('icon')
__fanart__ = __info__('fanart')

# Fanart
xbmcplugin.setPluginFanart(int(sys.argv[1]), __fanart__)

URL = urllib.urlopen('http://m.democracynow.org/').read().replace('&quot;', '"').replace('&#8217;', "'").replace('<span class="caps">', '').replace('</span>', '')


def Main():
  soup = BS(URL, parseOnlyThese=SoupStrainer('div', 'ui-content'))
  date = soup.find('div', 'context_header').h2.string.strip()
  for entry in soup('li'):
    if xbmcgui.getCurrentWindowId() == 10501:
      content = 'audio'
      try:
        url = entry('a', 'media_icon listen')[0]['href']
      except:
        url = ''
    else:
      url = entry('a', 'video_link')[0]['href']
      content = 'video'
    try:
      thumb = entry('img', 'video_poster')[0]['src']
    except:
      thumb = entry('a', 'video_link')[0].img['src']
    if not thumb.startswith("http://"):
      thumb = 'http://m.democracynow.org' + thumb
    title = entry('div', 'two_thirds')[0].a.string.strip()
    if title.startswith('Watch'):
      title = 'Full Show'
    elif title.startswith('A collection of news briefs from around the world.'):
      title = 'Headlines'
    try:
      summary = entry('div', 'more_summary')[0].p.string
    except:
      if title.startswith('Full Show'):
        summary = 'Watch Full Show'
      elif title.startswith('Headlines'):
        summary = 'A collection of news briefs from around the world.'
      else:
        summary = ''
    try:
      duration = entry('div', 'media_icon duration')[0].string.strip().replace(' ', '').replace('m', ':').replace('s', '')
    except:
      duration = ''
    listitem = xbmcgui.ListItem(title, iconImage="DefaultVideoBig.png", thumbnailImage=thumb)
    listitem.setProperty('fanart_image', __fanart__)
    listitem.setProperty('IsPlayable', 'true')
    listitem.setInfo(type=content,
                     infoLabels={"title": title,
                                 "label": title,
                                 "plot": summary,
                                 "duration": duration,
                                 "tvshowtitle": date})
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), url, listitem, isFolder=False)

  xbmcplugin.setContent(int(sys.argv[1]), 'episodes')

  # End of list...
  xbmcplugin.endOfDirectory(int(sys.argv[1]), True)

Main()
