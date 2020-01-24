FROM python:3
ADD src /code
CMD [ "python", "/code/run.py"]
