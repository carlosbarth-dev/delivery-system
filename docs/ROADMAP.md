# Roadmap e escopo do produto

## MVP — Marketplace de delivery

O MVP demonstra o fluxo completo de compra em um restaurante. Ele não pretende reproduzir todos os recursos de plataformas comerciais.

### Funcionalidades incluídas

| Área | Requisito |
| --- | --- |
| Descoberta | Listar restaurantes com status aberto/fechado, distância e tempo estimado. |
| Cardápio | Exibir categorias, produtos, foto/URL de imagem, descrição, preço e observação quando permitida. |
| Carrinho | Adicionar, remover e alterar quantidades; recalcular subtotal e total. |
| Entrega | Escolher entrega ou retirada; calcular a taxa de entrega. |
| Checkout | Finalizar sem login com os dados mínimos necessários para o pedido. |
| Pagamento | Permitir Pix e dinheiro na entrega. |
| Pedido | Criar pedido, exibir status e tempo estimado de entrega. |
| Resiliência | Preservar carrinho/pedido localmente, apresentar erros claros e evitar pedido duplicado. |

### Requisitos funcionais do MVP

| ID | Requisito |
| --- | --- |
| RF-01 | O sistema deve listar restaurantes com nome, status aberto/fechado, distância e tempo estimado. |
| RF-02 | O cliente deve consultar o cardápio de um restaurante por categoria. |
| RF-03 | Cada produto deve informar nome, descrição, preço, imagem/URL, disponibilidade e se aceita observação. |
| RF-04 | O cliente deve adicionar produtos ao carrinho, remover itens e alterar quantidades. |
| RF-05 | O carrinho deve aceitar itens de apenas um restaurante por pedido. |
| RF-06 | O cliente deve escolher entrega ou retirada; endereço é obrigatório somente para entrega. |
| RF-07 | O sistema deve calcular subtotal, taxa de entrega e total no backend. |
| RF-08 | O checkout anônimo deve aceitar somente Pix ou dinheiro na entrega no MVP. |
| RF-09 | O sistema deve criar um pedido com identificador, itens, valores, modalidade, pagamento e estado inicial. |
| RF-10 | O cliente deve consultar o pedido e visualizar seu status e tempo estimado. |
| RF-11 | O sistema deve impedir a duplicação de pedido quando a mesma solicitação for repetida. |
| RF-12 | O carrinho e a referência do pedido devem sobreviver ao recarregamento da página. |

### Fluxo do usuário

```text
Abrir aplicação
    ↓
Consultar restaurantes disponíveis
    ↓
Abrir cardápio e escolher produtos
    ↓
Montar carrinho de um único restaurante
    ↓
Escolher entrega ou retirada
    ↓
Informar dados obrigatórios e escolher Pix ou dinheiro
    ↓
Revisar valores calculados pelo sistema e confirmar pedido
    ↓
Receber identificação do pedido e acompanhar o status
```

### Requisitos não funcionais essenciais

- O backend valida dados, disponibilidade e valores antes de persistir o pedido.
- Erros devem ser claros para o cliente e não expor detalhes internos.
- A criação de pedido deve usar uma chave de idempotência.
- Dados locais do carrinho e pedido devem ser tratados de forma segura e recuperável em falha de rede.
- O MVP deve ser demonstrável em ambiente local com dados de exemplo.

### Regras de escopo

- Um pedido pertence a um único restaurante.
- O servidor calcula preços, taxa e total; o frontend nunca é fonte de verdade financeira.
- O checkout anônimo deve coletar endereço somente para entrega e contato mínimo para acompanhamento.
- Idempotência é obrigatória na criação de pedido: repetir a mesma solicitação não pode gerar dois pedidos.
- “Canal de emergência” e “alerta de atraso” podem ser apresentados como informações de contato e regra de interface no MVP; não exigem integração externa de mensagens.

### Fora do MVP

- Conta, login, perfil, histórico e favoritos.
- Pagamento on-line integrado ou confirmação automática de Pix.
- Rastreamento GPS, WebSocket, notificações por e-mail/SMS e aplicativo de entregador.
- Painel administrativo, cupons, avaliações e analytics.
- Infraestrutura de produção, microsserviços ou migração para MySQL.

## Próximos incrementos

| Incremento | Direção |
| --- | --- |
| 1 | Autenticação, perfil, endereços salvos, histórico e favoritos. |
| 2 | Notificações e rastreamento mais completo. |
| Futuro | Painel do restaurante, entregadores, pagamentos integrados e escala. |

## Critério de conclusão do MVP

Uma pessoa consegue escolher um restaurante, montar um pedido válido, escolher entrega ou retirada, finalizar sem login e consultar o status do pedido. O fluxo possui validações, tratamento de erro e testes dos cenários essenciais.

**Fonte de verdade do escopo.** Qualquer funcionalidade nova deve ser aprovada antes de entrar no desenvolvimento.
