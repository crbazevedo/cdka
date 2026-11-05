# Núcleo do manuscrito: interfaces de continuação realizáveis e renováveis

**5 de novembro de 2026.** Núcleo consolidado pela auditoria formal, de
mecanismos e de antecedentes identificados. O
[manuscrito com exemplo exato](../articles/core_interfaces.md) é agora a
exposição principal. O fechamento desta etapa é relativo às fontes
efetivamente consultadas: oito obras em passagens do texto integral e três
registros/resumos com acesso limitado. Prioridade histórica global permanece
aberta. A auditoria não ampliou o simulador físico recorrente; o resultado
v18 que chegou independentemente ao main durante a publicação foi integrado
com sua proveniência e altera a próxima obrigação, como registrado abaixo.

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
3. As respostas e as duas coberturas são verificadas a partir das leis e
   kernels fornecidos. Aquisição, observações, mecanismos e viabilidade comum
   são premissas do mesmo contrato, auditadas separadamente; o certificado
   algébrico não demonstra implementação de hardware.

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

## 3. Fechamento de leis, seleção e regeneração têm obrigações distintas

Uma representação estocástica de leis completas exige mais que a interface
de valores acima. Seja E uma matriz estocástica que emite estados físicos a
partir de fases do avaliador. Para uma gramática de palavras fixas,
a condição mais fraca

\[
E K_a=M_a E
\]

com M_a substocástica já basta. Para uma lei inicial `mu=lambda E`,
com lambda uma submedida não negativa nas fases, qualquer composição admitida
conserva essa família e sua massa de falha:

\[
\mu K_{a_1}\cdots K_{a_n}
=\lambda M_{a_1}\cdots M_{a_n}E.
\]

Uma seleção dependente de estado, `K_pi=sum_a D_a K_a`, exige verificar
primeiro essa decomposição como lei conjunta física. Fechamento por
primitiva não basta. Uma condição suficiente adicional é
`E D_a=Dhat_a E`, com máscaras diagonais não negativas que somam a
identidade em seus respectivos espaços. Então
`E K_pi=(sum_a Dhat_a M_a)E`.

A hipótese de regeneração `K_a=A_a E` é mais forte que o entrelaçamento.
Com A_a substocástica, qualquer seleção fisicamente verificada satisfaz
`K_pi=(sum_a D_a A_a)E`, mesmo sem compatibilidade das máscaras. O v16
realiza essa estrutura pela emissão fresca ao fim do ciclo. As fases
continuam ocultas e pertencem ao avaliador. Regeneração na saída não garante
que uma assinatura antiga da entrada determine os novos pesos de fase.
[Realização recorrente](../results/T4Q-recurrent-maintenance-loop.md)

O novo exemplo de três estados distingue todas essas obrigações. Um escalar
afim conserva os valores de todas as palavras fixas da gramática anterior;
uma seleção entre identidade e permutação rompe a família de leis. Uma nova
escolha condicionada entre dois kernels regeneradores preserva a emissão na
saída, mas separa duas entradas com o mesmo escalar antigo. Reutilizar o
decodificador fresco nessas entradas produz uma garantia falsa de decisão.
O teste usa uma etapa restante, preparações com o mesmo recurso e todas as
quatro políticas determinísticas do seletor binário. Dar duas etapas ou uma
moeda adicional muda os resultados, como mostram controles exatos.
[Auditoria e critérios](../results/core-formal-audit.md) ·
[Testemunho](../data/core-interface-witness.json)

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
| Caso analítico de três estados | Distingue fechamento por operação, compatibilidade do seletor e regeneração de saída | Uma etapa determinística; ampliar prazo ou randomização muda o problema |
| Emissão fresca v16 | Uma família de leis fecha sob os kernels admitidos | Doze fases de avaliação não são doze observações disponíveis |
| Retenção selecionada v17 | Uma mudança de gramática invalida a família de emissão antiga | Não é uma impossibilidade para todas as representações de mesma dimensão |
| Quociente físico v17 de 48 estados | Uma redução suficiente sobrevive à gramática ampliada | Não há prova de minimalidade ou de memória material concedida ao agente |
| Comparação completa de custos | Descobrir e verificar o certificado pode compensar em um regime | Prova maior, casos adversos e ausência de vantagem residente permanecem |

O exemplo numérico de fidelidade usa 16 estados físicos e uma fonte oculta.
O exemplo recorrente usa 64 estados vivos e sobrevivência sob recursos.
Nenhuma dimensão, porcentagem ou comparação deve atravessar esses contratos
sem uma tradução demonstrada.

## 5. Etapa concluída e próxima obrigação

O manuscrito agora contém contrato, critérios de seleção e regeneração,
exemplo de garantia falsa, proposição de decisão comum e aplicação v17.
As auditorias separam instrumentos estabelecidos, corolários demonstrados,
adaptações executadas e alegações ainda abertas. Os dois resumos próximos de
Murray já incluem suficiência de ação e fechamento recursivo; seus textos
integrais não foram obtidos. Essa limitação impede uma auditoria completa de
prioridade e permanece registrada, sem bloquear a verificação interna.

[Instrumentos matemáticos](../results/core-mathematical-antecedents.md) ·
[Mecanismos e manutenção](../results/core-realization-antecedents.md) ·
[Escopo e acesso às fontes](../results/core-scope-antecedents.md)

O passo de aquisição seletiva paga e falível foi executado independentemente
no main v18, commit `c8eb621acf04c6581795662596c3c41cf2cac43c`, enquanto a
auditoria era publicada. A seleção NAND usa comando de serviço e saldo
prévio; seu kernel mantém os ramos conjuntos. A omissão ideal preserva a
tarefa por `D 1=D Q=D T=0`, sem conservar necessariamente a memória terminal.
A prova vale em cada um dos 16 programas basais com as continuações e
transições de recursos fixadas. Ruído simétrico positivo tem um certificado
distinto de tolerância finita; preços de aquisição pertencem a uma
contabilidade esperada separada do saldo operacional.

[Resultado v18](../results/T4S-priced-selective-acquisition.md) ·
[Direção atual](direction-v18.md)

**Próxima obrigação:** unir aquisição e atuação em um orçamento por trajetória
e realizar a seleção com recursos físicos compartilhados. Derivar novamente
o kernel e o sucessor de recursos: devolver o token economizado já invalida
a antiga igualdade porque permite usar o registro antes de renová-lo. Uma
cobertura de custo/sobrevivência deve certificar ambas as respostas e a
dominância adequada; dominância apenas de sobrevivência não preserva aquela
fronteira automaticamente. Comparar políticas completas com as melhores
referências, incluindo não instalar e não renovar. Conservar uma família
de saída continua sem autorizar uma decisão a partir de entrada insuficiente.
