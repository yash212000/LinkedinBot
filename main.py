import streamlit as st
import requests
from apify_client import ApifyClient
import openai
import json

# Initialize APIs
APIFY_API_KEY = "apify_api_bo5a5G2lcChSsn5PjsIrcuY0NzkP0A0fsoeO"
openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=OPENAI_API_KEY)


def scrape_linkedin_profile(linkedin_url: str):
    """Fetch LinkedIn profile data using Apify."""
    client = ApifyClient(APIFY_API_KEY)
    run_input = {"profileUrls": [linkedin_url]}
    run = client.actor("2SyF0bVxmgGr8IVCZ").call(run_input=run_input)

    profile_data = []
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        profile_data.append(item)

    return profile_data[0] if profile_data else {}


def analyze_profile(profile_data):
    """Use OpenAI to analyze and provide feedback on the LinkedIn profile."""
    prompt = f"""
    Given the following LinkedIn profile data:
    {json.dumps(profile_data, indent=2)}

    Analyze the profile and provide feedback on missing information, improvements in the 'About' section, skill suggestions, and overall optimization tips.
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": "You are an expert LinkedIn profile optimizer."},
                  {"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()


def main():
    st.title("LinkedIn Profile Optimizer")
    st.write("Analyze and optimize your LinkedIn profile for better job opportunities!")

    linkedin_url = st.text_input("Enter your LinkedIn profile URL:")

    if st.button("Analyze Profile"):
        if linkedin_url:
            with st.spinner("Fetching and analyzing your profile..."):
                profile_data = scrape_linkedin_profile(linkedin_url)

                if profile_data:
                    feedback = analyze_profile(profile_data)
                    st.subheader("Profile Analysis Results:")
                    st.write(feedback)
                else:
                    st.error("Failed to retrieve profile data. Please check the LinkedIn URL and try again.")
        else:
            st.warning("Please enter a LinkedIn profile URL.")


if __name__ == "__main__":
    main()
