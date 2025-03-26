import streamlit as st
import requests
import json
from validations import is_valid_prompt
# Config
URL = "https://modelslab.com/api/v6/realtime/text2img"
API_KEY = "zn8Fji81He22rG9OsL2nqPkThmMG6t3kZgtxGiECrTsJIBhwA9XuXahi2koz"

st.set_page_config(page_title="Jewelry Image Generator", layout="wide")
st.title("💍 OLE AI Jewelry Image Generator")

prompt = st.text_input("Enter a jewelry-related prompt")

if st.button("Generate Images"):
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
                    cols = st.columns(4)
                    for i, image_url in enumerate(result["output"]):
                        with cols[i]:
                            # st.image(image_url, caption=f"Image {i+1}", use_column_width=True)
                            st.image(image_url, caption=f"Image {i+1}", use_container_width=True)
                else:
                    st.error("No images returned. Please try after some time.")
            except Exception as e:
                st.error(f"Request failed: {e}")
