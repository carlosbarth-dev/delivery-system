<<<<<<< HEAD
# 📡 Especificação API - MVP v0.1.0

Todos os endpoints disponíveis no MVP. Use isto como referência técnica.

---

## 🔵 Base URL


Local:        http://localhost:8000
Staging:      https://api-staging.delivery.com
Production:   https://api.delivery.com


---

## 📚 Documentação Interativa

Quando o backend estiver rodando:

http://localhost:8000/docs  (Swagger UI - interativo)
http://localhost:8000/redoc (ReDoc - leitura)


---

## ✅ Healthcheck

### GET /healthcheck

Verifica se API + Database estão OK.

*Resposta (200):*
json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2026-09-01T10:30:00Z"
}


*Resposta (503):*
json
{
  "status": "unhealthy",
  "database": "disconnected",
  "error": "Cannot connect to SQLite"
}


---

## 🛍️ Produtos

### GET /produtos

Lista todos os produtos disponíveis.

*Query Parameters (opcional):*

?skip=0         # Paginação: quantos pular
?limit=20       # Paginação: quantos retornar
?search=pizza   # Filtro por nome (case-insensitive)


*Exemplo:*

GET /produtos?skip=0&limit=10&search=pizza


*Resposta (200):*
json
{
  "total": 5,
  "items": [
    {
      "id": 1,
      "name": "Pizza Margherita",
      "price": 29.99,
      "description": "Mozzarella, tomate, manjericão",
      "created_at": "2026-09-01T08:00:00Z"
    },
    {
      "id": 2,
      "name": "Pizza Pepperoni",
      "price": 32.99,
      "description": "Mozzarella, pepperoni, tomate",
      "created_at": "2026-09-01T08:00:00Z"
    }
=======
# Contrato da API — MVP

Este é o contrato-alvo do MVP. Endpoints só devem ser considerados disponíveis após a implementação e os testes correspondentes.

Base local: `http://localhost:8000`. A documentação interativa do FastAPI, quando a API estiver executando, fica em `/docs`.

## Convenções

- Datas em ISO 8601 UTC.
- Valores monetários enviados e retornados como string decimal (`"29.90"`) ou inteiro em centavos; a implementação deve escolher um padrão e aplicá-lo a todo o contrato.
- Erros usam `{ "detail": "mensagem legível" }` e o status HTTP apropriado.
- `POST /pedidos` requer o header `Idempotency-Key`.

## Catálogo

| Método | Rota | Finalidade |
| --- | --- | --- |
| `GET` | `/healthcheck` | Verificar disponibilidade da API. |
| `GET` | `/restaurantes` | Listar restaurantes e seus indicadores de disponibilidade. |
| `GET` | `/restaurantes/{id}` | Consultar detalhes do restaurante. |
| `GET` | `/restaurantes/{id}/cardapio` | Consultar categorias e produtos disponíveis. |

Um produto de cardápio informa, no mínimo, `id`, `nome`, `descricao`, `preco`, `imagem_url`, `disponivel` e `permite_observacao`.

## Pedidos

| Método | Rota | Finalidade |
| --- | --- | --- |
| `POST` | `/pedidos` | Criar pedido anônimo. |
| `GET` | `/pedidos/{id}` | Consultar um pedido e seu status. |

Exemplo de criação:

json
{
  "restaurante_id": 1,
  "modalidade": "entrega",
  "contato": { "nome": "Cliente", "telefone": "11999999999" },
  "endereco": { "logradouro": "Rua Exemplo", "numero": "10", "bairro": "Centro" },
  "pagamento": { "metodo": "pix" },
  "itens": [
    { "produto_id": 10, "quantidade": 2, "observacao": "Sem cebola" }
>>>>>>> origin/dev
  ]
}


<<<<<<< HEAD
**Erros possíveis:**
- `400` - Parâmetros inválidos (skip/limit não numéricos)
- `500` - Erro do servidor

---

### `GET /produtos/{produto_id}`

Obtém detalhes de um produto específico.

**Path Parameters:**

produto_id (integer, required)  # ID único do produto


**Resposta (200):**
json
{
  "id": 1,
  "name": "Pizza Margherita",
  "price": 29.99,
  "description": "Mozzarella, tomate, manjericão",
  "created_at": "2026-09-01T08:00:00Z"
}


**Erros possíveis:**
- `404` - Produto não encontrado
- `500` - Erro do servidor

---

## 📦 Pedidos

### `POST /pedidos`

Cria um novo pedido anônimo.

**Headers (IMPORTANTE):**

Content-Type: application/json
Idempotency-Key: hash(carrinho+timestamp)  # Único por pedido


**Body (Request):**
json
{
  "email": "cliente@example.com",
  "items": [
    {
      "product_id": 1,
      "quantity": 2,
      "price": 29.99
    },
    {
      "product_id": 3,
      "quantity": 1,
      "price": 15.50
    }
  ],
  "total_price": 75.48
}


**Validações (lado servidor):**
- ✅ Email válido (formato email)
- ✅ Items não vazio (min 1)
- ✅ Quantity > 0
- ✅ Price > 0
- ✅ Total_price = sum(quantity * price)
- ✅ Idempotency-Key único

**Resposta (201 Created):**
json
{
  "order_id": 42,
  "email": "cliente@example.com",
  "status": "pending",
  "items": [
    {
      "product_id": 1,
      "quantity": 2,
      "price_at_purchase": 29.99
    }
  ],
  "total_price": 75.48,
  "tracking_code": "PED-42-ABC123",
  "created_at": "2026-09-01T10:30:00Z"
}


**Se pedido já existe (mesmo Idempotency-Key - 200):**
json
{
  "order_id": 42,
  "status": "already_exists",
  "message": "Pedido já foi criado com essa chave"
}


**Erros possíveis:**
- `400` - Validação falhou (email inválido, items vazio, etc)
- `409` - Conflito (quantidade insuficiente - será usado v0.2.0)
- `500` - Erro do servidor

---

### `GET /pedidos/{order_id}`

Recupera detalhes de um pedido existente.

**Query Parameters (obrigatório):**

?email=cliente@example.com  # Validar identidade


**Path Parameters:**

order_id (integer, required)  # ID do pedido


**Exemplo:**

GET /pedidos/42?email=cliente@example.com


**Resposta (200):**
json
{
  "order_id": 42,
  "email": "cliente@example.com",
  "status": "preparing",
  "items": [
    {
      "product_id": 1,
      "quantity": 2,
      "price_at_purchase": 29.99
    }
  ],
  "total_price": 75.48,
  "tracking_code": "PED-42-ABC123",
  "created_at": "2026-09-01T10:30:00Z",
  "updated_at": "2026-09-01T10:45:00Z"
}


**Erros possíveis:**
- `401` - Email não corresponde ao pedido
- `404` - Pedido não encontrado
- `500` - Erro do servidor

---

## Status de Pedido (Enum)

Valores possíveis para o campo `status`:


pending      → Pedido recebido, aguardando confirmação
preparing    → Sendo preparado em cozinha
ready        → Pronto para entrega
completed    → Entregue ao cliente
cancelled    → Cancelado pelo cliente


---

## Estatutos de Resposta HTTP

| Código | Significado | Quando ocorre |
|--------|------------|---------------|
| `200` | OK | GET bem-sucedido, ou pedido duplicado (Idempotency) |
| `201` | Created | POST bem-sucedido, pedido criado |
| `400` | Bad Request | Validação falhou (email inválido, itens vazio) |
| `401` | Unauthorized | Email não corresponde (GET /pedidos com email errado) |
| `404` | Not Found | Produto ou pedido não existem |
| `409` | Conflict | Conflito (ex: quantidade insuficiente - v0.2.0) |
| `500` | Server Error | Erro inesperado no servidor |
| `503` | Service Unavailable | Database offline |

---

## 🔐 Segurança na API (MVP)

**Implementado:**
- ✅ Validação com Pydantic
- ✅ SQL Injection protection (ORM)
- ✅ CORS básico

**NÃO implementado (v0.2.0+):**
- ❌ Rate limiting (será Railway/Render)
- ❌ Autenticação JWT
- ❌ HTTPS (será no deploy)
- ❌ HMAC das requisições

---

## 📝 Exemplo de Integração (Frontend)

javascript
// api/endpoints.js
import client from './client.js'

export async function getProducts(skip = 0, limit = 20) {
  try {
    const response = await client.get('/produtos', {
      params: { skip, limit }
    })
    return response
  } catch (error) {
    console.error('Erro ao buscar produtos:', error)
    throw error
  }
}

export async function createOrder(email, items, totalPrice) {
  try {
    // Gerar Idempotency-Key (evitar duplicação)
    const hash = generateHash(JSON.stringify(items) + Date.now())
    
    const response = await client.post('/pedidos', {
      email,
      items,
      total_price: totalPrice
    }, {
      headers: {
        'Idempotency-Key': hash
      }
    })
    return response
  } catch (error) {
    console.error('Erro ao criar pedido:', error)
    throw error
  }
}

export async function getOrderStatus(orderId, email) {
  try {
    const response = await client.get(/pedidos/${orderId}, {
      params: { email }
    })
    return response
  } catch (error) {
    console.error('Erro ao buscar pedido:', error)
    throw error
  }
}


---

## 🧪 Testando a API (cURL)

bash
# Teste healthcheck
curl http://localhost:8000/healthcheck

# Liste produtos
curl http://localhost:8000/produtos

# Crie um pedido
curl -X POST http://localhost:8000/pedidos \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: test-key-12345" \
  -d '{
    "email": "teste@example.com",
    "items": [
      {"product_id": 1, "quantity": 2, "price": 29.99}
    ],
    "total_price": 59.98
  }'

# Recupere pedido (rastreamento)
curl "http://localhost:8000/pedidos/1?email=teste@example.com"


---

## 📊 Estrutura de Erros

Todos os erros retornam JSON estruturado:

json
{
  "error": "Bad Request",
  "message": "Email inválido: 'notanemail'",
  "timestamp": "2026-09-01T10:30:00Z",
  "path": "/pedidos"
}


---

## 🔄 Rate Limiting (Futuro)

*Não implementado no MVP, será adicionado em v0.2.0*

Quando implementado, adicionaremos headers:

X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 2026-09-01T11:00:00Z
```

---

## 📞 Dúvidas sobre a API?

- Swagger interativo: http://localhost:8000/docs
- Perguntas técnicas: Abrir issue no GitHub
- Integração no Frontend: Ver frontend/src/api/endpoints.js

---

*Última atualização:* 2026-09-01
=======
Para retirada, endereco não é enviado. O servidor responde com identificador, status, itens, subtotal, taxa, total e tempo estimado. Preços enviados pelo cliente não são aceitos como fonte de cálculo.

## Validações críticas

- Restaurante e produtos existem, estão disponíveis e pertencem ao mesmo restaurante.
- A lista de itens não pode estar vazia e quantidades devem ser positivas.
- Endereço é obrigatório apenas para entrega.
- Pagamento só aceita pix ou dinheiro no MVP.
- A chave de idempotência deve ter unicidade por solicitação de criação.

## Estados e respostas

Estados válidos: criado, em_preparo, pronto, saiu_para_entrega, entregue, cancelado.

201 cria pedido; 200 consulta ou reapresenta uma criação idempotente; 404 indica recurso não encontrado; 422 indica entrada inválida; 409 indica conflito de idempotência quando a mesma chave é reutilizada com conteúdo diferente.

## Integração futura em estudo: geolocalização

Uma API de geolocalização poderá ser avaliada para transformar o endereço de entrega em coordenadas, calcular distância e estimar prazo de entrega. Possíveis usos incluem exibir restaurantes próximos e aplicar uma taxa de entrega por faixa de distância.

Esta integração *não é requisito nem dependência do MVP atual*. No MVP, distância, tempo estimado e taxa podem ser fornecidos pelos dados do restaurante ou por uma regra simplificada do backend. Antes de implementar uma integração externa, a equipe deve definir fornecedor, custo/limite de uso, tratamento de falha, privacidade dos endereços e impacto no contrato da API.
>>>>>>> origin/dev