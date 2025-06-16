From python:3:.10-slim

RUN apt-get update && apt-get install -y gcc && apt-get clean

WORKDIR /app

COPY ..

RUN pip install --no-cach-dir -r requirements.txt

EXPOSE 8501 #Running the streamlit port

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.enableCORS=false"]

