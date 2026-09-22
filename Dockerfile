# LLMAutodoc — container image.
#
#   docker build -t llmautodoc .
#   docker run --rm -e ANTHROPIC_API_KEY -v "$PWD/renderedDocs:/app/renderedDocs" \
#       llmautodoc https://github.com/se4ai2122-cs-uniba/CT-COVID.git --out renderedDocs/ct-covid
#
# Keys are passed as environment variables at run time (-e NAME, or -e NAME=value) and are
# never baked into the image. renderedDocs/ is mounted so that the outputs land on the host.
# Any main.py argument works after the image name; to run the experiment campaign instead:
#   docker run --rm -e ANTHROPIC_API_KEY -v "$PWD/renderedDocs:/app/renderedDocs" \
#       --entrypoint python llmautodoc run_experiments.py --only ct-covid --runs 2

FROM python:3.11-slim

# git: the repository to document is cloned and its history is read by the extractors.
RUN apt-get update \
 && apt-get install -y --no-install-recommends git \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY llmautodoc/ llmautodoc/
COPY evaluation/ evaluation/
COPY main.py run_experiments.py config.yaml ./

# Outputs go here; mount it from the host to keep them.
RUN mkdir -p renderedDocs
VOLUME ["/app/renderedDocs"]

ENV PYTHONUNBUFFERED=1
ENTRYPOINT ["python", "main.py"]
CMD ["--help"]
