# Technical Documentation - Kitchen Delivery Image Analyzer

## Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│           Web Interface (Streamlit)                 │
│  ┌──────────────────────┬──────────────────────┐   │
│  │   Image Upload       │ Configuration Panel  │   │
│  └──────────────────────┴──────────────────────┘   │
└─────────────────────────────────────────────────────┘
                        │
                        ↓
┌─────────────────────────────────────────────────────┐
│      Image Processing Pipeline                      │
│  ┌──────────────────────────────────────────────┐  │
│  │ 1. Load image from upload                    │  │
│  │ 2. Convert to base64 (PNG format)           │  │
│  │ 3. Pass to Mistral API                      │  │
│  └──────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
                        │
                        ↓
┌─────────────────────────────────────────────────────┐
│    Mistral AI Vision API (pixtral-12b-2409)         │
│  ┌──────────────────────────────────────────────┐  │
│  │ Processes image with structured prompt      │  │
│  │ Returns detailed text analysis              │  │
│  └──────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
                        │
                        ↓
┌─────────────────────────────────────────────────────┐
│    Analysis Processing & Visualization              │
│  ┌──────────────┬──────────────┬──────────────┐   │
│  │ Box Count    │ Grid Overlay │ Annotations  │   │
│  │ Extraction   │ Generation   │ Drawing      │   │
│  └──────────────┴──────────────┴──────────────┘   │
└─────────────────────────────────────────────────────┘
                        │
                        ↓
┌─────────────────────────────────────────────────────┐
│         Results Display & Export                    │
│  ┌──────────────┬──────────────┬──────────────┐   │
│  │ Metrics      │ Visualizations│Downloads    │   │
│  │ Display      │ Tabs         │ Export      │   │
│  └──────────────┴──────────────┴──────────────┘   │
└─────────────────────────────────────────────────────┘
```

## Core Functions

### 1. `get_mistral_client()`
**Purpose**: Initialize and cache Mistral API client

```python
@st.cache_resource
def get_mistral_client():
    api_key = st.secrets.get("MISTRAL_API_KEY") or os.getenv("MISTRAL_API_KEY")
    if not api_key:
        st.error("❌ MISTRAL_API_KEY not found...")
        st.stop()
    return Mistral(api_key=api_key)
```

**Behavior**:
- Uses `@st.cache_resource` for single instance
- Checks secrets first, then environment
- Raises error if key not found
- Returns initialized Mistral client

### 2. `analyze_image_with_mistral(image_data)`
**Purpose**: Send image to Mistral for analysis

**Parameters**:
- `image_data` (bytes or PIL.Image): Image to analyze

**Process**:
1. Convert image to base64 if needed
2. Create API request with image and prompt
3. Call Pixtral 12B 2409 model
4. Return response text

**Error Handling**:
- Catches API exceptions
- Displays error message to user
- Returns None on failure

### 3. `extract_box_count(analysis_text)`
**Purpose**: Extract box count from analysis using regex

**Regex Patterns** (checked in order):
1. `'I count (\d+) box'`
2. `'count.*?(\d+) box'`
3. `'There are (\d+) box'`
4. `'(?:total of |approximately |)(\d+) box'`

**Returns**: Integer count or None

### 4. `add_grid_overlay(image)`
**Purpose**: Create 9-zone grid reference overlay

**Grid Layout**:
```
┌────────┬────────┬────────┐
│  1 | 1 │  1 | 2 │  1 | 3 │
├────────┼────────┼────────┤
│  2 | 1 │  2 | 2 │  2 | 3 │
├────────┼────────┼────────┤
│  3 | 1 │  3 | 2 │  3 | 3 │
└────────┴────────┴────────┘
```

**Features**:
- Yellow lines (RGB: 200, 200, 100)
- Divides image into 9 equal sections
- Helps identify box locations by position names

### 5. `create_annotated_image(image, analysis_text)`
**Purpose**: Highlight detected box regions

**Process**:
1. Parse position keywords from analysis
2. Map keywords to grid coordinates
3. Draw green rectangles on detected regions
4. Return annotated image

**Position Keywords**:
- Corners: top-left, top-right, bottom-left, bottom-right
- Edges: top-center, middle-left, middle-right, bottom-center
- Center: center

## State Management

### Session State Variables
```python
st.session_state.analysis_result  # Full analysis text
st.session_state.box_count        # Extracted box count
st.session_state.image            # Uploaded PIL Image
```

### Caching
- Mistral client: `@st.cache_resource`
- Prevents redundant API initialization
- Persists across reruns within session

## Analysis Prompt Structure

### Multi-Question Format
The prompt uses numbered questions for clarity:

```
1. Context Analysis
2. Box Assessment  
3. Fragile Handling
4. Arrow Orientation
5. Documentation Detection
```

### Prompt Optimization
- Uses full sentences requirement
- Requests spatial descriptions
- Includes position keywords (for annotation)
- Asks for relative sizing

## Image Processing Pipeline

### Format Support
- **Input**: JPG, PNG, WebP
- **Storage in Memory**: NumPy arrays
- **API Format**: Base64-encoded PNG
- **Output**: PIL Images

### Size Limits
- Maximum upload: 5 MB
- Recommended: 800×600 to 1920×1080
- API accepts up to 5 MB

### Conversion Process
```
Upload File → PIL Image → NumPy Array → Base64 → Mistral API
                                                      ↓
