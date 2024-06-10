# Restful API for school grades management
The API was developed as a final test from Dr. Henrique Dezani's Programming Language subject, from Fatec Rio Preto

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
