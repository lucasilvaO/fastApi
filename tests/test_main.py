import pytest
from starlette.testclient import TestClient
from app.main import app, db, Student


@pytest.fixture(autouse=True)
def setup_db():

    initial_db = [Student(id=1, name="Lucas", email="lucas@gmail.com")]
    db[:] = initial_db
    yield


@pytest.fixture
def client():

    with TestClient(app) as client:
        yield client


def test_list_students_success(client: TestClient):
    """Teste de sucesso: lista todos os alunos e verifica o nome 'Lucas'."""
    response = client.get("/students")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Lucas"


def test_get_student_success(client: TestClient):
    """Teste de sucesso: busca o aluno existente por ID 1 (Lucas)."""
    response = client.get("/students/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Lucas"


def test_get_student_failure(client: TestClient):
    """Teste de falha esperada: ID não encontrado (404)."""
    response = client.get("/students/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found"


def test_create_student_success(client: TestClient):
    """Teste de sucesso: cria um novo aluno (ID 2)."""
    new_student_data = {"name": "Novo Aluno", "email": "novo.aluno@exemplo.com"}
    response = client.post("/students", json=new_student_data)
    assert response.status_code == 201

    assert response.json()["id"] == 2


def test_create_student_failure_duplicate_email(client: TestClient):
    """Teste de falha esperada: Tenta usar o e-mail duplicado 'lucas@gmail.com'."""
    duplicate_student_data = {"name": "Aluno Duplicado", "email": "lucas@gmail.com"}
    response = client.post("/students", json=duplicate_student_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"
