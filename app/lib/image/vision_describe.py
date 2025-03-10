from .image_describe.gemini_vision_describe import gemini_vision_describe
from .image_describe.ollama_vision_describe import ollama_vision_describe


def vision_describe(image_path, model='gemini'):

    if model == 'gemini':
        result = gemini_vision_describe(image_path)
    else:
        result = ollama_vision_describe(image_path)

    # print(result)

    return result