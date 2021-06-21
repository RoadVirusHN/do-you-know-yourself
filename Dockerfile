# Set base image (host OS)
FROM python:3.7.4

# By default, listen on port 5000
EXPOSE 5000/tcp

COPY . /app 

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# update pip
Run pip install --upgrade pip
# Install any dependencies
RUN pip install -r requirements.txt

# Specify the command to run on container start
CMD [ "python", "./server.py" ]