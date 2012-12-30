# This file is part of pgpsubmit
# Copyright (C) 2011, 2012 Fraser Tweedale
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
import os
import re
import subprocess
import urlparse

from . import html


def paragraphs(lines):
    """Given iterable of lines, yield paragraphs of joined lines."""
    para = []
    for line in lines:
        if line:
            para.append(line)
        else:
            yield '\n'.join(para)
            para = []
    if para:
        yield '\n'.join(para)


def get_key_id(para):
    """Extract the key ID from the given paragraph."""
    return re.match(r'pub\s+\w+/([\dA-F]*)', para).group(1)


class Keyring(object):
    """GnuPG keyring interface.

    This class uses the value of GNUPGHOME from the WSGI environment.
    It will explode if it is not configured.
    """
    def __init__(self, environ):
        """Initialise the keyring interface for the given environ."""
        if 'GNUPGHOME' not in environ:
            raise EnvironmentError('GNUPGHOME must be specified')
        self._environ = environ

    @property
    def environ(self):
        env = dict(os.environ)
        env['GNUPGHOME'] = self._environ['GNUPGHOME']
        return env

    @property
    def executable(self):
        return self._environ['PGPSUBMITEXECUTABLE']

    def count_keys(self, text):
        gpg = subprocess.Popen(
            [self.executable],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=self.environ
        )
        stdout, stderr = gpg.communicate(text)
        return len([l for l in stdout.splitlines() if l.startswith("pub ")])

    def import_keys(self, text):
        """Import key(s) from the text, returning stdout and stderr."""
        gpg = subprocess.Popen(
            [self.executable, '--import'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=self.environ
        )
        return gpg.communicate(text)

    def process_environ(self):
        """Add the submitted key, returning HTML."""
        div = html.Div()

        text = None

        if self._environ['REQUEST_METHOD'] == 'POST':
            fields = cgi.FieldStorage(
                environ=self._environ,
                fp=self._environ['wsgi.input']
            )
            if 'text' in fields and fields['text'].value:
                text = fields['text'].value
            elif 'file' in fields and fields['file'].value:
                text = fields['file'].value

        if text:
            div.add_child(html.H1('Submission result'))
            if self.count_keys(text) <= 1:
                stdout, stderr = self.import_keys(text)
                pattern = re.compile('^gpg: (?!WARNING)')
                lines = (l for l in stderr.splitlines() if pattern.match(l))
                div.add_child(html.Pre('\n'.join(lines)))
            else:
                div.add_child(
                    html.P("ERROR: Keys must be submitted one at a time.")
                )

        return div

    def export(self):
        """Return ASCII armoured keyring."""
        args = [self.executable, '-a', '--export']
        return subprocess.check_output(args, env=self.environ)

    def fingerprint(self):
        """Return a string list of keys with fingerprints.

        The keys are ordered by key ID.
        """
        args = [self.executable, '--fingerprint']
        output = subprocess.check_output(args, env=self.environ)
        lines = output.splitlines()
        paras = paragraphs(lines[2:])
        return '\n\n'.join(sorted(paras, key=get_key_id))
