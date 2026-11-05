# CA — Quando a seleção muda o que uma representação precisa conservar

**Estado científico:** corolários demonstrados de instrumentos clássicos,
exemplo construtivo exato e integração auditada. Prioridade histórica da
combinação não estabelecida. **Data:** 5 de novembro de 2026.

**Pergunta:** uma representação válida para todas as sequências de operações
continua válida quando o sistema pode escolher essas operações usando uma
distinção que a representação descartou?

O exemplo deste artigo responde negativamente e mostra uma garantia de
decisão que se torna falsa. Dois critérios suficientes identificam caminhos
positivos: compatibilidade entre seletor e emissão, ou regeneração comum
ao final das operações. O segundo restaura a família de saída, mas não torna
automaticamente suficiente uma representação antiga da entrada.

[Laboratório interativo](../lab/core_interfaces.html) ·
[Auditoria formal](../results/core-formal-audit.md) ·
[Evidência exata](../data/core-interface-witness.json)

## 1. Motivação: conservar as condições de uso da informação

O programa CDKA investiga quais distinções permitem uma continuação
operacionalmente adequada e como os mecanismos que usam essas distinções
afetam sua validade futura. A integração atual precisa separar três objetos:
valores de tarefas, leis de estados e mecanismos acessíveis ao controlador.
Uma redução pode ser exata para um deles sem realizar os outros.

O resultado de preparação/programas certificou decisões comuns sobre duas
famílias grandes usando representantes efetivos. O modelo recorrente mostrou
que registros perfeitamente retidos podem sair da família estatística criada
pela aquisição fresca. Faltava um caso pequeno que explicitasse a passagem
entre escolha, representação e renovação. Esse é o papel do exemplo a seguir.

## 2. Definições mínimas e contrato

Leis são vetores linha. Um kernel físico `K` tem entradas não negativas e
somas de linhas no máximo um; massa ausente representa falha quando esse
contrato se aplica. O estado inclui causas persistentes relevantes, memória
e recursos. Programas completos incorporam as observações efetivamente
permitidas e as regras de seleção; o avaliador não concede sinais adicionais.

| Símbolo | Significado | Dimensão ou domínio |
|---|---|---|
| `S`, `mu` | Estados físicos e lei de preparação | `n` estados; submedida não negativa |
| `K_a` | Operação física, incluindo o que o contrato cobra | `n × n`, substocástica |
| `g` | Sonda terminal da tarefa | Coluna de `n` valores |
| `x`, `r_p` | Assinatura da preparação e resposta de um programa | `V_x(p)=c+x r_p` no domínio certificado |
| `E` | Emissão de fases do avaliador para estados físicos | `m × n`, estocástica |
| `M_a` | Evolução das fases para uma operação | `m × m`, substocástica |
| `D_a` | Probabilidades de seleção por estado | Diagonal não negativa; `sum_a D_a=I` |

O exemplo analítico tem três estados, massa unitária, tarefa terminal binária
e políticas determinísticas de seleção. As duas preparações usam uma etapa
igualmente cobrada ou preenchida e deixam o mesmo orçamento: **uma única
operação de continuação até o prazo terminal**. A nova escolha condicionada
usa a observação declarada `O=(0,1,0)`, sem implementação de portas ou ruído
do seletor. Uma moeda adicional para randomizar entre políticas não integra
esse contrato. As aplicações físicas posteriores mantêm seus próprios
contratos de custo e observação.

## 3. Três obrigações de suficiência

**Valores.** Para uma gramática fixa de programas, uma assinatura pode
determinar `mu K_p g` sem determinar `mu K_p`. Na formulação linear,
preservar o espaço gerado pelas respostas das continuações resolve essa
obrigação. Um escalar afim com massa conhecida não é a mesma contagem que
uma representação linear homogênea com uma coordenada de massa.

**Leis.** Para emissões estocásticas, a condição

\[
E K_a=M_a E,\qquad \mu=\lambda E
\tag{1}
\]

com a mesma E para cada operação admitida e uma submedida de fases
`lambda>=0`, `lambda 1<=1`, implica, por multiplicação, para toda palavra
fixa admitida,

\[
\mu K_{a_1}\cdots K_{a_t}
=\lambda M_{a_1}\cdots M_{a_t}E.
\tag{2}
\]

Como `E` preserva massa, a reconstrução inclui a massa viva quando os
kernels são substocásticos. Aplicar a sonda `g` fornece também valores
exatos. A implicação inversa não vale em geral. O entrelaçamento em (1) é
um instrumento estabelecido [S4].

