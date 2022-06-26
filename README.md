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
* **¿Cómo los nodos se conectan?** La arquitectura de Cassandra está creada teniendo en cuenta que el sistema puede fallar en algún punto, por lo que su conjunto está conformado de Peers que se conectan unos a los otros (P2P). Los datos son distribuidos a lo largo de los nodos del clúster y estos se conectan a través de _Internode communications (gossip)_. Gossip es un protocolo de conexión Peer-to-peer, en donde cada uno de los nodos comparten su estado periódicamente, su información y también la que tienen de otros nodos. Estas actualizaciones ocurren cada segundo, lo que permite que cada nodo aprenda rápidamente del resto. Un mensaje _gossip_, en su estructura, cuenta con una versión, lo que admite sobreescribir mensajes que están a destiempo. Adicionalmente, al iniciar un clúster se define un nodo semilla, que será el primero en en iniciar este procesos de "chismes" (_gossip_), esto no significa que haya un único punto de falla, ya que luego de ser inicializado, todos los nodos tienen la opción de entregar y recibir _gossip messages_. Además, cada nodo está conectado con dos nodos vecinos, formando así una arquitectura tipo anillo, haciendo que los datos viajen en una ruta continua. Esto está pensado así para que la base de datos NoSQL pueda escalar de manera indefinida.
* **¿Qué ocurre cuando un cliente realiza una petición a uno de los nodos?** El nodo que recibe la petición será el coordinador, se encarga de direccionar esta petición al resto de nodos, generando distintos logs del commit realizado. Usando el protocolo _gossip_ los mensajes se distribuyen en cada una de las réplicas y se dirigen a la MemTable, almacenándolos en el volumen que SSTable.
* ¿Qué ocurre cuando uno de los nodos se desconecta? Cuando uno de los nodos se desconecta y suponiendo que hay pocos, existen distintas estrategias que Cassandra toma para tolerar este problema: Snitch y SimpleStrategy. El primero le enseña lo suficiente a Cassandra acerca de la topología de su red para poder rutear correctamente las peticiones, además de distribuir réplicas alrededor del clúster para evitar fallas correlacionadas, específicamente agrupa las máquinas en _datacenters_ y _racks_, Cassandra intentará que no exista más de una réplica en el mismo _rack_ (puede no ser una ubicación física). El segundo es usado cuando tienes un solo _datacenter_, SimpleStrategy coloca una primera réplica en el nodo seleccionado por el particionador, luego de eso las réplicas restantes son colocadas en sentido del reloj en el anillo de Nodos. Además, todas las desconexiones de nodos son avisadas a través de Gossip al resto. Además el balanceador de cargas determinará qué nodos se usarán en caso de fallo
* **¿La red generada entre los nodos siempre es eficiente?** No siempre, dependerá de la magnitud de datos que se están procesando, al estar pensada para escalar masivamente. Si se utiliza para muchos datos, pero el cómputo de los nodos no es lo suficiente para poder procesasrlos, puede generarse un cuello de botella. Además, una red P2P tiene limitaciones, la latencia puede aumentar por cada nodo presentado, no hay que olvidar que la comunicación por el protocolo _gossip_ pasa por cada uno de los nodos y, si hay demasiados, la latencia es evidente, lo que concluye en ineficiencia en ciertos casos.
* **¿Existe balanceo de carga?** Sí, Cassandra cuenta con un sistema LBP (_load balancing policy_), es un componente que determina qué nodos el driver se comunicarán y, por cada una de las nuevas querys, cuál coordinador escoger y qué nodos usar en casos de un fallo.
<br />
<div align="center">
<image src=https://i.imgur.com/MLdMopS.png>
 </div>
 
### 2. Cassandra posee principalmente dos estrategias para mantener redundancia en la replicación de datos:
* **¿Cuáles son?** SimpleStrategy y NetworkTopologyStrategy
* **¿Cuál es la ventaja de una sobre la otra?** SimpleStrategy es usada cuando sólo hay un _datacenter_, coloca una primera réplica en el nodo seleccionado por el particionador, luego de eso las réplicas restantes son colocadas en sentido del reloj en el anillo de Nodos. Tiene ventaja en sistemas de tamaño pequeño. Por otro lado, NetworkToplogyStrategy sirve cuando se tiene más de un _datacenter_, lo que implica que escalará mejor en el futuro, teniendo la capacidad de añadir nuevas regiones de datos, se usa en la mayoría de despliegues. 
* **¿Cuál utilizaría usted en el caso actual y por qué?** En este caso, al ser una aplicación simple y de baja escala, se utilizaría SimpleStrategy. 

### 3. Teniendo en cuenta el contexto del problema: 
_Oriente su respuesta hacia el Sharding (la replicación/distribución de los datos) y comente una estrategia que podría seguir para ordenar los datos._
* **¿Usted cree que la solución propuesta es la correcta?** Depende, se debe tener en consideración la cantidad de peticiones, usuarios concurrentes y el tamaño de los datos a procesar. Actualmente la topología utilizada es solo un _datacenter_, lo que no permite crear nuevas regiones de datos y en términos de escalabilidad puede no ser la mejor opción. Considerando un escenario real, donde existen miles de peticiones por segundo, se podría crear una topología de _datacenters_ y _racks_, pero esto requeriría una mayor inversión en el _hardware_ y en el _software_. 
* **¿Qué ocurre cuando se quiere escalar en la solución?** La estrategía SimpleStrategy no es la mejor opción, por lo tanto habría que considerar la topología de _datacenters_ y _racks_. Teniendo en cuenta la cantidad de datos que podrían ser manejados en el sistema (recetas, pacientes, etc.), lo mejor sería realizar un escalamiento horizontal con un sistema de _Sharding_. El _Sharding_ permite la partición horizontal de los datos, donde cada partición individual se denomina _shard_, lo que permite extender la carga. 
A continuación, se muestra una imagen de una arquitectura que incluye _Sharding_ en un escenario donde hay dos regiones (AZ-1 y AZ-2).
<br />
<div align="center">
<image src=/img/Sharding.drawio.png>
 </div>
* **¿Qué mejoras implementaría?**



## ℹ Información Importante
El uso de las imágenes de [Bitnami](https://hub.docker.com/u/bitnami) fueron reemplazadas por [wurstmeister](https://hub.docker.com/u/wurstmeister) por el simple hecho de que la utilización de [AIOKafka](https://github.com/aio-libs/aiokafka) no permitía establecer una conexión con el contenedor de Kafka. Esta librería de Python permite utilizar Kafka de manera asincrónica, exactamente lo que se requería para combinar Flask con un KafkaProducer. Para el api de bloqueo se usó un KafkaProducer asíncrono basado en la contribución de trabajo de [NimzyMaina](https://github.com/NimzyMaina/flask_kafka).
