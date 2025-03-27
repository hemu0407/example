import streamlit as st
from PIL import Image
import io

def compress_image(image, target_size_kb):
    """Compress an image to a target file size in KB."""
    target_size = target_size_kb * 1024  # Convert KB to Bytes
    quality = 95  # Start with high quality
    img_bytes = io.BytesIO()
    
    while quality > 10:
        img_bytes.seek(0)
        image.save(img_bytes, format='JPEG', quality=quality)
        size = img_bytes.tell()
        
        if size <= target_size:
            return img_bytes
        
        quality -= 5  # Reduce quality gradually
    
    return img_bytes  # Return the best achieved compression

# Streamlit UI
st.title("Image Compressor App")
st.write("Upload an image and choose a target file size to compress it.")

uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Open image
    image = Image.open(uploaded_file)
    st.image(image, caption="Original Image", use_column_width=True)
    
    # Choose target size
    target_size_kb = st.slider("Select Target Size (KB)", min_value=20, max_value=700, value=100)
    
    if st.button("Compress Image"):
        compressed_image_bytes = compress_image(image, target_size_kb)
        
        # Create download button
        st.download_button(
            label="Download Compressed Image",
            data=compressed_image_bytes.getvalue(),
            file_name="compressed_image.jpg",
            mime="image/jpeg"
        )

# Requirements (Save this as requirements.txt)
# streamlit
# pillow
