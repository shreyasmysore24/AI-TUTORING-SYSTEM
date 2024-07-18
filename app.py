import re
import streamlit as st
import os
import sqlite3
import google.generativeai as genai
from modtest import predict

genai.configure(api_key="AIzaSyD58EM2Qtnf9S5E9a0DJAMnDy5AGat4rWc")

def get_gemini_response(question,prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt[0],question])
#     print(response.text)
    return response.text

def get_gemini_response_two(question2,prompt2):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt2[0],question2])
#     print(response.text)
    return response.text

prompt=["""
        You are an expert in asking nine single word answers questions for fifth grader in maths,science,social studies based on category level!,it should be in order maths,science,social studies
for category easy ask simple question like addition, subtraction,multiplicatin in maths,ask simple science question like general facts like What is the hardest substance found on Earth?,simple social science question like What is the capital city of India?  \n
for category medium  ask bit tough question like If a pack of 24 pencils costs 360, what is the cost of each pencil?,ask  science question like name a state of matter, social science question like name a neighbouring county to India       \n
for category hard  ask bit tough and tricky question like  Solve: 3/4 * 16,ask  science question like Name the process by which plants release water vapor through their leaves, social science question like Which river is known as the lifeline of India     
 \nFor example(thest are just for your information please 'do not give back the same questions from the example')  do not forget to move to next line after each question of maths ,science,social  , \nExamp1e 1
my input text will be like 'hard' ,
your answers should be like \n
        QUESTIONS ON MATHS\n
        Question 1: How many sides does a decagon have?\n
        Question 2:What is the result of 37 divided by 4 (give the quotient)?\n
        Question 3: What is the perimeter of a square with each side measuring 12 cm?\n
        QUESTIONS ON SCIENCE\n
        Question 4: What type of rock forms from cooled magma or lava?\n
        Question 5: What is the name of the force that pulls objects towards the center of the Earth?\n
        Question 6: What is the term for the process by which plants release water vapor through their leaves?\n
        QUESTIONS ON SOCIAL STUDIES\n
        Question 7: Which Indian city hosted the first-ever Asian Games?\n
        Question 8: What is the official language of Jammu and Kashmir?\n
        Question 9: Which Indian river is also known as the Tsangpo-Brahmaputra?


\n\nExamp1e 2
my input text will be like 'medium' ,
your answers should be like \n
        questions on maths\n
        Question 1: What is the result of 24 minus 13?\n
        Question 2:What is the name for a number that can only be divided evenly by 1 and itself?\n
        Question 3: What is the sum of 15 and 23?n
        questions on science\n
        Question 4: What is the chemical formula for water?\n
        Question 5: What is the largest organ in the human body?\n
        Question 6: What is the process by which plants make their own food called?\n
        questions on social studies
        Question 7: Who was the first woman Prime Minister of India?n
        Question 8: What is the capital city of Maharashtra?\n
        Question 9: Which Indian state is known as the "Land of Five Rivers"?
\n\nExamp1e 3
my input text will be like 'medium' ,
your answers should be like \n
        questions on maths\n
        Question 1: What is the shape of a coin?\n
        Question 2:What is 45 divided by 5?\n
        Question 3: What is 8 multiplied by 7?\n
        questions on science\n
        Question 4: What is the natural satellite of the Earth?\n
        Question 5: What gas do plants absorb from the air to make food?\n
        Question 6: What is the hardest natural substance found on Earth?\n
        questions on social studies
        Question 7: What is the largest state in India by area?\n
        Question 8: Who is the President of India?\n
        Question 9: What is the largest state in India by area??
also the questions should not have ''' in the beginning or end and in output
"""]


prompt2=["""
        You are an expert in evaluating answers for the given questions!\n
 we will provide you with questions of 3 catagory namely maths,science,social studies and answers will be provided at the last by specifying question number\n
 analyse the answers with the give  question properly tell if the answers are true or false note most of the time the maths answers will be false so check the maths answers twice\n  for every false give explaination why it is false
         \n please  "do not put dot after the question number because i will extract the second element of each line for further processing"
 \nFor example , \nExamp1e 1
my input text will be like"questions are
QUESTIONS ON MATHS\n

Question 1: Solve: 3/4 * 16\n
Question 2: A rectangular garden is 15 meters long and 9 meters wide. What is its perimeter?\n
Question 3: Simplify: 5(2x + 3) - 3(x + 4)\n

QUESTIONS ON SCIENCE\n

Question 4: Name the process by which plants release water vapor through their leaves\n
Question 5: What is the unit of electric charge?\n
Question 6: What is the name of the outermost layer of the Earth's atmosphere?\n

QUESTIONS ON SOCIAL STUDIES

Question 7: Which river is known as the lifeline of India\n
Question 8: What is the nickname of the United States?\n
Question 9: Which is the largest continent in the world?" \,,\n
answers are
1. 14
2. 48 meters
3. 7x + 3
4. Transpiration
5. Coulomb (C)
6. stratosphere
7. Ganges River
8. USA or America
9. Antartica
your answers should be like \n
         1 false 'because the answer is 12'\n
         2 true\n
         3 true\n
         4 true\n
         5 true\n
         6 false 'because the answer is exosphere'\n
         7 true\n
         8 true\n
         9 false because answer is asia\n

        note" do not put dot after the question number"
         \n please show not attended any questions if all the 9 questions are not written

        



also the answers should not have ''' in the beginning or end and in output
"""]


def gemini():
#     prompt = "Your prompt here"  # Define this prompt or pass it as a parameter if needed
#     prompt2 = "Your second prompt here"  # Define this prompt or pass it as a parameter if needed

    # Initialize session state variables if they don't exist
    if 'response' not in st.session_state:
        conn = sqlite3.connect('test_scores.db')
        cursor = conn.cursor()
        sc=cursor.execute("""SELECT category
        FROM test_scores
        ORDER BY test_no DESC
        limit 1;""")
        result = cursor.fetchall()

        question =str(list(result[0])[0])
        print(question)
        st.session_state.response = get_gemini_response(question, prompt)
    
    if 'response2' not in st.session_state:
        st.session_state.response2 = None

    # Display the initial response
    st.text(st.session_state.response)

    # Text area for user to write answers with a unique key
    answers = st.text_area("Write your answers ('please specify the question number')", key="answers")

    # Submit button to process the second response
    if st.button("Submit"):
        question2 = f"Questions are: \n{st.session_state.response}\nAnswers are: \n{answers}"
        st.session_state.response2 = get_gemini_response_two(question2, prompt2)
        # question3=st.session_state.response2
        # st.session_state.response3 = get_gemini_response_three(question3, prompt3)
        # print(st.session_state.response3)
        questions = re.split(r'\n(?=\d+\.)',st.session_state.response2 )
        count_t1 = sum('true' in question.lower() for question in questions[0:3])
        count_t2 = sum('true' in question.lower() for question in questions[3:6])
        count_t3 = sum('true' in question.lower() for question in questions[6:9])
        
        print(f"Number of 'true': {count_t1,count_t2,count_t3}")
        predict(count_t1,count_t2,count_t3)
 
    # Display the second response if it exists
    if st.session_state.response2:
        st.text(st.session_state.response2)
        
     

gemini()