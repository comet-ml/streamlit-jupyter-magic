# -*- coding: utf-8 -*-

import os
import logging

from flask import Flask, request, jsonify

from .server import is_port_in_use, get_streamlit_server_direct, kill, get_pids, get_filenames, DEBUG, DATABASE


application = Flask(__name__)
application.logger.setLevel(logging.DEBUG if DEBUG else logging.CRITICAL)


@application.route("/get-streamlit-manager", methods=["POST", "GET"])
def get_streamlit_server():
    """
    Start (or reuse) streamlit server and return port number
    """
    if request.method == 'POST':
        data = request.get_json(force=True)

        code = data.get("code")
        instance_id = data.get("instanceId")
    else:
        code = request.args.get('code')
        instance_id = request.args.get('instanceId')

    return get_streamlit_server_direct(instance_id, code)


def main(host="localhost", port=5000):
    url = "http://%s:%s" % (host, port)

    if is_port_in_use(host, port):
        application.logger.info("Streamlit Manager Server already running on port %s" % port)
    else:
        application.logger.info("Starting Streamlit Manager Server on port %s..." % port)
        application.run(port=port)

        application.logger.info("Shutting down Streamlit Manager Server...")
        # Cleanup running streamlit servers and files:
        for pid in get_pids(DATABASE):
            kill(pid)
        for filename in get_filenames(DATABASE):
            os.remove(filename)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--host",
        type=str,
        default="localhost"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=5000
    )
    args = parser.parse_args()

    main(args.host, args.port)
