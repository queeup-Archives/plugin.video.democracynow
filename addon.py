# -*- coding: utf-8 -*-

from BeautifulSoup import SoupStrainer, BeautifulSoup as BS
import sys
import urllib
import xbmcgui
import xbmcplugin
import xbmcaddon

addon = xbmcaddon.Addon()
addon_icon = addon.getAddonInfo('icon')
addon_fanart = addon.getAddonInfo('fanart')
addon_handler = int(sys.argv[1])

# Fanart
xbmcplugin.setPluginFanart(int(sys.argv[1]), addon_fanart)

URL = urllib.urlopen('http://m.democracynow.org/').read().replace('&quot;', '"')\
                                                         .replace('&#8217;', "'")\
                                                         .replace('<span class="caps">', '')\
                                                         .replace('</span>', '')


def main():
  soup = BS(URL, parseOnlyThese=SoupStrainer('div', 'ui-content'))
  date = soup.find('div', 'context_header').h2.string.strip()
  for entry in soup('li'):
    try:
      url = entry('a', 'video_link')[0]['href'].replace('/ipod/', '/flash/')
    except IndexError:
      continue
    try:
      thumb = entry('img', 'video_poster')[0]['src']
    except IndexError:
      thumb = entry('a', 'video_link')[0].img['src']
    if not thumb.startswith("http://"):
      thumb = 'http://m.democracynow.org' + thumb
    title = entry('div', 'two_thirds')[0].a.string.strip()
    if title == 'Watch':
      title = 'Full Show'
    elif title.startswith('A collection of news briefs from around the world.'):
      title = 'Headlines'
    try:
      summary = entry('div', 'more_summary')[0].p.string
    except IndexError:
      if title.startswith('Full Show'):
        summary = 'Watch Full Show'
      elif title.startswith('Headlines'):
        summary = 'A collection of news briefs from around the world.'
      else:
        summary = ''
    try:
      duration = entry('div', 'media_icon duration')[0].string.strip().replace(' ', '')\
                                                                      .replace('m', ':')\
                                                                      .replace('s', '')
    except IndexError:
      duration = ''
    if url.startswith('http://'):
      listitem = xbmcgui.ListItem(title, iconImage="DefaultVideoBig.png", thumbnailImage=thumb)
      listitem.setProperty('fanart_image', addon_fanart)
      listitem.setProperty('IsPlayable', 'true')
      listitem.setInfo(type="video",
                       infoLabels={"title": title,
                                   "plot": summary,
                                   "duration": duration,
                                   "tvshowtitle": date})
      xbmcplugin.addDirectoryItem(addon_handler, url, listitem, isFolder=False)
    else:
      pass
  xbmcplugin.setContent(addon_handler, 'episodes')
  # End of list...
  xbmcplugin.endOfDirectory(addon_handler, True)

main()