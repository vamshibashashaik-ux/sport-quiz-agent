import streamlit as st
from google import genai
import json

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
            prompt = f"Create a {difficulty} quiz about {sport} with exactly {num_questions} multiple choice questions. Return the response strictly as a raw JSON format containing a list named 'quiz'. Inside the list, each item must be a dictionary with keys: 'question', 'options' (a list of 4 choices), 'correct_answer', and 'explanation'. Do not include markdown code block syntax."
            
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
            
            clean_text = response.text.strip()
            data = json.loads(clean_text)
            
            st.session_state['quiz_questions'] = data['quiz']
            st.success("Quiz Generated Successfully!")
            st.rerun()
            
        except Exception as err:
            st.error("Something went wrong. Please click the button again.")

    if 'quiz_questions' in st.session_state:
        questions_list = st.session_state['quiz_questions']
        user_selections = []
        
        for i in range(len(questions_list)):
            current_item = questions_list[i]
            st.write(f"**Question {i+1}:** {current_item['question']}")
            
            choice = st.radio("Choose one:", current_item['options'], key=f"question_{i}")
            user_selections.append(choice)
            st.write("")
            
        if st.button("Submit Answers"):
            score = 0
            
            for i in range(len(questions_list)):
                current_item = questions_list[i]
                correct = current_item['correct_answer']
                user_choice = user_selections[i]
                
                if user_choice == correct:
                    score = score + 1
                    st.write(f"✅ **Question {i+1} is Correct!**")
                else:
                    st.write(f"❌ **Question {i+1} is Wrong.** Correct answer: {correct}")
                
                st.write(f"🤖 *Fact:* {current_item['explanation']}")
                st.write("---")
                
            st.write(f"### Final Score: {score} / {len(questions_list)}")
