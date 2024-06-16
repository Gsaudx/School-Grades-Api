# Restful API for school grades management
Welcome! This API was developed by Guilherme Saud Favaro and Isaque Precioso de Andrade as a final test for Dr. Henrique Dezani's Programming Language subject, from Fatec Rio Preto

# File structure?
The project was developed not using only a single file (main.py), as usual for smaller designs. Instead, we decided to split it into some files. This is the current project's structure:
```
├── app
│   ├── routers
│       ├── students.py
│   └── crud.py
│   └── database.py
│   └── main.py
│   └── models.py
├── .gitignore
├── requirements.txt 
└── README.md
└── students.json
```
# How do each one of those files work?
### app/models.py
It's important to start with the data modeling we're using. In this API, we decided to model every data we use as input or output. That basically mean every operation we do in the database returns one of the models inside this file. Models in this file are objects, basically representations of the data we want to receive/return. For example, to return the statistics of a subject, we look for the given one in the respective endpoint and then we return the specific Statistic object which represents the metrics.

### app/crud.py
This file represents our repository (if we'd using the MVC design pattern). It's full of functions and each one is going to be called by an specific endpoint and has its self functionalities. In each function we run some basic validations, one example is when creating a student. We always check if the input given by the API consumer is from the Student model type by simply requiring the second argument to be from the type Student:
```
def create_student(student_id: int, student: Student)
```

### app/database.py
As we were told to not use a real database integration for this API, but a JSON file instead, we created two functions to represent the states of loading data and saving data:
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
  <li> Try to open a file called "students.json", which is in the current project folder and close it right after </li>
  <li> If it's existent, we read its data and store its value inside the data variable </li>
  <li> And finally we return a new dictionary in the same model as the students.json file</li>
</ul>

And the save_data() function:
```
def save_data(data: Dict[int, Student]):
    with open(FILE_PATH, "w") as file:
        json.dump({student_id: student_obj.dict() for student_id, student_obj in data.items()}, file, indent = 4)
```
In this one we: 
<ul>
  <li> Receive a dictionary with the student id and the student objet itself to insert into the JSON </li>
  <li> Open a file called "students.json" in the writing mode </li>
  <li> Store the data into the file with json.dump() function </li>
</ul>

## Setup
### 1. Clone the repository
```bash
git clone https://github.com/Gsaudx/API-Notas-Escolares.git
```
And then go into your folder you cloned the repo
```bash
cd API-Notas-Escolares
```

Or just clone it using Github Desktop

### 2. Install the dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the application
```bash
uvicorn app.main:app --reload
```

## Endpoints
You can also check the endpoints by going to the automatically generated Swagger Ui in your_server/docs

|  HTTP Method  |            Endpoint           |                 Description                |  
| ------------- | ----------------------------- | ------------------------------------------ |
|     POST      |           /students/          |           Add a student to the db          |
|     GET       |    /students/{student_id}/    |             Get a student by ID            |
|     GET       |      /grades/{subject}/       |        Get grades per subject name         |
|     GET       |  /grades/statistics{subject}/ |       Get statistics per subject name      |
|     GET       |      /grades/below_average/   | Get students with grades below average (6) |
