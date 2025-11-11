# Demand Forecasting SaaS


## Login example (API)

Use the standard authentication endpoint to obtain a JWT (example):

```bash
curl -s -X POST http://localhost:8000/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"vinsbox@gmail.com","password":"Myvin1234$"}' | jq
```

The response should include an `access_token` (JWT) you can use in `Authorization: Bearer <token>`.
