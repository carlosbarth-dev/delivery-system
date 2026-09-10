# Guia de contribuição

## Antes de começar

1. Receba a tarefa e o critério de aceite do Team Lead.
2. Confirme o requisito em [ROADMAP.md](./ROADMAP.md) e os impactos em [ARQUITETURA.md](./ARQUITETURA.md).
3. Atualize sua cópia de `dev` e crie uma branch específica.

```bash
git checkout dev
git pull origin dev
git checkout -b feature/nome-curto-da-tarefa
```

Não escolha nem atribua trabalho editando arquivos de documentação. O planejamento e a distribuição são conduzidos pelo Team Lead.

## Durante o desenvolvimento

- Faça alterações pequenas e relacionadas à tarefa.
- Não inclua `.env`, ambientes virtuais, `node_modules` ou banco local no commit.
- Valide entradas no backend; não confie em cálculos do frontend.
- Inclua ou atualize testes compatíveis com a mudança.
- Atualize a arquitetura ou API apenas quando a implementação alterar a fonte de verdade desses documentos.

## Pull request

Abra um PR para `dev` com:

- título objetivo;
- contexto e solução adotada;
- como testar;
- evidência de teste (comando e resultado);
- limitações ou pontos que precisam de revisão.

Antes do merge, o revisor confirma aderência ao MVP, funcionamento do fluxo afetado, testes e consistência com o contrato da API.

## Convenções

- Branches: `feature/`, `fix/` ou `docs/` seguidas de uma descrição curta.
- Commits: descreva a ação, por exemplo `feat: cria endpoint de restaurantes`.
- Não faça push direto para `main` ou merge sem revisão.
- Dúvidas de escopo são levantadas ao Team Lead antes de codificar.
