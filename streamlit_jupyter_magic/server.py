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
DATABASE = {}  # instance_id: {"page": , "timestamp": }
DIRECTORY = None


def get_pages():
    return [value["page"] for value in DATABASE.values()]


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

    # Update the page:
    subdir = os.path.join(DIRECTORY, "pages")
    os.makedirs(subdir, exist_ok=True)
    filename = os.path.join(subdir, "%d_page_%d.py" % (page, page))
    with open(filename, "w") as fp:
        fp.write(code)

    if start:
        page_0 = os.path.join(DIRECTORY, "page_0.py")
        # Make an empty top-level script:
        with open(page_0, "w") as fp:
            fp.write("")

        launch_streamlit(port, page_0)
        # Wait for app to get started:
        time.sleep(2)
    else:
        # Needed for some reason sometimes (streamlit bug?)
        def update():
            # Wait for after app displayed:
            time.sleep(2)
            # Force a chage:
            with open(os.path.join(filename), "a") as fp:
                fp.write(" ")

        t = threading.Thread(target=update)
        # So it doesn't go out of scope and get garbage collected:
        DATABASE[instance_id]["thread"] = t
        t.start()

    return DATABASE[instance_id]