**Realização.** A existência dessas coordenadas no avaliador não instala
um observador, memória ou seletor no sistema. A lei inicial, o kernel
conjunto, o acesso à observação e a viabilidade por trajetória continuam
obrigações do modelo. O verificador algébrico parte dos dados fornecidos;
metadados ou hashes de um contrato não demonstram sua adequação física.

## 4. A seleção exige uma condição adicional

Considere uma seleção fisicamente verificada com kernel

\[
K_\pi=\sum_a D_a K_a.
\tag{3}
\]

Essa identidade é uma hipótese operacional: os `K_a` devem ser os kernels
apropriados após a seleção. Se ruído de seleção e execução compartilha uma
causa não representada, não se pode presumir a mistura em (3).

### 4.1. Corolário de compatibilidade do seletor

Além de (1), suponha que existam diagonais não negativas `Dhat_a`, de ordem
`m`, que somem a identidade e satisfaçam

\[
E D_a=\widehat D_a E.
\tag{4}
\]

Então

\[
E K_\pi
=\sum_a E D_aK_a
=\left(\sum_a\widehat D_aM_a\right)E.
\tag{5}
\]

A matriz entre parênteses é substocástica. A seleção conserva a família de
emissão sob essas condições suficientes. A identidade (4) exige que a
reponderação selecionadora dentro de cada emissão respeite sua forma.
Nenhuma necessidade geral é reivindicada para esse critério.

### 4.2. Corolário de regeneração comum

Uma hipótese mais forte sobre cada operação é

\[
K_a=A_aE,\qquad A_a\geq0,\quad A_a\mathbf1\leq\mathbf1.
\tag{6}
\]

Ela implica (1) com `M_a=E A_a`. Para qualquer seleção que satisfaça (3),

\[
K_\pi=\left(\sum_a D_aA_a\right)E.
\tag{7}
\]

A família de saída é restaurada mesmo se (4) falhar. Essa propriedade dá
uma função precisa à regeneração comum. Entretanto, os pesos de saída
`mu sum_a D_aA_a` ainda podem depender de distinções de entrada que uma
assinatura antiga apagou. A prova da saída não fornece essa informação.

## 5. Exemplo exato de três estados

Os estados são `A0`, `A1` e `B`. A tarefa aceita os dois estados A:

\[
g=(1,1,0)^\top,\qquad
e_A=(1/2,1/2,0),\quad e_B=(0,0,1),\quad
E=\begin{pmatrix}e_A\\e_B\end{pmatrix}.
\]

A assinatura antiga é `z=mu(A0)+mu(A1)-1/2`. A gramática anterior à nova
escolha condicionada admite palavras fixas sobre cinco operações:

| Operação | Linhas do kernel ou transformação |
|---|---|
| `I` | Identidade |
| `T` | Troca A0 e A1; conserva B |
| `C` | Primitiva opaca: envia A0 e A1 para A0; conserva B |
| `R` | Linhas `e_A, e_A, e_B` |
| `S` | Linhas `e_B, e_B, e_A` |

`I,T,C,R` conservam `g`; `S g=1-g`. Todas conservam massa. Portanto, para
qualquer comprimento, a resposta de uma palavra é `g` ou `1-g`, conforme
a paridade do número de `S`. Um escalar mais a massa conhecida basta para
todos os valores dessa gramática. O espaço linear de respostas tem dimensão
dois. A prova usa identidades, não uma extrapolação de enumeração limitada.

### 5.1. Valores podem sobreviver à falha da família de leis

`e_A C=(1,0,0)` preserva o valor de `g`, mas sai da família de emissões,
que sempre dá massas iguais a A0 e A1. As três leis `e_A,e_B,e_A C` são
linearmente independentes. Qualquer espaço linear de leis que contenha essas
três precisa de dimensão ao menos três; isso é uma cota local dessa
construção, não uma cota de memória física ou sobre outros modelos CDKA.

### 5.2. Operações isoladas podem fechar e sua seleção não fechar

Na subgramática `{I,T}`, `E I=E T=E`; toda palavra fixa preserva a família.
Defina

\[
D_0=\operatorname{diag}(1,0,1),\qquad
D_1=\operatorname{diag}(0,1,0).
\]

Selecionar `I` em A0/B e `T` em A1 produz
`D_0 I+D_1 T=C`. A família deixa de fechar. O seletor usa precisamente a
distinção interna entre A0 e A1 que a emissão misturava; (4) falha.
Esse caso e a gramática maior de valores têm escopos distintos: não se
afirma que `C` preservava anteriormente a família de leis.

### 5.3. Renovação na saída não conserta a decisão na entrada

