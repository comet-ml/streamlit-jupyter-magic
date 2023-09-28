# -*- coding: utf-8 -*-

from .server import start_manager_server, get_streamlit_server_direct, DEBUG

try:
    from IPython.display import IFrame
    from IPython.core.magic import register_cell_magic
    from IPython.core.magic_arguments import (
        argument, magic_arguments, parse_argstring
    )

    @magic_arguments()
    @argument('-n', '--name', help='A unique name for the Streamlit Server', default="default")
    @argument('-h', '--host', help='Host for the Streamlit Manager', default="localhost")
    @argument('-p', '--port', help='Port for the Streamlit Manager', default=5000)
    @argument('--width', help='Width, percent or pixels, for the iframe', default="100%")
    @argument('--height', help='Height, in pixels, for the iframe', default="300px")
    @register_cell_magic
    def streamlit(line, cell):

        args = parse_argstring(streamlit, line)
        start_manager_server(args.host, args.port)
        results = get_streamlit_server_direct(args.name, cell)
        return IFrame(src="http://%s:%s" % (args.host, results["port"]),
                      width=args.width, height=args.height)

except Exception:
    if DEBUG:
        print("%%streamlit magic is not available")
