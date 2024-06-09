FROM --platform=$TARGETPLATFORM python:3.12
ARG TARGETPLATFORM
ARG BUILDPLATFORM
RUN echo "I am running on $BUILDPLATFORM, building for $TARGETPLATFORM" > /log
COPY requirements.txt .
RUN pip install -r requirements.txt --no-deps
COPY *.py .
RUN mkdir src
CMD ["fastapi", "run", "main.py"]