# -*- coding: utf-8 -*-

import psutil
import socket

def get_pid(port):
    connections = psutil.net_connections()
    for connection in connections:
        if connection.raddr:
            if connection.raddr.port == port:
                return connection.pid, connection.status
        if connection.laddr:
            if connection.laddr.port == port:
                return connection.pid, connection.status
    return None

def is_port_in_use(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) == 0

def kill(parent_pid):
    parent = psutil.Process(parent_pid)
    procs = parent.children(recursive=True)
    for child in procs:
        child.terminate()
    gone, alive = psutil.wait_procs(procs, timeout=3)
    for child in alive:
        child.kill()

