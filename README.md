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

<p allign="center">
<iframe width="1134" height="638" src="https://www.youtube.com/embed/IHcoLog6azg" title="Lo ha DESTROZADO!!!!! Xperia 1 IV vs iPhone 13 Pro Max **TEST A CIEGAS**" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</p>
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

La aplicación tiene una API dispoble en el puerto 3000

### Create
Genera una receta para un paciente específico
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
```sh
curl −−location −−request GET http://localhost:3000/edit
```
#### 
- ☄ MÉTODO: GET
#### Response
```js
{
    "users-blocked":[
      "user1",
      "user2"
    ]
}
```
## ❔ Preguntas

### 1. ¿Por qué Kafka funciona bien en este escenario?
Kafka es un software que permite el flujo y envío de información en gran volumen a través de su sistema de tópicos (brokers). Esto último permite a los servicios de Login y Bloqueo trabajar de manera asíncrona gracias al modelo productor/consumidor, dado que el servicio de Login es capaz de informar en el tópico de kafka cuales son las cuentas que han tratado de iniciar sesión de manera fallida, sin necesidad de esperar a que el servicio de bloqueo realice alguna acción, puesto que kafka se encarga de almacenar esto en el tópico el cual puede ser consumido por el servicio de Bloqueo en cualquier otro momento. 

Esto se traduce en un menor tiempo de respuesta para el usuario que esté utilizando el cliente o aplicación, ya que de no utilizar kafka la aplicación estaría esperando la respuesta del servicio de bloqueo (parecido a un modelo cliente/servidor) que en términos de escalabilidad resulta ineficiente, generando un cuello de botella que colapsaría este servicio.

### 2. Basado en las tecnologías que usted tiene a su disposición (Kafka, backend) ¿Qué haría usted para manejar una gran cantidad de usuarios al mismo tiempo?
Una opción inicial sería escalar kafka con más brokers o equipos de manera distribuida para lograr comunicar una mayor cantidad de datos en tiempo real. Adicional a esto último, también sería una buena opción distribuir el servicio de bloqueos agregando los siguientes servicios.

####
- Apache Flink: Flink es una herramienta de procesamiento de flujo en tiempo real y de código abierto, cuya funcionalidad radica en el procesamiento de múltiples tareas realizas simultáneamente en tiempo real, basado en algún tipo de input que provean datos y output donde se escribir o guardar los resultados obtenidos de estos procesamientos. Esta herramienta es ideal, puesto que nos permitiría consumir el tópico de kafka que contiene la lista de logins de usuarios, y determinar en tiempo real cuales cuentas deberán ser bloquedas.

- Redis: Es una base de datos en memoria NoSQL que se usa principalmente para la obtención de warmdata. En este servicio se almacenarían los resultados tras el procesamiento del servicio de flink, los cuales serían consumidos a través de la API del servicio de bloqueo.
####

A partir de esta arquitectura, será posible manejar una gran cantidad de usuarios en tiempo real, puesto que el servicio de bloqueo solamente accede a los datos almacenados en cache (Redis). El trabajo de procesamiento y análisis para determinar en el tiempo cuales cuentas corresponde a ser bloqueadas es llevado a cabo por Flink. Evitando lecturas y escrituras de archivos de manera ineficiente que solo empeora el rendimiento del sistema.

## ℹ Información Importante
El uso de las imágenes de [Bitnami](https://hub.docker.com/u/bitnami) fueron reemplazadas por [wurstmeister](https://hub.docker.com/u/wurstmeister) por el simple hecho de que la utilización de [AIOKafka](https://github.com/aio-libs/aiokafka) no permitía establecer una conexión con el contenedor de Kafka. Esta librería de Python permite utilizar Kafka de manera asincrónica, exactamente lo que se requería para combinar Flask con un KafkaProducer. Para el api de bloqueo se usó un KafkaProducer asíncrono basado en la contribución de trabajo de [NimzyMaina](https://github.com/NimzyMaina/flask_kafka).
