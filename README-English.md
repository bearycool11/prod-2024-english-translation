<br /> <p align="center"> <a href="https://github.com/Central-University-IT-prod/PROD-yet-another-common"> <img src="images/logo.png" alt="Logo" width="430"> </a> <h1 align="center">Yet Another SMM</h1> </p>
B2B product: SMM platform for your team with convenient internal team interaction

The project is available at https://smm.justmarfix.ru

Running the project locally
Dependencies:

Docker
Docker Compose
To run the project, use the command docker compose up --build -d in the root directory of the project.

Project Features
Ability to work with posts in teams (organizations)
Flexible role distribution within the team:
Observer
Editor
Reviewer
Administrator
Owner
Ability to manage the post lifecycle:
The editor can send the post for review
The reviewer can manage the review status and leave comments
The editor can schedule posts to be sent to one or multiple channels
Sent posts go to a separate list
Ability to use tags for posts and filter by tags
Posts are sent through a bot to which the administrator has full access
Post Lifecycle
<p align="center"> <a href="https://github.com/Central-University-IT-prod/PROD-yet-another-common"> <img src="images/post_live_cycle.png" alt="Logo"> </a> </p>
Project Stack
Backend:
Python 3
FastAPI
Pydantic
PostgreSQL
SQLAlchemy
Frontend:
Vue.JS
Tailwind CSS
Flowbite
Mobile:
Kotlin
Android Jetpack
Other:
Nginx
Docker
For ios/README.md:

IOS Application
Do not write or build manually!
If you want to build - go to the /frontend folder -> npm i -> npx cap open ios

More details: https://capacitorjs.com/docs/ios

Let me know if you need further assistance!
