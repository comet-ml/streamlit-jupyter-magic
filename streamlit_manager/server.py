# -*- coding: utf-8 -*-

import subprocess
import tempfile
import os
import time
import sys
import signal

from .utils import is_port_in_use

DEBUG = False
DATABASE = {} # instance_id: {"port": , "filename": , "timestamp":}

def launch_streamlit(code, port, filename=None):
    # I tried some lame security here, and also
    # RestrictedPython and restricted-functions, but
    # they don't play nicely with streamlits monkey-patched
    # environments
    preamble = ""

    if filename is None:
        temp_dir = tempfile.mkdtemp()
        with tempfile.NamedTemporaryFile('w+', suffix=".py", delete=False, dir=temp_dir) as fp:
            fp.write(preamble + code)
        fp.close()
        filename = fp.name

    # To use a specific version of python, use: "/usr/bin/python3.8 -m streamlit"
    # To add security, run as a specific user with no permissions
    # See "streamlit run --help" for more flags dealing with URLs, CORS, etc.
    command = [
        sys.executable,
        "-m",
        'streamlit',
        'run',
        '--server.fileWatcherType=none',
        '--logger.level=debug' if DEBUG else '--logger.level=error',
        '--server.headless=1',
        '--server.port=%s' % port,
        '--ui.hideTopBar=1',
        '--ui.hideSidebarNav=1',
        '--client.toolbarMode=minimal',
        filename,
    ]

    # Run in background
    if DEBUG:
        proc = subprocess.Popen(command)
    else:
        proc = subprocess.Popen(
            command,
            stdin=None,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    return proc.pid, filename

def get_pid(port):
    return [value["pid"] for value in DATABASE.values() if value["port"] == port][0]

def get_pids():
    return [value["pid"] for value in DATABASE.values()]

def get_ports():
    return [value["port"] for value in DATABASE.values()]

def get_filenames():
    return [value["filename"] for value in DATABASE.values()]

def get_streamlit_server_direct(instance_id, code, env=None):
    # First we see if this instance_id already has
    # a port associated with it:

    if instance_id in DATABASE:
        port = DATABASE[instance_id]["port"]
        if is_port_in_use("localhost", port):
            pid = get_pid(port)
            os.kill(pid, signal.SIGKILL)
        with open(DATABASE[instance_id]["filename"], "w") as fp:
            fp.write(code)
        pid, filename = launch_streamlit(code, port, DATABASE[instance_id]["filename"])
        DATABASE[instance_id]["pid"] = pid
        time.sleep(2)
        return DATABASE[instance_id]

    # Else, find empty port and start:

    port = 4000
    while is_port_in_use("localhost", port):
        port += 1

    DATABASE[instance_id] = {"port": port}

    if env:
        os.environ.update(env)
    
    pid, filename = launch_streamlit(code, port)

    DATABASE[instance_id]["filename"] = filename
    DATABASE[instance_id]["pid"] = pid
    DATABASE[instance_id]["timestamp"] = time.time()
    time.sleep(2)
    return DATABASE[instance_id]
