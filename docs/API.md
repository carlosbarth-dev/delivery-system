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

```json
{
  "restaurante_id": 1,
  "modalidade": "entrega",
  "contato": { "nome": "Cliente", "telefone": "11999999999" },
  "endereco": { "logradouro": "Rua Exemplo", "numero": "10", "bairro": "Centro" },
  "pagamento": { "metodo": "pix" },
  "itens": [
    { "produto_id": 10, "quantidade": 2, "observacao": "Sem cebola" }
  ]
}
```

Para `retirada`, `endereco` não é enviado. O servidor responde com identificador, status, itens, subtotal, taxa, total e tempo estimado. Preços enviados pelo cliente não são aceitos como fonte de cálculo.

## Validações críticas

- Restaurante e produtos existem, estão disponíveis e pertencem ao mesmo restaurante.
- A lista de itens não pode estar vazia e quantidades devem ser positivas.
- Endereço é obrigatório apenas para entrega.
- Pagamento só aceita `pix` ou `dinheiro` no MVP.
- A chave de idempotência deve ter unicidade por solicitação de criação.

## Estados e respostas

Estados válidos: `criado`, `em_preparo`, `pronto`, `saiu_para_entrega`, `entregue`, `cancelado`.

`201` cria pedido; `200` consulta ou reapresenta uma criação idempotente; `404` indica recurso não encontrado; `422` indica entrada inválida; `409` indica conflito de idempotência quando a mesma chave é reutilizada com conteúdo diferente.

## Integração futura em estudo: geolocalização

Uma API de geolocalização poderá ser avaliada para transformar o endereço de entrega em coordenadas, calcular distância e estimar prazo de entrega. Possíveis usos incluem exibir restaurantes próximos e aplicar uma taxa de entrega por faixa de distância.

Esta integração **não é requisito nem dependência do MVP atual**. No MVP, distância, tempo estimado e taxa podem ser fornecidos pelos dados do restaurante ou por uma regra simplificada do backend. Antes de implementar uma integração externa, a equipe deve definir fornecedor, custo/limite de uso, tratamento de falha, privacidade dos endereços e impacto no contrato da API.
