# Kindle-like prototype
## Objective
This is a small project that leverages the RESTful architecture for uploading and reading files. The idea is to design a smooth system to handle fast and efficient data transer between the frontend and backend emulating that of Kindle.
![High level design](https://github.com/secretmtgdev/Kindle-like-prototype/blob/master/assets/design/design_1.jpeg)

## Tech stack
- Frontend
    - React
        - Like the flexibility of the library over a framework
        - Enjoy the rich features of the virtual DOM
    - Axios
        - Provides progress tracking that fetch doesn't
- Backend
    - Python
        - Easy language to pick up
        - Using psycog2 to connect to postgres
    - Postgres
        - Flexible data types

## How to run
- Client `npm start`
- Server `flask --app PyAPI.py run`

## Q & A
- What can this project do?
    - Read files from blob storage
    - Upload files to the database & blob storage
- Will this project be expanded on?
    - Most likely yes but it is more of a sandbox to try things out for a bigger project
- What tables are there?
    - accounts
    - files
    - file_datastore
![Postgres table schemas](https://github.com/secretmtgdev/Kindle-like-prototype/blob/master/assets/server_images/table_schemas.png)
- What does the accounts table do?
    - Stores information on the username, password, email, and associated text via a list of filenames
    - Passwords are to be encrypted with a gen_salt algorithm
    - Since usernames are unique, the username will be a primary key to pull up saved content
- What does the files table do?
    - Stores information about the filename, and upload date
- What does the file_datastore table do?
    - Acts as blob storage linking to the files table through the foreign key filename in files
 