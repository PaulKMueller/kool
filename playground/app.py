"""
Creates a streamlit app for the playground.
The playground is used to test the model_api and the database_api.
"""

import streamlit as st
from pandas import DataFrame
from keybert import KeyBERT
import seaborn as sns
import requests
from download_button import download
import os

ENVIRONMENT_VARIABLE_MODEL_API_PORT = "MODEL_API_PORT"
MODEL_API_PORT = os.environ.get(ENVIRONMENT_VARIABLE_MODEL_API_PORT)

URL_OF_MODEL_API = "http://model_api:" + MODEL_API_PORT


def get_request_from_api(endpoint):
    """ This function sends a get request to the
    model_api and returns the response as json

    Args:
        endpoint (str): The endpoint of the model_api 

    Returns:
        json: The response of the model_api
    """
    response = requests.get(URL_OF_MODEL_API + endpoint)
    return response.json()


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
    st.title("👨‍🔬 Kool - Kompetency Extractor")
    st.header("")

with st.expander("ℹ️ - About this interface", expanded=True):

    st.write(
        ("The *Kool - Competency Extractor* app is an easy-to-use "
            "interface built in [Streamlit](https://streamlit.io/)"
            " for the amazing [KeyBERT]"
            "(https://github.com/MaartenGr/KeyBERT) library from "
            "Maarten Grootendorst!\n"
            "It uses a minimal keyword extraction technique that "
            "leverages multiple NLP embeddings and relies on "
            "[Transformers](https://huggingface.co/transformers/) 🤗 "
            "to extract competencies "
            "that are most similar to a document.")
    )

    st.markdown("")

st.markdown("")
st.markdown("## **📌 Paste document **")
with st.form(key="my_form"):

    ce, c1, c2, c3 = st.columns([0.07, 2, 5, 0.07])
    with c1:
        ModelType = st.selectbox(
            "Choose your model",
            ["KeyBERT (Default)", "Galactica 125M"],
            help=("These are the available models. "
                  "In applications frontend, DistilBERT is used."),
        )

        if ModelType == "KeyBERT (Default)":
            @st.cache(allow_output_mutation=True)
            def load_model():
                """Returns a KeyBERT model.

                Returns:
                    KeyBERT: A KeyBERT model
                """
                return KeyBERT("distilbert-base-nli-mean-tokens")

            kw_model = load_model()

            top_N = st.slider(
                "# of results",
                min_value=1,
                max_value=30,
                value=10,
                help=("You can choose the number of keywords/keyphrases "
                      "to display. Between 1 and 30, default number is 10."),
            )

            min_Ngrams = st.number_input(
                "Minimum Ngram",
                min_value=1,
                max_value=4,
                help=("The minimum value for the ngram range."
                      "\n\n*Keyphrase_ngram_range* sets the length"
                      "of the resulting keywords/keyphrases."
                      "\n\nTo extract keyphrases, simply set "
                      "*keyphrase_ngram_range* to (1, 2) or higher depending "
                      "on the number of words you would "
                      "like in the resulting keyphrases."),

            )

            max_Ngrams = st.number_input(
                "Maximum Ngram",
                value=2,
                min_value=1,
                max_value=4,
                help=("The maximum value for the keyphrase_ngram_range."
                      "\n\n*Keyphrase_ngram_range* sets the length "
                      "of the resulting keywords/keyphrases."
                      "\n\nTo extract keyphrases, simply set "
                      "*keyphrase_ngram_range* to (1, 2) or higher "
                      "depending on the number of words you would "
                      "like in the resulting keyphrases."),
            )

            StopWordsCheckbox = st.checkbox(
                "Remove stop words",
                help=("Tick this box to remove stop words "
                      "from the document (currently English only)"),
            )

            use_MMR = st.checkbox(
                "Use MMR",
                value=True,
                help=("You can use Maximal Margin Relevance "
                      "(MMR) to diversify the results. "
                      "It creates keywords/keyphrases based ",
                      "on cosine similarity. "
                      "Try high/low 'Diversity' settings "
                      "below for interesting variations."),
            )

            Diversity = st.slider(
                "Keyword diversity (MMR only)",
                value=0.5,
                min_value=0.0,
                max_value=1.0,
                step=0.1,
                help=("The higher the setting, the more diverse the keywords."
                      "\n\nNote that the *Keyword diversity* slider "
                      "only works if the *MMR* checkbox is ticked."),
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

    if StopWordsCheckbox:
        STOPWORDS = "english"
    else:
        STOPWORDS = None

if not submit_button:
    st.stop()

if min_Ngrams > max_Ngrams:
    st.warning("min_Ngrams can't be greater than max_Ngrams")
    st.stop()

keywords = kw_model.extract_keywords(
    doc,
    keyphrase_ngram_range=(min_Ngrams, max_Ngrams),
    use_mmr=use_MMR,
    stop_words=STOPWORDS,
    top_n=top_N,
    diversity=Diversity,
)

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
