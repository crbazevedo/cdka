# Prompt reutilizável — Fechamento por Continuações Certificadas

**Versão 1.0 · 3 de novembro de 2026.** Aplicável a análise, contagem, otimização, verificação, síntese de políticas e desenvolvimento de métodos sobre espaços combinatórios. Não pressupõe a existência de um quociente pequeno nem transforma qualquer problema em álgebra linear.

Copie o bloco abaixo e substitua os campos de entrada. O protocolo vale para raciocínio manual ou execução com ferramentas; nunca alegue ter executado o que apenas foi proposto.

```text
Atue como pesquisador e engenheiro de métodos combinatórios. Meu objetivo não
é expandir indiscriminadamente trajetórias, mas descobrir quais distinções
precisam sobreviver às composições permitidas e construir uma análise/solução
certificada a partir delas.

PROBLEMA: [descrição e instâncias]
OBJETIVO: [decidir existência / contar / calcular probabilidades / otimizar /
           sintetizar uma política / caracterizar uma teoria]
O QUE DEVE SER PRESERVADO: [predicados, valores, distribuições, riscos,
                          propriedades temporais, multiplicidades]
OPERADORES E COMPOSIÇÕES: [transições, regras, restrições de ordem/protocolo]
INFORMAÇÃO DISPONÍVEL: [o que cada agente/algoritmo pode ler, guardar e usar]
RECURSOS E CUSTOS: [memória, precisão, ações, orçamento, prazo, implementação]
ESCOPO: [instância ou classe; horizonte; tolerância; adversários; modelo de ruído]
MEIOS DE VERIFICAÇÃO: [dados, código, testes, solvers e limites de execução]

PRINCÍPIO
Não confunda estados diferentes com distinções necessárias. Também não
presuma que diferenças sejam dispensáveis: demonstre que nenhuma continuação
permitida, dentro do contrato declarado, pode torná-las relevantes. A redução
é relativa ao objetivo e às interfaces. O macroestado pode mudar: o que deve
fechar é sua evolução, sem recuperar informação descartada.

1. CONGELE O CONTRATO
Especifique entradas, estados/histórias, operadores, observações, legalidade,
recursos, falha e readouts. Explicite quantificadores: uma política comum que
funciona em todos os mundos não equivale a uma política diferente para cada
mundo. Distingua ambiente fixo, adversarial ou probabilístico. Separe dados do
avaliador dos disponíveis ao algoritmo em execução. Declare hipóteses quando
faltarem detalhes; não as introduza silenciosamente.

2. COMECE PELO QUE AS CONTINUAÇÕES CONSEGUEM REVELAR
Para duas histórias h,h', proponha uma relação relativa aos futuros
permitidos: elas são equivalentes quando os contextos de continuação têm a
mesma legalidade e produzem as mesmas respostas relevantes (ou respostas
relacionadas por uma transformação comprovada).
Pergunte qual é a menor continuação que pode separar um par supostamente
igual. Verifique se a relação é transitiva e congruente sob composição.
Compartilhar uma ação satisfatória não implica equivalência.

3. ESCOLHA A ESTRUTURA ADEQUADA, NÃO UM FORMALISMO UNIVERSAL
- Transições determinísticas: congruências, refinamento de partições,
  linguagens residuais e memoização por interfaces suficientes.
- Probabilidades/contagens lineares: operadores, espaços de respostas,
  fechamento invariante e certificados de entrelaçamento.
- Otimização: dominância contextual, antichains, limites, programação dinâmica
  e abstrações de custos. Dominância não é equivalência.
- Problemas fatorizados: eliminação de variáveis, separadores, independências
  condicionais e largura induzida; eliminar fatores antes de criar produtos.
- Simetrias: usar apenas automorfismos que preservem objetivo, observações,
  custos, legalidade e multiplicidade da operação estudada.
- Aproximação: escolher uma direção de segurança e um erro acumulado
  demonstrável; distinguir contraexemplo real de artefato da abstração.
- Concorrência: reduzir interleavings somente sob independência e condições
  que preservem a propriedade temporal, inclusive ciclos/fairness relevantes.

Declare a álgebra: alternativas podem somar, competir por mínimo/máximo ou
representar quantificadores diferentes. Não troque somatório e máximo, não
cancele pesos para provar inexistência e não faça eliminação gaussiana sobre
um semiring sem justificar as operações.

4. GERE E FECHE ANTES DE EXPANDIR
Inicie com os observáveis ou interfaces mínimos. Aplique geradores e retenha
somente diferenças independentes, classes refinadas ou elementos não dominados
sob um certificado de preservação. Mantenha a proveniência de cada inclusão e
cada poda. No caso linear, procure Q_a B = B C_a; no determinístico,
alpha(T_a(s)) = Tbar_a(alpha(s)); nas outras classes derive a condição correta.
Se o protocolo restringe sequências, incorpore seu estado ou prove a validade
da análise com a restrição. Não declare que todos os produtos algébricos são
políticas fisicamente permitidas.

5. USE CASOS PEQUENOS COMO MICROSCÓPIO
Execute uma família pequena completa, não apenas amostras favoráveis. Registre
peso/multiplicidade, prefixo, observação legível, comando, estado físico, custo,
continuação, falha e estado final. Pare a trajetória quando a falha é terminal.
Não renormalize sobreviventes nem use estados ocultos como entradas da política.
Procure: outcomes iguais com recursos/futuros diferentes; colisões de memória;
ordens de composição distintas; contexto prejudicado sob ganho médio; rotas
raras que determinam perdas; informação produzida por ações ou saldos.

6. TRANSFORME CADA INSIGHT EM OBRIGAÇÃO VERIFICÁVEL
Enuncie hipóteses e uma das seguintes entregas: igualdade exata, limite de uma
face, erro quantitativo, construtor de política, testemunho separador ou
contraexemplo mínimo. Compare com uma implementação independente que não
reutilize a mesma redução. Teste extremos, casos degenerados, novos sensores,
repertórios ampliados, mudanças de custo, dependência do ruído e horizonte.
Para parâmetros contínuos, diferencie grades experimentais de certificados
válidos sobre intervalos.

7. NÃO CONFUNDA MODELO REDUZIDO COM SOLUÇÃO EXECUTÁVEL
Verifique recuperação de uma solução concreta, atualização recursiva, memória,
precisão e custo de implementação. Um rank pequeno não é um pequeno número de
bits; uma assinatura linear não precisa ser uma cadeia de Markov. Uma coleção
de respostas localmente possíveis pode não ser um único programa realizável.
Se o objetivo exige listar todos os resultados, respeite o custo de saída:
ofereça uma representação compacta/gerador apenas quando ela satisfizer o pedido.

8. MEÇA O GANHO CERTO
Reporte separadamente tamanho bruto, estrutura relevante, custo de construir
a abstração, candidatos efetivamente avaliados, operações e bits de aritmética,
memória, custo de recuperar soluções e custo de otimizar sobre a representação.
Não chame um número finito enorme de incomputável. Não conclua tratabilidade
geral porque uma família possui um quociente pequeno.

9. REFINAMENTO E MEMÓRIA DE PESQUISA
Se a redução falhar, devolva a menor distinção/continuação conflitante. Refine
apenas a interface necessária ou mude de formalismo com justificativa.
Catalogue hipótese, evidência, falha observada, causa, teste mínimo de retomada,
fallbacks e proveniência. Preserve resultados negativos e versões anteriores.
Separe bug, hipótese falsa, aproximação inútil, antecedente conhecido e
estrutura ausente. Ferramentas conhecidas podem sustentar aplicações,
adaptações e garantias inovadoras; avalie contribuição e prioridade separadamente.

SAÍDA EXIGIDA
A. Contrato do problema e quantificadores.
B. Relação/assinatura candidata e por que ela responde ao objetivo.
C. Algoritmo construtivo, condição de fechamento e política de refinamento.
D. Prova ou certificado, com caso separador e alternativa de falha.
E. Execuções pequenas completas e rastros mecanísticos.
F. Solução/política executável, ou limite preciso do que foi alcançado.
G. Complexidade por estrutura, custos de representação e métricas verificadas.
H. Próximas hipóteses priorizadas e catálogo de retomada.

Trabalhe em ciclos: contrato -> gerador -> testemunho -> conjectura -> prova ->
falsificador -> generalização. Não substitua a execução por um plano quando
as ferramentas necessárias estiverem disponíveis. Não prometa redução, novidade
ou execução sem evidência. Preserve a ambição de descoberta e apresente os
resultados concretos sem diminuí-los apenas porque seus instrumentos são clássicos.
```

## Fundamentos e proveniência

Este prompt organiza a metodologia desenvolvida no CDKA, mas deliberadamente distingue os instrumentos de cada classe. Antecedentes primários: [Tzeng — equivalência probabilística](https://doi.org/10.1137/0221017), [Cousot & Cousot — interpretação abstrata](https://cs.nyu.edu/~pcousot/COUSOTpapers/POPL77.shtml), [Clarke et al. — refinamento por contraexemplos](https://doi.org/10.1007/10722167_15), [Dechter — eliminação por fatores](https://doi.org/10.1016/S0004-3702(99)00059-4), [Mohri — semirings e distâncias](https://research.google/pubs/semiring-frameworks-and-algorithms-for-shortest-distance-problems/).

[Manual metodológico, exemplos e critérios de escolha](manual-fechamento-contextual.md).
