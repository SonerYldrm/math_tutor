import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser


st.set_page_config(page_title="Your Friendly Math Tutor")
st.title("Your Friendly Math Tutor")
openai_api_key = st.sidebar.text_input('OpenAI API Key', type='password')

prompt = """
Act as a tutor that helps students solve math and arithmetic reasoning questions.
Students will ask you questions. Think step-by-step to reach the answer. Write down each reasoning step.
Once you find the answer, do not give away the answer.
Instead extract clues from the step and show these clues.

Examples:

Question: John has 2 houses. Each house has 3 bedrooms and there are 2 windows in each bedroom.
Each house has 1 kitchen with 2 windows. Also, each house has 5 windows that are not in the bedrooms or kitchens.
How many windows are there in John's houses?
Answer: Each house has 3 bedrooms with 2 windows each, so that's 3 x 2 = 6 windows per house.
Each house also has 1 kitchen with 2 windows, so that's 2 x 1 = 2 windows per house.
Each house has 5 windows that are not in the bedrooms or kitchens, so that's 5 x 1 = 5 windows per house.
In total, each house has 6 + 2 + 5 = 13 windows.
Since John has 2 houses, he has a total of 2 x 13 = 26 windows. The answer is 26.
Clues: 1. Find the number of bedroom windows, kitchen windows, and other windows separately
2. Add them together to find the total number of windows at each house
3. Find the total number of windows for all the houses

Question: There are 15 trees in the grove. Grove workers will plant trees in the grove today. After they are done, 
there will be 21 trees. How many trees did the grove workers plant today?
Answer: There are originally 15 trees. After the workers plant some trees, there are 21 trees. So the workers 
planted 21 - 15 = 6 trees. The answer is 6.
Clues: 1. Start with the total number of trees after planting and subtract the original number of trees to 
find how many were planted.
2. Use subtraction to find the difference between the two numbers.

Question: Leah had 32 chocolates and her sister had 42. If they ate 35, how many pieces do they have left in total? 
Answer: Originally, Leah had 32 chocolates. Her sister had 42. So in total they had 32 + 42 = 74. After eating 35, they
had 74 - 35 = 39. The answer is 39.
Clues: 1. Start with the total number of chocolates they had.
    2. Subtract the number of chocolates they ate.

Question: {question}

Format the output as JSON with the following keys: Answer, Clues
"""


def generate_response(question):
    chat = ChatOpenAI(temperature=0.0)
    answer_schema = ResponseSchema(
        name="Answer",
        description="Answer:"
    )

    clues_schema = ResponseSchema(
        name="Clues",
        description="Clues:"
    )

    response_schemas = [
        answer_schema,
        clues_schema
    ]

    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    format_instructions = output_parser.get_format_instructions()

    prompt_template = ChatPromptTemplate.from_template(template=prompt)

    messages = prompt_template.format_messages(
        question=question,
        format_instructions=format_instructions
    )
    response = chat(messages)
    output_dict = output_parser.parse(response.content)
    return st.info(output_dict.get("Clues"))


with st.form('myform'):
  question = st.text_input('Enter question:', '')
  submitted = st.form_submit_button('Submit')
  if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')
  if submitted and openai_api_key.startswith('sk-'):
    generate_response(question)

