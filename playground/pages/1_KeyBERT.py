"""Creates a streamlit app for the playground.
The playground is used to test the model_api and the database_api.
"""

import os
import requests
import streamlit as st
from pandas import DataFrame
import seaborn as sns
from download_button import download
from models import ask_keybert


st.set_page_config(
    page_title="Kool - Competency Extractor",
    page_icon="👨‍🔬",
)

use_mmr = True


def validate_min_max():
    return (minimum_number_of_keywords > maximum_number_of_keywords)


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
    st.title("🔑 KeyBERT")
    st.header("")

with st.expander("ℹ️ - About this interface", expanded=True):

    st.write(
        ("The *Kool - Competency Extractor* app is an easy-to-use "
            "interface built in [Streamlit](https://streamlit.io/).\n "
            "It uses minimal keyword extraction techniques that "
            "leverage multiple NLP embeddings and rely on "
            "[Transformers](https://huggingface.co/transformers/) 🤗 "
            "to extract competencies "
            "that are most similar to a given document.\n\n"
            "On this site you can experiment with different parametrizations"
            " of the model [KeyBERT](https://github.com/MaartenGr/KeyBERT) "
            "by Maarten Grootendorst"
            " and download the results in different formats.")
    )

    st.markdown("")

st.markdown("")
st.markdown("## **📌 Paste document **")
with st.form(key="my_form"):

    ce, c1, c2, c3 = st.columns([0.07, 2, 5, 0.07])
    with c1:
        ModelType = st.radio(
            "Your model:",
            ["KeyBERT",],
            help=("This is your chosen model."),
        )

        use_mmr = st.checkbox(
            "Use MMR:",
            value=True,
            help=("""Maximal Marginal Relevance (MMR).
                     Calculates the similarity between generated keywords.
                     The returned keywords are dissimilar, based on the MMR."""),
        )

        minimum_number_of_keywords = st.slider(
            "Minimum number of keywords:",
            min_value=1,
            max_value=5,
            value=1,
            help=("""The minimum number of keywords to extract.
                    The default is 1."""),
        )

        maximum_number_of_keywords = st.slider(
            "Maximum number of keywords:",
            min_value=1,
            max_value=5,
            value=2,
            help=("""The maximum number of keywords to extract.
                     The default is 2."""),
        )

        diversity = st.slider(
            "Diversity:",
            min_value=0.0,
            max_value=1.0,
            value=0.5,
            step=0.1,
            help=("""The diversity of the keywords.
                        The default is 0.5.
                        Only used when MMR is enabled."""),
        )

        minimum_relevancy = st.slider(
            "Minimum relevancy:",
            min_value=0.0,
            max_value=1.0,
            value=0.4,
            step=0.1,
            help=("""The minimum relevancy of the keywords.
                     The default is 0.4."""),
        )

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


keywords = []
if ModelType == "KeyBERT":
    keywords = ask_keybert(
        abstract=doc,
        use_mmr=use_mmr,
        diversity=diversity,
        keyphrase_ngram_range=(
            minimum_number_of_keywords,
            maximum_number_of_keywords),
        minimum_relevancy=minimum_relevancy)

st.markdown("## **🔎 Check & download results **")

st.header("")

cs, c1, c2, c3, cLast = st.columns([2, 1.5, 1.5, 1.5, 2])

with c1:
    download(keywords, "Data.csv", "📅 Download (.csv)")
with c2:
    download(keywords, "Data.txt", "📄 Download (.txt)")
with c3:
    download(keywords, "Data.json", "📥 Download (.json)")

st.header("")

df = (
    DataFrame(keywords, columns=["Keyword/Keyphrase", "Relevancy"])
    .sort_values(by="Relevancy", ascending=False)
    .reset_index(drop=True)
)

df.index += 1

# Add styling
cmGreen = sns.light_palette("green", as_cmap=True)
cmRed = sns.light_palette("red", as_cmap=True)
df = df.style.background_gradient(
    cmap=cmGreen,
    subset=[
        "Relevancy",
    ],
)

c1, c2, c3 = st.columns([1, 3, 1])

format_dictionary = {
    "Relevancy": "{:.1%}",
}

df = df.format(format_dictionary)

with c2:
    st.table(df)
