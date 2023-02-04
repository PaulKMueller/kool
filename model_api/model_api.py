"""
This API exposes different endpoints that can be used
to extract competencies from abstracts.
"""

import uvicorn
from fastapi import FastAPI
from models import (ask_pegasus, get_mock_competency,
                    ask_galactica, ask_xlnet, ask_bloom, ask_keybert,
                    get_competency_from_backend, ask_gpt_neo, get_category_of_competency)


app = FastAPI()


@app.get("/")
async def root():
    """Root endpoint.

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
async def gpt_neo(abstract: str):
    """Returns a list of competencies from an abstract using gpt-neo-2.7B

    Args:
        abstract (string): Text of the abstract from which
        competencies are extracted

    Returns:
        string: Response from the model
    """
    return ask_gpt_neo(abstract)


@app.get("/ask_pegasus/{abstract}")
async def pegasus(abstract: str):
    """Summarizes a given abstract.

    Returns:
        string: Response from the model
    """
    return ask_pegasus(abstract)


@app.get("/get_mock_competency/")
async def get_mock_competencies():
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
    """Xlnet's response to a prompt trying to extract competencies
    from an abstract.

    Returns:
        string: The model's response to the prompt.
    """
    return ask_xlnet(abstract)


@app.get("/ask_bloom/{abstract}")
async def bloom(abstract: str):
    """Bloom's response to a prompt trying to extract competencies
    from an abstract using the given method (default: 0).

    abstract (string): Text of the abstract from which competencies are extracted.

    Returns:
        string: The model's response to the prompt.
    """
    return ask_bloom(abstract)


@app.get("/ask_keybert/{abstract}")
async def keybert(abstract: str):
    """Tests keybert model's response to a prompt trying
    to extract competencies from an abstract.

    Returns:
        list: The model's response to the prompt.
    """
    return ask_keybert(abstract)
