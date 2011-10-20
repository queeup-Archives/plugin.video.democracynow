# -*- coding: utf-8 -*-

# Imports
import os, sys, time
import xbmc, xbmcgui, xbmcplugin, xbmcaddon

__settings__ = xbmcaddon.Addon(id='plugin.video.democracynow')
__icon__ = __settings__.getAddonInfo('icon')
__fanart__ = __settings__.getAddonInfo('fanart')
__language__ = __settings__.getLocalizedString

# Fanart
xbmcplugin.setPluginFanart(int(sys.argv[1]), __fanart__)

# Main
def Main():
  listitem_video = xbmcgui.ListItem('Video', thumbnailImage=__icon__)
  listitem_audio = xbmcgui.ListItem('Audio', thumbnailImage=__icon__)
  xbmcplugin.addDirectoryItem(int(sys.argv[1]), 'rss://www.democracynow.org/podcast-video.xml', listitem_video, True)
  xbmcplugin.addDirectoryItem(int(sys.argv[1]), 'rss://www.democracynow.org/podcast.xml', listitem_audio, True)

  xbmcplugin.setContent(int(sys.argv[1]), 'episodes')

  # End of list...
  xbmcplugin.endOfDirectory(int(sys.argv[1]), True)

Main()
