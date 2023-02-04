"""Creates a streamlit app for the playground.
The playground is used to test the model_api and the database_api.
"""

import streamlit as st
from pandas import DataFrame
from download_button import download
from models import ask_keybert, ask_galactica, ask_gpt_neo, ask_bloom


st.set_page_config(
    page_title="Kool - Competency Extractor",
    page_icon="👨‍🔬",
)


def _max_width_():
    max_width_str = "max-width: 1400px;"
    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}
    </style>
    """,
        unsafe_allow_html=True,
    )


_max_width_()

c30, c31, c32 = st.columns([2.5, 1, 3])

with c30:
    st.title("🏠 Kool - Competency Extractor - Benchmark")
    st.header("")

with st.expander("ℹ️ - About this interface", expanded=True):

    st.write(
        ("The *Kool - Competency Extractor* app is an easy-to-use "
            "interface built in [Streamlit](https://streamlit.io/).\n\n"
            "It uses a minimal keyword extraction technique that "
            "leverages multiple NLP embeddings and relies on "
            "[Transformers](https://huggingface.co/transformers/) 🤗 "
            "to extract competencies "
            "that are most similar to a document.\n\n"
            "All selected models will be benchmarked input document. "
            "The results are displayed in a table.")
    )

    st.markdown("")

st.markdown("")
st.markdown("## **📌 Paste document **")
with st.form(key="my_form"):

    ce, c1, c2, c3 = st.columns([0.07, 2, 5, 0.07])
    with c1:
        keybert = st.checkbox(
            "KeyBERT")
        galactica = st.checkbox(
            "Galactica 125M")
        gpt_neo = st.checkbox(
            "GPT-Neo 125M")
        bloom = st.checkbox(
            "Bloom 560M")

    with c2:
        doc = st.text_area(
            "Paste your text below (max 1000 words)",
            height=510,
        )

        MAX_WORDS = 1000
        import re
        res = len(re.findall(r"\w+", doc))
        if res > MAX_WORDS:
            st.warning(
                "⚠️ Your text contains "
                + str(res)
                + " words."
                + (" Only the first 1000 words will be reviewed. Since this "
                   "application is supposed to be used for abstracts, please "
                   "limit your text to 1000 words.")
            )

            doc = doc[:MAX_WORDS]

        submit_button = st.form_submit_button(label="📈 Get me the data!")

if not submit_button:
    st.stop()

keywords_keybert = []
keywords_galactica = []
keywords_gpt_neo = []
keywords_bloom = []

if keybert:
    keywords_keybert = ask_keybert(doc)
    # Get only keywords not relevancy
    keywords_keybert = [keyword[0] for keyword in keywords_keybert]
if galactica:
    keywords_galactica = ask_galactica(doc)
    # Get only keywords not relevancy
    keywords_galactica = [keyword[0] for keyword in keywords_galactica]
if gpt_neo:
    keywords_gpt_neo = ask_gpt_neo(doc)
    # Get only keywords not relevancy
    keywords_gpt_neo = [keyword[0] for keyword in keywords_gpt_neo]
if bloom:
    keywords_bloom = ask_bloom(abstract=doc)
    # Get only keywords not relevancy
    keywords_bloom = [keyword[0] for keyword in keywords_bloom]

st.markdown("## **🔎 Check & download results **")

st.header("")

cs, c1, c2, c3, cLast = st.columns([2, 1.5, 1.5, 1.5, 2])

result_dict = {}
if keybert:
    result_dict["KeyBERT"] = keywords_keybert
if galactica:
    result_dict["Galactica 125M"] = keywords_galactica
if gpt_neo:
    result_dict["GPT-Neo 125M"] = keywords_gpt_neo
if bloom:
    result_dict["Bloom 560M"] = keywords_bloom

with c1:
    download(
        result_dict, "Data.csv", "📅 Download (.csv)")
with c2:
    download(
        result_dict, "Data.txt", "📄 Download (.txt)")
with c3:
    download(
        result_dict, "Data.json", "📥 Download (.json)")

st.header("")

# Max keyword length
max_len = max(len(keywords_keybert),
              len(keywords_galactica),
              len(keywords_gpt_neo),
              len(keywords_bloom))

# Fill all keywords lists with empty strings
keywords_keybert += [""] * (max_len - len(keywords_keybert))
keywords_galactica += [""] * (max_len - len(keywords_galactica))
keywords_gpt_neo += [""] * (max_len - len(keywords_gpt_neo))
keywords_bloom += [""] * (max_len - len(keywords_bloom))

# Build dataframe dictionary based on checked checkboxes


df = (
    DataFrame(result_dict)
    .reset_index(drop=True)
)

df.index += 1


c1, c2, c3 = st.columns([1, 3, 1])

with c2:
    st.table(df)
