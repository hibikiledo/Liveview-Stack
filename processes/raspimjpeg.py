__author__ = 'hibiki'

import eventlet

import subprocess

running = True

'''
  This module acts as a middle man between the robot and the server.

    It will receive command from the socket and send it ti FIFO pipe
    of Raspimjpeg process.

'''

COMMAND_PIPE = None

def handler(s, a):

    pass


def server(HOST, PORT):

    print("Server started on {}:{}".format(HOST, PORT))

    # Make sure to initialize command pipe
    init()

    server_socket = eventlet.listen((HOST, PORT))
    thread_pool = eventlet.GreenPool(10)

    while running:
        client_socket, address = server_socket.accept()
        thread_pool.spawn_n(handler, client_socket, address)



def init(**kwargs):

    global COMMAND_PIPE

    pipe_path = kwargs.get('pipe_path')

    COMMAND_PIPE = open(pipe_path, 'w')


