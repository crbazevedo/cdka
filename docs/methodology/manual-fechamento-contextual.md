# Manual metodológico — Fechamento por Continuações Certificadas

**Versão 1.0 · 3 de novembro de 2026.** Da explosão de trajetórias à estrutura que realmente precisa ser preservada.

## 1. A tese metodológica e seu limite

Uma busca combinatória descreve frequentemente o mesmo problema de continuação muitas vezes. O objetivo é identificar o que uma continuação legal ainda consegue distinguir, construir uma representação fechada para isso e analisar os estados reduzidos com certificados.

A tese não é que todos os problemas comprimem. Alguns distinguem todos os estados. Outros têm representação pequena mas otimização difícil. Outros têm descrição sucinta cujo espaço explícito é enorme. A metodologia procura estrutura e verifica sua validade; não promete que ela exista.

Também não confunde invariância com imobilidade. Uma posição, recurso, crença ou estado de controle pode evoluir; queremos uma lei de evolução da descrição reduzida que não dependa de diferenças anteriormente descartadas.

## 2. O contrato vem antes do quociente

Registre um contrato C=(X,A,O,P,G,R,H,Pi): estados/histórias X; operadores A; observações O; protocolo/precedências P; propriedades G; recursos R; horizonte H; classe de políticas Pi.

Para histórias parciais h e h', uma versão exata de equivalência é:

    h ~_C h' <=> têm as mesmas continuações legais relevantes
                   e a mesma resposta para cada uma delas.

Quando há transporte explícito de continuações por simetria, a igualdade usa essa correspondência comprovada. Em problemas probabilísticos, a resposta pode ser uma medida, valor esperado, probabilidade de evento ou uma família de testes. Em jogos, preserve a alternância de quantificadores e observabilidade; não dê a um jogador informação sobre a estratégia futura adversária.

A congruência necessária para atualização é:

    h ~ h' => ha ~ h'a

para extensões correspondentes autorizadas, incorporando observações, recursos e estado do protocolo. Se a abstração mistura histórias que um mesmo novo sinal precisa separar, ela não é implementável por uma atualização determinística de seu próprio código.

### Quantificadores que não podem ser trocados

- `para cada mundo existe uma ação segura` não implica `existe uma política com a informação disponível que é segura em todo mundo`.
- `existe uma estratégia vencedora` não equivale a maximizar separadamente cada ramo depois de conhecer suas realizações.
- `max_a sum_w P(w) V(w,a)` geralmente difere de `sum_w P(w) max_a V(w,a)`.
- Garantia para toda perturbação, alta probabilidade sob uma distribuição e bom desempenho médio são contratos diferentes.

## 3. Escolha o tipo de redução pelo objetivo

| Objetivo | Estrutura útil | O que precisa ser preservado | Certificado |
|---|---|---|---|
| Reconhecimento/viabilidade determinística | Congruência de histórias e refinamento de partições | Legalidade e predicados futuros | Comutação da abstração com transições |
| Contagem | Estados residuais com pesos em inteiros | Número de realizações de cada macrotransição | Agregação de multiplicidades e recursão |
| Probabilidade | Núcleos estocásticos e medidas | Massa, dependências, eventos e observações | Entrelaçamento ou limite de discrepância |
| Avaliação linear de futuras sequências | Espaço invariante gerado por observáveis | Respostas de todos os produtos autorizados | `Q_a B = B C_a` |
| Custo ótimo | Dominância contextual, antichains, min-plus | Melhores continuações sob recursos iguais | Simulação de custo, limite e testemunho de atingimento |
| Satisfação de restrições fatorizadas | Eliminação e separadores | Relações residuais na fronteira | Equivalência dos fatores eliminados |
| Controle/jogo parcialmente observável | Estado informacional e memória realizável | Uma mesma política, sinais acessíveis e alternância | Síntese com observabilidade explícita |
| Verificação aproximada | Abstrações ordenadas, CEGAR | Direção da garantia e validade de contraexemplos | Sobre/subaproximação, erro acumulado |
| Concorrência | Independência e redução de ordens parciais | Propriedade temporal e condições de ciclo | Preservação sob interleavings omitidos |

Não universalize a álgebra linear. Inteiros não negativos, booleanos e min-plus não são todos corpos. Uma base sobre racionais pode usar coeficientes negativos; ela não é automaticamente uma cadeia probabilística nem um controlador físico.