Agora acrescente à biblioteca de uma etapa o programa observacional

\[
U=D_0S+D_1R
=\begin{pmatrix}e_B\\e_A\\e_A\end{pmatrix}.
\]

`U` satisfaz a regeneração comum de (7), e ele próprio preserva a família:
`E U=M_U E`, com linhas de `M_U` iguais a `(1/2,1/2)` e `(1,0)`.
A ampliação permite a nova escolha condicionada entre R e S. Isso não
equivale a declarar um sensor novo: C já era uma primitiva opaca permitida,
e sua decomposição acima não concedia liberdade para recombinar o seletor
com quaisquer outras operações. Não é um contraexemplo a uma
representação preditiva que já incluísse essas observações e políticas.

Da mesma aquisição `mu=(3/10,3/10,2/5)`, as histórias `I` e `C` produzem:

| Preparação real | Lei em `(A0,A1,B)` | `z` antigo | `V(R)` | `V(S)` | `V(U)` | Melhor entre R, S e U |
|---|---|---:|---:|---:|---:|---|
| `mu I` | `(3/10,3/10,2/5)` | `1/10` | `3/5` | `2/5` | `7/10` | `U` |
| `mu C` | `(3/5,0,2/5)` | `1/10` | `3/5` | `2/5` | `2/5` | `R` |

O seletor lê A1, cuja massa é `3/10` na primeira preparação e zero na
segunda. Esse fato altera o valor de `U`, embora ambas tenham o mesmo `z`.
Os pesos de emissão após `U` são `(7/10,3/10)` e `(2/5,3/5)`.

As quatro políticas determinísticas que mapeiam a observação binária para
R/S são R, S, U e `W=D_0R+D_1S`. W tem valores `(3/10,3/5)` e é dominada
por R nas duas preparações. A cobertura retém `{R,S,U}` e preserva a
decisão sobre a classe completa de quatro políticas. Para um único programa
comum, sem acesso gratuito à identidade da história, os resultados são:

| Programa | Pior arrependimento, com comparador na mesma preparação | Menor fidelidade |
|---|---:|---:|
| `R` | `1/10` | `3/5` |
| `S` | `3/10` | `2/5` |
| `U` | `1/5` | `2/5` |
| `W` — dominada por R | `2/5` | `3/10` |

As primitivas I, T e C também podem permanecer admitidas nessa etapa:
seus valores terminais igualam os de R para qualquer lei, e R as cobre.
Essa observação conserva a comparação com a gramática anterior sem supor
unicidade da identidade de um programa ótimo.

Logo, `R` é minimax e maximin nessa biblioteca determinística. Nenhum programa satisfaz
simultaneamente arrependimento no máximo `1/10` e fidelidade ao menos `2/3`.
Se um avaliador reconstruir indevidamente ambas as entradas pela emissão
fresca correspondente a `z`, atribuirá `7/10` a `U` nas duas histórias e
certificará falsamente a condição conjunta. A perda é operacional e aparece
em uma decisão concreta.

**Controles da fronteira.** Se o prazo permitir duas operações, `SU` vale
`4/5` nas duas preparações. Sobre as 16 palavras de duas etapas em
`{R,S,U,W}`, seu arrependimento é `1/20`, e a condição conjunta torna-se
viável. A dominância terminal de W por R não autoriza descartá-la dentro de
composições: `WU` vale `(17/20,7/10)` e altera o máximo informado. Se uma
moeda adicional permitir misturar U com probabilidade `1/3` e R com `2/3`,
os valores `19/30` e `8/15` dão arrependimento `1/15`, menor que o minimax
determinístico. Esses controles não pertencem ao contrato de uma etapa sem
randomização adicional. Eles impedem extrapolar o resultado para outra
classe de políticas ou outro orçamento. A insuficiência do escalar antigo
para avaliar U permanece a distinção estrutural.

## 6. Certificação de uma decisão comum sobre duas famílias

O exemplo testa a validade da interface. Uma vez estabelecida essa validade
para o contrato correto, a cobertura de preparações/programas resolve uma
obrigação diferente: reduzir a avaliação preservando a decisão comum.

Sejam `X` não vazio, `L` finita não vazia, `Q` finito não vazio contido em
`X`, e `F` contido em `L`. Todos os programas devem ser fisicamente viáveis
em toda a classe. Suponha `V_x(p)=c+x r_p`, `conv(Q)=conv(X)` com histórias
testemunhas reais, e

\[
\forall p\in L\;\exists f\in F\;\forall x\in X:
V_x(f)\geq V_x(p).
\tag{8}
\]

