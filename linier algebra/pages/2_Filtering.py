import streamlit as st
import numpy as np
from PIL import Image
from scipy.signal import convolve2d

st.title("🔍 Image Filtering")

# Upload image
uploaded_file = st.file_uploader("Upload gambar", type=["jpg", "png", "jpeg"])

# Pilihan filter (kernel)
filter_options = {
    "Blur": np.array([[1, 1, 1],
                      [1, 1, 1],
                      [1, 1, 1]]) / 9,

    "Sharpen": np.array([[0, -1, 0],
                         [-1, 5, -1],
                         [0, -1, 0]]),

    "Edge Detection": np.array([[-1, -1, -1],
                                [-1, 8, -1],
                                [-1, -1, -1]])
}

filter_type = st.selectbox("Pilih jenis filter:", list(filter_options.keys()))
kernel = filter_options[filter_type]

if uploaded_file:
    img = Image.open(uploaded_file)
    img_arr = np.array(img)

    # Jika RGB, ubah tiap channel
    if len(img_arr.shape) == 3:
        result_arr = np.zeros_like(img_arr)
        for i in range(3):
            result_arr[:, :, i] = convolve2d(img_arr[:, :, i], kernel, mode="same", boundary="wrap")
    else:
        result_arr = convolve2d(img_arr, kernel, mode="same", boundary="wrap")

    # Normalisasi agar tidak keluar dari 0–255
    result_arr = np.clip(result_arr, 0, 255).astype(np.uint8)
    result = Image.fromarray(result_arr)

    # Tampilkan hasil berdampingan
    c1, c2 = st.columns(2)

    with c1:
        st.image(img, caption="Original", use_container_width=True)

    with c2:
        st.image(result, caption="Hasil Filter", use_container_width=True)
        st.write("**Kernel yang digunakan:**")
        st.write(kernel)
