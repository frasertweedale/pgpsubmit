# This file is part of pgpsubmit
# Copyright (C) 2011 Fraser Tweedale
#
# pgpsubmit is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pgpsubmit is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with pgpsubmit.  If not, see <http://www.gnu.org/licenses/>.

import cgi
import datetime
import hashlib

from . import html
from . import pgp


class Application(object):
    def __init__(self, environ, start_response):
        self._environ = environ
        self._start = start_response
        self._keyring = pgp.Keyring(environ)
        if 'PGPSUBMITSOURCEURL' not in environ:
            raise EnvironmentError(
                'PGPSUBMITSOURCEURL must be specified and must be a URL '
                'at which may be found the corresponding source of this '
                'program, pursuant to section 15 of the GNU Affero '
                'General Public License Version 3 (or the equivalent '
                'section of any later version).'
            )
        self._srcurl = environ['PGPSUBMITSOURCEURL']

    def __iter__(self):
        if 'keyring' in cgi.parse_qs(self._environ.get('QUERY_STRING', '')):
            self._start('200 OK', [('Content-type', 'text/plain')])
            yield bytes(self._keyring.export())
            return
        if 'keylist' in cgi.parse_qs(self._environ.get('QUERY_STRING', '')):
            self._start('200 OK', [('Content-type', 'text/plain')])
            yield bytes(self._keyring.fingerprint())
            return
        self._start('200 OK', [('Content-type', 'application/xhtml+xml')])
        head = html.Head()
        title = html.Title()
        title.add_child('PGP key submission')
        head.add_child(title)

        body = html.Body()

        body.add_child(html.H1("Keysigning party key submission form."))

        until = None
        now = datetime.datetime.now()
        if 'PGPSUBMITUNTIL' in self._environ:
            until = datetime.datetime(
                *map(int, self._environ['PGPSUBMITUNTIL'].split('.'))
            )
        if not until or now < until:
            body.add_child(self._keyring.add_key())

            body.add_child(html.H2(
                "Paste ASCII-armored public key in the field below or "
                "select a file, then Submit."
            ))

            if until:
                delta = until - now
                msg = []
                days = delta.days
                if days:
                    msg.append(
                        '{} day{}'.format(days, '' if days == 1 else 's'))
                hours, seconds = divmod(delta.seconds, 3600)
                if hours or msg:
                    msg.append(
                        '{} hour{}'.format(hours, '' if hours == 1 else 's'))
                minutes, seconds = divmod(seconds, 60)
                if minutes or msg:
                    msg.append('{} minute{}'.format(
                        minutes, '' if minutes == 1 else 's'))
                msg.append(
                    '{} second{}'.format(seconds, '' if seconds == 1 else 's'))
                remaining = msg[0] if len(msg) == 1 \
                    else ' and '.join((', '.join(msg[:-1]), msg[-1]))
                body.add_child(html.H2(
                    "Key submission ends in {}.".format(remaining)
                ))

            form = html.Form(
                action='',
                method='post',
                enctype='multipart/form-data'
            )
            div = html.Div(
                html.Textarea(name='text', cols=64, rows=18),
                html.Br(),
                html.Input(type='file', name='file'),
                html.Br(),
                html.Input(type='submit')
            )
            form.add_child(div)

            body.add_child(form)
        else:
            body.add_child(html.H2('Key submission has ended.'))

        body.add_child(html.H2('Submitted keys:'))

        # get list of keys with fingerprints
        fprs = self._keyring.fingerprint()

        if not until \
                or 'PGPSUBMITDOWNLOADEARLY' in self._environ \
                or now >= until:
            a = html.A('Download keyring', href='?keyring=1')
            body.add_child(html.P(a))

            a = html.A('Download key list', href='?keylist=1')
            md5 = hashlib.md5(fprs).hexdigest()
            sha1 = hashlib.sha1(fprs).hexdigest()
            p = html.P(a, html.Br(), 'md5 = ', md5, html.Br(), 'sha1 = ', sha1)
            body.add_child(p)
        else:
            body.add_child(html.P(
                'Keyring and key list will be available for download '
                'when key submission has ended.'
            ))

        body.add_child(html.Pre(fprs))

        body.add_child(html.Hr())
        a = html.A(self._srcurl, href=self._srcurl)
        p = html.P()
        p.add_child(
            'pgpsubmit is free software, released under the terms of '
            'the GNU Affero General Public License.  You can access '
            'the Corresponding Source at '
        )
        p.add_child(a)
        p.add_child('.')
        body.add_child(p)

        attrs = {
            'xmlns': 'http://www.w3.org/1999/xhtml',
            'xml:lang': 'en'
        }
        doc = html.Html(**attrs)
        doc.add_child(head)
        doc.add_child(body)

        yield '<?xml version="1.0" encoding="UTF-8"?>\n'
        yield '<!DOCTYPE html PUBLIC ' \
            '"-//W3C//DTD XHTML 1.1//EN" ' \
            '"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">\n'
        for element in doc:
            yield element
