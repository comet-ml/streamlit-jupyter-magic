# streamlit-jupyter-magic

A local streamlit server for Jupyter environments, and more.

## Installation

```python
pip install streamlit-jupyter-magic
```

## Example

```python
# Cell:
import streamlit_jupyter_magic

# Cell:
%%streamlit 

import streamlit as st

st.title("This is a Test")

if st.button("Click me!"):
    st.button("Click me again!")
```

Results in the following:

![Jupyter Magic Demo](https://github.com/comet-ml/streamlit-jupyter-magic/blob/main/images/demo.gif?raw=true)

## Limitations

1. Currently doesn't work on colab, due to a couple of colab bugs
2. Currently doesn't work in multiple, simultaneous notebooks in same environment

## Flags

Use any of these flags with `%%streamlit FLAGS...`

* `--port NUMBER` - set the port for streamlit to use; default is 5000
* `--host HOST` - set the host for streamlit to use; default is "localhost"
* `--name NAME` - set the name (a unique instance id) for this cell app; default uses Jupyter cell ID
* `--width VALUE` - set the app width, such as "100%" 
* `--height VALUE` - set the app height, such as "700px" 
* `--use-colab-workaround` - on colab, use a window rather than iframe, but still doesn't work (colab bug)

## Under the hood

`streamlit-jupyter-magic` uses streamlit pages to keep memory usage down.

The magic code can be found in: [streamlit_jupyter_magic/\_\_init__.py](https://github.com/comet-ml/streamlit-jupyter-magic/blob/main/streamlit_jupyter_magic/__init__.py)

The rest of the code is utility code for managing the streamlit server.
