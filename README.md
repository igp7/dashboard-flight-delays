# Dashboard Flight Delays
La Oficina de Estadísticas de Transporte del Departamento de Transporte de Estados Unidos (DOT) realiza un seguimiento de la puntualidad de los vuelos nacionales operados por grandes compañías aéreas. La información resumida sobre el número de vuelos puntuales, retrasados, cancelados y desviados se publica en el informe mensual del DOT sobre el consumo de viajes aéreos y en este conjunto de datos sobre retrasos y cancelaciones de vuelos de 2015.

**Nota:** Para la realización del dashboard se ha cogido una muestra aleatoria de *10.000* vuelos.

## Indice
1. [Dataset](#dataset)
2. [Tecnología](#tecnología)
3. [Requisitos](#requisitos)
4. [Ejecutar](#ejecutar)
5. [CD (Continuous deployment)](#cd-continuous-deployment)


## Dataset
- [2015 Flight Delays and Cancellations](https://www.kaggle.com/usdot/flight-delays)

## Tecnología
- **Web Framework:** Dash
- **Librerias:** Pandas, Numpy, dash-bootstrap-components
- **Gestor de environments:** Pipenv
- **Contenirizacion:** Docker y docker-compose
- **Plataforma de deploy:** Heroku
- **CD:** Github Actions

## Requisitos
- [Pipenv](https://pipenv.pypa.io/en/latest/)
- [Docker](https://www.docker.com/get-started)
- [Docker-Compose](https://docs.docker.com/compose/install/)
- [Python 3.8](https://www.python.org/downloads/)
- [Github](https://github.com)
- [Heroku](https://www.heroku.com)

## Ejecutar
Crear fichero **.env** e introducir las variables de entorno del environment. Ejemplo:
```shell
ENTRYPOINT=entrypoint:server
HOST=0.0.0.0
PORT=8050
```

- **Lanzar aplicacion:**
```shell
docker-compose up -d
```

- **Lanzar aplicacion con build imagen:**
```shell
docker-compose up --build -d
```

- **Parar aplicacion:**
```shell
docker-compose stop
```

- **Eliminar aplicacion:**
```shell
docker-compose down
```
***Nota:*** **docker-compose down** para y elimina containers, networks, images y volumes.

## CD (Continuous Deployment)
El workflow de CD (pro.yml) utiliza Github Actions. El workflow despliega en Heroku cuando se realiza un push a master.
- **NOTA:** Los **Actions Secrets** son necesarios para ejecutar corractamente el pipeline de CD. 
   - **HEROKU_API_KEY:** Token de acceso a Heroku.
   - **HEROKU_APP_NAME:** Nombre de app en Heroku.