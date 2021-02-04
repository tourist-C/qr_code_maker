import streamlit as st
import numpy as np
import pandas as pd
import engine
import base64
from PIL import Image

# @st.cache
def load_data():
    df = pd.read_clipboard(header=None)
    df.columns = ['slide_id']
    return df
    
def main():
    # layout
    st.title('QR code generator')

    # col1
    col1, col2, col3 = st.beta_columns(3)
    col1.header("Step 1")

    # col2 
    col2.header("Step 2")

    # col3
    col3.header("Step 3")
    col3.subheader("Right click copy")

    # config
    qr_size_sb = col1.slider("qr_size", 0, 100, 40)
    text_size_sb = col1.slider("text_size", 0, 20, 8)
    bg_size_sb = col1.slider("bg_size", 0, 200, 100)
    qr_pos_sb = col1.slider("qr_pos", 0, 200, 50)
    text_pos_sb = col1.slider("text_pos", 0, 200, 50)

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
    if col2.button("Paste slide list"):
        df = load_data()
        col2.write(f"Total number of slides: {len(df)}")
        col2.write(df)
        l = list(df['slide_id'])
        output = engine.create_many_qr_codes(l, kwargs)
        col3.image(output)

if __name__ == '__main__':
    main()