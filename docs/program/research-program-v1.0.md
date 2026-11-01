# Counterfactual Dynamics of Knowledge and Agency (CDKA)

**Programa de pesquisa v1.0 — 2026-11-01**  
**Status:** agenda científica e teoremas-candidatos; não é um artigo com resultados novos comprovados.  
**Continuidade:** parte dos cadernos CDKA v0.1 e v0.2, preservados separadamente.

## Resumo

Pergunta central: **sob quais condições uma organização física produz, utiliza e preserva distinções sobre as consequências de intervenções próprias, de tal maneira que se tornam possíveis conhecimento operacional, regulação eficaz e autonomia?**

A hipótese-guia não atribui teleologia à mecânica, nem equipara entropia, controle, informação e agência. Procuramos a interação entre: (a) leis de trajetórias fisicamente realizáveis; (b) intervenções e restrições dinâmicas de recursos; (c) representações internas e sua suficiência contrafactual; e (d) organização que mantém ou recupera percepção, memória e atuação.

A contribuição almejada é uma **teoria composicional e dinâmica da suficiência informacional para controle sob viabilidade e capacidades endogenamente mutáveis**. Sua originalidade, ainda não estabelecida, depende de provar resultados além de teoremas clássicos de teoria da informação, controle, viabilidade e estados causais.

## A. Contrato ontológico

1. **Dinâmica física:** conjunto de leis de trajetória, incluindo ruído e interações. Não é um agente.
2. **Possibilidade:** trajetória no suporte de alguma medida fisicamente realizável, sob condição inicial e horizonte definidos. **Probabilidade** não se confunde com possibilidade.
3. **Influência causal:** intervenções físicas distinguíveis produzem diferentes leis de consequências. Pode ocorrer sem sensores.
4. **Controle potencial:** existem políticas que alcançam ou preservam certas regiões; pressupõe autoridade física e recursos declarados, não necessariamente acesso epistêmico interno.
5. **Controle informado:** a organização realmente consegue escolher uma política adequada usando suas observações, memória e prazos disponíveis.
6. **Suficiência de decisão:** código que permite escolher alguma ação viável. Não requer um modelo verdadeiro de todas as alternativas.
7. **Conhecimento contrafactual operacional:** representação física que é correta para uma família declarada de leis interacionais e cujo uso altera causalmente a escolha de intervenções e seus resultados. Uma política aberta universal pode funcionar com zero bits de discriminação sem, por isso, possuir esse conhecimento.
8. **Viabilidade:** continuação de processos constitutivos de uma organização física escolhida e operacionalmente mensurável. O investigador deve justificar fronteira, escala e critério; isso não implica finalidade física universal.
9. **Autonomia operacional:** organização que regula interações e contribui causalmente para manter ou reconstruir os mecanismos materiais de percepção, memória, atuação e regulação, sob perturbações. É relativa ao horizonte, fronteira e recursos; não significa isolamento completo nem consciência.
10. **Agência mínima (candidata):** individuação organizacional, assimetria de interação, regulação internamente condicionada e contribuição para sua própria continuidade. Não pressupor um modelo explícito do futuro, recompensas externas, nem mente fenomenológica.

**Anti-circularidade:** intervenções `do(u)` são instrumentos experimentais do pesquisador. Na operação natural, `u` deve ser produzido pela dinâmica interna do subsistema, e não por um operador externo implicitamente embutido na definição.

## B. Sistema mínimo de investigação

Adotar inicialmente tempo discreto e espaços finitos: `S_t=(X_t,Z_t,R_t,M_t)`; `X`=ambiente e processo controlado; `Z`=estrutura material de sensores/atuadores e organização; `R`=recursos; `M`=memória interna. A observação `Y_t` obedece `O_{Z_t}(dy|S_t)`; uma ação física `U_t` obedece a `U_t∈A(Z_t,R_t)` e à política interna `π(du|M_t,Z_t,R_t)`; a dinâmica do conjunto usa kernel `P(ds'|s,u)`, inclusive atualizações endógenas de `Z`, `R` e `M`.

Fixar um horizonte `T`, uma fronteira experimental, um conjunto constitutivo observável `V⊂S` e tempo de saída `τ_V`. A viabilidade é `P^π(τ_V>T)`; prolongar a duração, o nível de garantia ou a classe de perturbações muda o problema.

**Espaço causal de trajetórias:**

