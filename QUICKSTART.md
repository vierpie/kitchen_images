# 🚀 Kitchen Delivery Image Analyzer - Quick Start Guide

## Overview

This application analyzes kitchen delivery images using Mistral AI's vision model to:
- Count boxes and identify logos
- Detect damaged or fragile boxes
- Read brand information
- Analyze box positioning and handling requirements
- Provide visual annotations with bounding box references

## Prerequisites

✅ **What you need:**
- Python 3.8 or higher
- A Mistral API key (free tier available: https://console.mistral.ai/)
- ~5-10 minutes for setup

## Step 1: Get Your Mistral API Key

1. Visit [console.mistral.ai](https://console.mistral.ai/)
2. Sign up or log in
3. Navigate to API Keys section
4. Generate a new API key
5. Copy the key (keep it secret!)

## Step 2: Install Dependencies

```bash
cd /workspaces/kitchen_images
pip install -r requirements.txt
```

**Expected packages:**
- streamlit (web interface)
- mistralai (API client)
- opencv-python (image processing)
- pillow (image handling)
- numpy (numerical operations)
- python-dotenv (environment variables)

## Step 3: Configure API Key

### Option A: Streamlit Secrets (Recommended for Cloud Deployment)
```bash
mkdir -p .streamlit
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

Edit `.streamlit/secrets.toml`:
```toml
MISTRAL_API_KEY = "your_api_key_here"
```

### Option B: Environment Variable (for Local Testing)
```bash
export MISTRAL_API_KEY="your_api_key_here"
streamlit run streamlit_app.py
```

### Option C: Cloud Deployment (Streamlit Cloud)
1. Push to GitHub
2. Deploy on Streamlit Cloud
3. Add secret in App Secrets:
   - Key: `MISTRAL_API_KEY`
   - Value: Your API key

## Step 4: Run the App

```bash
streamlit run streamlit_app.py
```

The app will open in your browser at `http://localhost:8501`

## How to Use

### Basic Workflow

1. **Upload Image**
   - Click file uploader
   - Select JPG, PNG, or WebP image (max 5 MB)
   - Image preview appears instantly

2. **Analyze**
   - Click the "Analyze Image" button
   - Wait 10-30 seconds for Mistral to process
   - Results appear automatically

3. **View Results**
   - **📦 Box Count**: Prominently displayed
   - **📋 Full Analysis**: Detailed responses to all 5 questions
   - **🎯 Visual Aids**: 
     - Grid overlay (9 zones for spatial reference)
     - Annotated image highlighting detected regions

4. **Download**
   - Click "Download Analysis" to save as text file
   - Perfect for records and reports

### Analysis Questions Covered

The app answers these specific questions:

1. **Context & Location** - Is it inside or outside?
2. **Box Inventory** - Total count, logos, damage, brands
3. **Fragile Handling** - Fragile markers and stacking
4. **Arrow Orientation** - Direction of handling arrows
5. **Documentation** - Worksheet/forms detection and placement

## Features Explained

### 📊 Visual Enhancements

**Grid Reference**
- Divides image into 9 zones (3×3 grid)
- Helps identify box locations
- Reference: top-left, top-center, top-right, etc.

**Annotated View**
- Auto-highlights regions mentioned in analysis
- Green boxes show detected positions
- Helps visualize model's understanding

### 📈 Metrics

**Box Count Metric**
- Extracted automatically from analysis
- Uses regex pattern matching
- Falls back to manual entry if needed

**Analysis Status**
- Shows completion status
- Indicates processing success

### 💾 Export Features

- Download analysis as `.txt` file
- Full text format with all responses
- Suitable for team sharing and archival

## Troubleshooting

### Issue: "MISTRAL_API_KEY not found"

**Cause**: API key not configured

**Solutions**:
1. Check `.streamlit/secrets.toml` exists and has correct key
2. Verify environment variable: `echo $MISTRAL_API_KEY`
3. Restart app: `streamlit run streamlit_app.py`

### Issue: "Image upload fails"

**Possible causes & fixes**:
- File too large (> 5 MB) → Compress image
- Unsupported format → Convert to JPG/PNG
- Corrupted file → Re-upload

### Issue: "Analysis returns empty or incomplete"

**Possible causes & fixes**:
- Poor image quality → Use clear, well-lit image
- API quota exceeded → Check Mistral console
- Temporary API issue → Retry in a moment

## Cost Information

**Mistral Pricing**:
- Free tier: 10,000 requests/month
- Pay-as-you-go: ~$0.14 per 1M tokens
- Each image typically costs < 1 cent

**Estimate**: 
- 100 images/month = ~$1-2
- 1000 images/month = ~$10-20

## Performance Tips

### Optimize Images
- Use 800×600 to 1920×1080 resolution
- Good lighting conditions
- Clear, uncluttered background
- Face camera directly at boxes

### Batch Processing
- Analyze one image at a time
- Check API usage regularly
- Plan for ~20 seconds per image

### Improve Results
- Ensure all boxes clearly visible
- Include full context (floor, surroundings)
- Don't crop important box regions

## Project Structure

```
kitchen_images/
├── streamlit_app.py           # Main application (271 lines)
├── requirements.txt           # Python dependencies
├── README.md                  # Full documentation
├── LICENSE                    # Apache 2.0
├── .gitignore                 # Git ignore rules
├── .streamlit/
│   ├── config.toml           # Streamlit configuration
│   └── secrets.toml.example   # API key template
└── .devcontainer/            # Dev container files
```

## Next Steps

### For Personal Use
1. Set up secrets locally
2. Test with sample kitchen images
3. Iterate on image quality

### For Team Deployment
1. Push to GitHub
2. Deploy on Streamlit Cloud
3. Share URL with team
4. Monitor API usage

### For Production
1. Set up dedicated API account
2. Implement usage logging
3. Add database for results
4. Create API key rotation schedule

## Advanced Customization

### Modify Prompt
Edit `ANALYSIS_PROMPT` in `streamlit_app.py` to change questions

### Change Visual Style
Edit colors in `.streamlit/config.toml`

### Add Features
- Multi-image upload
- Result database
- Comparison tools
- Export to CSV/JSON

## Support Resources

- **Mistral Docs**: https://docs.mistral.ai/
- **Streamlit Docs**: https://docs.streamlit.io/
- **GitHub Issues**: Report bugs and request features

## Security Considerations

⚠️ **Important**:
- Never commit API keys to version control
- Use `.streamlit/secrets.toml` for local dev (gitignored)
- Use environment variables or cloud secrets for production
- Rotate API keys periodically
- Monitor usage for unauthorized access

## License

This project is open source. See LICENSE file for details.

---

**Ready to get started?** 

1. Get your API key from [console.mistral.ai](https://console.mistral.ai/)
2. Run the setup steps above
3. Upload your first kitchen image and analyze!

Questions? Check the README.md for detailed documentation.
