# Núcleo do manuscrito: interfaces de continuação realizáveis e renováveis

**5 de novembro de 2026.** Formulação de integração após o certificado de
preparações e a incorporação do v17 canônico. Este é um núcleo de manuscrito
com dependências explícitas; a auditoria de prioridade do enunciado unificado
permanece aberta. As provas, implementações e contraexemplos citados já têm
seus próprios contratos e evidências.

## Tese e pergunta delimitada

Uma organização conserva conhecimento operacional quando as distinções que
usa continuam suficientes para suas continuações, atravessam os mecanismos
físicos permitidos e chegam ao decisor pelos canais efetivamente disponíveis.
Quando sua atuação altera as condições estatísticas da informação, a validade
da interface precisa ser demonstrada de novo ou restaurada por uma operação
real de aquisição.

O manuscrito deve tornar verificáveis três obrigações: **decidir uma ação
comum**, **realizar as condições dessa decisão** e **identificar quando uma
mudança invalida a interface usada na prova**. Seu domínio é finito e
contratual. A tese não presume inteligência universal, sobrevivência infinita
ou uma equivalência geral entre agência e uma grandeza termodinâmica.

## 1. Contrato mínimo

Fixar um espaço físico finito S, leis de preparação admissíveis, operações
físicas, observações realmente acessíveis, recursos por trajetória, horizonte,
tarefa e uma biblioteca finita não vazia L de programas completos. Saúde, restauração
e outras causas ocultas permanecem na lei conjunta, sem acesso gratuito.

Cada p em L deve ser realizável por um mesmo controlador em toda a classe de
preparações. Se recursos remanescentes mudam sua viabilidade, esse estado de
capacidade deve integrar a representação ou determinar famílias tipadas.
O avaliador não pode substituir essa obrigação por ações ótimas escolhidas
separadamente em estados ocultos.

Uma interface de valores é um mapa de preparação para x, com respostas r_p
tais que, no domínio declarado,

\[
V_x(p)=c+xr_p.
\]

A constante c é conhecida e comum no contrato. Essa interface pode bastar
para a tarefa sem reconstruir a lei física completa. Sua computação offline
não cria uma memória legível ou um observador físico dentro do controlador.

## 2. Proposição central: cobertura que conserva uma decisão comum

Sejam X um conjunto não vazio de assinaturas de preparações admissíveis,
Q um subconjunto finito não vazio de X com histórias físicas testemunhas e
F um subconjunto da biblioteca finita não vazia L de programas completos
originais. Suponha:

1. `conv(Q)=conv(X)`, por identidades exatas de cobertura de preparações.
2. Para cada p em L, existe f em F com `V_x(f)>=V_x(p)` para todo x em X.
3. A física, as respostas, as duas coberturas e a viabilidade comum são
   verificadas sob o mesmo contrato.

Então calcular sobre Q e F preserva o valor minimax de arrependimento, o
valor maximin de fidelidade e a existência de pelo menos um programa comum que satisfaça
simultaneamente um teto de arrependimento e um piso de fidelidade sobre X e L.
Os extremos por programa retido admitem testemunhas em Q.

**Demonstração.** Para p fixo, V_x(p) é afim, logo seu mínimo sobre X é o
mínimo sobre Q. Para p,q fixos, a diferença `V_x(q)-V_x(p)` também é afim.
Comutar os máximos sobre x e q preserva o pior arrependimento ao substituir
X por Q. A dominância por um f original conserva o máximo informado em cada
x, não aumenta arrependimento e não diminui fidelidade. Como F é subconjunto
de L, as duas inclusões dão igualdade dos ótimos e equivalência da
viabilidade conjunta. A cobertura de preparações é propagada pela indução
dos filhos físicos; a dos programas, pela gramática e pelas identidades de
contexto. As verificações e os limites completos estão nas provas citadas.

[Preparações e composição](../results/preparation-family-proof.md) ·
[Programas completos](../results/program-family-proof.md) ·
[Contextos finitos](../results/suffix-context-proof.md)

O resultado não depende de interpolar `max_p V_x(p)`, que em geral não é
afim. Tampouco uma única história de pior caso certifica optimalidade global.
O programa escolhido e seu comparador usam a mesma preparação; todos os
candidatos restantes precisam de limites suficientes.

## 3. Uma realização renovável tem uma obrigação diferente

