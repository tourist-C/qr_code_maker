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


def main():

    st.set_page_config(page_title="Slide QR Code Generator", page_icon="icon.ico", layout='centered', initial_sidebar_state='auto')
    
    # layout
    st.title('Slide QR Code Generator')


    # col1
    col1, col2, col3 = st.beta_columns(3)

    with col1:
        st.header("Step 1")
        st.subheader("Paste Data")

        copy_button = Button(label="Paste", max_width =100)
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

    # col2 
    with col2:
        st.header("Step 2")
        st.subheader("Set Configuration")

        # config
        qr_size_sb = st.slider("QR code size", 0, 100, 40)
        text_size_sb = st.slider("Label text height", 0, 20, 8)
        bg_size_sb = st.slider("QR + label height", 0, 200, 100)
        qr_pos_sb = st.slider("QR vertical position", 0, 200, 50)
        text_pos_sb = st.slider("Label text position", 0, 200, 50)

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


    # col3
    with col3:
        st.header("Step 3")
        st.subheader("Right Click & Copy")

    if result:
        if "GET_TEXT" in result:
            # df = pd.read_csv(StringIO(result.get("GET_TEXT")), header=None)
            df = pd.DataFrame(StringIO(result.get("GET_TEXT")))

            df.columns = ['slide_id']

            # logic
            col1.write(f"Total number of slides: {len(df)}")
            col1.write(df)
            l = list(df['slide_id'])
            output = engine.create_many_qr_codes(l, kwargs)
            col3.image(output)



if __name__ == '__main__':
    main()