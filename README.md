<br />
<div align="center">

  <h3 align="center">Sistemas Distribuidos: Tarea 03</h3>

  <p align="center">
    Fernando Bur贸n, Felipe Condore
  </p>
 
</div>

## Acerca del proyecto

El objetivo de esta tarea consiste en poner en pr谩ctica el concepto de replicaci贸n en bases de datos utilizando Cassandra

### 馃洜 Constru铆do con:

Esta secci贸n muestra las tecnolog铆as con las que fue constru铆do el proyecto.

- [Apache Cassandra](https://cassandra.apache.org/_/index.html)
- [Python](https://www.python.org)
- [Docker](https://www.docker.com)

## :octocat: Comenzando

Para iniciar el proyecto, primero hay que copiar el repositorio `git clone https://github.com/CondePoponcio/SD-T3-cassandra .` y escribir el siguiente comando en la consola:

- docker

```sh
docker-compose build
```

Para que los contenedores se inician en el ambiente local se utiliza el siguiente comando en la consola:

- docker

```sh
docker-compose up -d
```

Los tiempos de iniciaci贸n son extensos debido a la alta demanda de c贸mputo para los nodos de Cassandra

### Pre-Requisitos

Tener Docker y Docker Compose instalado

- [Installation Guide](https://docs.docker.com/compose/install/)

## 馃 Uso

La aplicaci贸n tiene una API disponible en el puerto 3000 :trollface:

### Create

Genera una receta para un paciente.

#### Request example

```ru
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
  "status": "success"
}
```

### Edit

Edita una receta en espec铆fico

#### Request example

```ru
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
  "status": "success"
}
```

### Delete

Elimina una receta

#### Request example

```ru
curl --location --request POST http://localhost:3000/delete \
--header 'Content-Type: application/json' \
--data-raw '{
    "id": "4483b1fa-cfd6-4351-952f-87f4eff8c9bd",
}'
```

#### Response example

```json
{
  "status": "success"
}
```

## 鉂? Preguntas

### 1. Explique la arquitectura que Cassandra maneja al crear un cl煤ster:

- **驴C贸mo los nodos se conectan?** La arquitectura de Cassandra est谩 creada teniendo en cuenta que el sistema puede fallar en alg煤n punto, por lo que su conjunto est谩 conformado de Peers que se conectan unos a los otros (P2P). Los datos son distribuidos a lo largo de los nodos del cl煤ster y estos se conectan a trav茅s de _Internode communications (gossip)_. Gossip es un protocolo de conexi贸n Peer-to-peer, en donde cada uno de los nodos comparten su estado peri贸dicamente, su informaci贸n y tambi茅n la que tienen de otros nodos. Estas actualizaciones ocurren cada segundo, lo que permite que cada nodo aprenda r谩pidamente del resto. Un mensaje _gossip_, en su estructura, cuenta con una versi贸n, lo que admite sobreescribir mensajes que est谩n a destiempo. Adicionalmente, al iniciar un cl煤ster se define un nodo semilla, que ser谩 el primero en en iniciar este procesos de "chismes" (_gossip_), esto no significa que haya un 煤nico punto de falla, ya que luego de ser inicializado, todos los nodos tienen la opci贸n de entregar y recibir _gossip messages_. Adem谩s, cada nodo est谩 conectado con dos nodos vecinos, formando as铆 una arquitectura tipo anillo, haciendo que los datos viajen en una ruta continua. Esto est谩 pensado as铆 para que la base de datos NoSQL pueda escalar de manera indefinida.
- **驴Qu茅 ocurre cuando un cliente realiza una petici贸n a uno de los nodos?** El nodo que recibe la petici贸n ser谩 el coordinador, se encarga de direccionar esta petici贸n al resto de nodos, generando distintos logs del commit realizado. Usando el protocolo _gossip_ los mensajes se distribuyen en cada una de las r茅plicas y se dirigen a la MemTable, almacen谩ndolos en el volumen que SSTable.
- **驴Qu茅 ocurre cuando uno de los nodos se desconecta?** Cuando uno de los nodos se desconecta y suponiendo que hay pocos, existen distintas estrategias que Cassandra toma para tolerar este problema: Snitch y SimpleStrategy. El primero le ense帽a lo suficiente a Cassandra acerca de la topolog铆a de su red para poder rutear correctamente las peticiones, adem谩s de distribuir r茅plicas alrededor del cl煤ster para evitar fallas correlacionadas, espec铆ficamente agrupa las m谩quinas en _datacenters_ y _racks_, Cassandra intentar谩 que no exista m谩s de una r茅plica en el mismo _rack_ (puede no ser una ubicaci贸n f铆sica). El segundo es usado cuando tienes un solo _datacenter_, SimpleStrategy coloca una primera r茅plica en el nodo seleccionado por el particionador, luego de eso las r茅plicas restantes son colocadas en sentido del reloj en el anillo de Nodos. Adem谩s, todas las desconexiones de nodos son avisadas a trav茅s de Gossip al resto. Adem谩s el balanceador de cargas determinar谩 qu茅 nodos se usar谩n en caso de fallo
- **驴La red generada entre los nodos siempre es eficiente?** No siempre, depender谩 de la magnitud de datos que se est谩n procesando, al estar pensada para escalar masivamente. Si se utiliza para muchos datos, pero el c贸mputo de los nodos no es lo suficiente para poder procesasrlos, puede generarse un cuello de botella. Adem谩s, una red P2P tiene limitaciones, la latencia puede aumentar por cada nodo presentado, no hay que olvidar que la comunicaci贸n por el protocolo _gossip_ pasa por cada uno de los nodos y, si hay demasiados, la latencia es evidente, lo que concluye en ineficiencia en ciertos casos.
- **驴Existe balanceo de carga?** S铆, Cassandra cuenta con un sistema LBP (_load balancing policy_), es un componente que determina qu茅 nodos el driver se comunicar谩n y, por cada una de las nuevas querys, cu谩l coordinador escoger y qu茅 nodos usar en casos de un fallo.
<br />
<div align="center">
<image src=https://i.imgur.com/MLdMopS.png>
 </div>

### 2. Cassandra posee principalmente dos estrategias para mantener redundancia en la replicaci贸n de datos:

- **驴Cu谩les son?** SimpleStrategy y NetworkTopologyStrategy
- **驴Cu谩l es la ventaja de una sobre la otra?** SimpleStrategy es usada cuando s贸lo hay un _datacenter_, coloca una primera r茅plica en el nodo seleccionado por el particionador, luego de eso las r茅plicas restantes son colocadas en sentido del reloj en el anillo de Nodos. Tiene ventaja en sistemas de tama帽o peque帽o. Por otro lado, NetworkToplogyStrategy sirve cuando se tiene m谩s de un _datacenter_, lo que implica que escalar谩 mejor en el futuro, teniendo la capacidad de a帽adir nuevas regiones de datos, se usa en la mayor铆a de despliegues.
- **驴Cu谩l utilizar铆a usted en el caso actual y por qu茅?** En este caso, al ser una aplicaci贸n simple y de baja escala, se utilizar铆a SimpleStrategy.

### 3. Teniendo en cuenta el contexto del problema:

_Oriente su respuesta hacia el Sharding (la replicaci贸n/distribuci贸n de los datos) y comente una estrategia que podr铆a seguir para ordenar los datos._

- **驴Usted cree que la soluci贸n propuesta es la correcta?** Depende, se debe tener en consideraci贸n la cantidad de peticiones, usuarios concurrentes y el tama帽o de los datos a procesar. Actualmente la topolog铆a utilizada es solo un _datacenter_, lo que no permite crear nuevas regiones de datos y en t茅rminos de escalabilidad puede no ser la mejor opci贸n. Considerando un escenario real, donde existen miles de peticiones por segundo, se podr铆a crear una topolog铆a de _datacenters_ y _racks_, pero esto requerir铆a una mayor inversi贸n en el _hardware_ y en el _software_.
- **驴Qu茅 ocurre cuando se quiere escalar en la soluci贸n?** La estrateg铆a SimpleStrategy no es la mejor opci贸n, por lo tanto habr铆a que considerar la topolog铆a de _datacenters_ y _racks_. Teniendo en cuenta la cantidad de datos que podr铆an ser manejados en el sistema (recetas, pacientes, etc.), lo mejor ser铆a realizar un escalamiento horizontal con un sistema de _Sharding_. El _Sharding_ permite la partici贸n horizontal de los datos, donde cada partici贸n individual se denomina _shard_, lo que permite extender la carga.
A continuaci贸n, se muestra una imagen de una arquitectura que incluye _Sharding_ en un escenario donde hay dos regiones (AZ-1 y AZ-2).
<br />
<div align="center">
<image src=/img/Sharding.drawio.png>
 </div>

Donde cada shard es una partici贸n de datos, puede ser una table en espec铆fico o incluso una tabla compuesta por varias tablas. En este caso puede ser un shard para pacientes y el resto para recetas.

- **驴Qu茅 mejoras implementar铆a?** El sistema de _Sharding_ es una excelente opci贸n si se considera que la escala de datos ser谩 masiva. Escenario en donde existen m煤ltiples cl铆nicas, clientes y recetas. Adicionalmente se debe generar un cl煤ster que realice la configuraci贸n de los shards, almacenando rutas y aplicaci贸n de pol铆ticas preferenciales que permitan aproximar la carga de los shards. En la figura anterior es el balanceador de cargas, pero puede ser un cl煤ster de Cassandra que act煤e como tal.
