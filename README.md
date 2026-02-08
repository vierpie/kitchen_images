# 📦 Kitchen Delivery Image Analyzer

A Streamlit application for analyzing kitchen delivery box images using Mistral AI's vision model. This tool automatically detects and analyzes boxes, logos, damage, and other delivery-related characteristics.

## Features

✨ **AI-Powered Analysis** - Uses Mistral's Pixtral vision model for accurate image recognition

📦 **Box Detection** - Counts boxes and identifies:
- Logos and branding on boxes
- Damaged or compromised boxes
- Fragile markings and handling symbols
- Arrow directions on boxes
- Potential worksheet/documentation containers

📊 **Visual Annotations** - Provides:
- 9-zone grid overlay for spatial reference
- Annotated image highlighting detected regions
- Position-based box identification

📥 **Export Capabilities** - Download detailed analysis reports as text files

## Installation

### Prerequisites
- Python 3.8+
- Mistral API key (get it from [console.mistral.ai](https://console.mistral.ai/))

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd kitchen_images
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Mistral API Key**
   
   **Option A: For local development**
   ```bash
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
   ```
   Then edit `.streamlit/secrets.toml` and add your API key:
   ```toml
   MISTRAL_API_KEY = "your_actual_api_key_here"
   ```
   
   **Option B: For Streamlit Cloud**
   - Go to your app settings
   - Navigate to Secrets
   - Add: `MISTRAL_API_KEY = "your_actual_api_key_here"`
   
   **Option C: Environment variable**
   ```bash
   export MISTRAL_API_KEY="your_actual_api_key_here"
   ```

4. **Run the app**
   ```bash
   streamlit run streamlit_app.py
   ```

## Usage

1. **Upload Image** - Click to upload a kitchen delivery image (JPG, PNG, or WebP)

2. **Analyze** - Click the "Analyze Image" button to process with Mistral AI

3. **View Results**:
   - 📦 Box count displayed as a metric card
   - 📋 Full detailed analysis with all questions answered
   - 🎯 Visual annotations with grid reference
   - 📥 Download complete analysis report

## Prompt Details

The analysis covers:

1. **Context Analysis** - Overall scene description and indoor/outdoor location
2. **Box Assessment** - Count, logos, damage, and brand identification
3. **Fragile Handling** - Detection of fragile markings and stacking assessment
4. **Arrow Direction** - Analysis of handling arrow orientations
5. **Documentation** - Detection of potential worksheet containers and positioning

## Model Information

- **Model**: Mistral Pixtral 12B 2409
- **Vision Capabilities**: Full image understanding and spatial reasoning
- **Input Formats**: PNG, JPG, WebP (auto-converted)

## Architecture

```
streamlit_app.py
├── Image Upload & Display
├── Mistral API Integration
│   └── Image-to-base64 conversion
│   └── Multi-turn vision prompting
├── Analysis Results Processing
│   ├── Box count extraction
│   ├── Spatial analysis
│   └── Report generation
└── Visualization
    ├── Grid overlay (9-zone reference)
    ├── Annotated detection zones
    └── Export functionality
```

## API Limits

Default usage tier on Mistral:
- Rate limiting: 10,000 requests/month on free tier
- Image size: Up to 5 MB supported
- Processing time: ~10-30 seconds per image

## Troubleshooting

### "MISTRAL_API_KEY not found"
- Ensure you've set the API key in one of the configuration methods above
- Check that `.streamlit/secrets.toml` is not listed in `.gitignore` for local dev
- Verify the key is valid at [console.mistral.ai](https://console.mistral.ai/)

### Image upload not working
- Check file format (JPG, PNG, WebP supported)
- Verify file size is under 5 MB
- Ensure browser has proper permissions

### Empty or incomplete analysis
- Try with a clearer image
- Ensure good lighting and box visibility
- Check Mistral API status and quotas

## Dependencies

- `streamlit` - Web interface framework
- `mistralai` - Mistral API client
- `pillow` - Image processing
- `opencv-python` - Advanced image manipulation
- `numpy` - Numerical operations
- `python-dotenv` - Environment variable management

## File Structure

```
kitchen_images/
├── streamlit_app.py           # Main application
├── requirements.txt           # Dependencies
├── README.md                  # Documentation
├── LICENSE                    # License
└── .streamlit/
    └── secrets.toml.example   # API key template
```

## Security Notes

- API keys should never be committed to version control
- Add `.streamlit/secrets.toml` to `.gitignore`
- For Streamlit Cloud, use the Secrets management UI
- Environment variables preferred for production deployments

## Future Enhancements

Potential improvements:
- Multi-image batch processing
- Custom analysis templates
- Database logging of results
- Advanced bounding box coordinates from Mistral
- Real-time camera feed analysis
- Integration with delivery management systems

## Support

For issues or questions:
1. Check the troubleshooting section
2. Verify Mistral API key configuration
3. Review application logs in Streamlit terminal

## License

See LICENSE file for details

## Contributing

Contributions welcome! Please ensure:
- Code follows existing style
- All features tested
- Documentation updated
- Sensitive data not included
