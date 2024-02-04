# -*- coding: utf-8 -*-
############################################
# Copyright (c) 2023                       #
# Streamlit Jupyter Magic Development Team #
# All rights reserved                      #
############################################

import os
import subprocess
import sys
import tempfile
import threading
import time

DEBUG = False
DIRECTORY = None


def update(filename):
    # Wait for after app displayed:
    time.sleep(2)
    # Force a chage:
    with open(os.path.join(filename), "a") as fp:
        fp.write(" ")

def launch_streamlit(port, page_0):
    """
    Start a streamlit singleton server watching a tempdir/page_0.py and
    tempdir/pages/.
    """
    # See "streamlit run --help" for more flags dealing with URLs, CORS, etc.
    command = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        "--logger.level=debug" if DEBUG else "--logger.level=error",
        "--server.runOnSave=1",
        "--server.headless=1",
        "--server.port=%s" % port,
        "--ui.hideTopBar=1",
        "--ui.hideSidebarNav=1",
        "--client.toolbarMode=minimal",
        "--browser.gatherUsageStats=0",
        page_0,
    ]

    # Run in background
    if DEBUG:
        proc = subprocess.Popen(command, cwd=DIRECTORY)
    else:
        proc = subprocess.Popen(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            cwd=DIRECTORY,
        )

    return proc.pid


def get_streamlit_page(host, port, instance_id, code):
    """
    Get the details of a streamlit page for a particular
    instance_id (name).
    """
    global DIRECTORY

    start = False

    if DIRECTORY is None:
        DIRECTORY = tempfile.mkdtemp()
        start = True

    # Update the page:
    subdir = os.path.join(DIRECTORY, "pages")
    os.makedirs(subdir, exist_ok=True)
    page = "page_%s" % instance_id
    filename = os.path.join(subdir, page + ".py")

    with open(filename, "w") as fp:
        fp.write(code)

    if start:
        page_0 = "page_0.py"
        # Make an empty top-level script:
        with open(os.path.join(DIRECTORY, "page_0.py"), "w") as fp:
            fp.write("""
import streamlit as st
st.write("streamlit-jupyter-magic error; please restart kernel")
""")
        launch_streamlit(port, page_0)
        # Wait for app to get started:
        time.sleep(2)

    else:
        # Needed for some reason sometimes (streamlit bug?, or running in jupyter issue?)
        #t = threading.Thread(target=update, args=(filename,))
        #t.start()
        pass

    return {"page": page}
