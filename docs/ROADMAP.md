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
