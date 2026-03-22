import streamlit as st
from PIL import Image
import io
import base64
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="PPT Generator",
    page_icon="GK",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .slide-container {
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        background-color: #f9f9f9;
    }
    .slide-preview {
        text-align: center;
        background-color: white;
        border-radius: 5px;
        padding: 10px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'slides' not in st.session_state:
    st.session_state.slides = []
if 'generated' not in st.session_state:
    st.session_state.generated = False
if 'ppt_file' not in st.session_state:
    st.session_state.ppt_file = None

# Sidebar for global settings
with st.sidebar:
    st.header("⚙️ Settings")
    
    num_slides = st.slider(
        "Number of Slides",
        min_value=1,
        max_value=20,
        value=3,
        help="Choose how many slides you want to generate"
    )
    
    theme = st.selectbox(
        "Theme",
        ["Professional", "Creative", "Minimal", "Colorful", "Dark"],
        help="Select a theme for your presentation"
    )
    
    aspect_ratio = st.radio(
        "Aspect Ratio",
        ["16:9", "4:3"],
        help="Choose slide dimensions"
    )
    
    st.divider()
    
    # Reset button
    if st.button("🔄 Reset All", use_container_width=True):
        st.session_state.slides = []
        st.session_state.generated = False
        st.session_state.ppt_file = None
        st.rerun()

# Main content
st.title("PPT Generator")
st.markdown("Generate professional presentations with AI-powered slide creation")

# Main prompt section
st.header("Main Prompt")
main_prompt = st.text_area(
    "Describe your presentation",
    placeholder="E.g., Create a presentation about climate change covering causes, effects, and solutions...",
    height=100,
    help="Provide a detailed description of what you want in your presentation"
)

# Per-slide customization section
st.header("Slide Customization")
st.markdown("Customize each slide individually")

slides_container = st.container()

with slides_container:
    custom_prompts = []
    for i in range(num_slides):
        with st.expander(f"Slide {i+1} Configuration", expanded=(i==0)):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                slide_prompt = st.text_area(
                    f"Slide {i+1} Prompt",
                    key=f"slide_{i}_prompt",
                    placeholder=f"Describe what you want on slide {i+1}...",
                    height=80,
                    label_visibility="collapsed"
                )
                custom_prompts.append(slide_prompt)
            
            with col2:
                slide_layout = st.selectbox(
                    "Layout",
                    ["Title & Content", "Two Column", "Image Focus", "Bullet Points", "Quote", "Blank"],
                    key=f"slide_{i}_layout",
                    label_visibility="collapsed"
                )

# Generate button section
st.divider()
col1, col2, col3 = st.columns([2, 1, 2])
with col2:
    generate_btn = st.button(
        "✨ Generate Presentation",
        type="primary",
        use_container_width=True
    )

# Generation logic (placeholder - integrate with your actual generator)
if generate_btn and main_prompt:
    with st.spinner("🚀 Generating your presentation..."):
        # TODO: Replace this with your actual PPT generation logic
        # This is where you'll call your PPT generation API/function
        
        # Simulating generation for demo
        import time
        time.sleep(2)
        
        # Create dummy slide images for preview (replace with actual generated images)
        st.session_state.slides = []
        for i in range(num_slides):
            # Create a placeholder image
            img = Image.new('RGB', (800, 450), color=(255, 255, 255))
            st.session_state.slides.append(img)
        
        st.session_state.generated = True
        st.success("✅ Presentation generated successfully!")
        st.rerun()

# Preview section
if st.session_state.generated and st.session_state.slides:
    st.header("👁️ Preview")
    st.markdown("Preview your slides before downloading")
    
    # Create tabs for each slide
    tabs = st.tabs([f"Slide {i+1}" for i in range(len(st.session_state.slides))])
    
    for i, tab in enumerate(tabs):
        with tab:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Display slide image
                st.image(
                    st.session_state.slides[i],
                    use_container_width=True,
                    caption=f"Slide {i+1} Preview"
                )
            
            with col2:
                st.subheader(f"Slide {i+1} Details")
                
                # Show the prompt used
                st.markdown("**Prompt:**")
                prompt_used = custom_prompts[i] if custom_prompts[i] else "Using main prompt"
                st.info(prompt_used)
                
                # Show layout
                st.markdown("**Layout:**")
                st.write(f"📐 {slide_layout}")
                
                # Regenerate single slide option
                if st.button(f"🔄 Regenerate Slide {i+1}", key=f"regen_{i}"):
                    # TODO: Add logic to regenerate specific slide
                    st.info("Regeneration logic to be implemented")
    
    # Download section
    st.divider()
    st.header("💾 Download")
    
    download_col1, download_col2, download_col3 = st.columns([2, 1, 2])
    
    with download_col2:
        # Create PPT file (placeholder - integrate with your actual generator)
        # TODO: Replace with actual PPT creation logic
        buffer = io.BytesIO()
        # Your PPT generation code here
        # Example: ppt.save(buffer)
        
        # For demo, creating a dummy file
        buffer.write(b"Dummy PPT content - Replace with actual PPT generation")
        buffer.seek(0)
        
        st.download_button(
            label="📥 Download PowerPoint",
            data=buffer,
            file_name="presentation.pptx",
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            use_container_width=True
        )
    
    # Export options
    with download_col3:
        st.markdown("**Export as Images:**")
        for idx, slide in enumerate(st.session_state.slides):
            img_buffer = io.BytesIO()
            slide.save(img_buffer, format='PNG')
            img_buffer.seek(0)
            
            st.download_button(
                label=f"🖼️ Slide {idx+1} (PNG)",
                data=img_buffer,
                file_name=f"slide_{idx+1}.png",
                mime="image/png",
                use_container_width=True
            )

# Help section
with st.expander("❓ How to use"):
    st.markdown("""
    ### Quick Start Guide
    
    1. **Enter Main Prompt**: Describe your overall presentation topic
    2. **Configure Slides**: Customize each slide with specific prompts
    3. **Choose Settings**: Select theme, aspect ratio, and number of slides
    4. **Generate**: Click the generate button to create your presentation
    5. **Preview**: Review each slide in the preview section
    6. **Download**: Download as PPTX or individual slide images
    
    ### Tips
    - Be specific in your prompts for better results
    - Use different layouts for visual variety
    - Preview before downloading to ensure quality
    """)

# Footer
st.divider()
st.markdown(
    "<div style='text-align: center; color: #666; padding: 20px;'>"
    "Built with ❤️ using Streamlit"
    "</div>",
    unsafe_allow_html=True
)
