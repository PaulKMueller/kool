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
>[!important]
>**Generate a new Secret Key**, e.g. by running the secret_key_generator.py in the frontend folder or following [this Tutorial](https://www.educative.io/answers/how-to-generate-a-django-secretkey). **DONT SHARE** your .env after that as this is a huge security risk when running the application in production
4. Open a command shell in the main directory of the project and type
> docker compose up
5. After building the containers, the Application should now be running on http://FRONTEND_HOST:FRONTEND_PORT, e.g. http://localhost:8000

*View [detailed Installation](#installation-guide) Guide for more information*

## Installation Guide
### Requirements
- When installing model_api and playground we recommend at least 10GB of storage as the models are big. When you dont want to install them view [Configuring the Project](#configuring-the-project)
- Docker must be installed (Tested on Docker version 20.10.20 and Docker Desktop v4.13.1, but other versions might work too)
- When running the model_api you either need a good GPU or much patience
### Installation
1. Make sure your system meets the [requirements](#installation)  
2. Clone this Repository and open it up using an IDE (we recommend using VS Code) or in the command shell.
3. Open up the ".env" file and specify the IPv4 addresses of the Frontend and Playground Host and the ports, which the Services should be running on.  
>[!important]
>**Generate a new Secret Key**, e.g. by running the secret_key_generator.py in the frontend folder or following [this Tutorial](https://www.educative.io/answers/how-to-generate-a-django-secretkey). **DONT SHARE** your .env after that as this is a huge security risk when running the application in production
4. If you only want to run the Main-Application (Frontend and Database) without the playground and model_api open up the docker-compose.yml and comment it from line 35 (model_api) till the end using a # in each line
5. Open a command shell (Terminal -> New Terminal in VS Code) in the main directory (where the docker-compose.yml sits) and run
> docker compose up
*if you already build the container in the past but changed something in the docker-compose-yml or in one of the Dockerfiles run*
> docker compose up --build
*to apply those changes*
6. Wait for the container to build. When installing model_api and playground go grab a coffee. Building the container can take up to 20 min (at least on our crappy laptops)
7. The Application should now be running on http://FRONTEND_HOST:FRONTEND_PORT, e.g. http://localhost:8000

## Configuring the Project
### Changing the Secret Key 

### Starting only a subset of services
When you dont want to regenerate, add abstracts to the database (model_api service) or test the models with different inputs (playground service) it might be desired to not run the model_api and playground service to save some resources. In this case comment the model_api block (line 45-43) and/or the playground block (line 47-56) in the docker-compose.yml (comment using one # in each line).

When the containers are already built you can start the desired services using the Docker Desktop GUI by only pressing the play button next to the service you want to start. 

>[!Info]
>The frontend dervice depends on the database_api service as specified in the docker-compose.yml in
>'''
>depends_on:
>     - database_api
>'''
>in the frontend service block, so you wont be able to start the frontend_api without starting the 
>database_api.
### Changing Ports and Hosts
The Ports and Hosts which the services will be running on are specified in the ".env" file in the main directory of the project. Here you can specify other environment variables, but make sure to *don't push them on git when adding sensitive data*.

>[!Info]
>Specifiyng the Hosts IPv4 Adress or URL obviously **won't change which system the Application will be running on**, but tells Django the Allowed Host Name (frontend/kool/settings.py) besides localhost and 
>the admin page where to find the playground.
>Other Host Names (from database_api and model_api) are resolved thanks to Dockers Internal Network. >Thats why you don't have to add those to ".env". 

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