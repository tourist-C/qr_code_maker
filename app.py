import streamlit as st
import numpy as np
import pandas as pd
import engine
import base64
from PIL import Image

import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from io import StringIO
import pandas as pd









# # @st.cache
# def load_data():
#     df = pd.read_clipboard(header=None)
#     df.columns = ['slide_id']
#     return df

copy_button = Button(label="Paste")

def main():

    # layout
    st.title('QR code generator')


    # col1
    col1, col2, col3 = st.beta_columns(3)
    col1.header("Step 1")
    col1.subheader("Paste Data")



    # col2 
    col2.header("Step 2")
    col2.subheader("Set Configuration")



    # col3
    col3.header("Step 3")
    col3.subheader("Right click copy")

    # config
    qr_size_sb = col2.slider("qr_size", 0, 100, 40)
    text_size_sb = col2.slider("text_size", 0, 20, 8)
    bg_size_sb = col2.slider("bg_size", 0, 200, 100)
    qr_pos_sb = col2.slider("qr_pos", 0, 200, 50)
    text_pos_sb = col2.slider("text_pos", 0, 200, 50)

    qr_size = qr_size_sb, qr_size_sb
    text_size = 200, text_size_sb
    bg_size = 150, bg_size_sb
    qr_pos = qr_pos_sb, 0
    text_pos = 0, text_pos_sb
    kwargs = dict(
                       qr_size=qr_size, 
                       text_size=text_size, 
                       bg_size=bg_size, 
                       qr_pos=qr_pos, 
                       text_pos=text_pos
    )

    # logic

    copy_button.js_on_event("button_click", CustomJS(code="""
        navigator.clipboard.readText().then(text => document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: text})))
        """))

    result = streamlit_bokeh_events(
            copy_button,
            events="GET_TEXT",
            key="get_text",
            refresh_on_update=False,
            override_height=75,
            debounce_time=0)

    if "GET_TEXT" in result:
        df = pd.read_csv(StringIO(result.get("GET_TEXT")), header=None)
        df.columns = ['slide_id']

        col1.write(f"Total number of slides: {len(df)}")
        col1.write(df)
        l = list(df['slide_id'])
        output = engine.create_many_qr_codes(l, kwargs)
        col3.image(output)

if __name__ == '__main__':
    main()