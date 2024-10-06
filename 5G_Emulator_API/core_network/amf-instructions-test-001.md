
Initial UE Context Setup.

```bash

curl -X POST http://localhost:9000/amf/ue/ue001 -H "Content-Type: application/json" -d '{"initial_gnb_id": "gnb001"}'

{"message":"UE context created"}

```

Quick Peek at Context

```bash
curl -X GET http://localhost:9000/amf/ue/ue001

```

Request or "trigger" Handover from UE

```bash

curl -X POST http://localhost:9000/amf/handover -H "Content-Type: application/json" -d '{"ue_id": "ue001", "source_gnb_id": "gnb001"}'

{"message":"Handover process completed","duration":0.09120726585388184}

```

ngap_handover_request_ack

- in the terminal (jaeger agent, collector, and query would persist data)

```bash
curl -X POST http://localhost:9000/amf/handover -H "Content-Type: application/json" -d '{"ue_id": "ue001", "source_gnb_id": "gnb001"}'

{"message":"Handover process completed","duration":0.09120726585388184}
```

Peek at New Context

```bash

curl -X GET http://localhost:9000/amf/ue/ue001

```