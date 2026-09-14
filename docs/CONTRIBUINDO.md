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

## Quando sua branch foi criada a partir de uma versão antiga

Uma branch antiga não significa que o trabalho deve ser apagado. Ela funciona como um rascunho ou backup do que já foi feito. O problema é fazer merge dela diretamente em `dev`: isso pode trazer arquivos duplicados, rotas antigas ou uma estrutura que o projeto não usa mais.

Nessa situação, mantenha a branch antiga guardada e crie uma nova a partir da `dev` atual:

```bash
# Primeiro, garanta que não há alteração sem commit na sua branch atual.
git fetch origin
git switch dev
git pull origin dev
git switch -c feat/area-objetivo
```

Exemplos de nomes:

- `feat/modelagem-pedidos-mysql`
- `feat/catalogo-restaurantes-frontend`
- `feat/seguranca-catalogo-mvp`

Na nova branch, reaproveite apenas os arquivos e trechos úteis da branch antiga. Adapte-os à estrutura, aos nomes e ao contrato atuais; não copie uma pasta inteira sem revisar. Depois, teste, faça novos commits e abra uma nova PR para `dev`.

```bash
git add .
git commit -m "feat: descreve a alteração"
git push origin feat/area-objetivo
```

### O que fazer com a branch e a PR antigas

1. Não apague a branch antiga enquanto a nova PR ainda não foi aprovada: ela é seu backup.
2. Deixe um comentário na PR antiga informando que ela foi substituída pela nova PR, incluindo o link ou número dela.
3. Feche a PR antiga sem fazer merge.
4. Depois que a nova PR entrar em `dev` e o conteúdo estiver confirmado, a branch antiga pode ser apagada.

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
