FROM continuumio/anaconda3
COPY . .
WORKDIR /src
# RUN conda update anaconda -y
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 8810
CMD python main.py
# CMD streamlit run upload.py --server.port 8899
