import streamlit as st
import requests
import json
from validations import is_valid_prompt
# Config
URL = st.secrets["api_url"]
API_KEY = st.secrets["api_key"]


# Store generated image URLs
if "generated_images" not in st.session_state:
    st.session_state.generated_images = []

st.title("💎 OLE AI Jewelry Image Generator")

# --- Form for prompt input and submit on ENTER ---
with st.form(key="prompt_form"):
    prompt = st.text_input("Enter a jewelry-related prompt:")
    submitted = st.form_submit_button("Generate Images")

if submitted:
    validate_prompt = is_valid_prompt(prompt)
    print(validate_prompt)

    if not validate_prompt:
        st.error("❌ Opps!!! Prompt is either not jewelry-related or contains negative content.")
    else:
        with st.spinner("Generating images..."):
            payload = json.dumps({
                "key": API_KEY,
                "prompt": validate_prompt[1],
                "negative_prompt": "bad quality",
                "width": "512",
                "height": "512",
                "safety_checker": True,
                "seed": None,
                "samples": 4,
                "base64": False,
                "webhook": None,
                "track_id": None
            })

            headers = {
                'Content-Type': 'application/json'
            }

            try:
                response = requests.post(URL, headers=headers, data=payload)
                result = response.json()

                if "output" in result:
                    st.session_state.generated_images = result["output"]
                else:
                    st.error("No images returned. Please try after some time.")
            except Exception as e:
                st.error(f"Request failed: {e}")

# --- Display Generated Images ---
if st.session_state.generated_images:
    st.subheader("🖼️ Generated Images")
    cols = st.columns(4)
    for i, image_url in enumerate(st.session_state.generated_images):
        with cols[i]:
            st.image(image_url, caption=f"Image {i+1}", use_container_width=True)

# --- Clear Output Button ---
if st.button("🧹 Clear Output"):
    st.session_state.generated_images = []
    st.rerun()