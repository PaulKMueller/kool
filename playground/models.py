"""
This module summarizes the functions used to generate the competencies.
It contains a multitude of functions that are used to extract competencies
from abstracts using different language models.
"""

import random
import galai as gal
from transformers import (XLNetTokenizer, XLNetForQuestionAnsweringSimple,
                          BloomForCausalLM, BloomTokenizerFast,
                          pipeline, AutoTokenizer, OPTForCausalLM)
from torch import argmax
from torch.nn import functional as F
from keybert import KeyBERT
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

CATEGORIES = ["Mathematics", "Computer and Informations Sciences",
                  "Physical Sciences", "Chemical Sciences",
                  "Environmental Sciences",
                  "Earth Sciences", "Biological Sciences",
                  "Civil Engineering",
                  "Electrical Engineering", "Mechanical Engineering",
                  "Chemical Engineering", "Materials Engineering",
                  "Medical Engineering", "Nano-technology", "Medicine",
                  "Health Sciences", "Agriculture, Forestry, and Fisheries",
                  "Animal and Dairy Sciences", "Veterinary Sciences",
                  "Agricultural Engineering", "Psychology",
                  "Economics and Business",
                  "Educational Sciences", "Sociology",
                  "Law", "Political Sciences",
                  "Geography", "Media and Communication",
                  "History and Archeology",
                  "Languages and Literature", "Philosophy",
                  "Ethics and Religion"]


def get_competency_from_backend(abstract: str):
    """Returns a list of competencies using KeyBERT with optimized paramters.

    Args:
        abstract (str): A scientific abstract in text format

    Returns:
        list: list in the form of [(competency, score), ...]
    """
    kw_model = KeyBERT("distilbert-base-nli-mean-tokens")
    keywords = kw_model.extract_keywords(abstract,
                                         keyphrase_ngram_range=(1, 2),
                                         use_mmr=True, diversity=0.5)

    filtered_keywords = list(filter(lambda x: x[1] > 0.4, keywords))
    return filtered_keywords


def answer_abstract_question(abstract: str):
    """Answers the question "What is the most meaningful word in the text?"
    for a given abstract.

    Args:
        abstract (str): A scienfific abstract in text format

    Returns:
        json: The answer and the confidence of the model
    """
    context = abstract
    question = "What skill is mentioned in the text?"
    qa_model = pipeline("question-answering")
    answer = qa_model(question=question,
                      context=context, max_answer_length=5)

    return {"answer": answer["answer"], "confidence": answer["score"]}


def summarize(abstract: str):
    """Summarizes a given abstract

    Args:
        abstract (str): A scientific abstract in text format
    """
    summarizer = pipeline("summarization", model="google/pegasus-xsum")
    answer = summarizer(abstract, max_length=2000)[0]["summary_text"]
    return answer


def get_mock_competency():
    """Returns a mock competency

    Returns:
        str: A mock competency
    """
    competence_list = ["ner", "sentiment-analysis", "text-generation",
                       "text-classification", "question-answering",
                       "fill-mask", "summarization", "clonation",
                       "mathematics", "linear-algebra", "analysis"]

    return random.choice(competence_list)


def ask_galactica(abstract: str, max_length_output: int = 512,
                  max_length_competencies: int = 4,
                  min_length_competencies: int = 1,
                  model_version: str = "mini"):
    """Returns galactica's answer to being asked what competencies an
    abstract author has.

    Args:
        abstract (str): A scientific abstract in text format
        max_length_output (int, optional): Maximum length in
                                           tokens of the generated text
                                           (including prompt).
        min_length_competencies (int, optional): Minimum number of words
                                                 in a competency.
        max_length_competencies (int, optional): Maximum number of words
                                                 in a competency.
        model_version (str, optional): The version of the model to use.
                                       Available versions are "mini" (125M),
                                       base (1.3 B), standard (6.7 B),
                                       large (30 B) and huge (120 B).

    Returns:
        list: list in the form of [(competency, score), ...]
    """
    model = gal.load_model(name=model_version)

    prompt = f"Extract keywords from this abstract:{abstract} \n\n Keywords:"

    # Generate keywords and refactor them to list
    competency_list = model.generate(prompt,
                                     max_length_output).replace(prompt,
                                                                "").split(',')

    # Remove unnecessary whitespaces
    competency_list = [competency.strip() for competency in competency_list]

    # Lowercase all competencies
    competency_list = [competency.lower() for competency in competency_list]

    # Remove duplicates
    competency_list = list(dict.fromkeys(competency_list))

    # Remove empty strings
    competency_list = list(filter(None, competency_list))

    # Remove competencies with more than max_length_competencies words
    competency_list = list(filter(
        lambda x: len(x.split()) <= max_length_competencies,
        competency_list))

    # Remove competencies with less than min_length_competencies words
    competency_list = list(filter(
        lambda x: len(x.split()) >= min_length_competencies,
        competency_list))

    # Set the score of each competency to -1 (default relevancy
    # for all models that do not calculate relevancy)
    competency_list = [(competency, -1) for competency in competency_list]
    return competency_list


