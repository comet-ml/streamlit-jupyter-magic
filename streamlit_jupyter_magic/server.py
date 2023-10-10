# -*- coding: utf-8 -*-
############################################
# Copyright (c) 2023                       #
# Streamlit Jupyter Magic Development Team #
# All rights reserved                      #
############################################

import subprocess
import tempfile
import os
import time
import sys
import signal

from .utils import is_port_in_use

DEBUG = False
DATABASE = {} # instance_id: {"page": , "timestamp": }
DIRECTORY = None

def get_pages():
    return [value["page"] for value in DATABASE.values()]

def launch_streamlit(port):
    """
    Start a streamlit singleton server watching a tempdir/page_0.py and
    tempdir/pages/.
    """
    directory = tempfile.mkdtemp()
    page_0 = os.path.join(directory, "page_0.py")
    # Make an empty top-level script:
    with open(page_0, "w") as fp:
        fp.write("")

    # See "streamlit run --help" for more flags dealing with URLs, CORS, etc.
    command = [
        sys.executable,
        "-m",
        'streamlit',
        'run',
        '--logger.level=debug' if DEBUG else '--logger.level=error',
        '--server.runOnSave=1',
        '--server.headless=1',
        '--server.port=%s' % port,
        '--ui.hideTopBar=1',
        '--ui.hideSidebarNav=1',
        '--client.toolbarMode=minimal',
        page_0,
    ]

    # Run in background
    if DEBUG:
        proc = subprocess.Popen(command)
    else:
        proc = subprocess.Popen(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    return proc.pid, directory

def get_streamlit_page(host, port, instance_id, code):
    """
    Get the details of a streamlit page for a particular
    instance_id (name). 
    """
    global DIRECTORY
    if not is_port_in_use(host, port):
        pid, DIRECTORY = launch_streamlit(port)
        time.sleep(2)
    elif DIRECTORY is None:
        raise Exception("Port %s is unavailable; " % port)

    # First we see if this instance_id already has
    # a page associated with it:
    if instance_id in DATABASE:
        page = DATABASE[instance_id]["page"]
    else:
        # Get next page:
        pages = get_pages()
        if pages:
            page = max(pages) + 1
        else:
            page = 1
        # Add to database:
        DATABASE[instance_id] = {
            "page": page,
            "timestamp": time.time(),
        }

    subdir = os.path.join(DIRECTORY, "pages")
    if not os.path.isdir(subdir):
        os.makedirs(subdir, exist_ok=False)
    filename = os.path.join(subdir, "%d_page_%d.py" % (page, page))
    with open(filename, "w") as fp:
        fp.write(code)

    return DATABASE[instance_id]