Uma representação estocástica de leis completas exige mais que a interface
de valores acima. Seja E uma matriz estocástica que emite estados físicos a
partir de fases do avaliador. Se cada kernel físico admitido satisfaz

\[
K_a=A_aE,\qquad M_a=EA_a,
\]

com A_a substocástica, então `E K_a=M_a E`. Para uma lei inicial `mu=lambda E`,
com lambda uma submedida não negativa nas fases, qualquer composição admitida
conserva essa família e sua massa de falha:

\[
\mu K_{a_1}\cdots K_{a_n}
=\lambda M_{a_1}\cdots M_{a_n}E.
\]

Essa é a realização de emissão fresca do v16. Renovar o diagnóstico no fim
do ciclo estabelece a distribuição condicional necessária à fatoração.
As fases continuam ocultas e pertencem ao avaliador.
[Realização recorrente](../results/T4Q-recurrent-maintenance-loop.md)

O v17 muda uma premissa: permite reter os bits. A própria seleção por ações,
saldo e sobrevivência repondera os registros. No testemunho, as palavras 011
e 101 terminam com massas diferentes, embora toda mistura das emissões
antigas lhes atribua massas iguais. O fenômeno permanece com saúde estática;
há também um testemunho por suporte com seletor sem erro. Assim, aquela
família de emissão deixa de ser fechada.

Uma redução física por simetria com 48 estados continua válida para os 64
programas ampliados. Isso demonstra uma construção suficiente. **Não prova
minimalidade de 48 nem impossibilidade de toda interface de valores com doze
dimensões.** A falha de uma família particular de leis não equivale a um limite
inferior geral de representação da tarefa.
[Renovação, seleção e contraexemplos](../results/T4R-renewal-and-selected-memory.md)

## 4. Mapa das dependências e do que cada peça demonstra

| Peça | Obrigação que resolve | Limite que deve acompanhá-la |
|---|---|---|
| Realização de programas e atualização física | Uma tabela abstrata precisa de seletor, memória, execução e recursos | Um avaliador exato não instala esses mecanismos |
| Contraste alcançável de quatro coordenadas | Suficiência de valores no domínio da aquisição e das histórias D/R | Não é quociente de quatro estados; M pode sair do domínio |
| Coberturas de preparações e programas | Uma decisão comum e seus limites sobre duas famílias não enumeradas | Não preserva todas as identidades empatadas nem reduz custos físicos automaticamente |
| Emissão fresca v16 | Uma família de leis fecha sob os kernels admitidos | Doze fases de avaliação não são doze observações disponíveis |
| Retenção selecionada v17 | Uma mudança de gramática invalida a família de emissão antiga | Não é uma impossibilidade para todas as representações de mesma dimensão |
| Quociente físico v17 de 48 estados | Uma redução suficiente sobrevive à gramática ampliada | Não há prova de minimalidade ou de memória material concedida ao agente |
| Comparação completa de custos | Descobrir e verificar o certificado pode compensar em um regime | Prova maior, casos adversos e ausência de vantagem residente permanecem |

O exemplo numérico de fidelidade usa 16 estados físicos e uma fonte oculta.
O exemplo recorrente usa 64 estados vivos e sobrevivência sob recursos.
Nenhuma dimensão, porcentagem ou comparação deve atravessar esses contratos
sem uma tradução demonstrada.

## 5. Unidade mínima do manuscrito e critério de conclusão

O corpo principal precisa de um contrato, da proposição de decisão comum,
de uma realização física positiva e de um contraexemplo à reutilização
indevida de sua interface. Os compiladores e suas medições podem sustentar
um apêndice construtivo; o corpus inteiro não precisa virar uma coleção de
modelos dentro do mesmo texto.

A auditoria seguinte deve verificar a proposição contra cada hipótese das
provas existentes, localizar os antecedentes primários mais próximos e
separar instrumentos gerais, acoplamentos implementados e adaptações úteis.
O critério de conclusão é um enunciado preciso, uma cadeia de dependências
sem passagem gratuita entre contratos e um caso mínimo que o torne útil ou
refutável. A prioridade histórica é avaliada sobre esse enunciado.

Só depois se amplia o mecanismo de aquisição seletiva. Seu seletor precisa
usar evidência e memória física disponíveis, ter seus custos e falhas
contabilizados e enfrentar o melhor programa estacionário completo. O
controle v17 de preços iguais continua como referência; não se alteram os
preços para produzir artificialmente uma vantagem.
