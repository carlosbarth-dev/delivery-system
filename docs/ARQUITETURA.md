# Arquitetura do MVP

## Visão geral

```text
Vue 3 (interface e estado local)
            │ HTTP/JSON
            ▼
FastAPI (validação e regras de negócio)
            │ ORM
            ▼
MySQL (dados do MVP)
```

O frontend mantém apenas estado de interface e o carrinho temporário. O backend valida a solicitação, consulta o catálogo, calcula valores e persiste o pedido. Valores enviados pelo cliente devem ser recalculados no servidor.

## Componentes

| Camada | Responsabilidade |
| --- | --- |
| Vue + Pinia | Catálogo, cardápio, carrinho, checkout, acompanhamento e persistência local. |
| Axios | Comunicação HTTP e apresentação consistente de falhas. |
| FastAPI + Pydantic | Endpoints, validação de entrada e respostas de erro. |
| SQLAlchemy | Modelagem e acesso ao banco. |
| MySQL | Persistência relacional do MVP, acessada por SQLAlchemy e PyMySQL. |

## Domínio mínimo

```text
Restaurante 1 ── * Categoria 1 ── * Produto
Restaurante 1 ── * TaxaEntrega
Restaurante 1 ── * Pedido 1 ── * ItemPedido
```

| Entidade | Dados relevantes |
| --- | --- |
| Restaurante | nome, status, endereço/referência de localização, tempo estimado. |
| Categoria | restaurante, nome e ordem de exibição. |
| Produto | categoria, nome, descrição, preço, imagem, disponibilidade e permite observação. |
| TaxaEntrega | restaurante e regra/faixa usada para calcular a taxa. |
| Pedido | restaurante, status, modalidade, contato, endereço quando aplicável, pagamento, subtotal, taxa, total e chave de idempotência. |
| ItemPedido | pedido, produto, quantidade, observação e preço registrado no momento da compra. |

## Fluxo do pedido

1. O cliente consulta restaurantes e cardápio.
2. O carrinho aceita itens de apenas um restaurante.
3. No checkout, o cliente escolhe entrega ou retirada e forma de pagamento.
4. O backend valida disponibilidade, modalidade e dados obrigatórios; depois recalcula subtotal, taxa e total.
5. A criação usa `Idempotency-Key`; a mesma chave retorna o resultado original.
6. O pedido é persistido com um estado inicial e pode ser consultado pelo identificador e dado de contato definido no contrato da API.

## Estados do pedido

`criado` → `em_preparo` → `pronto` → `saiu_para_entrega` → `entregue`

Para retirada, `pronto` pode seguir diretamente para `entregue`. Cancelamento é um estado terminal permitido antes da entrega.

## Princípios técnicos

- Dinheiro usa decimal/centavos, nunca `float` como regra de negócio.
- Senhas e autenticação não fazem parte do MVP.
- CORS é restrito aos endereços do frontend em cada ambiente.
- Erros retornam um formato previsível, sem expor detalhes internos.
- Testes cobrem cálculo de total, validações, idempotência e fluxo principal de pedido.

## Evolução

MySQL é o banco adotado desde o MVP, inclusive no ambiente local. Uma migração para banco gerenciado, autenticação e notificações só será planejada depois de o MVP estar validado.