`C_T(s) = { P_s^π(S_{0:T}∈·) : π∈Π_phys(s) }`.

Os elementos são medidas de trajetórias, não uma lista de futuros equiprováveis; `Π_phys` é limitado por física, disponibilidade de observações, latência, recursos e estrutura `Z`.

**Compatibilidade estática de ações:** dado um conjunto finito de contextos `W` e ações `A`, definir `R_{T,α}(w,a)=1{ P(τ_V>T | w, do(a), continuação admissível)≥1−α }`. Fixar explicitamente qual política de continuação está permitida. Definir `W_a={w:R(w,a)=1}`.

**Suficiência contrafactual:** para histórico `h`, política física `π` e futura lei de trajetórias `K_T(h,π)`, uma representação `m=q(h)` é suficiente para a família `Π` quando `K_T(h,π)=Khat_T(m,π)` para todos os pares e políticas em escopo. A versão aproximada pode usar `sup_{π∈Π} TV(K_T(h,π),Khat_T(m,π)) ≤ δ`. Não reivindicar novidade: há antecedentes em processos entrada–saída, representações preditivas e controle comprimido.

**Distintos custos:** (i) quantidade de memória ou informação mútua usada em distinções (bits); (ii) intervenção física e sua mudança na lei de trajetórias (energia, path-KL ou equivalente); (iii) orçamento de recursos que mantém sensores, memórias e atuadores. Não somar unidades diferentes sem conversões e multiplicadores bem definidos; preferir uma região de viabilidade multiobjetivo.

## C. Teoremas-baseline a reproduzir (conhecidos, não novos)

### B1. Cobertura e memória mínima de decisão

Sob `W` finito, ações finitas, observação perfeita no momento da decisão, memória determinística e sucesso sem erro, cada código `m` deve agrupar apenas estados que compartilhem uma ação segura. O menor número `k*` de códigos satisfaz

`k* = min {|B| : B⊆A, ∪_{a∈B}W_a=W}`.

**Prova:** uma política de `k` mensagens escolhe no máximo `k` ações, cujos conjuntos de sucesso necessariamente cobrem `W`; qualquer cobertura por `k` ações constrói um codificador atribuindo a cada estado uma ação viável da cobertura e um decodificador que a executa. Logo os ótimos coincidem. Armazenamento fixo de pior caso exige `ceil(log2 k*)` bits. **Isso NÃO implica que o ótimo de informação mútua seja `log2 k*`**, nem que exista conhecimento contrafactual. Antecedente direto: Murray 2026; relevante informação anterior: Polani, Fox/Tishby.

### B2. Incompatibilidade de ordem superior

Contextos A,B,C com ações viáveis `{1,2}`, `{2,3}`, `{1,3}`: cada par admite uma ação comum, mas a tripla não. A relação `R⊂W×A` induz o complexo de Dowker `D(R)={σ⊆W:∃a,∀w∈σ,R(w,a)}`. Grafos de conflitos pares não representam toda a estrutura. Antecedente matemático: Dowker.

### B3. Informação para distinguir decisões incompatíveis (Fano)

Se `W` contém `n` mundos equiprováveis com conjuntos de ações seguras mutuamente disjuntos, e uma política cujo único acesso a `W` vem do canal de observação `Y` escolhe com erro ≤δ, uma decodificação de `W` a partir da ação tem erro ≤δ. Para `δ≤1−1/n`, Fano e processamento de dados implicam:

`I(W;Y) ≥ I(W;U) ≥ log2(n)−h2(δ)−δ log2(n−1)`.

Se a memória é o único mediador `W→Y→M→U`, também `I(W;M)` satisfaz o limite inferior. É condição necessária, não suficiente. Para dois mundos igualmente prováveis e observação binária com erro `η`, o teste MAP falha com probabilidade mínima `η`, saturando Fano. É uma prova-base; não é nova.

### B4. Garantia uniforme de decisão por predição contrafactual

Se `sup_{π}TV(K_T(h,π),Khat_T(m,π))≤δ`, então toda consequência avaliada com payoff `[0,1]` tem erro de expectativa ≤δ para cada política. O regret da escolha ótima pelo modelo em relação à escolha ótima com histórico integral é ≤`2δ`, assumindo a **mesma classe de políticas admissíveis** e controle real da representação. Demonstração pela decomposição triangular de dois erros de avaliação e pela otimalidade da escolha aproximada. Baseline clássico.

