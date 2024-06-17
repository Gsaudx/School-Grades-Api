## Setup
### 1. Clone the repository
```bash
git clone https://github.com/Gsaudx/API-Notas-Escolares.git
```
Then go into the folder where you cloned the repo:
```bash
cd API-Notas-Escolares
```

Or clone it using GitHub Desktop.

### 2. Create a virtual environment and install the dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the application
```bash
uvicorn app.main:app --reload
```

## Endpoints
You can also check the endpoints by going to the automatically generated Swagger UI at your_server/docs. We also recommend that you test the API there.

|  HTTP Method  |            Endpoint           |                 Description                |  
| ------------- | ----------------------------- | ------------------------------------------ |
|     POST      |           /students/          |           Add a student to the db          |
|     GET       |    /students/{student_id}/    |             Get a student by ID            |
|     GET       |      /grades/{subject}/       |        Get grades per subject name         |
|     GET       |  /grades/statistics{subject}/ |       Get statistics per subject name      |
|     GET       |      /grades/below_average/   | Get students with grades below average (6) |
|     DELETE       |      /students/remove/no_grades/   | Remove every student that does not have any grade from the database |

<hr>

## File structure
The project is not developed using a single file (main.py) as is usual for smaller designs. Instead, we decided to split it into multiple files. This is the current project structure:
```
├── app
│   ├── routers
│       ├── students.py
│   └── crud.py
│   └── database.py
│   └── main.py
│   └── models.py
├── guides
│   ├── guide_en.md
│   ├── guide_ptbr.md
├── .gitignore
├── requirements.txt 
└── README.md
└── students.json
```
## How does each file work?
### app/models.py
It's important to start with how the things work in this project. In this API, we decided to model the data we use as input and output. This means that every request that requires a value is validated before really being passed to the database. These models are inside the `models.py` file. Models in this file are classes, basically representations of the data we want to receive/return. For example, to return the statistics of a subject, we look for the given one in the respective endpoint and then return the Statistic object which represents the metrics.

### app/crud.py
This file represents our repository (if we were using the MVC design pattern). It's full of functions, each one called by a specific endpoint and having its own functionalities. In each function, we run some basic validations. For example, when creating a student, we always check if the input given by the API consumer is of the Student model type by simply requiring the second argument to be of type Student:
```
def create_student(student_id: int, student: Student)
```

### app/database.py
As we were instructed not to use a real database for this API, but a JSON file instead, we created two functions to represent the states of loading data and saving data:
```
def load_data() -> Dict[int, Student]:
    try:
        with open(FILE_PATH, "r") as file:
            data = json.load(file)
            return {int(student_id): Student(**student_obj) for student_id, student_obj in data.items()}
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}
```
In this function we:
<ul>
    <li> Try to open a file called "students.json", which is in the current project folder, and close it right after. </li>
    <li> If it exists, we read its data and store its value inside the data variable. </li>
    <li> Finally, we return a new dictionary in the same format as the students.json file. </li>
</ul>

And the save_data() function:
```
def save_data(data: Dict[int, Student]):
    with open(FILE_PATH, "w") as file:
        json.dump({student_id: student_obj.dict() for student_id, student_obj in data.items()}, file, indent = 4)
```
In this one we: 
<ul>
  <li> Receive a dictionary with the student ID and the student object itself to insert into the JSON file. </li>
  <li> Open a file called "students.json" in write mode. </li>
  <li> Store the data into the file using the json.dump() function. </li>
</ul>

### app/main.py
Here is where our API is initialized. We define a decorator used to create an async context manager, which defines a block of code executed before and after some context. The lifespan function is the context manager in this application, defining the life cycle of our API. It must receive a FastAPI object as an argument.

Then, we have the startup event, which updates the students_db variable (the one storing every student in the students.json file) using the load_data() function explained above.

Right after that, we have the yield keyword, which temporarily transfers control to the code that is using the context manager (our API).

Finally, when our API is shut down, the code below yield is executed. In other words, save_data() receives student_db and updates the students.json file.

Outside the function, we can see two more lines:

This one creates our API life cycle using the context manager we declared before:
```
app = FastAPI(lifespan = lifespan)
```

And this one includes the routes defined inside the students.py file:
```
app.include_router(students.router)
```

### app/routers/student.py
Now that we understand how the API essentially works, we can discuss the routers. In FastAPI, a router is a way to group related routes, which are basically URLs (endpoints) in our API associated with functions. When an endpoint is accessed, the associated function is executed to handle that request.

We can identify a route and the HTTP method necessary to access it by identifying the decorators `@router` followed by the HTTP method, for example, `.post`:
```
@router.post("/students/", response_model = Student, summary = "Add a student to the database")
```
This decorator specifically receives three parameters:
<ul>
    <li> The first one defines the endpoint </li>
    <li> The second parameter defines the response model of the request. In this case, we must return an object of type Student, defined in the models.py file. </li>
    <li> The third parameter gives a short description of the endpoint, which can be checked in the automatically generated Swagger documentation (see the image below). </li>
</ul>
<img src="https://github.com/Gsaudx/School-Grades-Api/assets/62403672/87b6d824-e52c-4413-966e-9dca0e5259fa">

<hr>

# Thanks for reading!
## By:
<ul>
    <li> Guilherme Saud Favaro (me) </li>
    <li> Isaque Precioso de Andrade </li>
</ul>

