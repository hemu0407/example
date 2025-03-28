import streamlit as st
from PIL import Image
import io

def compress_image(image, target_size_kb):
    """Compress an image to an exact target file size in KB using binary search."""
    target_size = target_size_kb * 1024  # Convert KB to Bytes
    img_bytes = io.BytesIO()
    
    # Binary search for the best quality
    low, high = 5, 95
    best_quality = high
    best_bytes = None
    
    while low <= high:
        mid = (low + high) // 2
        img_bytes.seek(0)
        image.save(img_bytes, format='JPEG', quality=mid)
        size = img_bytes.tell()
        
        if size <= target_size * 1.02 and size >= target_size * 0.98:
            return img_bytes
        elif size > target_size:
            high = mid - 1  # Reduce quality if too large
        else:
            low = mid + 1   # Increase quality if too small
        
        best_quality = mid
        best_bytes = img_bytes.getvalue()
    
    return io.BytesIO(best_bytes)  # Return best achieved compression

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
