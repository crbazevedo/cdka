# Direção competitiva v19 — Ganhar uma classe antes de ampliar a teoria

## Decisão executada

Buscar uma especialização verificável: famílias de implementações estocásticas com um espaço comum pequeno de continuações e horizontes longos. O método deve complementar verificadores atuais, não reivindicar que todo POMDP ou toda combinatória ficou fácil.

Piloto: Storm via Stormpy2.0.0, família inteira, três repetições por componente,35 casos. Ganho16,54–26,22× em horizonte100mil na classe sintética construída, incluindo compilação. Perdas em horizontes curtos e no caso original CDKA48. A prova não será vendida como economia em regimes onde seu custo supera a vantagem.

## Ordem de execução

1. Concluído: teorema necessário/suficiente para escolhas locais retangulares, algoritmo exato, testemunhos, teste externo e classe positiva/negativa.
2. R11: testar a fronteira rank–horizonte–amortização em casos públicos e contra um comparador algébrico direto. Cobrar descoberta, verificação, decisão de rejeitar e fallback.
3. R14: usar equivalência de sobrevivência para separar escolhas de implementação, sem esquecer que custos que mudam o saldo podem mudar os operadores e invalidar o certificado.
4. Artigo delimitado: “Common-continuation certificates for families of stochastic implementations”. O modelo físico é uma aplicação e controle de corretude, não toda a avaliação.
5. Depois: dividir famílias em regiões de continuação comum ou aproximada, somente com novo enunciado e garantia. Máximos não se transportam automaticamente para uma assinatura linear arbitrária.

## Comparações obrigatórias

Storm esparso e alternativas simbólicas adequadas; método de Krylov/recorrência com verificação de linhas; equivalência probabilística/APEX; ferramentas de família/PAYNT quando a interface experimental permitir. A amostra QVBS/PRISM deve ser escolhida por critérios de estrutura prévios, não apenas pelos casos em que ganhamos. Não importar uma política onisciente para o controlador físico.

## Critérios de promoção

Resultado reprodutível em uma subclasse publicada, com instâncias retidas; vantagens em tempo total e qualidade/certificado compatíveis; negativos e custos de descoberta documentados; nenhuma alegação de precisão exata para a projeção numérica sem controle de erro. Memória medida por método antes de alegar vantagem de RAM.

## Decisão de prioridade

Somente R11/R14 ativos; R51 é um instrumento de avaliação competitiva. Preservar as apostas fundacionais, mas não acrescentar outro componente sem demonstrar ampliação de classe, melhoria algorítmica, aplicação relevante ou certificado mais forte. Uma aplicação inovadora de instrumentos conhecidos continua contando como contribuição.
