import streamlit as st
from audio_recorder_streamlit import audio_recorder
import openai
import base64

# Function to setup the OpenAI client
def setup_openai_client(api_key):
    return openai.OpenAI(api_key=api_key)

# Function to transcribe audio
def transcribe_audio(client, audio_path):
    with open(audio_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(model="whisper-1", file=audio_file)
        return transcript.text

# Function to fetch AI response
def fetch_ai_response(client, input_text):
    messages = [{"role": "user", "content": input_text}]
    response = client.chat.completions.create(model="gpt-3.5-turbo-1106", messages=messages)
    return response.choices[0].message.content

# Function to convert text to speech
def text_to_audio(client, text, audio_path):
    response = client.audio.speech.create(model="tts-1", voice="echo", input=text)
    response.stream_to_file(audio_path)

# Main function
def main():
    # Set the app's page title and icon
    st.set_page_config(page_title="Cute Voice Assistant", page_icon="💬")

    # Sidebar for API Key
    st.sidebar.title("API Key 🗝️")
    api_key = st.sidebar.text_input("Enter your API Key", type="password")

    # Custom styling for a clean and neutral UI
    st.markdown("""
        <style>
        body {
            background-color: #f7f7f7;
            color: #333;
            font-family: 'Arial', sans-serif;
        }
        .stButton>button {
            background-color: #66B2FF;
            color: white;
            border-radius: 25px;
            font-size: 16px;
            padding: 10px 20px;
            border: none;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #4d9eff;
        }
        .stTextInput>div>input {
            background-color: #f0f8ff;
            border: 2px solid #66B2FF;
            border-radius: 12px;
            padding: 12px;
        }
        .stTitle {
            color: #4d9eff;
            font-weight: bold;
        }
        .stText {
            font-size: 18px;
            font-style: italic;
        }
        /* Custom card styling */
        .card {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 20px;
            margin-top: 20px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }
        .card h4 {
            color: #4d9eff;
        }
        .card p {
            color: #333;
            font-size: 16px;
            word-wrap: break-word;
        }
        </style>
    """, unsafe_allow_html=True)

    # App title and description
    st.title("💬 Voice Assistant 🎤")
    st.write("Click on 'Start Recording' to speak and get a response!")

    if api_key:
        client = setup_openai_client(api_key)

        # Start recording button with cute design
        recorded_audio = audio_recorder()
        if recorded_audio:
            audio_file = "audio.mp3"
            with open(audio_file, "wb") as f:
                f.write(recorded_audio)

            # Transcribe the audio to text
            transcribe_text = transcribe_audio(client, audio_file)

            # Display the input transcript in a styled card
            st.markdown(f"""
                <div class="card">
                    <h4>🎤 Transcribed Text:</h4>
                    <p>{transcribe_text}</p>
                </div>
            """, unsafe_allow_html=True)

            # Fetch AI response
            ai_response = fetch_ai_response(client, transcribe_text)

            # Convert AI response to speech
            response_audio_file = "audio_response.mp3"
            text_to_audio(client, ai_response, response_audio_file)

            # Display the AI response in a styled card and play audio
            st.markdown(f"""
                <div class="card">
                    <h4>🤖 AI Response:</h4>
                    <p>{ai_response}</p>
                </div>
            """, unsafe_allow_html=True)

            st.audio(response_audio_file)

# Run the app
if __name__ == "__main__":
    main()
