# coding: utf-8
from __future__ import unicode_literals

import re

from .common import InfoExtractor
from ..compat import (
    compat_urlparse,
    compat_parse_qs,
    compat_urllib_parse_urlparse,
)
from ..utils import (
    try_get,
    int_or_none,
)


class SeznamZpravyIE(InfoExtractor):
    _VALID_URL = (r'https://www\.seznamzpravy\.cz/iframe/player\?.*'
                  r'\&contentId=(?P<id>[0-9]*)\&.*')
    _TESTS = [{
        'url': 'https://www.seznamzpravy.cz/iframe/player?duration=320&serviceSlug=zpravy&src=https%3A%2F%2Fv39-a.sdn.szn.cz%2Fv_39%2Fvmd%2F5a2c47695fe86d1ccb7203f5%3Ffl%3Dmdk%2C69c40b2e%7C&itemType=video&autoPlay=false&title=%C5%A0%C5%A5astn%C3%A9%20pond%C4%9Bl%C3%AD%20Jind%C5%99icha%20%C5%A0%C3%ADdla&series=%C5%A0%C5%A5astn%C3%A9%20pond%C4%9Bl%C3%AD&serviceName=Seznam%20Zpr%C3%A1vy&poster=%2F%2Fd39-a.sdn.szn.cz%2Fd_39%2Fc_img_F_J%2FFWRTY.png%3Ffl%3Dcrs%2C600%2C337%2C7%7Cjpg%2C80%2C%2C1&width=16&height=9&cutFrom=0&cutTo=0&splVersion=VOD&contentId=323247&contextId=40592&showAdvert=true&collocation=premi%C3%A9r%20Andrej%20Babi%C5%A1%20%C4%8Cap%C3%AD%20hn%C3%ADzdo%20Sn%C4%9Bmovna%20St%C3%A1tn%C3%AD%20bezpe%C4%8Dnost%20imunita%20Jarom%C3%ADr%20Soukup%20Ji%C5%99%C3%AD%20Ov%C4%8D%C3%A1%C4%8Dek%20Milo%C5%A1%20Zeman%20Tomio%20Okamura&midrollPoint=%5B%5D&autoplayPossible=true&embed=&isVideoTooShortForPreroll=false&isVideoTooLongForPostroll=false&videoCommentOpKey=&videoCommentId=&version=5.0.23&dotService=zpravy&gemiusPrismIdentifier=zD3g7byfW5ekpXmxTVLaq5Srjw5i4hsYo0HY1aBwIe..27&zoneIdPreroll=seznam.pack.videospot&skipOffsetPreroll=5&sectionPrefixPreroll=%2Fzpravy%2Fstastnepondeli&zoneIdMidroll=seznam.pack.videospot&skipOffsetMidroll=5&sectionPrefixMidroll=%2Fzpravy%2Fstastnepondeli&zoneIdPostroll=seznam.pack.videospot&skipOffsetPostroll=5&sectionPrefixPostroll=%2Fzpravy%2Fstastnepondeli',
        'md5': 'c39de2f18b47e51dbc2875714eb865a3',
        'info_dict': {
            'id': '323247',
            'ext': 'mp4',
            'title': 'Šťastné pondělí Jindřicha Šídla',
            'thumbnail': 'https://d39-a.sdn.szn.cz/d_39/c_img_F_J/FWRTY.png?fl=crs,600,337,7|jpg,80,,1',
            'duration': 320.36,
        }
    }, {  # This uses meta JSON playlist with just 'Location' key
        'url': 'https://www.seznamzpravy.cz/iframe/player?duration=null&serviceSlug=zpravy&src=https%3A%2F%2Flive-a.sdn.szn.cz%2Fv_39%2F5a377f77c2d57c1483a09ac9%3Ffl%3Dmdk%2C4401d46a%7C&itemType=&autoPlay=false&title=P%C5%99edseda%20Nejvy%C5%A1%C5%A1%C3%ADho%20spr%C3%A1vn%C3%ADho%20soudu%20Josef%20Baxa%20%C5%BEiv%C4%9B%20na%20Seznamu&series=V%C3%BDzva&serviceName=Seznam%20Zpr%C3%A1vy&poster=%2F%2Fd39-a.sdn.szn.cz%2Fd_39%2Fc_img_H_J%2FmHIYB.jpeg%3Ffl%3Dcro%2C0%2C0%2C1280%2C720%7Cres%2C1200%2C%2C1%7Cjpg%2C80%2C%2C1&width=16&height=9&cutFrom=0&cutTo=0&splVersion=VOD&contentId=325037&contextId=40865&showAdvert=true&collocation=&autoplayPossible=true&embed=&isVideoTooShortForPreroll=false&isVideoTooLongForPostroll=false&videoCommentOpKey=&videoCommentId=&trim=default_16x9&noPrerollVideoLength=30&noMidrollVideoLength=0&noPostrollVideoLength=999999&version=5.0.24&dotService=zpravy&gemiusPrismIdentifier=zD3g7byfW5ekpXmxTVLaq5Srjw5i4hsYo0HY1aBwIe..27&zoneIdPreroll=seznam.pack.videospot&skipOffsetPreroll=5&sectionPrefixPreroll=%2Fzpravy%2Fvyzva&zoneIdPostroll=seznam.pack.videospot&skipOffsetPostroll=5&sectionPrefixPostroll=%2Fzpravy%2Fvyzva',
        # The server keeps altering the file for an unknown reason
        # 'md5': 'cf7e521eea0e946a2d03c511fa950de4',
        'info_dict': {
            'id': '325037',
            'ext': 'mp4',
            'title': 'Předseda Nejvyššího správního soudu Josef Baxa živě na Seznamu',
            'duration': 1534.437,
        }
    },
    ]

    @staticmethod
    def _extract_urls(webpage):
        return re.findall(
            r'<iframe\b[^>]+\bsrc=["\'](?P<url>https://www\.seznamzpravy\.cz'
            r'/iframe/player\?[^"\']*)["\']', webpage)

    def _real_extract(self, url):
        video_id = self._match_id(url)

        qs = compat_parse_qs(compat_urllib_parse_urlparse(url).query)

        for attr in ['src', 'splVersion', 'title', 'duration', 'poster']:
            assert attr in qs, 'No %s attribute in the query' % attr

        # The following magic was deterined by behavioral analysis of
        # the JS-based player. Without it, server returns HTTP 400.
        player_magic = "spl2,2,%s" % qs['splVersion'][0]
        src = qs['src'][0] + player_magic
        formatspage = self._download_json(src, video_id)
        if 'Location' in formatspage:
            src = formatspage['Location']
            formatspage = self._download_json(src, video_id)

        formats = []
        for k, v in try_get(formatspage, lambda x:
                            list(x['data']['mp4'].items()),
                            list) or []:
                formats.append({
                    'url': compat_urlparse.urljoin(src, v['url']),
                    'format_id': k,
                    'vcodec': v['codec'],
                    'tbr': int(v['bandwidth']) / 1000,
                    'width': int(v['resolution'][0]),
                    'height': int(v['resolution'][1]),
                    'duration': float(v['duration']) / 1000,
                })
        dash_url = try_get(formatspage,
                           lambda x: compat_urlparse.urljoin(
                               src,
                               x['pls']['dash']['url']
                           ), str)
        if dash_url:
            dash_formats = self._extract_mpd_formats(dash_url, video_id,
                                                     fatal=False)
            formats.extend(dash_formats)

        hls_url = try_get(formatspage,
                          lambda x: compat_urlparse.urljoin(
                              src,
                              x['pls']['hls']['url']
                          ), str)
        if hls_url:
            hls_formats = self._extract_m3u8_formats(hls_url, video_id,
                                                     'mp4', 'm3u8_native',
                                                     fatal=False)
            formats.extend(hls_formats)

        self._sort_formats(formats)
        return {
            'id': video_id,
            'title': qs['title'][0],
            'duration': int_or_none(qs['duration'][0]),
            'thumbnail': compat_urlparse.urljoin(src, qs['poster'][0]),
            'formats': formats,
        }
