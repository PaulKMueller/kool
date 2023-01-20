# kool (KompetenzpOOL)

## Name
kool (KompetenzpOOL)

>[!Info]
> This README is currently under construction and not yet finished

## Description
Let people know what your project can do specifically. Provide context and add a link to any reference visitors might be unfamiliar with. A list of Features or a Background subsection can also be added here. If there are alternatives to your project, this is a good place to list differentiating factors.

## Quick-Installation guide

1. [Install Docker Desktop](https://docs.docker.com/get-docker/)
2. Clone this Repository and open it up using an IDE (we recommend using VS Code) or in the command shell.
3. Open up the ".env" file and specify the IPv4 addresses of the Frontend and Playground Host and the ports, which the Services should be running on.  
4. Open a command shell in the main folder and type
> docker compose up
5. The Application should now be running on http://FRONTEND_HOST:FRONTEND_PORT, e.g. http://localhost:8000

*View detailed Installation Guide for more information*

## Installation Guide
### Requirements
- When installing model_api and playground we recommend at least 10GB of storage as the models are big. When you dont want to install them view [...]
- Docker must be installed (Tested on Docker version 20.10.20 and Docker Desktop v4.13.1, but other versions might work too)
- When running the model_api you either need a good GPU or much patience
### Installation
1. Make sure your system meets the [requirements](kool#Installation Guide#Installation)  
2. Clone this Repository and open it up using an IDE (we recommend using VS Code) or in the command shell.
3. Open up the ".env" file and specify the IPv4 addresses of the Frontend and Playground Host and the ports, which the Services should be running on.  
4. If you only want to run the Main-Application (Frontend and Database) without the playground and model_api open up the docker-compose.yml and comment it from line 35 (model_api) till the end using a # in each line
5. Open a command shell (Terminal -> New Terminal in VS Code) in the main directory (where the docker-compose.yml sits) and run
> docker compose up
*if you already build the container in the past but changed something in the docker-compose-yml or in one of the Dockerfiles run*
> docker compose up --build
*to apply those changes*
6. Wait for the container to build. When installing model_api and playground go grab a coffee. Building the container can take up to 20 min (at least on our crappy laptops)
7. The Application should now be running on http://FRONTEND_HOST:FRONTEND_PORT, e.g. http://localhost:8000

## Visuals
Depending on what you are making, it can be a good idea to include screenshots or even a video (you'll frequently see GIFs rather than actual videos). Tools like ttygif can help, but check out Asciinema for a more sophisticated method.


## Usage
Use examples liberally, and show the expected output if you can. It's helpful to have inline the smallest example of usage that you can demonstrate, while providing links to more sophisticated examples if they are too long to reasonably include in the README.

## Support
Tell people where they can go to for help. It can be any combination of an issue tracker, a chat room, an email address, etc.

## Roadmap
If you have ideas for releases in the future, it is a good idea to list them in the README.

## Contributing
State if you are open to contributions and what your requirements are for accepting them.

For people who want to make changes to your project, it's helpful to have some documentation on how to get started. Perhaps there is a script that they should run or some environment variables that they need to set. Make these steps explicit. These instructions could also be useful to your future self.

You can also document commands to lint the code or run tests. These steps help to ensure high code quality and reduce the likelihood that the changes inadvertently break something. Having instructions for running tests is especially helpful if it requires external setup, such as starting a Selenium server for testing in a browser.

## Authors and acknowledgment
Show your appreciation to those who have contributed to the project.

## License
For open source projects, say how it is licensed.

## Project status
If you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.