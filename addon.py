# -*- coding: utf-8 -*-

import sys
import xbmcgui
import xbmcplugin
import xbmcaddon
import requests
import re
import html


addon = xbmcaddon.Addon()
addon_icon = addon.getAddonInfo('icon')
addon_fanart = addon.getAddonInfo('fanart')

try:
    addon_handler = int(sys.argv[1])
except IndexError:
    addon_handler = int()

# Fanart
xbmcplugin.setPluginFanart(addon_handler, addon_fanart)

thumb_replacement = 'https://assets.democracynow.org/assets/default_content_image-354f4555cc64afadc730d64243c658dd0af1f330152adcda6c4900cb4a26f082.jpg'
current_show = 'http://www.democracynow.org/api/1/current_show'


def get_json(url):
    r = requests.get(url).json()
    return r


def remove_html_tags(text):
    """Remove html tags from a string"""
    clean = re.compile(r'<[^>]+>')
    return re.sub(clean, '', text)


def decode_html_entities(text):
    """Decode html entities from a string"""
    return html.unescape(text)


def string_correction(_str):
    return remove_html_tags(decode_html_entities(_str))


class Main:
    def __init__(self):
        for show in get_json(current_show)['media']:
            if 'High' in show['title']:
                url = show['src']
                title = 'Full Show'
                thumb = thumb_replacement
                summary = ''
                listitem = xbmcgui.ListItem(title)
                listitem.setInfo(type="video",
                                 infoLabels={"title": title,
                                             "plot": summary})
                listitem.setArt({"icon": "DefaultVideoBig.png",
                                 "thumb": thumb,
                                 "fanart": addon_fanart})
                listitem.setProperty('IsPlayable', 'true')
                xbmcplugin.addDirectoryItem(addon_handler, url, listitem, isFolder=False)

        for video in get_json(current_show)['items']:
            if video['itemType'] == 'headline_section':
                title = u'Headlines'
            else:
                title = string_correction(video['title'])

            url = None
            for _video in video['media']:
                if 'High' in _video['title']:
                    url = _video['src']
                else:
                    pass

            try:
                thumb = video['images'][0]['url']
            except KeyError:
                thumb = thumb_replacement

            try:
                duration = int(video['duration'])
            except KeyError:
                duration = ''

            try:
                summary = string_correction(video['summary'])
            except KeyError:
                summary = ''

            if url is not None:
                listitem = xbmcgui.ListItem(title)
                listitem.setInfo(type="video",
                                 infoLabels={"title": title,
                                             "plot": summary,
                                             "duration": duration})
                listitem.setArt({"icon": "DefaultVideoBig.png",
                                 "thumb": thumb,
                                 "fanart": addon_fanart})
                listitem.setProperty('IsPlayable', 'true')
                xbmcplugin.addDirectoryItem(addon_handler, url, listitem, isFolder=False)
            else:
                pass
        xbmcplugin.setContent(addon_handler, 'episodes')
        xbmcplugin.endOfDirectory(addon_handler, True)


if __name__ == '__main__':
    Main()
