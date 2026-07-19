import streamlit as st
from google import genai

st.title("🏆 Statupbox: AI Sports Quiz Generator")
st.write("Generate basic sports quizzes using AI.")

api_key = st.sidebar.text_input("Enter Google Gemini API Key:", type="password")

if api_key == "":
    st.warning("Please enter your Gemini API Key in the sidebar to start.")
else:
    sport = st.selectbox("Choose a Sport:", ["Cricket", "Football", "Basketball"])
    difficulty = st.selectbox("Select Difficulty:", ["Easy", "Medium", "Hard"])
    num_questions = st.slider("Number of Questions:", min_value=1, max_value=5, value=3)

    if st.button("Generate Quiz"):
        st.write("AI Agent is working... Please wait.")
        
        try:
            prompt = f"Create a {difficulty} quiz about {sport} with exactly {num_questions} multiple choice questions. For each question, display the options clearly and list the correct answer at the very bottom with a short explanation."
            
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
            
            st.session_state['quiz_result'] = response.text
            st.success("Quiz Generated Successfully!")
            
        except Exception as err:
            st.error("Something went wrong. Please click the button again.")

    if 'quiz_result' in st.session_state:
        st.write("---")
        st.write(st.session_state['quiz_result'])
