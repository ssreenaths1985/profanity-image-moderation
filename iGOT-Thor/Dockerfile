FROM python:3.7
ENV CONDA_PREFIX /usr/local
RUN apt update -y && apt install -y libgl1-mesa-glx libegl1-mesa
ADD . /app
WORKDIR /app
RUN pip3 install -r req.txt
RUN pip3 install -r req2.txt
#RUN pip3 install -r requirements.txt
RUN  cd  patch && ./linux.sh
RUN python -m spacy download en
EXPOSE 5006
CMD [ "python3", "app.py" ]

