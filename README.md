Simple RESTful API using FastAPI for a social networking application

### Descpition
<details>
  <summary>Functional requirements</summary>

 - There should be some form of authentication and registration (JWT, Oauth, Oauth 2.0, etc..)
 - As a user I need to be able to signup and login
 - As a user I need to be able to create, edit, delete and view posts
 - As a user I can like or dislike other users’ posts but not my own 
 - The API needs a UI Documentation (Swagger/ReDoc)
  
</details>


<details>
  <summary>Bonus section (not required)</summary>
  
 - Use https://clearbit.com/platform/enrichment for getting additional data for the user on signup
 - Use emailhunter.co for verifying email existence on registration
 - Use an in-memory DB for storing post likes and dislikes
(As a cache, that gets updated whenever new likes and dislikes get added)
  
</details>


<details>
  <summary>Technology requirements</summary>
  
Tasks should be completed:
 - Using FastAPI 0.50.0+
 - With any DBMS (Sqlite, PostgreSQL, MySQL)
 - Uploaded to GitHub
  
</details>


<details>
  <summary>Other requirements</summary>
  
When implementing your solution, please make sure that the code is:
 - Well-structured
 - Contains instructions (best to be put into readme.md) about how to deploy and test it
 - Clean
 - The program you implement must be a complete program product, i.e. should be easy to install,
provide for the handling of non-standard situations, be resistant to incorrect user actions, etc.

</details>

### Install and run
Instructions requires `docker` and `docker-compose plugin` installed

<details>
  <summary>How to run</summary>
  
- Clone the repo with the command
```commandline
git clone https://github.com/yaitzhan/webtronics
```
- Create `.env` file from  `.env.copy`, optionally fill variables `CLEARBIT_API_KEY` and `EMAIL_HUNT_API_KEY`
  
- Enter it's directory and execute following:
```commandline
docker-compose up -d
```

- Open web-browser at `http://0.0.0.0:8000/docs/swagger.yml` to get access to the interactive API documentation
- Use following credentials for authorization: 

| username | password |
| ------ | ------ |
| admin@example.com | admin |

- Explore and attempt!
</details>


<details>
  <summary>How to stop</summary>
  
- Within the same directory execute:
```commandline
docker-compose down
```
</details>

### TODO

- [ ] use celery instead fastapi:BackgroundTasks
- [ ] use possible usage of plugins architecture for all 3d party integrations
- [ ] use more complex approach by caching to avoid collisions
- [ ] optimize Dockerfile: use multistage-build and alpine as base image
- [ ] ...