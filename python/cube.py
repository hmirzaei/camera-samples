import pygame
from pygame.locals import *
import json

from OpenGL.GL import *
from OpenGL.GLU import *

from http.server import BaseHTTPRequestHandler, HTTPServer
import logging

verticies = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
    )

edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
    )

def Cube():
    glColor3f(1,1,1)
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()

def Axes():
  qobj = gluNewQuadric();
  gluQuadricDrawStyle( qobj, GLU_FILL );

  glPushMatrix();
  glColor3f(1,0,0);
  glRotatef(90,0,1,0);
  gluCylinder(qobj, 0.05, 0.05, 3, 10, 16);
  glPopMatrix();

  glPushMatrix();
  glColor3f(0,1,0);
  glRotatef(-90,1,0,0);
  gluCylinder(qobj, 0.05, 0.05, 3, 10, 16);
  glPopMatrix();

  glPushMatrix();
  glColor3f(0,0,1);
  gluCylinder(qobj, 0.05, 0.05, 3, 10, 16);
  glPopMatrix();


class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        # logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
        #         str(self.path), str(self.headers), post_data.decode('utf-8'))

        rpy = json.loads(post_data.decode('utf-8'))


        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity();
        gluLookAt(-10,0,0,0,0,0,0,0,1)

        glRotatef(-rpy['y'], 0, 0, 1)
        glRotatef(rpy['p'], 0, 1, 0)
        glRotatef(rpy['r'], 1, 0, 0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        Cube()
        Axes()
        pygame.display.flip()
        pygame.time.wait(10)


def run(server_class=HTTPServer, handler_class=S, port=8000):
    logging.basicConfig(level=logging.ERROR)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')



def main():
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity();
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    run()
    # while True:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             pygame.quit()
    #             quit()
        

    
main()