### B5. Limite de energia para provocar um evento raro

Para difusão com ruído e controle nos mesmos canais, distribuições iniciais iguais e condições de Girsanov:

`dX_t=(f(X_t)+σ(X_t)u_t)dt+√ε σ(X_t)dW_t`,  
`KL(P^u||P^0)=(1/(2ε))E_{P^u}∫_0^T||u_t||²dt`.

Dado evento `E` e `p0=P^0(E)`, `q=P^u(E)`, processamento de dados pela projeção de trajetórias em `1_E` implica

`E_{P^u}∫||u||²dt ≥ 2ε d_Bern(q||p0)`

com `d_Bern(q||p)=q ln(q/p)+(1−q)ln((1−q)/(1−p))`. Se a meta é `q≥β>p0`, então a energia média é pelo menos `2ε d_Bern(β||p0)` (monotonicidade de KL Bernoulli nesse ramo). É uma consequência **conhecida** de Girsanov e processamento de dados, não uma lei geral de custo físico para todos os sistemas.

### B6. Não identificação da autonomia por trajetórias externas

Duas organizações podem produzir a mesma lei externa `P(X_{0:T})`, uma por realimentação interna e outra por reprodução externa da mesma política. Nenhuma estatística dessas trajetórias pode, em geral, diferenciar a fonte interna de controle. Intervenções nos mecanismos e testes fora de distribuição podem separar as arquiteturas. Prova construtiva simples; não é uma descoberta original.

## D. Teoremas-candidatos e hipóteses novas

### T1 — Lei de limiares de conhecimento de ação (prioridade alta; baixo risco)

**Caso determinístico exato:** `W={−1,+1}`, `A={−1,+1}`, `y=λw+a`, saída segura se `|y|≤3/2`, com `λ≥0`.

- `0≤λ≤1/2`: qualquer ação é segura em ambos os estados, logo `k*(λ)=1` e memória fixa mínima = 0 bits.
- `1/2<λ≤5/2`: apenas `a=−w` é segura; `k*(λ)=2` e 1 bit é necessário.
- `λ>5/2`: nenhuma ação é segura; não existe controle robusto dentro da classe de ações.

A lei física varia continuamente com `λ` e não inclui mudança de atratores, mas a memória requerida sofre salto. Os exemplos foram checados por enumeração (`CDKA_seed_checks_v1.py`). Trata-se de uma prova simples com valor pedagógico, **não um resultado novo suficiente para publicação**.

**Versão geral:** para `W,A` finitos e probabilidades de sucesso contínuas em `λ`, `k*(λ)` é localmente constante em todos os pontos nos quais nenhum par `(w,a)` está exatamente no limiar de viabilidade `1−α`. Prova: continuidade preserva sinais de um conjunto finito de desigualdades estritas num entorno; logo relação `R` não muda, tampouco sua cobertura ótima. **Salto informacional não implica bifurcação física.**

### T2 — Barreira-para-bits via grandes desvios (prioridade alta; risco médio)

Para cada contexto `w`, ação `a` e prazo `T`, suponha a existência do limite de grandes desvios para falha

`lim_{ε→0} −ε ln P_ε(falha até T|w,a) = J_T(w,a)`.

Escolha orçamento de falha `α_ε=e^{−c/ε}`, `c>0`. Quando `J_T(w,a)≠c`, a relação de viabilidade assintótica é `R_c(w,a)=1{J_T(w,a)>c}` para `ε` suficientemente pequeno. Com `W,A` finitos e margens estritas em todos os pares, a relação inteira se estabiliza; a memória mínima torna-se o número de cobertura dos conjuntos `W_a(c)={w:J_T(w,a)>c}`. A prova combina comparação de expoentes de grandes desvios e B1.

**Nota de originalidade:** isoladamente é um corolário direto de grandes desvios + cobertura. A fronteira de contribuição será demonstrar condições **uniformes, dinâmicas e endógenas**, com `J_T` dependente de `Z_t`, recursos, observação parcial, ação adaptativa e reparo. Testar diferenças entre limiares de ação/epistêmicos e bifurcações físicas.

### T3 — Limites conjuntos de diagnóstico, intervenção e sustentação (prioridade máxima; risco alto)

