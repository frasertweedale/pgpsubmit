import cgi
import urlparse

import gnupg

from . import html


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
        self._gpg = gnupg.GPG(gnupghome=environ['GNUPGHOME'])

    def add_key(self):
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
            result = self._gpg.import_keys(text)
            div.add_child(html.H1(
                '{} key{} imported.'
                ''.format(result.count or 0, '' if result.count == 1 else 's')
            ))

        return div

    def list_keys(self):
        """Return HTML list of keys in keyring."""
        list = html.Ul()
        for key in sorted(
            self._gpg.list_keys(),
            key=lambda x: x['keyid'][-8:]
        ):
            keyid = str(key['keyid'][-8:])
            uid = cgi.escape(key['uids'][0].encode('UTF-8'))
            list.add_child(html.Li(keyid + ' ' + uid))
        return list
