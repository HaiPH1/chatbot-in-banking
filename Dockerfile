FROM ubuntu:18.04
MAINTAINER QuangPH <pham.huu.quang@sun-asterisk.com>

RUN apt-get update
RUN apt-get install -y \
        software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update && apt-get install -y \
        python3.7 \
        python3-pip
RUN python3.7 -m pip install pip
RUN cd /usr/local/bin
RUN ln -s /usr/bin/python3.7 python
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 1
RUN pip3 install -U pip

RUN mkdir /chatbot
WORKDIR /chatbot
COPY requirements.txt /chatbot/requirements.txt
RUN pip3 install rasa
RUN pip3 install -r requirements.txt
CMD ["./run.sh"]

EXPOSE 8000/tcp
