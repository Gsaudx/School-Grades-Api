## Configuração
### 1. Clone o Repositório
```bash
git clone https://github.com/Gsaudx/API-Notas-Escolares.git
```
Em seguida, entre na pasta onde você clonou o repositório:
```bash
cd API-Notas-Escolares
```

Ou clone usando o GitHub Desktop.

### 2. Instale as Dependências
```bash
pip install -r requirements.txt
```

### 3. Execute a Aplicação
```bash
uvicorn app.main:app --reload
```

## Endpoints/Rotas
Você também pode verificar os endpoints acessando a interface Swagger gerada automaticamente em seu_servidor/docs.

|  Método HTTP  |            Endpoint           |                 Descrição                  |  
| ------------- | ----------------------------- | ------------------------------------------  |
|     POST      |           /students/          |           Adiciona um aluno ao banco de dados          |
|     GET       |    /students/{student_id}/    |             Retorna um aluno pelo ID            |
|     GET       |      /grades/{subject}/       |        Retorna as notas por nome da disciplina         |
|     GET       |  /grades/statistics{subject}/ |       Retorna as estatísticas por nome da disciplina      |
|     GET       |      /grades/below_average/   | Retorna os alunos com notas abaixo do limite (6) |
|     DELETE       |      /students/remove/no_grades/   | Apaga todos os estudantes que não possuem nenhuma nota do banco de dados |

<hr>

## Estrutura de Arquivos
O projeto não foi desenvolvido usando um único arquivo (main.py), como é comum para designs menores. Em vez disso, decidimos dividi-lo em vários arquivos. Esta é a estrutura atual do projeto:
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
## Como Cada Arquivo Funciona?
### app/models.py
É importante começar com a modelagem de dados que estamos usando. Nesta API, decidimos modelar todos os dados que usamos como entrada ou saída. Isso significa que toda operação que fazemos no banco de dados retorna um dos modelos dentro deste arquivo. Os modelos neste arquivo são objetos, basicamente representações dos dados que queremos receber/retornar. Por exemplo, para retornar as estatísticas de uma disciplina, procuramos pela disciplina específica no respectivo endpoint e então retornamos o objeto Statistic específico que representa as métricas.

### app/crud.py
Este arquivo representa nosso repositório (se estivéssemos usando o padrão de design MVC). Ele está cheio de funções, cada uma chamada por um endpoint específico e tendo suas próprias funcionalidades. Em cada função, fazemos algumas validações básicas. Por exemplo, ao criar um aluno, sempre verificamos se a entrada fornecida pelo consumidor da API é do tipo Student simplesmente exigindo que o segundo argumento seja do tipo Student:
```
def create_student(student_id: int, student: Student)
```

### app/database.py
Como fomos instruídos a não usar um banco de dados real para esta API, mas sim um arquivo JSON, criamos duas funções para representar os estados de carregamento de dados e salvamento de dados:
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
Nesta função, nós:
<ul>
    <li> Tentamos abrir um arquivo chamado "students.json", que está na pasta atual do projeto, e o fechamos logo em seguida. </li>
    <li> Se ele existir, lemos seus dados e armazenamos seu valor na variável data. </li>
    <li> Finalmente, retornamos um novo dicionário no mesmo formato do arquivo students.json. </li>
</ul>

E a função save_data():
```
def save_data(data: Dict[int, Student]):
    with open(FILE_PATH, "w") as file:
        json.dump({student_id: student_obj.dict() for student_id, student_obj in data.items()}, file, indent = 4)
```
E nessa nós:
<ul>
  <li> Recebemos um dicionário com o ID do aluno e o próprio objeto aluno para inserir no arquivo JSON. </li>
  <li> Abrimos o arquivo chamado "students.json" no modo de escrita. </li>
  <li> Armazenamos os dados no arquivo usando a função json.dump(). </li>
</ul>

### app/main.py
Aqui é onde nossa API é inicializada. Definimos um decorator usado para criar um gerenciador de contexto assíncrono, que define um bloco de código executado antes e depois de algum contexto. A função lifespan é o gerenciador de contexto nesta aplicação, definindo o ciclo de vida da nossa API. Ela deve receber um objeto FastAPI como argumento.

Em seguida, temos o evento de inicialização, que atualiza a variável students_db (a que armazena todos os alunos no arquivo students.json) usando a função load_data() explicada acima.

Logo depois, temos a palavra-chave yield, que transfere temporariamente o controle para o código que está usando o gerenciador de contexto (nossa API).

Finalmente, quando nossa API é desligada, o código abaixo do yield é executado. Em outras palavras, save_data() recebe student_db e atualiza o arquivo students.json.

Fora da função, podemos ver mais duas linhas:

Esta cria o ciclo de vida da nossa API usando o gerenciador de contexto que declaramos antes:
```
app = FastAPI(lifespan = lifespan)
```

E esta inclui as rotas definidas no arquivo students.py:
```
app.include_router(students.router)
```

### app/routers/student.py
Agora que entendemos como a API funciona essencialmente, podemos discutir os roteadores. No FastAPI, um roteador é uma forma de agrupar rotas relacionadas, que são basicamente URLs (endpoints) em nossa API associadas a funções. Quando um endpoint é acessado, a função associada é executada para lidar com a solicitação.

Podemos identificar uma rota e o método HTTP necessário para acessá-la identificando os decoratores `@router` seguidos pelo método HTTP, por exemplo, `.post`:
```
@router.post("/students/", response_model = Student, summary = "Add a student to the database")
```
Este decorator especificamente recebe três parâmetros:
<ul>
    <li> O primeiro parâmetro define o endpoint. </li>
    <li> O segundo parâmetro define o modelo de resposta da solicitação. Neste caso, devemos retornar um objeto do tipo Student, definido no arquivo models.py. </li>
    <li> O terceiro parâmetro fornece uma breve descrição do endpoint, que pode ser verificada na documentação Swagger gerada automaticamente (veja a imagem abaixo). </li>
</ul>
<img src="https://github.com/Gsaudx/School-Grades-Api/assets/62403672/87b6d824-e52c-4413-966e-9dca0e5259fa">
