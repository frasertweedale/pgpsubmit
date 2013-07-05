WSGI OpenPGP public key submission system
=========================================

pgpsubmit is a simple WSGI_ application that can be used for collecting
OpenPGP_ public keys on a keyring e.g. for a keysigning party.

.. _WSGI: http://www.python.org/dev/peps/pep-3333/

Features include:

- submission deadline and "time remaining" display
- keyring and key list export (with MD5 and SHA-1 hashes)
- configured entirely through environment


Dependencies
------------

- `GnuPG`__
- A WSGI capable web server (e.g. Apache_ with `mod_wsgi`__).

.. _OpenPGP: http://en.wikipedia.org/wiki/Pretty_Good_Privacy
.. _Apache: http://httpd.apache.org/
__ http://gnupg.org/
__ http://code.google.com/p/modwsgi/


Configuration
-------------

Three WSGI ``environ`` variables must be set:

``PGPSUBMITEXECUTABLE``
  Name or full path of the GnuPG executable.  If the value does not
  begin with ``"/"``, an executable will be looked for on ``PATH``
  by the normal mechanism.  If using Apache httpd and encountering
  ``OSError``, try specifying the full path to the GnuPG executable.
``GNUPGHOME``
  The GnuPG home directory.  Must be writable by the user running the
  application.  Multiple pgpsubmit instances could be run in parallel,
  each with a different ``GNUPGHOME``.
``PGPSUBMITSOURCEURL``
  URL at which may be found the corresponding source of pgpsubmit,
  pursuant to section 15 of the AGPL.  If you run a modified version of
  pgpsubmit, the source code for that modified version must be available
  at this URL.

There are some other configuration variables for controlling
submission deadlines:

``PGPSUBMITUNTIL``
  Specify a deadline for submission.  After this time, submission will
  be disabled, and a message to effect of same will appear.  While the
  deadline looms, time remaining will be displayed.  The format is
  ``'Y.M.D[.H[.M[.S]]]'``.
``PGPSUBMITDOWNLOADEARLY``
  If a deadline is set, links to download the keyring and key list are
  not shown until the submission deadline is reached.  Settings this
  environment variable (to any value) causes these links to be shown
  regardless of whether or not the deadline has passed.

A configuration for Apache with mod_wsgi might be::

    <Directory /usr/home/joe/pgpsubmit>
        Order allow,deny
        Allow from all
    </Directory>

    <VirtualHost *:80>
        ServerAdmin joe@example.com
        ServerName pgpsubmit.example.com
        DocumentRoot "/usr/home/joe/pgpsubmit"

        WSGIScriptAlias / /usr/home/joe/pgpsubmit/scripts/pgpsubmit.wsgi
        SetEnv PGPSUBMITEXECUTABLE /usr/local/bin/gpg
        SetEnv GNUPGHOME /usr/home/joe/.pgpsubmit
        SetEnv PGPSUBMITSOURCEURL https://github.com/frasertweedale/pgpsubmit
        SetEnv PGPSUBMITUNTIL 2011.12.31.18.30
    </VirtualHost>


License
-------

pgpsubmit is free software: you can redistribute it and/or modify
it under the terms of the `GNU Affero General Public License`__ as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

__ http://www.gnu.org/licenses/agpl.html


Contributing
------------

The pgpsubmit source code is available from
https://github.com/frasertweedale/pgpsubmit.

Bug reports, patches, feature requests, code review and
documentation are welcomed.

To submit a patch, please use ``git send-email`` or generate a pull
request.  Write a `well formed commit message`_.  If your patch is
nontrivial, update the copyright notice at the top of each changed
file.

.. _well formed commit message: http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html
