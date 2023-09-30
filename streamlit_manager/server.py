# -*- coding: utf-8 -*-

import subprocess
import tempfile
import os
import time
import sys
from threading import Thread

from .utils import is_port_in_use

DEBUG = False
DATABASE = {} # instance_id: {"port": , "filename": , "timestamp":}

def launch_streamlit(code, port):

    # I tried some lame security here, and also
    # RestrictedPython and restricted-functions, but
    # they don't play nicely with streamlits monkey-patched
    # environments
    preamble = ""

    filename = "streamlit-code-%s.py" % port
    with open(filename, "w") as fp:
        fp.write(preamble + code)
    
    #with tempfile.NamedTemporaryFile('w+', suffix=".py", delete=False) as fp:
    #    fp.write(preamble + code)
    #fp.close()

    #filename = fp.name

    # To use a specific version of python, use: "/usr/bin/python3.8 -m streamlit"
    # To add security, run as a specific user with no permissions
    # See "streamlit run --help" for more flags dealing with URLs, CORS, etc.
    command = [
        sys.executable,
        "-m",
        'streamlit',
        '--',
        'run',
        '--global.dataFrameSerialization=arrow',
        '--logger.level=debug',
        '--logger.enableRich=1',
        '--client.showErrorDetails=1',
        '--client.toolbarMode=minimal',
        '--runner.fixMatplotlib=1',
        '--server.fileWatcherType=auto',
        '--server.headless=1',
        '--server.port=%s' % port,
        '--server.scriptHealthCheckEnabled=1',
        '--ui.hideTopBar=1',
        '--ui.hideSidebarNav=1',
        '--theme.base=light',
        filename,
    ]

    # Run in background
    os.system(" ".join(command) + " &")

    return filename

def get_ports(db):
    return [value["port"] for value in db.values()]

def get_filenames(db):
    return [value["filename"] for value in db.values()]

def get_streamlit_server_direct(instance_id, code, env=None):
    # First we see if this instance_id already has
    # a port associated with it:

    if instance_id in DATABASE:
        port = DATABASE[instance_id]["port"]
        # Update file with latest code, if changed:
        with open(DATABASE[instance_id]["filename"], "w") as fp:
            fp.write(code)
        return DATABASE[instance_id]

    # Else, find an open port, and start a streamlit server:

    port = 4000
    while is_port_in_use("localhost", port):
        port += 1

    DATABASE[instance_id] = {"port": port}

    if env:
        os.environ.update(env)
    
    filename = launch_streamlit(code, port)

    DATABASE[instance_id]["filename"] = filename
    DATABASE[instance_id]["timestamp"] = time.time()
    time.sleep(2)
    return DATABASE[instance_id]


def start_manager_server(host, port):
    command = [sys.executable, "-m", "streamlit_manager", "--host", host, "--port", str(port)]
    if DEBUG:
        proc = subprocess.Popen(command)
    else:
        proc = subprocess.Popen(
            command,
            stdin=None,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