Almejamos um conjunto de políticas admissíveis por horizonte que satisfaça simultaneamente (i) orçamento de informação, (ii) orçamento de energia ou mudança na lei de trajetórias, (iii) evolução da capacidade `Z_t`/recursos, e (iv) garantia `P(τ_V>T)≥1−α`.

Definir região realizável `F_T={(B_I,B_U,B_R,α): existe controlador fisicamente implementável com esses orçamentos}`. Procurar cortes necessários (Fano, TV, Girsanov, robustez de viabilidade), condições suficientes em subclasses e casos de equivalência exata. O objeto **não deve** ser arbitrariamente escalarizado como um único 'custo de agência'.

**Critério de avanço:** obter um limite não redutível a Fano e Girsanov aplicados independentemente; isto exigirá que a manutenção endógena da capacidade interfira nas possibilidades e no custo das intervenções futuras.

### T4 — Fechamento recursivo de conhecimento de ação com capacidades endógenas (prioridade máxima; risco médio-alto)

Em um modelo finito parcialmente observado, considerar conjuntos de estados possíveis `B_t` (ou crenças `b_t` sob critérios probabilísticos) incluindo variáveis `Z,R`. Uma representação suficiente para escolher ação hoje não é necessariamente suficiente para a sequência futura. Construir um operador exato de viabilidade robusta `Safe_{t+1}` sobre estados de informação, sob ações comuns aos estados indistinguíveis, transições de observação e atualizações físicas da organização.

Procurar caracterização da **menor memória implementável** para viabilidade repetida e quando uma política de reparo torna possível um controlador antes inviável. Confrontar com POMDP, games de informação imperfeita, bisimulação, data-rate theorems, estados causais e viability kernels antes de reivindicar novidade.

### T5 — Critério causal de autonomia auto-sustentada (prioridade média; risco alto)

Uma arquitetura é candidata a autonomia operacional se (a) regula sua interação com o meio usando uma dinâmica internamente produzida; (b) sensores, atuadores e outras condições constitutivas são variáveis físicas do próprio modelo; (c) intervenções seletivas de lesão e reparo revelam contribuição causal dos mecanismos endógenos à recuperação de capacidade futura. Controle externo capaz de reproduzir a mesma trajetória nominal é contraste necessário, não prova de autonomia.

Almejar condições de identificabilidade de tal organização sob uma bateria declarada de intervenções. Restringir o enunciado às classes de mecanismos e fronteiras especificadas. **Não concluir que toda auto-reparação implica agência**, nem que o critério resolve consciência ou intencionalidade filosófica.

### T6 — Seleção replicadora como memória implementável (prioridade exploratória; risco alto)

Com frequências `p_i` de mecanismos, `dp_i/dt=p_i(F_i−Fbar)`, o log-ratio integra a diferença de fitness ao longo do passado: `d/dt log(p_i/p_j)=F_i−F_j`. Se `F_i` depende do ambiente, `p_t` carrega uma estatística física da história. Investigar condições nas quais `p_t` seja suficiente ou aproximadamente suficiente para escolher intervenções que preservam `Z,R`, em contraste com registros históricos sem uso causal. Acoplar `dp/dt`, `dX/dt` e `dZ/dt`. Evitar equiparar seleção à cognição; testar contra-casos.

## E. Programa experimental mínimo

**E0 — Enumeração finita e provas-baseline:** dois a seis estados, duas a seis ações, compatibilidade, complexos de Dowker, set cover, Fano. Resultado exigido: enumeração reproduz B1, B2 e T1; condições de falha explicitadas.

**E1 — Controle sequencial com sensores e memória:** contexto oculto, diagnóstico com erro e prazo, sensor que pode deixar de funcionar, memória custosa e ação reversível/irreversível. Comparar observabilidade perfeita, parcial, memória 0/1/2+ bits, políticas adaptativas. Resolver por DP exata quando possível. Medir `P(τ_V>T)` e custo de informação/latência.

**E2 — Paisagem bistável estocástica:** `dq_t=(q_t−q_t³+κu_t)dt+√(2D)dW_t`; atratores próximos de `±1` sem controle e ponto separador `0`. Estimar bacias, probabilidades de escape, custos de trajetórias e `J_T`; validar relação limiar-para-bits contra cálculo direto da probabilidade de falha. Comparar caminho mínimo/quasipotencial com Fokker–Planck, solução do problema de fronteira ou amostragem de eventos raros.

