from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
import threading
import datetime

from src.models import *

class ScoreServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(self.doctype_header())
            self.wfile.write(self.title("SOAB High Scores"))
            self.wfile.write(self.head())
            self.wfile.write(self.top())
            self.wfile.write(self.content())
            self.wfile.write(self.footer())
        elif self.path == '/main.js':
            self.send_response(200)
            self.send_header("Content-type", "text/javascript")
            self.end_headers()
            # return in-memory version of main.js
            self.wfile.write("""$(document).ready(function() {
                $('table').dataTable({
                    'aaSorting': [[0, 'desc']]
                });
            });""")
        else:
            self.send_response(404)
            self.end_headers()
        return

    def doctype_header(self):
        return """<!DOCTYPE html>
        <html lang='en'>
        <head>"""

    def title(self, title):
        return "<title>%s</title>" % title

    def head(self):
        return """<link rel='stylesheet' href='http://3530.nickpresta.ca/css/main.css' type='text/css'>
                  <link rel='stylesheet' href='http://3530.nickpresta.ca/js/DataTables-1.7.4/media/css/demo_table.css'>
                  <script type='text/javascript' src='http://ajax.googleapis.com/ajax/libs/jquery/1.4.4/jquery.min.js'></script>
                  <script type='text/javascript' src='http://3530.nickpresta.ca/js/DataTables-1.7.4/media/js/jquery.dataTables.min.js'></script>
                  <script type='text/javascript' src='/main.js'></script>
                  <style type="text/css">
                    tr,td {
                        background: transparent !important;
                    }
                    table tbody tr.first { background: rgba(212, 175, 55, 1) !important; }
                    table tbody tr.second { background: rgba(168, 168, 168, 0.4) !important; }
                    table tbody tr.third { background: rgba(150, 90, 56, 0.4) !important; }
                    table tbody tr.last { background: rgba(255, 105, 180, 0.4) !important; }
                  </style>
                  </head>"""

    def top(self):
        return "<h1>SOAB High Scores!</h1>"

    def content(self):
        out = """<div id="content"><p>Last updated: %s</p>""" % datetime.datetime.ctime(datetime.datetime.now())
        out += """<table width='100%' cellspacing="0" cellpadding="0" border="0" class="display"><thead>
                    <tr>
                        <th>Score</th>
                        <th>Name</th>
                        <th>Wins</th>
                        <th>Losses</th>
                        <th>Surrenders</th>
                        <th>Total Games</th>
                     </tr><thead><tbody>"""
        scores = [(s.score(), s.player_name, s.wins, s.losses, s.surrenders, s.total_games()) for s in Scores.query.all()]
        scores.sort(key=lambda t: t[0])
        scores.reverse()
        cl = ''
        max = scores[0][0]
        for i, s in enumerate(scores):
            if s[0] == max:
                cl = 'first'
            elif i == len(scores) - 1:
                cl = 'last'
            else:
                cl = ''
            out += "<tr class='%s'><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (cl, s[0], s[1], s[2], s[3], s[4], s[5])
        out += '</tbody></table></div>'
        return out

    def footer(self):
        return "<div id='footer'>&copy; Team Shroud 2010</div>";

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """ Handle the request in a separate thread """

if __name__ == '__main__':
    try:
        server = ThreadedHTTPServer(('131.104.48.113', 8081), ScoreServer)
        server.serve_forever()
    except KeyboardInterrupt:
        server.socket.close()
