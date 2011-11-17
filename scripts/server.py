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

from wsgiref.simple_server import make_server

import pgpsubmitlib.application

httpd = make_server('', 8000, pgpsubmitlib.application.Application)
print "Serving on port 8000..."
httpd.serve_forever()
