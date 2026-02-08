import streamlit as st
import os
from mistralai import Mistral, UserMessage, ImageURLChunk, TextChunk
from PIL import Image, ImageDraw
import io
import base64
import json
import re
import numpy as np
import cv2

# Page configuration
st.set_page_config(
    page_title="Kitchen Delivery Image Analyzer",
    page_icon="📦",
    layout="wide"
)

st.title("📦 Kitchen Delivery Image Analyzer")
st.markdown("Analyze kitchen delivery images using Mistral AI vision model")

# Initialize Mistral client
@st.cache_resource
def get_mistral_client():
    api_key = st.secrets.get("MISTRAL_API_KEY") or os.getenv("MISTRAL_API_KEY")
    if not api_key:
        st.error("❌ MISTRAL_API_KEY not found. Please set it in secrets or environment variables.")
        st.stop()
    return Mistral(api_key=api_key)

# Analysis prompt with bounding box request
ANALYSIS_PROMPT = """Please make full sentences when answering to the following questions, and answer in French:

1. Describe the overall context of the picture and specify if the picture is taken inside or outside?

2. How many boxes do you count on this picture? Are there logos on the boxes, if yes, which ones? Are there damaged boxes? Can you read brands on the boxes? If yes, how many boxes have brands?

3. If there is a box with "fragile" (or icon of a wine glass), is there a box on top?

4. If there is a box with arrows on it, are the arrows positioned vertically?

5. Is there a box that could contain a worksheet for a kitchen? If yes, is it stored on the side which is not protected by cardboard?

IMPORTANT: For bounding box detection, please provide coordinates as well. For each box you identify, if you can estimate its location, describe it using relative position (top-left, top-center, top-right, middle-left, center, middle-right, bottom-left, bottom-center, bottom-right) and describe the approximate size (small, medium, large).

Please structure your response clearly with numbered answers corresponding to each question."""

def analyze_image_with_mistral(image_data):
    """Send image to Mistral for analysis"""
    client = get_mistral_client()
    
    # Convert image to base64
    if isinstance(image_data, Image.Image):
        buffered = io.BytesIO()
        image_data.save(buffered, format="PNG")
        image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
    else:
        image_base64 = base64.b64encode(image_data).decode('utf-8')
    
    try:
        response = client.chat.complete(
            model="pixtral-12b-2409",
            messages=[
                UserMessage(
                    content=[
                        ImageURLChunk(image_url=f"data:image/png;base64,{image_base64}"),
                        TextChunk(text=ANALYSIS_PROMPT),
                    ],
                )
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"❌ Error analyzing image: {str(e)}")
        return None

def extract_box_count(analysis_text):
    """Extract box count from analysis text"""
    # Look for patterns like "I count X boxes" or "X boxes"
    patterns = [
        r'I count (\d+) box',
        r'count.*?(\d+) box',
        r'There are (\d+) box',
        r'(?:total of |approximately |)(\d+) box'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, analysis_text, re.IGNORECASE)
        if match:
            return int(match.group(1))
    return None

def add_grid_overlay(image):
    """Add a grid overlay to help with positioning reference"""
    img_array = np.array(image)
    h, w = img_array.shape[:2]
    
    # Create a copy for overlay
    overlay = img_array.copy()
    
    # Draw vertical lines (9 equal sections)
    for i in range(1, 9):
        x = int(w * i / 9)
        overlay[:, x:x+2] = [200, 200, 100]  # Yellow lines
    
    # Draw horizontal lines (9 equal sections)
    for i in range(1, 9):
        y = int(h * i / 9)
        overlay[y:y+2, :] = [200, 200, 100]  # Yellow lines
    
    return Image.fromarray(overlay)

def create_annotated_image(image, analysis_text):
    """Create an annotated version of the image with detected boxes highlighted"""
    img_array = np.array(image)
    h, w = img_array.shape[:2]
    
    # Create a copy for drawing
    annotated = img_array.copy()
    
    # Parse box locations from analysis (if provided)
    # This is a simplified approach - you could enhance this with more sophisticated parsing
    position_keywords = {
        'top-left': (0.1, 0.1, 0.3, 0.3),
        'top-center': (0.35, 0.1, 0.65, 0.3),
        'top-right': (0.7, 0.1, 0.9, 0.3),
        'middle-left': (0.1, 0.35, 0.3, 0.65),
        'center': (0.35, 0.35, 0.65, 0.65),
        'middle-right': (0.7, 0.35, 0.9, 0.65),
        'bottom-left': (0.1, 0.7, 0.3, 0.9),
        'bottom-center': (0.35, 0.7, 0.65, 0.9),
        'bottom-right': (0.7, 0.7, 0.9, 0.9),
    }
    
    # Highlight regions mentioned in the analysis
    for pos, (x1_norm, y1_norm, x2_norm, y2_norm) in position_keywords.items():
        if pos.lower() in analysis_text.lower():
            x1, y1 = int(x1_norm * w), int(y1_norm * h)
            x2, y2 = int(x2_norm * w), int(y2_norm * h)
            # Draw box with semi-transparent overlay
            cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 3)
    
    return Image.fromarray(annotated)

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    st.info("💡 To use this app, set MISTRAL_API_KEY in Streamlit secrets or environment variables.")
    st.markdown("### Setup Instructions:")
    st.markdown("""
    1. Get API key from [Mistral Console](https://console.mistral.ai/)
    2. For Streamlit Cloud: Add to App Secrets
    3. For local: Set environment variable or create `.streamlit/secrets.toml`
    """)
    
    show_grid = st.checkbox("Show position grid overlay", value=False)

