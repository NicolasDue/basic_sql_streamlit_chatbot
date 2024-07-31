FROM python:3.10

# Update system packages
RUN apt-get update && apt-get install -y build-essential

# Set environment variables
ENV PATH "/root/.local/bin:$PATH"
ENV PYTHONPATH="$PYTHONPATH:/app"
ENV PORT 8501

# Install Python dependencies
COPY requirements.txt /.
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /code
COPY app app

# Run streamlit in app/main
CMD ["streamlit", "run", "app/main.py"]