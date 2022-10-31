
# First Stage - install selenium python module and dependencies
FROM selenium/standalone-chrome@sha256:5e9c5548a1e7e8e0b51424f24ac6abd746edbd98c07983c793ee50c597e5ccbd as stageone

# Copy files
ADD requirements.txt .

# Install pip
USER root
RUN sudo apt-get update
RUN sudo apt-get install -y software-properties-common
RUN sudo apt-add-repository universe
RUN sudo apt-get update
RUN sudo apt-get install -y python3-pip
# Install selenium
RUN pip3 install -r requirements.txt



# Second Stage - Copy files, modules from stage one and define CND execution
FROM selenium/standalone-chrome

# Copy files
ADD code .
# Become root
USER root
# Copy python dependencies for selenium
COPY --from=stageone /usr/local/lib/python3.8/dist-packages/ /usr/local/lib/python3.8/dist-packages/
COPY --from=stageone /usr/lib/python3/dist-packages /usr/local/lib/python3.8/dist-packages/

# Change back to weak user
USER 1001
# What is the running environmnent
ENV CONTAINER_RUNNING=true
# CMD execution
CMD ["python3", "app.py"]