"""Creates a streamlit app for the playground.
The playground is used to test the model_api and the database_api.
"""

import streamlit as st
from pandas import DataFrame
import seaborn as sns
from download_button import download
from models import ask_gpt_neo

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
    st.title("🦾 GPT-Neo")
    st.header("")

with st.expander("ℹ️ - About this interface", expanded=True):

    st.write(
        ("The *Kool - Competency Extractor* app is an easy-to-use "
            "interface built in [Streamlit](https://streamlit.io/). "
            "It uses minimal keyword extraction techniques that "
            "leverage multiple NLP embeddings and rely on "
            "[Transformers](https://huggingface.co/transformers/) 🤗 "
            "to extract competencies "
            "that are most similar to a given document. \n\n"
            "On this site you can experiment with different parametrizations"
            " of the model "
            "[GPT-Neo](https://huggingface.co/EleutherAI/gpt-neo-125M) "
            "by [EleutherAI](https://www.eleuther.ai/)."
            " For further information about this model see its "
            "[documentation](https://galactica.org/static/paper.pdf) "
            "in HuggingFace.")
    )

    st.markdown("")

st.markdown("")
st.markdown("## **📌 Paste document **")
with st.form(key="my_form"):

    ce, c1, c2, c3 = st.columns([0.07, 2, 5, 0.07])
    with c1:
        ModelType = st.radio(
            "Your model:",
            ["GPT-Neo"],
            help=("This is your chosen model."),
        )

        max_length_output = st.selectbox(
            "Max length output:",
            [512, 64, 128, 256, 1024, 2048, 4096],
            help=("This is the maximum length of the "
                  "output generated GPT-Neo.\n\n"
                  "The default value is 512. "
                  "Only powers of 2 are allowed."),
        )

        min_length_competencies = st.slider(
            "Minimum length of competencies:",
            min_value=1,
            max_value=5,
            value=1,
            help=("This is the minimum length of the competencies "
                  "being generated. \n\n"
                  "The default value is 1."),
        )

        max_length_competencies = st.slider(
            "Maximum length of competencies:",
            min_value=1,
            max_value=5,
            value=4,
            help=("This is the maximum length of the competencies "
                  "being generated. \n\n"
                  "The default value is 4."),
        )

        temperature = st.slider(
            "Temperature:",
            min_value=0.00001,
            max_value=1.0,
            value=0.00001,
            help=("This is the temperature used by the model."
                  "\n\n"
                  "The default value is 0.00001."),
        )

        model_version = st.selectbox(
            "Model version:",
            ["gpt-neo-125M", "gpt-neo-1.3B", "gpt-neo-2.7B"],
            help=("This is the version of your chosen model.\n\n"
                  "The default version is gpt-neo-125M. "
                  "The number indicates "
                  "the number of parameters."),
        )

        st.warning(
            "⚠️ If you are unsure if your device is able to handle the "
            "bigger models,  use the 125M parameter version!"
        )

    with c2:
        doc = st.text_area(
            "Paste your text below (max 1000 words)",
            height=680,
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
if ModelType == "GPT-Neo":
    keywords = ask_gpt_neo(abstract=doc,
                           model_version="EleutherAI/" + model_version,
                           max_length_output=max_length_output,
                           min_length_competencies=min_length_competencies,
                           max_length_competencies=max_length_competencies,
                           temperature=temperature)

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