**E3 — Osciladores acoplados e organização:** `dφ/dt=Δω−K(Z_t)sin φ`; acoplar `φ` ao potencial de `q`; introduzir `Z_t` e orçamento `R_t` com física de reparo e degradação. Regimes contrastados: passivo, feedback reativo, memória, predição contrafactual, lesão de memória, replay externo e autorreparo. Mesmo orçamento inicial e perturbações comparáveis; separar fonte interna da ação de observação externa do comportamento.

**E4 — Replicador acoplado:** só se E0–E3 produzirem fenômeno robusto. População de mecanismos com taxas de crescimento fisicamente especificadas; variar velocidade de seleção versus controle e checar memória histórica, suficiência e robustez fora da distribuição.

**Métricas-base:** conjunto de leis acessíveis; separação causal entre ações; probabilidade de permanecer na região viável; tempo até perda de capacidade; memória de decisão e memória de previsão; path-KL/energia; custo de recuperação; desempenho sob lesão; divergência das leis sob intervenções estruturais; número de cobertura e feições simpliciais. Evitar condensar tudo em um 'agency score'.

**Controles negativos:** ruído imprevisível sem atuador, atuador sem observabilidade, acoplamento passivo sincronizado, preditor perfeito não conectado ao atuador, circuito de reparo sem discriminação informada, controlador potente que consome o próprio recurso, replay externo e distribuição alterada de perturbações.

## F. Roadmap com gates científicos

| Etapa | Janela proposta | Entrega objetiva | Gate de continuação |
|---|---|---|---|
| M0. Ontologia e anterioridade | Semana 1 | Glossário operacional, matriz comparativa de 12 antecedentes, catálogo de contraexemplos | Nenhuma definição essencial depende de recompensa ou propósito implícitos |
| M1. Modelo finito | Semanas 2–3 | B1–B4 demonstrados, suite exaustiva, T1 com prova e exemplos | Testes reproduzem casos-limite; definição de memória distingue cardinalidade, entropia e MI |
| M2. Geometria e grandes desvios | Semanas 4–6 | T2 enunciado/prova sob hipóteses declaradas, toy bistável, comparação analítica/numeric | Limiares preditos concordam com probabilidades exatas/estimadas, fora da zona assintótica ambígua |
| M3. Informação e controle sequencial | Semanas 7–9 | Bellman/belief-state, limites B5 e Fano, frentes de viabilidade, T3/T4 parcialmente provados ou refutados | Pelo menos um resultado substantivo usa capacidade variável, não apenas problema clássico com nomes trocados |
| M4. Autonomia dinâmica | Semanas 10–12 | Sensor/atuador degradáveis, reparo endógeno, testes lesion/replay, T5 revisado | Critérios discriminam mecanismos internos e externos sob experimentos pré-registrados |
| M5. Síntese e seleção | Semanas 13–14 | Nota formal enxuta com prova, limite de validade, benchmark e survey de novidade | Se sem novo teorema, publicar como síntese conceitual/benchmark, sem reivindicação forte |
| M6. Extensão replicadora | Depois do gate M5 | Modelo mínimo de seleção–organização–ambiente | Somente se adicionar poder explicativo e não virar um segundo projeto prematuro |

As semanas são **horizontes de planejamento**, não promessa de execução assíncrona. O gate lógico é mais importante que o calendário.

## G. Kit teórico-metodológico mínimo

**Indispensável agora:** relações finitas, cobertura de conjuntos/hipergrafos, conceitos elementares de informação (`H`, `I`, Fano, processamento de dados, variação total), processos Markovianos/POMDP e programação dinâmica, intervenções causais, controle robusto/viabilidade, análise elementar de atratores e bifurcações. Demonstrar resultados pequenos por prova manual e enumeração automatizada.

**Indispensável apenas na segunda fase:** difusões, Girsanov, ações de Freidlin–Wentzell e quasipotencial, métodos para eventos raros. Considerar estimação com incerteza e checagens de discretização.

**Posteriormente, se justificado:** teoria do replicador e geometria Fisher–Shahshahani, topologia computacional mais avançada, termodinâmica estocástica e identificabilidade causal de organizações fechadas.

**Não necessário para o primeiro resultado:** deep RL, LLMs, FEP universal, geometria categorial abstrata, otimização de centena de parâmetros, TDA persistente, grandes sistemas many-body ou interpretações de consciência. Essas ferramentas só entram quando uma hipótese demonstrar a necessidade.

