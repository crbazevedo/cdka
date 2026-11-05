# Sufixos certificados pelo contexto que ainda pode ocorrer

**5 de novembro de 2026 · R11/R14.** Este incremento reduz a enumeração dos
sufixos sem manutenção e preserva as decisões sobre programas completos no
modelo físico herdado. A garantia acompanha um horizonte declarado. O ganho
de tempo aparece nos casos maiores medidos; nos menores, construir a prova
custa mais que avaliar os sufixos diretamente.

Com 16 preparações e 14 atualizações obrigatórias, a mediana de três execuções,
incluindo construção física e certificação, caiu de **16,1921 s para 4,3270 s**, contra a
fronteira anterior já fortalecida com a mesma álgebra de oito coordenadas.
Isso corresponde a **3,7421 vezes** menos tempo. A nova recorrência gera 160
dos 262.144 programas legais e retém 53 representantes. O comparador já evitava
229.284 programas; o ganho incremental é evitar mais 32.700 construções no
nível final. [Experimento exato](../data/suffix-context-results.json) ·
[Medições completas](../data/suffix-context-benchmark.json)

## Motivação

A [fronteira de famílias anterior](program_families.md) já descartava programas
inteiros por dominância, mas conservava todos os `2^K` sufixos ordinários. Eles
eram necessários para avaliar a manutenção seguida por qualquer sequência de
D/R. Essa fronteira era o gargalo remanescente do compilador.

Uma comparação entre sufixos precisa sobreviver aos contextos em que o sufixo
ainda será utilizado. A ordem de quatro coordenadas válida na entrada não
atravessa M automaticamente. Também é caro exigir proteção contra prefixos de
todos os comprimentos quando a decisão atual admite apenas um número finito.
O mecanismo desenvolvido aqui faz a exigência acompanhar esse número.
[Prova e contraexemplos](../results/suffix-context-proof.md)

## Contrato físico e saída

O sistema conserva os 16 estados físicos, a saúde oculta do substrato, uma
aquisição paga com uma única saída de sensor compartilhada pelas três escritas,
e o votador efetivo de seis NANDs. D difunde as células; R executa o votador e
reescreve; M usa seu resultado físico para uma tentativa de manutenção
pré-paga. O controlador executa uma palavra fixa, com exatamente K operações
D/R e no máximo um M adicional. A tarefa terminal é reproduzir a fonte oculta H.

O domínio alcançável tem contraste `mu_1-mu_0=-x E`, com `x>=0`. O valor de uma
palavra é `V(w)=1/2-x E K_w g`. A cobertura preserva os valores informados,
um minimizador do arrependimento máximo, um maximizador da fidelidade mínima e
a existência de um programa que atenda simultaneamente a um limite de
arrependimento e a um piso de fidelidade. Os programas continuam sujeitos à
mesma reserva comum de recursos. [Contrato herdado](reachable_diagnosis.md) ·
[Consequências da dominância](../results/program-family-proof.md)

## Duas construções separadas

### Oito coordenadas exatas para avaliar sufixos

Uma matriz fixa `O`, com oito linhas e 16 colunas, satisfaz identidades físicas
verificadas exatamente:

\[
O K_a=T_aO,\qquad E=UO,\qquad EK_M=JO,\qquad a\in\{D,R\}.
\]

O sufixo `w` passa a ser avaliado por `z(w)=O K_w g`. Acrescentar uma operação
à esquerda custa `z(aw)=T_a z(w)`, e a semente com manutenção tem resposta
`q(Mw)=Jz(w)`. Essa construção reduz o custo aritmético e também foi entregue
ao comparador. Ela utiliza coordenadas assinadas de avaliação; as matrizes
`T_a` podem ter coeficientes negativos. Sua dimensão não define uma ordem de
dominância nem uma memória física de oito estados.
[Implementação e certificado](../../cdka/suffix_features.py)

### Cones de contextos com horizonte finito

Para um horizonte K≥1, o certificado fornece famílias aninhadas de linhas
`C_0,...,C_(K-1)` contendo o contexto de manutenção. A implementação também
inclui as linhas de extração ordinária. Cada extensão satisfaz

\[
C_tT_a=L_{t,a}C_{t+1},\qquad L_{t,a}\ge0.
\]

