import streamlit as st
import json
import random

# Set page configuration
st.set_page_config(
    page_title="Python Quiz App",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    /* Main container styling */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 20px;
        border-radius: 10px;
    }
    
    /* Header styling */
    h1, h2, h3 {
        color: #2c3e50;
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* Question styling */
    .question-container {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    
    /* Progress bar styling */
    .stProgress > div > div {
        background-color: #6c5ce7;
    }
    
    /* Radio button styling */
    .stRadio > div {
        padding: 10px;
        background-color: #f8f9fa;
        border-radius: 8px;
        margin-bottom: 10px;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #6c5ce7;
        color: white;
        font-size: 16px;
        border-radius: 8px;
        padding: 10px 24px;
        border: none;
        transition: all 0.3s ease;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #5649c0;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    /* Score display styling */
    .score-container {
        border: 2px solid #6c5ce7;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        margin: 20px 0;
        background: linear-gradient(to right, #e0eafc, #cfdef3);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
    }
    
    /* Category selection styling */
    .stSelectbox > div > div {
        background-color: white;
        border-radius: 8px;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #2c3e50;
    }
    .sidebar .sidebar-content {
        background-color: #2c3e50;
        color: white;
    }
    
    /* Footer styling */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #2c3e50;
        color: white;
        text-align: center;
        padding: 10px 0;
        font-size: 14px;
    }
    
    /* Success/Error message styling */
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #28a745;
        margin: 15px 0;
    }
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #dc3545;
        margin: 15px 0;
    }
    
    /* Explanation box styling */
    .explanation-box {
        background-color: #e2f0fb;
        border-left: 5px solid #17a2b8;
        padding: 15px;
        border-radius: 8px;
        margin: 15px 0;
    }
</style>
""", unsafe_allow_html=True)

# Load questions from JSON
def load_questions():
    try:
        with open("quiz.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Initialize session state
if "score" not in st.session_state:
    st.session_state.score = 0
if "question_index" not in st.session_state:
    st.session_state.question_index = 0
if "selected_category" not in st.session_state:
    st.session_state.selected_category = None
if "page" not in st.session_state:
    st.session_state.page = "home"
if "player_name" not in st.session_state:
    st.session_state.player_name = ""
if "shuffled_questions" not in st.session_state:
    st.session_state.shuffled_questions = []
if "selected_answer" not in st.session_state:
    st.session_state.selected_answer = None
if "show_feedback" not in st.session_state:
    st.session_state.show_feedback = False

# Load quiz data
quiz_data = load_questions()

# Define categories
categories = list(quiz_data.keys())

# Sidebar Instructions with enhanced styling
st.sidebar.markdown("""
<div style="color: white; padding: 10px;">
    <h2 style="color: #a29bfe;">📜 Quiz Instructions</h2>
    <div style="background-color: #34495e; padding: 15px; border-radius: 10px;">
        <p>1️⃣ Select a category</p>
        <p>2️⃣ Read the question carefully</p>
        <p>3️⃣ Choose an answer and submit it</p>
        <p>4️⃣ Get feedback and explanation</p>
        <p>5️⃣ Your score is tracked throughout</p>
        <p>6️⃣ Last question takes you to the score page</p>
    </div>
    <div style="margin-top: 20px; background-color: #6c5ce7; padding: 15px; border-radius: 10px; text-align: center;">
        <h3 style="color: white; margin: 0;">📢 Good Luck! 🚀</h3>
    </div>
</div>
""", unsafe_allow_html=True)

# Home Page
if st.session_state.page == "home":
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
            <div style="text-align: center; padding: 30px; background: linear-gradient(to right, #a29bfe, #6c5ce7); border-radius: 15px; margin-bottom: 30px;">
                <h1 style="color: white; font-size: 42px; margin-bottom: 10px;">🎓 Python Quiz App</h1>
                <p style="color: white; font-size: 20px;">Test your Python knowledge across multiple topics! 🚀</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div style="background-color: white; padding: 30px; border-radius: 15px; box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);">
                <h3 style="color: #2c3e50; text-align: center; margin-bottom: 20px;">Enter Your Details</h3>
        """, unsafe_allow_html=True)
        
        st.session_state.player_name = st.text_input("Enter your name:", "", 
                                                    placeholder="Type your name here...",
                                                    help="We'll use this to personalize your quiz experience")
        
        st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)
        
        if st.button("🚀 Start Quiz", key="start_button"):
            if st.session_state.player_name.strip():
                st.session_state.page = "category_selection"
                st.rerun()
            else:
                st.markdown("""
                    <div style="background-color: #f8d7da; color: #721c24; padding: 15px; border-radius: 8px; text-align: center; margin-top: 15px;">
                        ⚠️ Please enter your name before starting!
                    </div>
                """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

# Category Selection Page
elif st.session_state.page == "category_selection":
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
            <div style="text-align: center; padding: 20px; background: linear-gradient(to right, #a29bfe, #6c5ce7); border-radius: 15px; margin-bottom: 30px;">
                <h1 style="color: white;">📚 Select a Quiz Category</h1>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div style="background-color: white; padding: 30px; border-radius: 15px; box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);">
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div style="text-align: center; margin-bottom: 20px;">
                <h3 style="color: #2c3e50;">Welcome, {st.session_state.player_name}! 👋</h3>
                <p>Choose a category to begin your quiz journey</p>
            </div>
        """, unsafe_allow_html=True)

        st.session_state.selected_category = st.selectbox(
            "Choose a category:", 
            ["Select"] + categories, 
            key="category_select",
            format_func=lambda x: f"🔍 {x}" if x != "Select" else "Select a category..."
        )

        st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)

        if st.session_state.selected_category and st.session_state.selected_category != "Select":
            if st.button("🎮 Start Quiz", key="start_category_button"):
                st.session_state.question_index = 0
                st.session_state.score = 0
                
                # Shuffle questions and options
                questions = quiz_data.get(st.session_state.selected_category, [])
                random.shuffle(questions)
                for q in questions:
                    random.shuffle(q["options"])
                
                st.session_state.shuffled_questions = questions
                st.session_state.page = "quiz"
                st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)

# Quiz Page
elif st.session_state.page == "quiz":
    questions = st.session_state.shuffled_questions
    total_questions = len(questions)

    if st.session_state.question_index < total_questions:
        question = questions[st.session_state.question_index]
        
        # Header with category and player info
        st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; 
                        padding: 15px; background: linear-gradient(to right, #a29bfe, #6c5ce7); 
                        border-radius: 15px; margin-bottom: 20px; color: white;">
                <div>
                    <h3 style="margin: 0;">Category: {st.session_state.selected_category}</h3>
                </div>
                <div>
                    <h3 style="margin: 0;">Player: {st.session_state.player_name}</h3>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Question container
        st.markdown("""
            <div class="question-container">
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <h2 style="color: #6c5ce7; margin-bottom: 20px;">Question {st.session_state.question_index + 1} of {total_questions}</h2>
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 5px solid #6c5ce7; margin-bottom: 20px;">
                <h3 style="margin: 0;">{question['question']}</h3>
            </div>
        """, unsafe_allow_html=True)
        
        options = question["options"]
        selected_answer = st.radio("Select your answer:", options, key=f"q{st.session_state.question_index}")
        
        st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)
        
        # Check answer on submission
        if st.button("📝 Submit Answer", key="submit_answer") and not st.session_state.show_feedback:
            st.session_state.selected_answer = selected_answer
            st.session_state.show_feedback = True

            if selected_answer == question["answer"]:
                st.session_state.score += 1
                st.session_state.feedback_message = "✅ Correct! 🎉 Keep going!"
                st.session_state.feedback_type = "success"
            else:
                st.session_state.feedback_message = f"❌ Incorrect! The correct answer is: {question['answer']}"
                st.session_state.feedback_type = "error"

            st.rerun()

        # Show feedback
        if st.session_state.show_feedback:
            if st.session_state.feedback_type == "success":
                st.markdown(f"""
                    <div class="success-message">
                        <h3 style="margin: 0;">{st.session_state.feedback_message}</h3>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div class="error-message">
                        <h3 style="margin: 0;">{st.session_state.feedback_message}</h3>
                    </div>
                """, unsafe_allow_html=True)

            # Show Explanation
            if "explanation" in question and question["explanation"].strip():
                st.markdown(f"""
                    <div class="explanation-box">
                        <h3 style="margin: 0; color: #17a2b8;">📖 Explanation:</h3>
                        <p style="margin-top: 10px;">{question["explanation"]}</p>
                    </div>
                """, unsafe_allow_html=True)

            # If last question, go to score page
            if st.session_state.question_index == total_questions - 1:
                if st.button("🏆 View Final Score", key="view_score"):
                    st.session_state.page = "score"
                    st.rerun()
            else:
                if st.button("⏭️ Next Question", key="next_question"):
                    st.session_state.question_index += 1
                    st.session_state.show_feedback = False
                    st.session_state.selected_answer = None
                    st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Progress information
        progress = (st.session_state.question_index + 1) / total_questions
        
        st.markdown(f"""
            <div style="background-color: white; padding: 20px; border-radius: 10px; margin-top: 20px;">
                <h3 style="margin-bottom: 10px;">Your Progress</h3>
        """, unsafe_allow_html=True)
        
        st.progress(progress)
        
        st.markdown(f"""
                <div style="display: flex; justify-content: space-between; margin-top: 10px;">
                    <div>Question {st.session_state.question_index + 1} of {total_questions}</div>
                    <div>{int(progress * 100)}% Completed</div>
                </div>
                <div style="display: flex; justify-content: space-between; margin-top: 15px;">
                    <div>Current Score: {st.session_state.score}/{st.session_state.question_index + (1 if st.session_state.show_feedback else 0)}</div>
                    <div>Remaining: {total_questions - (st.session_state.question_index + 1)} questions</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

# Score Page
elif st.session_state.page == "score":
    total_questions = len(st.session_state.shuffled_questions)
    score = st.session_state.score
    player_name = st.session_state.player_name
    percentage = (score / total_questions) * 100
    passing_score = percentage >= 50  # Define passing as 50% or higher

    # Header
    st.markdown("""
        <div style="text-align: center; padding: 30px; background: linear-gradient(to right, #a29bfe, #6c5ce7); border-radius: 15px; margin-bottom: 30px;">
            <h1 style="color: white; font-size: 42px;">🎉 Quiz Completed! 🎉</h1>
        </div>
    """, unsafe_allow_html=True)

    # Dynamic feedback messages
    if score == total_questions:
        message = f"🌟 Outstanding, {player_name}! You got a perfect score! 🚀"
        emoji = "🏆"
        grade = "A+"
        color = "#28a745"
    elif score >= total_questions * 0.8:
        message = f"👏 Well done, {player_name}! You really know your Python! 🔥"
        emoji = "🥇"
        grade = "A"
        color = "#28a745"
    elif score >= total_questions * 0.6:
        message = f"👍 Good effort, {player_name}! Keep practicing and you'll master it! 💪"
        emoji = "🥈"
        grade = "B"
        color = "#17a2b8"
    elif score >= total_questions * 0.4:
        message = f"😊 Not bad, {player_name}! Every mistake is a step toward learning. 📚"
        emoji = "🥉"
        grade = "C"
        color = "#ffc107"
    elif score > 0:
        message = f"😅 It's okay, {player_name}. Learning takes time! Keep trying! 💡"
        emoji = "📝"
        grade = "D"
        color = "#fd7e14"
    else:
        message = f"🤔 Don't worry, {player_name}. Everyone starts somewhere! Try again! 🔄"
        emoji = "📚"
        grade = "E"
        color = "#dc3545"

    # Score display with improved UI
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Basic score display for all users
        st.markdown(f"""
        <div class="score-container">
            <div style="font-size: 80px; margin-bottom: 20px;">{emoji}</div>
            <h2 style="color: {color}; font-size: 36px; margin-bottom: 20px;">Final Score: {score}/{total_questions}</h2>
            <div style="display: flex; justify-content: center; margin: 30px 0;">
                <div style="width: 150px; height: 150px; border-radius: 50%; background: conic-gradient({color} {percentage}%, #f1f1f1 0); 
                            display: flex; align-items: center; justify-content: center; position: relative;">
                    <div style="width: 130px; height: 130px; border-radius: 50%; background-color: white; 
                                display: flex; align-items: center; justify-content: center; flex-direction: column;">
                        <div style="font-size: 36px; font-weight: bold; color: {color};">{int(percentage)}%</div>
                        <div style="font-size: 24px; color: {color};">Grade: {grade}</div>
                    </div>
                </div>
            </div>
            <p style="margin: 20px 0; font-size: 18px;">{message}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Only show detailed summary for passing scores
        if passing_score:
            st.markdown(f"""
            <div style="background-color: white; padding: 20px; border-radius: 10px; margin-top: 20px; text-align: left;">
                <h3 style="color: #2c3e50; margin-bottom: 15px;">Quiz Summary</h3>
                <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                    <div>Category:</div>
                    <div style="font-weight: bold;">{st.session_state.selected_category}</div>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                    <div>Total Questions:</div>
                    <div style="font-weight: bold;">{total_questions}</div>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                    <div>Correct Answers:</div>
                    <div style="font-weight: bold; color: #28a745;">{score}</div>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                    <div>Incorrect Answers:</div>
                    <div style="font-weight: bold; color: #dc3545;">{total_questions - score}</div>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <div>Accuracy:</div>
                    <div style="font-weight: bold;">{int(percentage)}%</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Restart button
        if st.button("🔄 Restart Quiz", key="restart_button"):
            st.session_state.page = "home"
            st.session_state.question_index = 0
            st.session_state.score = 0
            st.session_state.show_feedback = False
            st.rerun()

# Footer
st.markdown("""
    <div class="footer">
        <div style="display: flex; justify-content: space-between; padding: 0 20px;">
            <div>© 2024 Python Quiz App</div>
            <div>Created with ❤️ Mehboob Ahmed</div>
            <div>I Love Python</div>
        </div>
    </div>
""", unsafe_allow_html=True)
