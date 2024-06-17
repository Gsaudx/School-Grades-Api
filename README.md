# Fatec API

Welcome to the school grades API, a project developed for Doctor Henrique Dezani from FATEC Rio Preto by <b> Guilherme Saud Favaro </b> and <b> Isaque Precioso de Andrade </b>

## Documentation
<a href="guides/guide_en.md"> English </a> 
<br>
<a href="guides/guide_ptbr.md"> Português </a>

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

### 2. Install the dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the application
```bash
uvicorn app.main:app --reload
```

## Endpoints
You can also check the endpoints by going to the automatically generated Swagger UI at your_server/docs.

|  HTTP Method  |            Endpoint           |                 Description                |  
| ------------- | ----------------------------- | ------------------------------------------ |
|     POST      |           /students/          |           Add a student to the db          |
|     GET       |    /students/{student_id}/    |             Get a student by ID            |
|     GET       |      /grades/{subject}/       |        Get grades per subject name         |
|     GET       |  /grades/statistics{subject}/ |       Get statistics per subject name      |
|     GET       |      /grades/below_average/   | Get students with grades below average (6) |
|     DELETE       |      /students/remove/no_grades/   | Remove every student that does not have any grade from the database |

