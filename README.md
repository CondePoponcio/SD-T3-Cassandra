<br />
<div align="center">

  <h3 align="center">Sistemas Distribuidos: Tarea 03</h3>

  <p align="center">
    Fernando Burón, Felipe Condore
  </p>
 
</div>

## Acerca del proyecto

El objetivo de esta tarea consiste en poner en práctica el concepto de replicación en bases de datos utilizando Cassandra


### 🛠 Construído con:

Esta sección muestra las tecnologías con las que fue construído el proyecto.

* [Apache Cassandra](https://cassandra.apache.org/_/index.html)
* [Python](https://www.python.org)
* [Docker](https://www.docker.com)


## :octocat: Comenzando

Para iniciar el proyecto, primero hay que copiar el repositorio `git clone https://github.com/CondePoponcio/SD-T3-cassandra .` y escribir el siguiente comando en la consola:
* docker
```sh
docker-compose build
```
Para que los contenedores se inician en el ambiente local se utiliza el siguiente comando en la consola:
* docker
```sh
docker-compose up -d
```
Los tiempos de iniciación son extensos debido a la alta demanda de cómputo para los nodos de Cassandra

### Pre-Requisitos

Tener Docker y Docker Compose instalado
* [Installation Guide](https://docs.docker.com/compose/install/)


## 🤝 Uso

La aplicación tiene una API disponible en el puerto 3000 :trollface:

### Create
Genera una receta para un paciente.
#### Request example
```sh
curl --location --request POST http://localhost:3000/create \
--header 'Content-Type: application/json' \
--data-raw '{
    "nombre": "Cosme", 
    "apellido": "Fulanito",
    "rut": "19650228-9",
    "email": "fcondore@gmail.com",
    "fecha_nacimiento": "1998-08-28",
    "comentario": "Nada en particular",
    "farmacos": "Su paracetamil",
    "doctor": "Dr. Simi"
}'
```
#### Response example
```json
{
  "status":"success"
}
```

### Edit
Edita una receta en específico
#### Request example
```sh
curl --location --request POST http://localhost:3000/edit \
--header 'Content-Type: application/json' \
--data-raw '{
    "id": "4483b1fa-cfd6-4351-952f-87f4eff8c9bd",
    "comentario": "Nada en particular XD",
    "farmacos": "Drogas de la buena",
    "doctor": "Jordi"
}'
```
#### Response example
```json
{
  "status":"success"
}
```

### Delete
Elimina una receta
#### Request example
```sh
curl --location --request POST http://localhost:3000/delete \
--header 'Content-Type: application/json' \
--data-raw '{
    "id": "4483b1fa-cfd6-4351-952f-87f4eff8c9bd",
}'
```
#### Response example
```json
{
  "status":"success"
}
```
## ❔ Preguntas

### 1. Explique la arquitectura que Cassandra maneja al crear un clúster:
* ¿Cómo los nodos se conectan? 
* ¿Qué ocurre cuando un cliente realiza una petición a uno de los nodos? 
* ¿Qué ocurre cuando uno de los nodos se desconecta?
* ¿La red generada entre los nodos siempre es eficiente? 
* ¿Existe balanceo de carga?

### 2. Cassandra posee principalmente dos estrategias para mantener redundancia en la replicación de datos:
* ¿Cuáles son?
* ¿Cuál es la ventaja de una sobre la otra?
* ¿Cuál utilizaría usted en el caso actual y por qué?

### 3. Teniendo en cuenta el contexto del problema: 
_Oriente su respuesta hacia el Sharding (la replicación/distribución de los datos) y comente una estrategia que podría seguir para ordenar los datos._
* ¿Usted cree que la solución propuesta es la correcta? 
* ¿Qué ocurre cuando se quiere escalar en la solución? 
* ¿Qué mejoras implementaría?



## ℹ Información Importante
El uso de las imágenes de [Bitnami](https://hub.docker.com/u/bitnami) fueron reemplazadas por [wurstmeister](https://hub.docker.com/u/wurstmeister) por el simple hecho de que la utilización de [AIOKafka](https://github.com/aio-libs/aiokafka) no permitía establecer una conexión con el contenedor de Kafka. Esta librería de Python permite utilizar Kafka de manera asincrónica, exactamente lo que se requería para combinar Flask con un KafkaProducer. Para el api de bloqueo se usó un KafkaProducer asíncrono basado en la contribución de trabajo de [NimzyMaina](https://github.com/NimzyMaina/flask_kafka).
