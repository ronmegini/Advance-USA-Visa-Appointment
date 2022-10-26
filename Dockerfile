FROM selenium/standalone-chrome@sha256:5e9c5548a1e7e8e0b51424f24ac6abd746edbd98c07983c793ee50c597e5ccbd as stageone

# Copy files
# ADD . .

# Install pip
USER root
RUN sudo apt-get update
RUN sudo apt-get install -y software-properties-common
RUN sudo apt-add-repository universe
RUN sudo apt-get update
RUN sudo apt-get install -y python3-pip
RUN pip3 install -r requirements.txt
#USER 1001
#ENV CONTAINER_RUNNING=true

# Run the program
#CMD ["python3", "app.py"]

FROM selenium/standalone-chrome

ADD . .
USER root
COPY --from=stageone /usr/local/lib/python3.8/dist-packages/selenium /usr/local/lib/python3.8/dist-packages
USER 1001
ENV CONTAINER_RUNNING=true
CMD ["python3", "app.py"]