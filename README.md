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
2. Currently doesn't work with multiple notebooks open simultaneously
