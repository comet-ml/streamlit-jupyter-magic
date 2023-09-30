# -*- coding: utf-8 -*-

import subprocess
import psutil
import tempfile
import os
import time
import sys
from threading import Thread
import socket


DEBUG = False
DATABASE = {} # instance_id: {"port": , "filename": , "timestamp": , "pid":}

def is_port_in_use(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) == 0

def launch_streamlit(code, port):

    # I tried some lame security here, and also
    # RestrictedPython and restricted-functions, but
    # they don't play nicely with streamlits monkey-patched
    # environments
    preamble = ""

    with tempfile.NamedTemporaryFile('w+', suffix=".py", delete=False) as fp:
        fp.write(preamble + code)

    filename = fp.name

    # To use a specific version of python, use: "/usr/bin/python3.8 -m streamlit"
    # To add security, run as a specific user with no permissions
    # See "streamlit run --help" for more flags dealing with URLs, CORS, etc.
    command = [
        sys.executable,
        "-m",
        'streamlit',
        '--',
        'run',
        '--global.disableWatchdogWarning=0',
        '--global.developmentMode=0',
        '--global.unitTest=0',
        '--global.suppressDeprecationWarnings=1',
        '--global.dataFrameSerialization=arrow',
        '--logger.level=info',
        '--logger.enableRich=1',
        '--client.displayEnabled=1',
        '--client.showErrorDetails=1',
        '--client.toolbarMode=minimal',
        '--runner.magicEnabled=0',
        '--runner.installTracer=0',
        '--runner.fixMatplotlib=1',
        '--runner.postScriptGC=0',
        '--runner.fastReruns=0',
        '--runner.enforceSerializableSessionState=1',
        '--server.fileWatcherType=auto',
        '--server.headless=1',
        '--server.runOnSave=1',
        '--server.allowRunOnSave=1',
        '--server.port=%s' % port,
        '--server.scriptHealthCheckEnabled=1',
        '--server.maxMessageSize=10',
        '--server.enableWebsocketCompression=1',
        '--server.enableStaticServing=0',
        '--browser.gatherUsageStats=0',
        '--ui.hideTopBar=1',
        '--ui.hideSidebarNav=1',
        '--deprecation.showPyplotGlobalUse=0',
        '--theme.base=light',
        filename,
    ]

    if DEBUG:
        proc = subprocess.Popen(command)
    else:
        proc = subprocess.Popen(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        
    return proc.pid, filename

def kill(parent_pid):
    parent = psutil.Process(parent_pid)
    procs = parent.children(recursive=True)
    for child in procs:
        child.terminate()
    gone, alive = psutil.wait_procs(procs, timeout=3)
    for child in alive:
        child.kill()

def get_ports(db):
    return [value["port"] for value in db.values()]

def get_pids(db):
    return [value["pid"] for value in db.values()]

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
    
    pid, filename = launch_streamlit(code, port)

    DATABASE[instance_id]["pid"] = pid
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

