# app.py
import streamlit as st
from PIL import Image
import os

st.set_page_config(
    page_title="Group 11 - Image Processing",
    page_icon="camera",
    layout="wide"
)

st.title("Group 11 - Matrix Transformations in Image Processing")

st.markdown("### Anggota Kelompok")

names = ["Alya Mukhbita", "Nabila Maharani Yudhistiro", "Talytha Belva Clarisa", "Zahra Aulia Al Madani"]
files = ["alya.jpg", "nabila.jpg", "talytha.jpg", "zahra.jpg"]

cols = st.columns(4)
for i, col in enumerate(cols):
    with col:
        st.markdown(f"**{names[i]}**")
        path = os.path.join("assets", files[i])
        if os.path.exists(path):
            img = Image.open(path)
            img = img.resize((180, 180))
            st.image(img, use_container_width=True)  # DIUBAH DI SINI!
        else:
            st.image("https://via.placeholder.com/180?text=Foto+Tidak+Ada", use_container_width=True)

st.markdown("---")
st.markdown("""
**Fitur Aplikasi:**
- Transformasi Geometri (Translation, Scaling, Rotation, Shear, Reflection)
- Filtering (Blur & Sharpen)
- Tampilan multi-page yang rapi
""")