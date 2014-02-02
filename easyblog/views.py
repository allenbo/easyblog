import os
from django.http import HttpResponse


def query_by_ext(ext):
  mimetype = {
          'css': 'text/css',
          'js': 'application/x-javascript',
          'png': 'image/png',
          'PNG': 'image/png',
          'jpg': 'image/jpeg',
          'JPG': 'image/jpeg',
          'JPEG': 'image/jpeg',
          'gif': 'image/gif',
          'GIF': 'image/gif',
          'xml': 'text/xml',
          'swf': 'application/x-shockwave-flash',
          'html': 'text/html',

      }
  
  return mimetype.get(ext, '')


def get_file(request, ext):
  path = request.path
  abspath = os.path.abspath('.') + path
  stream = open(abspath, 'rb').read()

  mimetype = query_by_ext(ext)
  return HttpResponse(stream, mimetype = mimetype)
