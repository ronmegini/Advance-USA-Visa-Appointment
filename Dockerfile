FROM selenium/standalone-chrome

# Copy files
ADD . .

# Install pip
USER root
RUN sudo apt-get update
RUN sudo apt-get install -y software-properties-common
RUN sudo apt-add-repository universe
RUN sudo apt-get update
RUN sudo apt-get install -y python3-pip
RUN pip3 install -r requirements.txt
USER 1001

# Run the program
CMD ["python3", "app.py"]