**Ferramentas práticas:** Python 3.11+, biblioteca padrão para enumeração; NumPy/SciPy para matrizes e integrais; bibliotecas de grafos/otimização apenas se set cover crescer; controle de versão Git; testes unitários; notebooks de experimentação acompanhados de scripts reproduzíveis; ambiente versionado; seeds. Prover CIs numéricos, análise de discretização e evidência independente de Monte Carlo em eventos raros.

**Protocolo obrigatório de teoremas:** enunciado, quantificadores, hipóteses, domínio, exemplos positivos, contraexemplos, prova, teste por enumeração em casos finitos, auditoria de literatura e registro de novidade: `resultado conhecido`, `corolário`, `extensão candidata`, `teorema original verificado`, `refutado`.

## H. Critérios de falsificação e abandono

- Se diferenças propostas entre 'agência' e viabilidade forem indistinguíveis de simples realimentação ou de uma fronteira arbitrária, rebaixar a hipótese a propriedade relativa do modelo.
- Se T2 se reduzir integralmente a uma LDP + set cover sem extensão dinâmica, mantê-lo como lema instrumental, não como artigo novo.
- Se custo informacional, custo energético e custo de manutenção forem separáveis em toda a classe estudada, abandonar a hipótese de novo limite conjunto nessa classe.
- Se a topologia acrescentar apenas visualização, descartá-la do formalismo central; relações de compatibilidade bastam.
- Se não existirem observações/intervenções que discriminem os modelos endógeno e externo sob orçamento experimental, classificar autonomia como não identificável nesse protocolo.
- Se a equação do replicador não alterar propriedades regulatórias além da mera composição, não interpretar suas frequências como conhecimento.

## I. Cinco leituras de entrada e anterioridade adicional

**Core 5 (ordem estratégica):**

1. Roy Fox e Naftali Tishby, *Minimum-Information LQG Control, Part II* (2016) — https://royf.org/pub/Fox2016LQG2/
2. Artemy Kolchinsky e David Wolpert, *Semantic information, autonomous agency and non-equilibrium statistical physics* (2018) — https://doi.org/10.1098/rsfs.2018.0041
3. Jean-Pierre Aubin, *A Survey of Viability Theory* (1990) — https://doi.org/10.1137/0328044
4. Xabier Barandiaran, Ezequiel Di Paolo e Marieke Rohde, *Defining Agency* (2009) — https://doi.org/10.1177/1059712309343819
5. Daniel John Murray, *From Predictive State to Viable Action* (preprint de setembro de 2026; não assumir avaliação por pares) — https://ssrn.com/abstract=7427100

**Métodos de extensão:**

- Doyen & De Lara (2010), *Stochastic viability and dynamic programming* — https://doi.org/10.1016/j.sysconle.2010.07.008
- Barnett & Crutchfield (2016), *Computational Mechanics of Input-Output Processes: The ε-Transducer* — https://arxiv.org/abs/1412.2690
- Kolchinsky & Wolpert (texto completo) — https://pmc.ncbi.nlm.nih.gov/articles/PMC6227811/
- Klyubin, Polani & Nehaniv (2008), *Keep Your Options Open* — https://doi.org/10.1371/journal.pone.0004018
- Wissner-Gross & Freer (2013), *Causal Entropic Forces* — https://doi.org/10.1103/PhysRevLett.110.168702
- Nair & Evans (2004), *Stabilizability of Stochastic Linear Systems with Finite Feedback Data Rates* — https://doi.org/10.1137/S0363012902402116
- Dowker complexes/duality — https://link.springer.com/article/10.1007/s41468-026-00239-x
- Girsanov/KL/control survey (2026) — https://pmc.ncbi.nlm.nih.gov/articles/PMC13596642/

## J. Primeira decisão de pesquisa

**Começar por T1 + T2, não por agência total.** O exemplo físico determinístico separa dinamicamente aquilo que parecia ontologicamente inseparável. Seu prolongamento estocástico permite deduzir quais barreiras físicas tornam determinadas distinções necessárias. T3/T4 serão o primeiro teste sério de novidade: o que acontece quando produzir, manter e recuperar a própria capacidade de distinguir/agir também é parte da dinâmica?

**Princípio operacional:** um teorema pequeno que exclui uma confusão conceitual vale mais que uma ontologia abrangente sem um experimento discriminativo.