Defina `B(x)=max_{q in L}V_x(q)`, `Reg(p)=sup_{x in X}[B(x)-V_x(p)]`
e `Fid(p)=inf_{x in X}V_x(p)`. Então `Q,F` preservam o mínimo de `Reg`,
o máximo de `Fid` e a existência de programa que satisfaça qualquer teto de
arrependimento e piso de fidelidade simultâneos. Cada extremo de um programa
retido tem uma testemunha em `Q`.

**Prova.** `V_x(p)` e cada diferença `V_x(q)-V_x(p)` são afins. Seus
extremos sobre `X` são os extremos sobre `Q`. O máximo sobre a biblioteca
finita de comparadores comuta com o supremo sobre preparações. (8) preserva
`B`, não aumenta arrependimento e não diminui fidelidade ao trocar `p` por
seu representante. A inclusão `F subset L` dá as desigualdades inversas
para os ótimos e conserva a equivalência da condição conjunta.

Não há troca entre mínimo e máximo, nem interpolação do máximo informado,
que em geral é convexo e não afim. Uma testemunha de extremo não basta para
provar optimalidade: limites sobre todos os candidatos são necessários.
As identidades de cobertura são verificadas a partir dos kernels fornecidos;
aquisição, acesso e implementação permanecem premissas auditadas do modelo.
[Prova composta](../results/preparation-family-proof.md).

## 7. Aplicação física e separação dos contratos

O modelo recorrente v16 usa aquisição fresca para obter a fatoração de
regeneração. O v17 permite reter os registros. A seleção por ação, saldo e
sobrevivência repondera os registros e invalida a família antiga: 011 e 101
podem ter massas distintas, enquanto toda emissão antiga lhes dava massas
iguais. Isso também ocorre com saúde estática. Uma simetria residual fornece
um quociente suficiente de 48 estados para os 64 programas considerados.
[Resultado físico v17](../results/T4R-renewal-and-selected-memory.md).

O banco de seis NAND participa da seleção por votação/inversão e do
trabalho, com sorteios novos de falhas condicionados à saúde persistente.
O controlador lê células e saldo; a regra de aquisição lê o comando
executado. Saúde e sucesso da restauração permanecem ocultos. Guarda,
roteamento, comandos constantes e tabela de aquisição conservam
idealizações. Trata-se de um modelo de circuito implementado em software.

A comparação de oito ciclos dá uma diferença renovar–reter de 2,1601588
pontos percentuais com roteamento fixo e de 0,5945024 ponto após reotimizar
cada regra. Preço igual por operação não iguala o gasto total esperado.
Essas são medidas de sobrevivência do modelo de 64 estados vivos; não são
as fidelidades do compilador separado de 16 estados. A família antiga falhar
não prova impossibilidade de toda interface de valores com doze dimensões,
nem minimalidade do quociente de 48 estados.
[Auditoria do mecanismo](../results/core-realization-antecedents.md).

### Integração durante a publicação: omissão seletiva v18

Enquanto esta auditoria era concluída, o main avançou independentemente para
`c8eb621acf04c6581795662596c3c41cf2cac43c`. Seu
[resultado v18](../results/T4S-priced-selective-acquisition.md) executa o
seletor de aquisição que estava preparado como próximo passo. A integração
preserva seus arquivos e sua proveniência; não o apresenta como um
experimento novo desta auditoria.

O novo circuito de habilitação lê apenas serviço executado e saldo prévio
igual a três. Uma NAND ideal omite a escrita após serviço nesse saldo, pois
o ramo bem-sucedido termina com saldo dois. A continuação é então forçada a
pular a manutenção e renova o diagnóstico antes de voltar a usá-lo. Para o
kernel Q de renovação e o kernel T de omissão, `D=T-Q` satisfaz
`D 1=0`, `D Q=0` e `D T=0`. Isso conserva sobrevivência para todos os
horizontes e medidas iniciais, em cada um dos 16 programas basais. A memória
terminal pode diferir. É equivalência para as continuações da tarefa, sem
alegação de igualdade de leis ou regeneração comum em toda etapa.

O kernel é construído por ramos conjuntos condicionados ao comando executado.
Substituí-lo por uma probabilidade marginal de escrita multiplicada por
kernels incondicionais perderia dependências entre serviço, saúde e saldo.
Esse mecanismo exemplifica a obrigação de lei conjunta da seção 4.

A NAND de habilitação é separada do banco de seis portas e tem falhas novas
com taxa fixa gamma. Com gamma positivo, omissões em outros contextos podem
ser prejudiciais; a garantia ideal para todo horizonte não se transfere.
O v18 oferece então certificados finitos de tolerância e uma síntese
delimitada que inclui não instalar o circuito e não renovar o diagnóstico.

