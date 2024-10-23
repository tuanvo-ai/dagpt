import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
#import os
from dotenv import load_dotenv

from langchain_experimental.agents.agent_toolkits.pandas.base import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI
from langchain_google_genai import GoogleGenerativeAI
from langchain_google_genai import ChatGoogleGenerativeAI

import os
import time
from google.api_core.exceptions import ResourceExhausted

from scr.logger.base import BaseLogger
from scr.models.llms import load_llm
from scr.utils import execute_plt_code


load_dotenv()
google_api_key = os.environ.get("GOOGLE_API_KEY")
if not google_api_key:
    raise ValueError("Google API Key not found in environment variables.")

openai_api_key = os.environ.get("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OpenAI API Key not found in environment variables.")

# Đảm bảo rằng API key được lấy từ môi trường

logger = BaseLogger()
#   LUA CHON MODEL DE CHAY
#MODEL_NAME = "gpt-4o-mini"
#MODEL_NAME = "gemini-pro"
MODEL_NAME = "gemini-1.5-pro-002"
api_key = google_api_key

# THEM HAM NAY DE BAO LOI ResourceExhausted 
def call_once(da_agent, query,):
    try:
        response = da_agent.invoke(query)
        return response
    except ResourceExhausted as e:
        print("Resource exhausted, cannot complete the request at this time.")
        raise
    except Exception as e:
        print(f"An error occurred: {e}")
        raise

def call_with_retry(da_agent, query, retries=2):
    for i in range(retries):
        try:
            response = da_agent.invoke(query)
            return response
        except ResourceExhausted as e:
            wait_time = 5 ** i  # Exponential backoff
            print(f"Resource exhausted, retrying in {wait_time} seconds...")
            time.sleep(wait_time)
        except Exception as e:
            print(f"An error occurred: {e}")
            raise
    raise RuntimeError("Maximum retry limit reached")

# hàm trích xuất code python trong result cua LLM
def extract_python_code(data):
        # Loại bỏ phần đầu và cuối chứa ```python và ```
        data = data.replace("```python\n", "").replace("\n```", "")
    
        return data

def process_query(da_agent, query):

    #response = da_agent(query)
    #action = response["intermediate_steps"][-1][0].tool_input["query"]
    try:
        response = call_once(da_agent, query)
        print(response)
    except RuntimeError as e:
        print(f"Failed to get a response: {e}")
    
    code_reg = response["intermediate_steps"][-1][0].tool_input
    
    action = extract_python_code(code_reg)

    if "plt" in action:
        st.write(response["output"])

        fig = execute_plt_code(action, df=st.session_state.df)
        if fig:
            st.pyplot(fig)

        st.write("**Executed code:**")
        st.code(action)

        to_display_string = response["output"] + "\n" + f"```python\n{action}\n```"
        st.session_state.history.append((query, to_display_string))

    else:
        st.write(response["output"])
        st.session_state.history.append((query, response["output"]))


def display_chat_history():
    st.markdown("## Chat History: ")
    for i, (q, r) in enumerate(st.session_state.history):
        st.markdown(f"**Query: {i+1}:** {q}")
        st.markdown(f"**Response: {i+1}:** {r}")
        st.markdown("---")

def main():

    # Set up streamlit interface
    st.set_page_config(page_title="📊 Smart Data Analysis Tool",page_icon= "📊",layout="centered")
    st.header("📊 Smart Data Analysis Tool")
    st.write(
        "### Welcome to our data analysis tool. This tools can assist your daily data analysis tasks. Please enjoy !"
    )

    # Load llms model
    #llm = load_llm(model_name=MODEL_NAME)
    try:
        llm = load_llm(api_key, MODEL_NAME)
        print(llm)
    except TypeError as e:
        print(f"Error: {e}")
    except ValueError as e:
        print(f"Error: {e}")
        
    logger.info(f"### Successfully loaded {MODEL_NAME} !###")

    # Upload csv file
    with st.sidebar:
        uploaded_file = st.file_uploader("Upload your csv file here", type="csv")

    # Initial chat history
    if "history" not in st.session_state:
        st.session_state.history = []


    # Read csv file
    if uploaded_file is not None:
        st.session_state.df = pd.read_csv(uploaded_file)
        st.write("### Your uploaded data: ", st.session_state.df.head())

        # Create data analysis agent to query with our data
        try:
            da_agent = create_pandas_dataframe_agent(
                llm=llm,
                df=st.session_state.df,
                agent_type='zero-shot-react-description',
                allow_dangerous_code=True,
                verbose=True,
                return_intermediate_steps=True,
            )
        except Exception as e:
            raise RuntimeError(f"Failed to create pandas DataFrame agent: {e}")
        
        logger.info("### Sucessfully loaded data analysis agent !###")

        # Input query and process query
        query = st.text_input("Enter your questions: ")

        if st.button("Run query"):
            with st.spinner("Processing..."):
                process_query(da_agent, query)

    # Display chat history
    st.divider()
    display_chat_history()


    

if __name__ == "__main__":
    main()




