# Project Details

The project is split into frontend/backend folders

execution commands backend: 
uvicorn database_service:app --host 0.0.0.0 --port 8001

uvicorn event_service:app --host 0.0.0.0 --port 8000

py event_simulator.py

execution commands frontend:

ng serve -o

## Frontend
The frontend is built using angular and provides a simple management console for simulated event details that is part of the backend script. A user can "complete" a event if they so wish, but this may be overriden by the backend script as it simulates things.

This is also used as proof for testing, because we can see the system running.

## Backend

The backend is split into two parts, the services and the simulator.

The simulator generates event information and uses the database service to write information to the .db file. Sometimes it may look for an event to update or create a new one.

The services come in two parts: the event_service and the database_service.

First, the event_service is used as a gateway to the database_service for the frontend. I thought it would be good to provide an abstraction layer that simplifies communication between services and front end.

The event_simulator communicates directly with the database_service, the reason for this choice was because of the architecture diagram provided, incomming messages are directly ingested into the TXN database. This somewhat replicates that approach without putting extra load on the TXN database as we are creating a seperate table.

With these two services, a microservice architecture has been implemented. This allows for extensibility and scalability to the API's/integration into the functional layer.

## Other considerations

I had spent a little bit of time implementing RabbitMQ into the solution, but it deviated too much from the list of the objectives because it could remove the requirement of an API & database in this instance and goes against polling. Albeit it would be slightly more efficient.

I also noted that the messaging infrastructure was available to us. This swayed my decision to implement RabbitMQ. I do not know what the messaging infrastructure looks like, therefore I decided against this. I thought it would be better to stick to microservices that can be easily integrated into other known parts of the system.

Because this did not take too long, I decided to build some Lambda functions for the services. These would require hooking up to an API gateway, and these are untested, but they are representations of the functionality provided in the existing services.

I added pagination to the front-end because a long table is horrible to look at. Buttons for completetion of a event confirm end-to-end functionality. New additions to the table on "live" updates also confirm system functionality.