# Main interface
col1, col2 = st.columns([1.5, 1])

with col1:
    st.subheader("📸 Image Input")
    
    uploaded_file = st.file_uploader(
        "Choose an image of kitchen delivery boxes",
        type=["jpg", "jpeg", "png", "webp"],
        help="Supported formats: JPG, PNG, WebP. Recommended size: 1-5 MB"
    )
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)

with col2:
    st.subheader("📊 Quick Stats")
    if uploaded_file is not None and st.button("🔍 Analyze Image", type="primary"):
        with st.spinner("🔄 Analyzing image with Mistral AI..."):
            # Analyze
            analysis_result = analyze_image_with_mistral(uploaded_file.getvalue())
            
            if analysis_result:
                # Extract box count
                box_count = extract_box_count(analysis_result)
                
                # Store in session state for display
                st.session_state.analysis_result = analysis_result
                st.session_state.box_count = box_count
                st.session_state.image = image

# Display results if available
if 'analysis_result' in st.session_state:
    st.divider()
    
    # Results section
    results_col1, results_col2, results_col3 = st.columns([1, 1, 1])
    
    with results_col1:
        if st.session_state.box_count is not None:
            st.metric(
                label="📦 Boxes Detected",
                value=st.session_state.box_count,
            )
        else:
            st.metric(label="📦 Boxes Detected", value="N/A")
    
    with results_col2:
        st.metric(label="✅ Analysis Status", value="Complete")
    
    with results_col3:
        if st.download_button(
            label="📥 Download Analysis",
            data=st.session_state.analysis_result,
            file_name="kitchen_analysis.txt",
            mime="text/plain"
        ):
            st.success("Downloaded!")
    
    # Display full analysis
    st.subheader("📋 Detailed Analysis")
    st.write(st.session_state.analysis_result)
    
    # Display annotated image
    st.subheader("🎯 Visual Analysis")
    
    tab1, tab2 = st.tabs(["Grid Reference", "Annotated"])
    
    with tab1:
        st.info("This grid helps identify box locations by dividing the image into 9 zones")
        grid_img = add_grid_overlay(st.session_state.image)
        st.image(grid_img, caption="Grid Reference (9 zones)", use_container_width=True)
    
    with tab2:
        annotated_img = create_annotated_image(st.session_state.image, st.session_state.analysis_result)
        st.image(annotated_img, caption="Detected Box Regions", use_container_width=True)
    
    # Summary section
    st.subheader("📌 Summary")
    summary_col1, summary_col2 = st.columns(2)
    
    with summary_col1:
        st.markdown("""
        **Analysis covered:**
        - ✓ Context and location (indoor/outdoor)
        - ✓ Box count and logos
        - ✓ Damage assessment
        - ✓ Brand identification
        - ✓ Fragile box detection
        - ✓ Arrow direction analysis
        - ✓ Worksheet container detection
        """)
    
    with summary_col2:
        st.markdown("""
        **Next steps:**
        1. Review the detailed analysis
        2. Check grid and annotated views
        3. Extract relevant information
        4. Download results for records
        """)

else:
    if uploaded_file is None:
        st.info("👆 **Upload an image** to begin analysis")