## 4. Três operações parecidas, mas não intercambiáveis

**Equivalência** substitui objetos indistinguíveis sob todos os testes declarados. **Agregação ponderada** soma contribuições que chegam à mesma continuação. **Dominância** remove uma opção porque outra é pelo menos tão boa sob todo contexto relevante, sem dizer que são iguais.

Exemplo mínimo de contagem: duas arestas distintas levam ao mesmo estado residual. Há um estado residual, mas duas trajetórias. Fundir nós é válido; descartar o peso 2 não é. O mesmo princípio vale para probabilidades e tamanhos de órbitas de simetrias.

Exemplo mínimo de otimização: dois caminhos chegam à mesma posição com custos 3 e 5. O segundo pode ser descartado para minimizar custo futuro se todos os outros recursos e obrigações coincidirem. Para contar soluções, para otimizar outra função ou para conservar rotas distintas, essa poda pode ser inválida.

## 5. Algoritmo de pesquisa, não uma receita única

### Etapa A — Especificação regressiva

Comece pelo resultado que o problema precisa preservar. Pergunte qual prefixo pode influenciá-lo. Liste recursos, obrigações pendentes, observações, custos futuros e possibilidades de intervenção. Construa o menor estado residual candidato.

### Etapa B — Casos completos pequenos

Antes de generalizar, enumere completamente uma família mínima. Conserve probabilidades ou multiplicidades exatas. Registre estados concretos, estado reduzido, ação escolhida, sinal, recurso, motivo de falha e continuação. Não selecione apenas rastros de sucesso.

### Etapa C — Separadores

Procure duas histórias candidatas à fusão e uma continuação que as distingue. Uma boa refutação não diz apenas que os outcomes diferem; identifica a primeira obrigação futura que precisa da informação descartada.

### Etapa D — Fechamento

Pseudocódigo abstrato:

    estrutura <- observáveis/interfaces terminais
    fronteira <- geradores ainda não certificados
    enquanto fronteira não vazia:
        candidato, proveniência <- aplicar gerador permitido
        se candidato altera respostas/viabilidade/custo de forma relevante:
            reter distinção ou refinar partição
            registrar testemunho e novas obrigações
        senão:
            registrar certificado de redundância/dominância
    emitir representação + atualização + certificado + testemunhos

O teste de redundância é específico à classe. Igualdade de hashes não prova semântica; resultados numéricos próximos não provam igualdade exata; igualdade em horizonte curto não prova fechamento.

### Etapa E — Verificação independente

Compare a análise reduzida com a enumeração física ou lógica direta em casos pequenos. Não reutilize no oráculo a própria fórmula que está sendo testada. Para algoritmos de eliminação, compare com busca completa; para abstrações probabilísticas, compare linhas e eventos; para síntese de circuitos, execute as portas e compare todas as entradas.

### Etapa F — Realização e continuação

Reconstrua uma solução original a partir da solução reduzida. Para uma política, materialize a memória e as regras de atualização. Para um plano, preserve ações legais e recursos em todos os prefixos. Para um método geral, identifique o parâmetro estrutural que controla o custo.

## 6. Três aplicações exemplares

### 6.1. SAT, CSP e contagem

Um prefixo é uma atribuição parcial. Sua continuação depende da fórmula residual sobre variáveis não atribuídas, dos pesos e das obrigações adicionais. Dois prefixos que geram a mesma instância residual podem compartilhar uma análise. Porém, contagem de modelos exige multiplicar/somar o número de prefixos representados; otimização ponderada exige levar o custo acumulado. Eliminação por fatores pode evitar construir atribuições globais, com custo dependente da largura induzida. A metodologia não promete uma largura pequena.

### 6.2. Planejamento e roteamento

Uma localização igual não basta: combustível, prazo, tarefas já realizadas e obrigações futuras podem diferir. O estado residual deve incluir apenas as diferenças que alguma ação futura pode tornar decisivas. Dominância por menor custo vale somente se não deteriora outro recurso relevante. Para mundos parcialmente observáveis, a rota do pesquisador não pode consultar o estado oculto.

### 6.3. Síntese de pequenos circuitos

Um prefixo de circuito contém os sinais já calculados e o número de portas utilizadas. Sob portas determinísticas ideais, fanout livre e custos uniformes, duas construções que disponibilizam as mesmas funções verdade e custam o mesmo admitem exatamente as mesmas extensões. Podemos fundir esses prefixos antes de explorar mais portas.

