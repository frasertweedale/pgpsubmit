from wsgiref.simple_server import make_server

import pgpsubmitlib.application

httpd = make_server('', 8000, pgpsubmitlib.application.Application)
print "Serving on port 8000..."
httpd.serve_forever()
