# StuBank Project

To Run the project, it can be built and ran using docker using the instructions below and the dockerfile. Alternatively, it can also be open in PyCharm or another python IDE, and built and ran, using the pipfile to set up the working environment.

Depending on the connection speed and system performance, this may take time in both docker, and loading the project 


## Docker Support
### How to build
To build the image, type the following command into your terminal or command prompt:  
`docker build . -t name:tag`  
This command will build the dockerfile, and give the image a name and tag.
### How to run
The command `docker run --rm name:tag arg1 arg2` will run the image

### Example
`docker build -t stubank:latest .`

`docker run -d -p 5000:5000 stubank`

This command will build and then run the image after downloading and installing all the required packages
The project will be available at the local host port that was specified, so in this instance: [127.0.0.1:5000](127.0.0.1:5000)



## Login Information
### Admin Account
Email: `admin@stubank.co.uk`  
Password: `Password1`  
Security Question: `What is your mother's maiden name?`  
Security Answer: `mum`

### Normal User Account
Email: `user@stubank.co.uk`  
Password: `Password2`  
Security Question: `What was your first pet's name?`  
Security Answer: `User`


Two Factor Authentication has been disabled for both these accounts