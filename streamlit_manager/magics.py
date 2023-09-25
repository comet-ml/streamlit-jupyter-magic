# -*- coding: utf-8 -*-

try:
    from IPython.display import IFrame
    from IPython.core.magic import register_cell_magic
    from IPython.core.magic_arguments import (
        argument, magic_arguments, parse_argstring
    )

    @magic_arguments()
    @argument('-n', '--name', help='A unique name for the Streamlit Server', default="default")
    @argument('-h', '--host', help='Host for the Streamlit Server', default="localhost")
    @register_cell_magic
    def streamlit(line, cell):
        from streamlit_manager.server import start_manager_server

        args = parse_argstring(my_cell_magic, line)

        start_manager_server(args.host, args.port)

        results = get_streamlit_server_direct(args.name, cell)
        return IFrame(src="http://%s:%s" % (args.host, results["port"]),
                      width="100%", height="700px")

except ImportError:
    pass