Mistral Response → Text Analysis → Parse → Display
```

## Error Handling

### API Errors
```python
try:
    message = client.messages.create(...)
    return message.content[0].text
except Exception as e:
    st.error(f"❌ Error analyzing image: {str(e)}")
    return None
```

### Configuration Errors
- Missing API key → User-friendly error message
- Invalid key → API returns authentication error

### Processing Errors
- Regex fails to extract count → Returns None
- Position parsing incomplete → Highlights available regions

## Performance Considerations

### Optimization Techniques
1. **Image Caching**: PIL images cached in session state
2. **Client Caching**: Mistral client reused via `@st.cache_resource`
3. **Lazy Loading**: Grid and annotations generated on-demand
4. **Stream Processing**: Results displayed incrementally

### Typical Processing Times
- Image upload & display: < 1 second
- Mistral API call: 10-30 seconds
- Image annotation: < 1 second
- Display rendering: < 1 second

**Total**: ~15-35 seconds per image

## API Integration Details

### Mistral Client Configuration
```python
client.messages.create(
    model="pixtral-12b-2409",  # Vision-capable model
    messages=[{
        "role": "user",
        "content": [
            {"type": "image", "format": "png", "data": image_base64},
            {"type": "text", "text": ANALYSIS_PROMPT}
        ]
    }]
)
```

### Request Structure
- **Model**: pixtral-12b-2409 (vision-enabled)
- **Input**: Multi-turn messages with image and text
- **Output**: Single text response
- **Cost**: ~$0.14 per 1M tokens

## Visualization Components

### 1. Metric Cards
```
┌─────────────────┐
│ 📦 Boxes        │
│ Detected: 8     │
└─────────────────┘
```

### 2. Tab Interface
- **Grid Reference**: Yellow grid overlay
- **Annotated**: Green highlighted regions

### 3. Download Button
- Format: Plain text (.txt)
- Content: Full analysis response
- Trigger: User click

## File Organization

### Application Files
- `streamlit_app.py`: Main application (271 lines)
  - 5 functions
  - 1 prompt constant
  - 3 main UI sections

### Configuration Files
- `.streamlit/config.toml`: Streamlit settings
- `.streamlit/secrets.toml`: API credentials (not in repo)
- `requirements.txt`: Python dependencies

### Documentation
- `README.md`: User-facing documentation
- `QUICKSTART.md`: Quick setup guide
- `TECHNICAL.md`: This file

## Future Enhancement Opportunities

### Bounding Box Improvements
- Request pixel coordinates from Mistral
- Use OpenCV for box detection
- Draw precise rectangles instead of zones

### Database Integration
- Store analysis results
- Track trends over time
- Support queries and reporting

### Batch Processing
- Upload multiple images
- Process in sequence or parallel
- Generate summary report

### Custom Prompts
- Allow user to modify questions
- Save prompt templates
- Support different analysis types

### Result Export
- CSV export with structured data
- JSON export for programmatic use
- PDF report generation

## Dependencies and Versions

| Package | Purpose | Min Version |
|---------|---------|-------------|
| streamlit | UI Framework | 1.0+ |
| mistralai | API Client | Latest |
| pillow | Image I/O | 8.0+ |
| opencv-python | Image Processing | 4.5+ |
| numpy | Numerical Ops | 1.19+ |
| python-dotenv | Env Loading | 0.19+ |

## Security Implementation

### API Key Protection
- Stored in `.streamlit/secrets.toml` (gitignored)
- Alternative: Environment variables
- Cloud: Use Streamlit secrets UI

### Data Privacy
- Images processed locally first
- Only base64 sent to Mistral
- No data retention on device
- User controls uploaded images

## Testing Recommendations

### Unit Tests
- Test box count extraction
- Test grid coordinate calculation
- Test image format conversion

### Integration Tests
- Test Mistral API connectivity
- Test full analysis pipeline
- Test error conditions

### UI Tests
- Test file upload
- Test button interactions
- Test tab switching
- Test download functionality

## Deployment Checklist

- [ ] API key configured (secrets or env)
- [ ] All dependencies installed
- [ ] Python syntax validated
- [ ] Mistral account active
- [ ] API quota confirmed
- [ ] Image formats supported
- [ ] Error messages tested
- [ ] Download functionality working
- [ ] Grid and annotations rendering

## Debugging Tips

### Enable Streamlit Logging
```bash
streamlit run streamlit_app.py --logger.level=debug
```

### Check API Status
```python
from mistralai import Mistral
client = Mistral(api_key="your_key")
# Test API connection
```

### Examine Session State
```python
st.write(st.session_state)  # Show all state variables
```

### Validate Images
```python
from PIL import Image
img = Image.open("test.jpg")
print(f"Size: {img.size}, Format: {img.format}")
```

---

**Last Updated**: February 7, 2026  
**Version**: 1.0  
**Status**: Production Ready
