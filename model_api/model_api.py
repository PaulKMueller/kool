"""
This API exposes different endpoints that can be used
to extract competencies from abstracts.
"""

import uvicorn
from fastapi import FastAPI
from models import (answer_abstract_question, summarize, get_mock_competency,
                    ask_galactica, ask_xlnet, ask_bloom, ask_keybert,
                    get_competency_from_backend, ask_gpt_neo, get_category_of_competency)


app = FastAPI()


@app.get("/")
async def root():
    """Root endpoint

    Returns:
        json: Welcome message
    """
    return ("Welcome to the kool backend. This backend provides "
            "multiple endpoints to extract competencies from abstracts. "
            "For more in depth information about the endpoints and their "
            "details, please visit http://127.0.0.1:8000/docs.")


@app.get("/get_competency/{abstract}")
def get_competency(abstract: str):
    """Standard endpoint for extracting competencies from an abstract.
    Optimized for best possible results. This endpoint is also visualized
    in the playground.

    Args:
        abstract (str): An abstract from which competencies are extracted
    """
    return get_competency_from_backend(abstract)


@app.get("/get_category_of_competency/{competency}")
def get_category(competency: str):
    """Endpoint for getting the category of a specific competency. Returns
    the id of the category.

    Args:
        competency (str): a competency

    Returns:
        int: id of the category
    """
    return get_category_of_competency(competency)


@app.get("/ask_gpt_neo/{abstract}")
async def get_competencies_from_abstract(abstract: str):
    """Returns a list of competencies from an abstract using gpt-neo-2.7B

    Args:
        abstract (string): Text of the abstract from which
        competencies are extracted

    Returns:
        string: Response from the model
    """
    return ask_gpt_neo(abstract)


@app.get("/question_answering/{abstract}")
async def get_competencies_from_test_abstract(abstract: str):
    """This endpoint is used to test the question answering model.
    Its output is saved in test_out.
    """

    return answer_abstract_question(abstract)


@app.get("/summarize/{abstract}")
async def test_summarizatino(abstract: str):
    """Extracts competencies from the abstracts in test_in/data.xlsx
    using summarization model and saves the output in test_out/output.xlsx

    Returns:
        string: Response from the model
    """
    return summarize(abstract)


@app.get("/get_mock_competency/")
async def get_mock_competences():
    """Used create a mock output for the frontend.

    Returns:
        json: A json object with a list of competencies.
    """
    return get_mock_competency()


@app.get("/ask_galactica/{abstract}")
async def galactica(abstract: str):
    """Tests galactica 1.3b model's response to a prompt trying to extract
    competencies from an abstract.

    Returns:
        string: The model's response to the prompt.
    """
    return ask_galactica(abstract)


@app.get("/ask_xlnet/{abstract}")
async def xlnet(abstract: str):
    """Tests xlnet model's response to a prompt trying to extract competencies
    from an abstract.

    Returns:
        string: The model's response to the prompt.
    """
    return ask_xlnet(abstract)


@app.get("/ask_bloom/{abstract}/{method}")
async def bloom(abstract: str, method: int = 0):
    """Tests bloom model's response to a prompt trying to extract competencies
    from an abstract using the given method (default: 0).

    Args:
        method (int): The method used internally by the model to generate
        text. 0 for greedy, 1 for beam search, 2 for top-k sampling.

    Returns:
        string: The model's response to the prompt.
    """
    return ask_bloom(abstract, int(method))


@app.get("/ask_keybert/{abstract}")
async def get_keybert_answer(abstract: str):
    """Tests keybert model's response to a prompt trying
    to extract competencies from an abstract.

    Returns:
        list: The model's response to the prompt.
    """
    return ask_keybert(abstract)
