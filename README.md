# ohana-server

## Guia de inicio rapido

### Requisitos

- docker
- docker-compose

### Instalacion

- Clonar repositorio
```
git clone https://github.com/juanpsenn/ohana-server.git
```
- Correr `docker-compose` dentro de `/ohana-server`
```
cd /ohana-server
docker-compose up
```
- Inicializar base de datos
```
docker-compose run api python3 manage.py migrate
```
- Opcionalmente se pueden generar `n` eventos de prueba
```
docker-compose run api python3 manage.py populate_test_db --n 10
```
