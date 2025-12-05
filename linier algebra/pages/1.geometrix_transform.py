# pages/1_Geometric_Transform.py
import streamlit as st
from PIL import Image
import numpy as np
import os

st.title("Geometric Transformations")

def load_image(uploaded):
    return Image.open(uploaded).convert("RGB")

def build_affine(translate=(0,0), scale=(1,1), rotate=0, shear=(0,0), reflect=None):
    tx, ty = translate
    sx, sy = scale
    shx, shy = shear
    theta = np.deg2rad(rotate)

    T = np.array([[1, 0, tx], [0, 1, ty], [0, 0, 1]])
    R = np.array([[np.cos(theta), -np.sin(theta), 0],
                  [np.sin(theta), np.cos(theta), 0], [0,0,1]])
    S = np.array([[sx, 0, 0], [0, sy, 0], [0,0,1]])
    Sh = np.array([[1, shx, 0], [shy, 1, 0], [0,0,1]])
    Re = np.eye(3)
    if reflect == "x": Re = np.array([[1,0,0],[0,-1,0],[0,0,1]])
    if reflect == "y": Re = np.array([[-1,0,0],[0,1,0],[0,0,1]])
    if reflect == "origin": Re = np.array([[-1,0,0],[0,-1,0],[0,0,1]])

    return T @ R @ Sh @ S @ Re

def apply_transform(img, M):
    w, h = img.size
    cx, cy = w/2, h/2
    T1 = np.array([[1,0,-cx],[0,1,-cy],[0,0,1]])
    T2 = np.array([[1,0,cx],[0,1,cy],[0,0,1]])
    M_c = T2 @ M @ T1
    Minv = np.linalg.inv(M_c)
    coeffs = (Minv[0,0], Minv[0,1], Minv[0,2], Minv[1,0], Minv[1,1], Minv[1,2])
    return img.transform((w,h), Image.AFFINE, coeffs, Image.BICUBIC)

uploaded = st.file_uploader("Upload gambar", type=["png","jpg","jpeg"])
if uploaded:
    img = load_image(uploaded)
    c1, c2 = st.columns(2)
    with c1: st.image(img, "Original", use_container_width=True)

    choice = st.selectbox("Pilih Transformasi", 
              ["Translation","Scaling","Rotation","Shearing","Reflection"])

    if choice == "Translation":
        tx = st.slider("X", -300, 300, 0)
        ty = st.slider("Y", -300, 300, 0)
        M = build_affine(translate=(tx,ty))
    elif choice == "Scaling":
        sx = st.slider("Scale X", 0.1, 3.0, 1.0, 0.1)
        sy = st.slider("Scale Y", 0.1, 3.0, 1.0, 0.1)
        M = build_affine(scale=(sx,sy))
    elif choice == "Rotation":
        ang = st.slider("Sudut (°)", -180, 180, 0)
        M = build_affine(rotate=ang)
    elif choice == "Shearing":
        shx = st.slider("Shear X", -1.0, 1.0, 0.0, 0.05)
        shy = st.slider("Shear Y", -1.0, 1.0, 0.0, 0.05)
        M = build_affine(shear=(shx,shy))
    else:
        axis = st.selectbox("Axis", ["x","y","origin"])
        M = build_affine(reflect=axis)

    result = apply_transform(img, M)
    with c2:
        st.image(result, "Hasil Transformasi", use_container_width=True)
    st.write("**Matriks:**"); st.write(M)