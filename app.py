import streamlit as st
import google.generativeai as genai


# 1. Setup -  key from Google AI Studio
genai.configure(api_key=st.secrets["GEMINI_KEY"])

st.set_page_config(page_title="Bahá'í Faith Assistant", page_icon="✴")
st.title("Bahá'í Faith Information AI")
st.caption(" ")

# 2. System Instructions
SYSTEM_PROMPT = """
You are a respectful, scholarly, and helpful assistant dedicated to providing 
accurate information about the Bahá'í Faith. 
Your primary goal is to share insights based on the Bahá'í Sacred Writings 
(such as the works of Bahá'u'lláh, the Báb, and ‘Abdu’l-Bahá). 
Maintain a tone of humility and service. If a question is unrelated to the Faith, 
kindly steer the conversation back to relevant Bahá'í principles like the 
oneness of humanity or the investigation of truth. 
Always try to include a short quote from the Bahá'í writings in your response and mention which book it came from.
"""

# 3. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Chat Logic
if prompt := st.chat_input("Ask about Bahá'í principles, history, or writings..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Calling Gemini
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=SYSTEM_PROMPT
        )
        
        # Sending the conversation history to Gemini
        response = model.generate_content(prompt)
        st.markdown(response.text)
        
    st.session_state.messages.append({"role": "assistant", "content": response.text})



# 5 --- SIDEBAR SECTION ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Bahai_star.svg/1280px-Bahai_star.svg.png", width=100)
    st.header("Resources")
    
    st.link_button("Visit Bahai.org", "https://www.bahai.org", use_container_width=True)
    st.link_button("Reference Library", "https://www.bahai.org/library/", use_container_width=True)
    
    st.divider()
    # MAKE SURE THE LINE BELOW IS ALIGNED WITH THE ONES ABOVE!
    st.subheader("Suggested Topics")

    suggestions = [
        "What is the 'Oneness of Humanity'?",
        "Tell me about the life of Bahá'u'lláh.",
        "What are the Bahá'í House of Worship?",
        "How do Bahá'ís view science and religion?"
    ]

    for question in suggestions:
        if st.button(question, use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": question})
            st.rerun()
# --- END SIDEBAR SECTION ---


