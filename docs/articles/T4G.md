# T4.G — Corrigir a memória não é atualizar o conhecimento

**Status:** modelo finito e certificados clássicos aplicados; originalidade não estabelecida.

## Pergunta e motivação

Como analisar um controlador cujo mundo muda, cuja memória sofre erros e cujo corretor também degrada? Precisamos demonstrar quando uma descrição pequena preserva as garantias físicas sem dar ao controlador informação que ele não possui.

## Definições mínimas

W é o mundo oculto; três células guardam uma representação; h é a saúde do corretor; b é um reservatório finito. Manter custa 0, corrigir 1, observar novamente ou fazer manutenção 2. Percepção, correção, escrita, execução e manutenção podem falhar. Recurso chega só após uma operação correta.

A descrição reduzida usa discordância legível, h e b. A contagem de erros só é inferível nos estados vivos específicos do modelo; não é uma observação gratuita do mundo.

## Formulação e resultado

A composição dos canais e suas simetrias permite 80 estados físicos vivos -> 20 estados legíveis. As 240 linhas de transição foram comparadas com enumeração bruta independente e aritmética racional, com erro exatamente zero. A política reduzida pode ser implementada pelos sinais declarados.

    K^a L = L Kbar^a

## Exemplo

Com mudança ambiental de 20%, uma memória antiga perfeita fornece 80% de comando correto quando mantida ou copiada. Uma observação nova com 5% de erro fornece 95%. Corrigir os dados não atualiza automaticamente sua relação com o mundo.

O horizonte também muda a primeira operação: no exemplo com corretor degradado, manter é ótimo para uma etapa; manutenção é ótima para horizontes maiores.

## Falsificação

Com falhas por célula (.30,.01,.01), a localização da discordância passa a importar. Dois estados com a mesma contagem geram distância TV=.2568095. A agregação exata deve ser rejeitada. Refinar a partição ou certificar aproximação, não esconder a diferença.

## Certificado aproximado

Se cada componente tem erro uniforme delta_i e a mesma classe de políticas físicas corresponde nos dois modelos,

    Delta_n = 1-[produto_i(1-delta_i)]^n

limita a diferença de probabilidade até n etapas. O limite pode ficar conservador ou vazio; não prova segurança infinita.

## Bigger picture e o que habilita

A descrição reduzida passa a ter uma ligação verificável com a política física. Isso fornece um instrumento para análises modulares e calibração de componentes. Os próximos gates tornam a saúde parcialmente observável e cobram pelo mecanismo de seleção conjunta de operações. Saúde perfeitamente legível ainda é uma hipótese.

## Simulador

[Laboratório interativo](../lab/composition.html): curvas de sobrevivência, ablações de percepção/manutenção, mapa de políticas, erro de calibração e catálogo pesquisável de 32 abordagens.

[Provas e limites](../results/T4G-compositional-contracts.md) · [Estratégia v6](../strategy/proof-engine-v6.md) · [Catálogo de alternativas](../../registry/research-options.md).

## Antecedentes

Agregação e abstrações composicionais têm antecedentes diretos: [Buchholz](https://www.cambridge.org/core/journals/journal-of-applied-probability/article/abs/exact-and-ordinary-lumpability-in-finite-markov-chains/2DC748F09D80BEEB03CCF18036E149D7), [Lavaei, Soudjani e Zamani](https://arxiv.org/abs/1808.00893), [Junges et al.](https://proceedings.mlr.press/r16/junges18a.html). Esta demonstração verifica uma organização específica, não reivindica essas ferramentas como novas.
