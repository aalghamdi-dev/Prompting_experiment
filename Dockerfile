
FROM python:3.12


WORKDIR /PROMTING_EXPERIMENT


RUN pip install --no-cache-dir openai


COPY . .


CMD ["python", "PromptsTesting.py"]