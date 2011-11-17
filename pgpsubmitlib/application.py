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

from . import html
from . import pgp


class Application(object):
    def __init__(self, environ, start_response):
        self._environ = environ
        self._start = start_response
        self._keyring = pgp.Keyring(environ)

    def __iter__(self):
        self._start('200 OK', [('Content-type', 'application/xhtml+xml')])
        head = html.Head()
        title = html.Title()
        title.add_child('PGP key submission')
        head.add_child(title)

        body = html.Body()

        body.add_child(html.H1("Keysigning party key submission form."))

        body.add_child(self._keyring.add_key())

        body.add_child(html.H2(
            "Paste ASCII-armored public key in the field below or "
            "select a file, then Submit."
        ))

        form = html.Form(method='POST', enctype='multipart/form-data')
        form.add_child(html.Textarea(name='text', cols=64, rows=18))
        form.add_child(html.Br())
        form.add_child(html.Input(type='file', name='file'))
        form.add_child(html.Br())
        form.add_child(html.Input(type='submit'))

        body.add_child(form)

        body.add_child(html.H2('Submitted keys:'))
        body.add_child(self._keyring.list_keys())

        attrs = {
            'xmlns': 'http://www.w3.org/1999/xhtml',
            'xml:lang': 'en'
        }
        doc = html.Html(**attrs)
        doc.add_child(head)
        doc.add_child(body)

        yield '<!DOCTYPE html PUBLIC ' \
            '"-//W3C//DTD XHTML 1.1//EN" ' \
            '"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">\n'
        for element in doc:
            yield element
