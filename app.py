# Librairies imports
from dotenv import load_dotenv # load the gemini api key
import os
from logger import logging # logs

import streamlit as st # streamlit for easy web app
import google.generativeai as genai # use google genai

from youtube_transcript_api import YouTubeTranscriptApi

# Load the environment variables

env_vars = load_dotenv()

if env_vars:
    genai.configure(api_key=os.getenv("GOOGLE_AI_API_KEY"))
else:
    logging.error("No environment variables found")

# Get the data transcript from the Youtube Video
def extract_transcript_data(youtube_video_url):
    try:
        # Get the video ID from the URL
        video_id = youtube_video_url.split("=")[-1]
        # Get the transcript from the id of the video
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        # String variable to store the transcript
        transcript  = ""

        # Store the text wo
        for i in transcript_text:
            transcript += " " + i["text"]

        logging.info("Extract data from the video.")

        return transcript

    except Exception as e:
        logging.error(e)

        raise e

# Create the prompt to generate the video summrizer
prompt = """
As a data science and statistics expert, analyze a YouTube video transcript.
Create detailed notes resembling a student's, encompassing data science topics like data collection, cleaning, analysis, and visualization. 
Discuss machine learning techniques, real-world applications, and data ethics. 
For statistics, cover core concepts, hypothesis testing, and regression analysis, highlighting their importance and practical use with examples.
        """

# Streamlit application
st.title("YouTube Transcript to Detailed Notes Converter for ML videos")

# Create the text area for video link
youtube_url = st.text_input("Enter YouTube Video Link:", key="input")

# Check if the file is not None
if youtube_url is not None:
    if "=" in youtube_url:
        st.video(youtube_url)
    else:
        st.write("Please upload your YouTube video link.")
else:
    st.write("Please upload your YouTube video link.")

submit = st.button("Get Detailed Notes...", key="submit")

if submit:
    if youtube_url !="":
        transcript_text = extract_transcript_data(youtube_url)
        if transcript_text is not None: # check if transcript data is not None
                        model = genai.GenerativeModel('gemini-1.0-pro-latest')
                        response = model.generate_content(prompt + transcript_text)
                        final_response = response.text
                        st.subheader("Generated Notes:")
                        st.write(final_response)
                        logging.info("Notes generated.")

