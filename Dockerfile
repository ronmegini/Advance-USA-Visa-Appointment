FROM selenium/standalone-chrome

# Copy files
ADD . .

# Install pip
USER root
RUN sudo apt-get update
RUN sudo apt-get install -y software-properties-common
RUN sudo apt-add-repository universe
RUN sudo apt-get update
RUN sudo apt-get install python3-pip
#RUN wget https://bootstrap.pypa.io/get-pip.py
#RUN python3 get-pip.py
RUN pip3 install -r requirements.txt
USER 1001

# Run the program
CMD ["python", "app.py"]