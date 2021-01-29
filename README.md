# Docker Support
## How to build
To build the image:
`docker build . -t name:tag` will build the dockerfile and name and tag the image
## How to run
The command `docker run --rm name:tag arg1 arg2` will run the image

## Example
`docker build -t stubank:latest .`

`docker run -d -p 5000:5000 stubank`

These commands will build and then run the image after downloading and installing all the required packages  
The project will be available if you type `127.0.0.1:5000` into your browser.

#Login Information
##Admin Account
Email: `admin@stubank.co.uk`  
Password: `Password1`  
Security Question: `What is your mother's maiden name?`  
Security Answer: `mum`

##Normal User Account
Email: `user@stubank.co.uk`  
Password: `Password2`  
Security Question: `What was your first pet's name?`  
Security Answer: `User`