No nível n, com `1≤n≤K`, a comparação usa `C_(K-n)`. Um único
sufixo retido precisa ser pelo menos tão bom quanto o descartado em todas
essas linhas. A identidade acima garante que acrescentar D ou R transporta
a comparação para o conjunto de contextos apropriado ao próximo nível.
Em K=0, o sufixo é a identidade e a cobertura externa compara diretamente I e M.

As combinações positivas pertencem à prova sobre os contextos. Cada
representante continua sendo uma palavra executável original. A recorrência
externa preserva a cobertura de programas completos usando os transportes
positivos de quatro coordenadas já estabelecidos e as novas sementes `M w`.
[Implementação](../../cdka/suffix_contexts.py) ·
[Induções de cobertura](../results/suffix-context-proof.md#3-nested-suffix-and-complete-program-covers)

A descoberta usa programação linear numérica para propor suportes. Cada
suporte aceito é reconstruído em racionais, com coeficientes não negativos e
igualdade exata da linha. Se a proposta falha, a descoberta conserva uma nova
linha. O verificador recebe apenas o certificado racional e verifica as
identidades, os limites de índices e cada substituição; funciona sem NumPy,
SciPy ou uma nova busca de fronteira.

A descoberta utiliza `scipy.optimize.linprog` com `method='highs'`, conforme
a [API oficial do SciPy 1.17](https://docs.scipy.org/doc/scipy-1.17.0/reference/optimize.linprog-highs.html).
As tolerâncias numéricas pertencem à proposta de suporte; a aceitação lógica
depende das igualdades racionais verificadas posteriormente.

## Redução verificada de trabalho

As contagens abaixo são do nível final. “Gerados” conta a união de todos os
candidatos de sufixo e dos candidatos externos, incluindo os descartados. Não
é a contagem dos representantes sobreviventes.

| K | Programas legais | Gerados pelo comparador com oito coordenadas | Gerados pelo novo método | Sufixos finais retidos | Programas finais retidos |
|---:|---:|---:|---:|---:|---:|
| 4 | 96 | 44 | 22 | 4 | 10 |
| 8 | 2.560 | 542 | 55 | 9 | 17 |
| 12 | 57.344 | 8.260 | 121 | 19 | 37 |
| 14 | 262.144 | 32.860 | 160 | 24 | 53 |

Em K=14, a última expansão de sufixos constrói 44 candidatos e conserva 24,
em vez de construir os 16.384 sufixos ordinários. O arquivo exato também
contabiliza todos os níveis intermediários, as linhas dos cones, o tamanho
dos certificados e os comprimentos dos racionais.
[Dados e certificados](../data/suffix-context-results.json)

O caso principal conserva os 384 valores da matriz anterior. Seu programa
minimax continua sendo **DRDDM**, com arrependimento
`0,0025321961178476887` e fidelidade mínima `0,8491834489516084`.
**DDDDM** continua sendo o programa maximin, com fidelidade mínima
`0,8500277369367224`. O limite conjunto de arrependimento `0,003` e fidelidade
`0,85` permanece inviável. [Caso principal](../data/suffix-context-results.json)

## Quando a construção compensa

Cada observação usou um processo novo. Ambos os métodos pagaram construção
física, preparação, codificação, descoberta das características exatas,
compilação, serialização, leitura e verificação dos certificados, consultas e
certificação das decisões. A versão contextual pagou também a importação de
NumPy/SciPy e a primeira inicialização do HiGHS dentro da compilação
temporizada. Nenhum cone previamente descoberto entrou nas medições.
A inicialização do interpretador e as importações comuns de módulos Python e
do projeto ficam fora dos dois temporizadores. A exportação opcional do cache
de respostas é medida separadamente e não integra o total da decisão solicitada.

| Preparações | K | Comparador: mediana completa | Contextos: mediana completa | Razão comparador/contextos |
|---:|---:|---:|---:|---:|
| 4 | 4 | 0,1560 s | 0,6854 s | 0,228 |
| 16 | 8 | 0,4385 s | 1,1747 s | 0,373 |
| 16 | 12 | 3,6523 s | 2,6758 s | 1,365 |
| 16 | 14 | 16,1921 s | 4,3270 s | 3,742 |

São três repetições por método e caso, alternando a ordem. A soma das medianas
dos componentes, registrada separadamente, dá razões 0,228, 0,377, 1,304 e
3,837. Essa segunda estatística não é a mediana de uma execução completa. Os
dados incluem todas as amostras. O resultado autoriza adoção nos casos maiores
demonstrados e preserva o comparador direto nos pequenos medidos; não estima
um ponto de cruzamento universal. [Protocolo e amostras](../data/suffix-context-benchmark.json)

Há um custo adverso explícito: em K=14 o certificado cresce de **71.505 para
796.063 bytes**. O maior numerador ou denominador do certificado contextual
tem 1.646 bits. O cache da fronteira de respostas permanece com 49.657 bytes
nos dois métodos. Essas são medidas de serialização, sem afirmação sobre pico
de memória residente.

Os horizontes maiores também impõem mais trabalho físico. Para 16 preparações,
a fidelidade mínima do programa minimax cai de `0,8005053` em K=8 para
`0,7599289` em K=14. O ganho registrado é no custo de resolver exatamente a
decisão declarada; a qualidade absoluta permanece exposta em todos os casos.
[Qualidade e custos](../data/suffix-context-results.json)

## Falhas preservadas como informação

**Ordem insuficiente.** `RDDRRD` domina `RDRDDR` na representação original de
quatro coordenadas. Após a preparação fisicamente alcançável `D^32`, acrescentar
M à esquerda reverte a preferência. A diferença passa de aproximadamente
`+3,65648e-6` para `-1,57748e-7`. Esse caso impede reutilizar a ordem original
através de M. [Controle exato](../data/suffix-context-controls.json)

**Exigência excessiva.** Uma ordem contextual válida para todos os horizontes
força igualdade das duas respostas de contraste do substrato degradado. A
prova usa identidades espectrais e limites exatos. Há 67 pares distintos em
K=8 e 272 em K=12, contra 9 e 19 sufixos retidos pela ordem finita. É um limite
para essa garantia universal, sem resultado de impossibilidade para toda
forma de poda. [Obstrução demonstrada](../results/suffix-context-proof.md#an-all-horizon-context-cone-forces-two-equalities)

**Certificado incompleto.** O primeiro verificador exploratório aceitava um
cone vazio porque iterava sobre uma lista truncada de testemunhas. As
comparações se tornavam verdadeiras por vacuidade e MR perdia cobertura. O
verificador final exige todas as identidades e rejeita esse ataque. O teste
permanece no repositório. [Regressões](../../tests/test_suffix_contexts.py)

**Aproximação que pouco comprime.** A rota de erro uniforme por seminorma de
amplitude preservava 256 de 256 sufixos em K=8 com tolerância `1e-4`, e 1.023
de 1.024 em K=10. Seus controles, inclusive os resultados desfavoráveis,
foram mantidos; seus tempos exploratórios não entram no benchmark central.
[Rota rejeitada](../results/suffix-span-control.md)

## Alcance e próxima obrigação

A prova cobre um representante comum e as decisões declaradas. Empates
completos, envelopes de previsão e objetivos adicionais de custo físico
precisam de outra garantia. O número de linhas de contexto, a fronteira e os
bits racionais podem crescer; não há limite polinomial demonstrado. A
enumeração das `2^h` preparações permanece explícita.

A próxima obrigação registrada é certificar famílias de preparações sob o
mesmo contrato. A saída desse futuro teste deverá ser compacta — decisão,
valores e testemunhas atingentes — porque listar um valor informado para cada
uma das `2^h` histórias já impõe esse custo de saída. A correlação entre o
programa e seu comparador deverá ser preservada em cada testemunha.
[Integração e decisão seguinte](../strategy/suffix-context-integration.md)

## Reprodução

Verificação congelada, sem pacotes externos e com assertions desativadas:

```bash
python -S -O -m experiments.suffix_context_sweep --check
python -S -O -m experiments.suffix_context_controls
python -S -O -m unittest tests.test_suffix_features tests.test_suffix_contexts
```

Descoberta e medição completas usam as dependências opcionais registradas:

```bash
python -m pip install -r requirements-suffix-discovery.txt
python -m experiments.suffix_context_sweep --write --check
python -m experiments.suffix_context_sweep --benchmark
```

A biblioteca congelada armazena uma única sequência de cones até K=14 e
reconstrói certificados autocontidos para cada horizonte. O benchmark descobre
o cone de cada caso dentro de seu próprio processo. Alterar operadores,
terminal ou horizonte exige as verificações e vinculações correspondentes.