def ask_xlnet(abstract: str, question: str = "What keyword is mentioned in the abstract?"):
    """Generates an answer to the question "What competency is mentioned in
    the abstract?" using XLNet.

    Args:
        abstract (str): A scientific abstract in text format

    Returns:
        list: A list of competencies generated by XLNet
    """
    tokenizer = XLNetTokenizer.from_pretrained("xlnet-base-cased")
    model = XLNetForQuestionAnsweringSimple.from_pretrained("xlnet-base-cased",
                                                            return_dict=True)
    inputs = tokenizer.encode_plus(question, abstract,
                                   return_tensors='pt')
    output = model(**inputs)
    start_max = argmax(F.softmax(output.start_logits, dim=-1))
    end_max = argmax(F.softmax(output.end_logits, dim=-1)) + 1
    # Add one because of python list indexing
    answer = tokenizer.decode(inputs["input_ids"][0][start_max: end_max])
    return answer


def ask_bloom(abstract: str, method: int):
    """Generates an answer to the question "What competency is mentioned in
    the abstract?" using Bloom. A method can be chosen to generate the
    answer. The methods are: 0: Greedy Search, 1: Beam Search, 2: Sampling

    Args:
        abstract (str): An abstract in text format
        method (int): The method to use for generating the answer
    """
    model = BloomForCausalLM.from_pretrained("bigscience/bloom-560m")
    tokenizer = BloomTokenizerFast.from_pretrained("bigscience/bloom-560m")
    question = "What competency is mentioned in the abstract?"
    prompt = abstract + question
    result_length = 50
    inputs = tokenizer(prompt, return_tensors="pt")

    if method == 0:
        # Greedy Search
        return tokenizer.decode(model.generate(inputs["input_ids"],
                                max_length=result_length)[0])
    elif method == 1:
        # Beam Search
        return tokenizer.decode(model.generate(inputs["input_ids"],
                                max_length=result_length,
                                num_beams=2,
                                no_repeat_ngram_size=2,
                                early_stopping=True)[0])
    elif method == 2:
        # Sampling Top-k + Top-p
        return tokenizer.decode(model.generate(inputs["input_ids"],
                                               max_length=result_length,
                                               do_sample=True,
                                               top_k=50,
                                               top_p=0.9)[0])


def ask_keybert(abstract: str, use_mmr: bool = True,
                diversity: float = 0.5, keyphrase_ngram_range: tuple = (1, 2),
                minimum_relevancy: float = 0.4):
    """Extracts keywords from an abstract using KeyBert.

    Args:
        abstract (str): A scientific abstract in text format

    Returns:
        list: [[keyword, relevancy], [keyword, relevancy], ...]
    """
    kw_model = KeyBERT("distilbert-base-nli-mean-tokens")
    keywords = kw_model.extract_keywords(
        abstract,
        keyphrase_ngram_range=keyphrase_ngram_range,
        use_mmr=use_mmr, diversity=diversity)

    # Filter keywords with relevancy below minimum_relevancy
    filtered_keywords = list(filter(lambda x: x[1] > minimum_relevancy,
                                    keywords))
    return filtered_keywords


def get_category_of_competency(competence: str):
    """Maps one of the 33 categories to a given competence based on
    the competence's similarity to the category's keywords.

    Args:
        competence (str): The string representation of a competence
    """
    competency_and_categories = [competence] + CATEGORIES
    model = SentenceTransformer("bert-base-nli-mean-tokens")
    categories_embeddings = model.encode(competency_and_categories)
    similarities = cosine_similarity([categories_embeddings[0]],
                                     categories_embeddings[1:])
    # Get index with maximum similarity, convertion to int, as fastapi
    # cant handle numpy int
    index = int(similarities[0].argmax())
    return index


def ask_gpt_neo(abstract: str,
                min_length_competencies: int = 1,
                max_length_competencies: int = 4,
                max_length_output: int = 512,
                model_version: str = "EleutherAI/gpt-neo-125M",
                temperature: float = 0.00001):
    """Generates text based on an abstract using GPT-Neo.

    Args:
        abstract (str): A scientific abstract in text format
        min_length_competencies (int): The minimum length of
                                       a competency in words
        max_length_competencies (int): The maximum length of
                                       a competency in words
        max_length_output (int): The maximum length of the output
                                 generated by GPT-Neo
        model_version (str): The model version to use
        temperature (float): The temperature to use for sampling


    Returns:
        list: A list of generated texts
    """
    prompt = f"Extract keywords from this abstract:{abstract} \n\n Keywords:"
    generator = pipeline(
                         "text-generation",
                         model=model_version,
                         max_length=max_length_output,
                         do_sample=True,
                         temperature=temperature
                         )
    response = generator(prompt)[0]['generated_text']

    # Remove prompt and abstract from response
    response = response.replace(abstract, "")
    response = response.replace("Extract skills from this abstract:", "")
    response = response.replace("\n\n Keywords:", "")

    # Split response to get single competencies
    competency_list = response.split(',')

    # Remove unnecessary whitespaces
    competency_list = [competency.strip() for competency in competency_list]

    # Lowercase all competencies
    competency_list = [competency.lower() for competency in competency_list]

    # Remove duplicates
    competency_list = list(dict.fromkeys(competency_list))

    # Add -1 as relevancy for each competency (default value
    # for models that do not calcute relevancy)
    competency_list = [(competency, -1) for competency in competency_list]

    # Remove empty competencies
    competency_list = [
        competency for competency in competency_list if competency[0] != '']

    # Remove all competencies that have more than max_length_competencies words
    competency_list = [
        competency for competency in competency_list if len(
            competency[0].split()) <= max_length_competencies]

    # Remove all competencies that have less than min_length_competencies words
    competency_list = [
        competency for competency in competency_list if len(
            competency[0].split()) >= min_length_competencies]

    return competency_list