Sua economia ideal de 6,08455% usa preços ilustrativos de escrita, invocação
e instalação em uma **contabilidade esperada separada** do saldo operacional.
Ela não é economia de energia medida nem garantia de gasto por trajetória.
A cobertura escalar da seção 6 não preserva automaticamente uma fronteira
de sobrevivência e custo: um representante precisaria também não aumentar
o custo em todo o mesmo domínio, com ambas as respostas certificadas.

Um controle devolve um token por aquisição omitida: a próxima decisão muda,
e a igualdade antiga deixa de valer. A representação necessária depende,
portanto, também das continuações abertas pelo recurso economizado.
Certas distinções podem deixar de ser atualizadas com segurança quando a
organização garante sua substituição antes de qualquer uso relevante. O
próximo teste deve verificar essa garantia quando a economia altera a
própria continuação. [Direção canônica v18](../strategy/direction-v18.md).

## 8. Antecedentes, contribuição e limites

O núcleo utiliza fechamento de respostas de continuação [S1], distinções
entre preservação de modelo e valor [S2], compatibilidade de quocientes
[S3], entrelaçamento [S4], comparações afins de arrependimento [S5] e
controladores sob observação parcial [J]. Os resumos de Murray já tratam
tanto de suficiência de ação quanto de fechamento recursivo [M1,M2].
Informação causalmente relevante à viabilidade também tem antecedente direto
[K]. A atribuição detalhada e os limites de acesso estão nas auditorias:

- [S1–S6: instrumentos matemáticos e fontes primárias](../results/core-mathematical-antecedents.md).
- [J,O: controladores e manutenção](../results/core-realization-antecedents.md).
- [M1,M2,K: suficiência, viabilidade e escopo](../results/core-scope-antecedents.md).

A contribuição aqui demonstrada é uma integração construtiva: explicitar a
obrigação de seleção, prover um exemplo exato com garantia falsa, ligar a
renovação à realização estocástica e compor certificados sob um contrato
operacional. A auditoria cobre oito obras em passagens relevantes do texto
integral, mais três registros/resumos com acesso limitado. Isso delimita
alegações; não estabelece prioridade global.

Os certificados anteriores têm ganhos medidos em regimes definidos e perdas
em casos menores; custam descoberta, aritmética e verificação, e podem ser
maiores que os dados enumerados. Essa eficiência computacional não é ganho
físico de fidelidade, capacidade do controlador ou medida de agência.
[Custos completos e controles](../strategy/preparation-family-integration.md).

## 9. Simulador e reprodutibilidade

O laboratório varia a massa inicial `a` em A, conservando a família
`(a/2,a/2,1-a)` e suas duas histórias. As respostas reais de `R,S,U` são
`(a,1-a,1-a/2)` na primeira e `(a,1-a,1-a)` na segunda. Mostra leis,
decisões e a reconstrução incorreta lado a lado. O controle não introduz
ruído ou novos recursos no circuito recorrente; é a visualização do caso
analítico. Nos extremos e empates, preserva todos os vencedores indicados.

O verificador usa frações exatas, identidades matriciais que provam fechamento
para todos os comprimentos e uma enumeração independente limitada como
controle. A visualização numérica ilustra o certificado e não substitui a
prova ou uma busca de prioridade.

```bash
python -S -O -m experiments.core_interface_witness --check
python -S -O -m unittest discover -s tests -p 'test_core_interface_witness.py' -v
node --test tests/core-interfaces-lab.test.mjs
```

Fontes: [experimento](../../experiments/core_interface_witness.py),
[testes exatos](../../tests/test_core_interface_witness.py),
[núcleo da visualização](../lab/core-interfaces.mjs) e
[registro de alegações](../../registry/core-audit-addendum.json).

## 10. O que habilita e próxima obrigação

Com o v18 integrado, a próxima obrigação é colocar aquisição e atuação em
um orçamento comum por trajetória e realizar a seleção com recursos físicos
compartilhados. O custo economizado passa a alterar o saldo que determina
as próximas decisões; o kernel conjunto e a suficiência de continuação
precisam ser derivados novamente. A comparação inclui a melhor política
completa admissível, renovação, retenção e ausência de circuito adicional.

Um resultado negativo permanece informativo: pode mostrar que o seletor
custa mais que o benefício, que a retenção exige uma distinção adicional ou
que a regeneração restaura a saída sem fornecer uma decisão suficiente na
entrada. Nenhuma dessas saídas autoriza mudar os preços ou conceder
observações ocultas para produzir uma vantagem.
