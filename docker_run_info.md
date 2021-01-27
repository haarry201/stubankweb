# Docker Support
## How to build
To build the image:
`docker build . -t name:tag` will build the dockerfile and name and tag the image
## How to run
The command `docker run --rm name:tag arg1 arg2` will run the image

## Example
`docker build -t stubank:latest .`

`docker run -d -p 5000:5000 stubank`

This command will build and then run the image after downloading and installing all the required packages
The project will be available at 127.0.0.1:5000