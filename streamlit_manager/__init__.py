# -*- coding: utf-8 -*-

from .server import DEBUG, get_streamlit_server_direct
from .utils import in_colab_environment

try:
    from IPython.core.magic import register_cell_magic
    from IPython.core.magic_arguments import argument  # noqa: E501
    from IPython.core.magic_arguments import magic_arguments, parse_argstring
    from IPython.display import IFrame, Javascript, clear_output

    @magic_arguments()
    @argument(
        "-n",
        "--name",
        help="A unique name for the Streamlit Server",
        default="comet-default",
    )
    @argument(
        "-h",
        "--host",
        help="Host for the Streamlit Manager",
        default="localhost",  # noqa: E501
    )
    @argument(
        "-p", "--port", help="Port for the Streamlit Manager", default=5000
    )  # noqa: E501
    @argument(
        "--width",
        help="Width, percent or pixels, for the iframe",
        default="100%",  # noqa: E501
    )
    @argument(
        "--height", help="Height, in pixels, for the iframe", default="300px"
    )  # noqa: E501
    @register_cell_magic
    def streamlit(line, cell):
        args = parse_argstring(streamlit, line)
        results = get_streamlit_server_direct(args.name, cell)

        if in_colab_environment():
            clear_output(wait=True)
            return Javascript(
                """
(async ()=>{{
    fm = document.createElement('iframe');
    fm.src = (await google.colab.kernel.proxyPort({port}));
    fm.width = '{width}';
    fm.height = '{height}';
    fm.frameBorder = 0;
    document.body.append(fm);
}})();
""".format(
                    port=results["port"],
                    width=args.width,
                    height=args.height,
                )
            )
        else:
            return IFrame(
                src="http://%s:%s" % (args.host, results["port"]),
                width=args.width,
                height=args.height,
            )

except Exception:
    if DEBUG:
        print("%%streamlit magic is not available")
