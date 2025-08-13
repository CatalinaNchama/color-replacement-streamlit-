import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.set_page_config(page_title="Color Replacement Tool", layout="centered")

st.title("🎨 Color Replacement in Image")
st.write("Upload an image, pick the color you want to replace, choose the new color, and click the button!")

# Upload image
uploaded_file = st.file_uploader("📂 Upload Image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    # Load image
    image = Image.open(uploaded_file).convert("RGB")
    img_array = np.array(image)

    st.subheader("📌 Original Image")
    st.image(img_array, caption="Original Image", use_container_width=True)

    # Step 1: Select target color
    st.subheader("🎯 Step 1: Select Target Color")
    target_color = st.color_picker("Pick the color you want to replace", "#ffffff")
    tolerance = st.slider("Tolerance", 0, 100, 30)

    # Step 2: Select new color
    st.subheader("🎨 Step 2: Select New Color")
    new_color = st.color_picker("Pick the new color", "#000000")

    # Button to replace color
    if st.button("✅ Replace Color"):
        # Convert hex colors to RGB
        target_rgb = tuple(int(target_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        new_rgb = tuple(int(new_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

        # Create a mask for pixels within tolerance
        lower_bound = np.array([max(0, c - tolerance) for c in target_rgb], dtype=np.uint8)
        upper_bound = np.array([min(255, c + tolerance) for c in target_rgb], dtype=np.uint8)
        mask = cv2.inRange(img_array, lower_bound, upper_bound)

        # Replace color
        result_img = img_array.copy()
        result_img[mask > 0] = new_rgb

        st.subheader("✅ Result")
        st.image(result_img, caption="Image with Replaced Color", use_container_width=True)

        # Download option
        result_pil = Image.fromarray(result_img)
        result_pil.save("output.png")
        with open("output.png", "rb") as file:
            st.download_button("📥 Download Image", data=file, file_name="color_replaced.png", mime="image/png")