Isso é utilizado no incremento CDKA v13. Mas, com falhas internas de portas, os sinais podem ter dependências diferentes. Um fio e dois inversores têm a mesma função perfeita; sob inversões independentes em cada porta, não têm a mesma confiabilidade. O contrato de análise determina a equivalência.

## 7. Aproximação e tolerâncias

Use aproximação quando a equivalência exata preserva diferenças mais finas que o objetivo exige, mas indique o que está sendo limitado: erro de transição, perda de valor, risco de segurança, contagem relativa ou erro de uma política transferida.

Um limite local não é um limite de horizonte infinito. Propague o erro e mostre quando o certificado se torna inútil. Distingua sobreaproximação que certifica segurança, subaproximação com solução concreta, contraexemplo espúrio que exige refinamento e testemunho real que refuta a garantia.

Nunca apresente um valor de grade como ótimo de um problema contínuo sem um limite entre os pontos.

## 8. Complexidade: quatro contabilidades

Registre (1) tamanho da descrição de entrada; (2) espaço explícito gerado; (3) estrutura efetiva — rank, classes, largura, número de fatores ou antichain; (4) custo de produzir a solução, incluindo precisão e tamanho da saída.

Por exemplo, `|G|+|A|d` candidatos em um fechamento linear não é esse número de operações de CPU: cada candidato exige produtos e testes algébricos. Um modelo sucinto pode levar exponencialmente muitos estados para ser construído. A síntese ótima sobre um bom modelo reduzido pode continuar difícil.

Se a tarefa exige enumerar N objetos distintos, nenhuma representação compacta equivale à sua listagem explícita sem pagar o custo de saída. Um gerador com atraso controlado, um circuito de contagem ou um certificado podem ser alternativas, desde que atendam ao objetivo declarado.

## 9. Memória de pesquisa e retomada

Cada abordagem deve manter: ID, hipótese, contrato, evidência, classificação de contribuição, falha observada, gatilho de retomada, menor próximo teste, ferramentas, alternativas, critérios de conclusão e arquivos de origem.

Separe bug de implementação, hipótese falsa, interface incompleta, incerteza numérica, certificado conservador demais, custo de modelo e antecedente equivalente. O tratamento é diferente em cada caso.

Uma contribuição pode ser uma formulação nova, adaptação necessária, resultado de subproblema, certificado, método de síntese ou aplicação com ganho explicável. Prioridade bibliográfica, correção e fertilidade são eixos distintos. Documente limites sem transformar automaticamente o uso de teoria existente em ausência de inovação.

## 10. Critérios de conclusão

Uma etapa está concluída quando oferece enunciado e contrato inequívocos; prova ou limite e testemunho de atingimento; implementação reproduzível e oráculo independente; falsificador de uma generalização excessiva; contabilidade de complexidade; solução recuperável ou lacuna de implementação explícita; antecedente e diferença concreta; registro das hipóteses seguintes sem crescimento arbitrário do modelo.

## Referências primárias

- Tzeng, W.-G. (1992), *A Polynomial-Time Algorithm for the Equivalence of Probabilistic Automata*, DOI 10.1137/0221017.
- Cousot, P.; Cousot, R. (1977), *Abstract interpretation: a unified lattice model for static analysis of programs by construction or approximation of fixpoints*. https://cs.nyu.edu/~pcousot/COUSOTpapers/POPL77.shtml .
- Clarke et al. (2000), *Counterexample-Guided Abstraction Refinement*, DOI 10.1007/10722167_15.
- Dechter, R. (1999), *Bucket elimination: A unifying framework for reasoning*, DOI 10.1016/S0004-3702(99)00059-4.
- Mohri, M. (2002), *Semiring Frameworks and Algorithms for Shortest-Distance Problems*, https://research.google/pubs/semiring-frameworks-and-algorithms-for-shortest-distance-problems/ .
- De Micheli, Brayton e Sangiovanni-Vincentelli (1985), *Optimal State Assignment for Finite State Machines*, https://research.ibm.com/publications/optimal-state-assignment-for-finite-state-machines .

A contribuição do protocolo é organizar a escolha e a ligação desses instrumentos em torno de contratos, continuações, mecanismos e certificados. Não identifica uma única técnica como solução universal para problemas combinatórios.
