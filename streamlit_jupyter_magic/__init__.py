# -*- coding: utf-8 -*-
############################################
# Copyright (c) 2023                       #
# Streamlit Jupyter Magic Development Team #
# All rights reserved                      #
############################################

from .server import DEBUG, get_streamlit_page
from .utils import in_colab_environment

CELL_ID = None

try:
    from IPython import get_ipython
    from IPython.core.magic import register_cell_magic
    from IPython.core.magic_arguments import argument  # noqa: E501
    from IPython.core.magic_arguments import magic_arguments, parse_argstring
    from IPython.display import IFrame

    def pre_run_cell(info):
        global CELL_ID
        CELL_ID = info.cell_id

    get_ipython().events.register("pre_run_cell", pre_run_cell)

    @magic_arguments()
    @argument(
        "-n",
        "--name",
        help="A unique name for the Streamlit page",
        type=str,
        default=None,
    )
    @argument(
        "-h",
        "--host",
        help="Host for the Streamlit Server",
        default="localhost",  # noqa: E501
    )
    @argument(
        "-p", "--port", help="Port for the Streamlit Server", default=5000
    )  # noqa: E501
    @argument(
        "--width",
        help="Width, percent or pixels, for the iframe",
        default="100%",  # noqa: E501
    )
    @argument(
        "--height", help="Height, in pixels, for the iframe", default="300px"
    )  # noqa: E501
    @argument(
        "--use-colab-workaround",
        help="Use when colab won't open iframe",
        default=False,
        action="store_true",
    )
    @register_cell_magic
    def streamlit(line, cell):
        args = parse_argstring(streamlit, line)

        if args.name is None:
            args.name = CELL_ID if CELL_ID else "streamlit-default"

        results = get_streamlit_page(args.host, args.port, args.name, cell)

        if in_colab_environment():
            from google.colab import output

            if args.use_colab_workaround:
                output.serve_kernel_port_as_window(
                    args.port,
                    path="/page_%d" % results["page"],
                    anchor_text="Open streamlit app in window",
                )
            else:
                output.serve_kernel_port_as_iframe(
                    args.port,
                    path="/page_%d" % results["page"],
                    width=args.width,
                    height=args.height,
                )
        else:
            return IFrame(
                src="http://%s:%s/page_%d"
                % (
                    args.host,
                    args.port,
                    results["page"],
                ),
                width=args.width,
                height=args.height,
            )

except Exception:
    if DEBUG:
        print("%%streamlit magic is not available")
