import validators, streamlit as st
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader

import os
from dotenv import load_dotenv
load_dotenv()
os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")

## sstreamlit APP
st.set_page_config(page_title="Summarize Text From YT or Website", page_icon="💬")
st.title("Summarize Text from Youtube or a Website")
st.subheader('Summarize URL')

# Get the URL
generic_url=st.text_input("URL",label_visibility="collapsed")

## Gemma Model USsing Groq API
llm=ChatGroq(model="Gemma-7b-It")

# Prompt Template
prompt_template="""
Provide a summary of the following content in 400 words:
Content: {text}

"""
prompt=PromptTemplate(template=prompt_template,input_variables=["text"])

if st.button("Summarize"):
    ## Validate all the inputs
    if not generic_url.strip():
        st.error("Please provide the information to get started")
    elif not validators.url(generic_url):
        st.error("Please enter a valid Url. It can be a YT video or a website")

    else:
        try:
            with st.spinner("Waiting..."):
                ## loading the website or yt video data
                if "youtube.com" in generic_url:
                    loader=YoutubeLoader.from_youtube_url(generic_url, add_video_info=True)
                else:
                    loader=UnstructuredURLLoader(urls=[generic_url], ssl_verify=False,
                                                 headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"})
                docs=loader.load()

                ## Chain For Summarization
                chain=load_summarize_chain(llm, chain_type="stuff", prompt=prompt)
                output_summary=chain.run(docs)

                st.success(output_summary)
        except Exception as e:
            st.exception(f"Exception:{e}")