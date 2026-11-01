/* Generated from the same source objects as docs/articles/*.md. */
export const ARTICLES = [
  {
    "id": "B1",
    "number": "01",
    "title": "Quantas distinções são necessárias para agir?",
    "status": "Baseline conhecido · prova exata",
    "kind": "Demonstração",
    "question": "Quantas mensagens internas são suficientes para escolher alguma ação segura em qualquer estado possível?",
    "intuition": "Conhecer o mundo inteiro pode ser desnecessário. Estados distintos só precisam gerar mensagens diferentes se não houver uma mesma ação aceitável para eles.",
    "motivation": "A teoria da informação quantifica incerteza. Para controle, a pergunta relevante é quantas distinções alteram a escolha de ação. Sem essa separação, confundimos capacidade preditiva com conhecimento necessário para uma tarefa.",
    "definitions": [
      [
        "Estado w",
        "Uma condição possível do sistema ou ambiente."
      ],
      [
        "Ação a",
        "Uma intervenção fisicamente admissível."
      ],
      [
        "Relação de viabilidade R(w,a)",
        "Verdadeira quando a ação a satisfaz o critério de segurança no estado w."
      ],
      [
        "Código de decisão",
        "Mapa estado → mensagem interna → ação. Não exige prever todas as alternativas."
      ]
    ],
    "formula": "W_a = {w : R(w,a)=1}\nN_min = min{|B| : B ⊆ A e ⋃(a∈B) W_a = W}\nBits fixos = ⌈log₂ N_min⌉",
    "example": "Três situações possuem ações seguras {1,2}, {2,3} e {1,3}. Cada par compartilha uma ação, mas nenhuma ação serve para as três. A estrutura de compatibilidade precisa representar conjuntos, não apenas pares.",
    "finding": "O número mínimo de códigos é exatamente o tamanho da menor cobertura de estados por ações seguras. É um resultado conhecido, não um novo teorema. O número de bits de armazenamento não deve ser confundido com informação mútua média.",
    "bigger": "B1 fornece a ponte entre a estrutura causal das ações possíveis e o custo de memória para decisões. T1 altera essa estrutura através de um parâmetro físico; T2 a relaciona a probabilidades de falha.",
    "next": "Uma versão dinâmica em que os conjuntos de ações viáveis mudem com atratores, recursos e sensores; depois, buscar limites informacionais para decisões sequenciais.",
    "limits": "Pressupõe observação perfeita na codificação, uma ação por decisão, zero erro e conjuntos finitos. Não estabelece intencionalidade ou autonomia.",
    "simulator": "Altere a matriz de viabilidade. O algoritmo busca exatamente a menor cobertura e o diagrama de três estados mostra compatibilidades de ordem superior.",
    "sources": [
      [
        "Murray (2026), From Predictive State to Viable Action",
        "https://ssrn.com/abstract=7427100"
      ]
    ]
  },
  {
    "id": "T1",
    "number": "02",
    "title": "Quando a física muda suavemente e a memória dá um salto",
    "status": "Exemplo provado · sem novidade reivindicada",
    "kind": "Resultado exato",
    "question": "Pode a informação mínima para controle mudar abruptamente sem qualquer bifurcação de atratores?",
    "intuition": "Uma perturbação pequena pode tornar incompatíveis ações que antes funcionavam nos mesmos estados. O mundo muda continuamente, mas a necessidade de distinguir situações salta.",
    "motivation": "Teorias de auto-organização estudam transições nos atratores; uma teoria de conhecimento precisa também estudar transições no conjunto de decisões possíveis.",
    "definitions": [
      [
        "Dinâmica",
        "dx/dt = −x + λw + u, com w,u∈{−1,+1} e x(0)=0."
      ],
      [
        "Segurança",
        "Manter |x(t)| ≤ 1,5 durante o horizonte escolhido."
      ],
      [
        "Horizonte T",
        "Prazo durante o qual a segurança precisa ser garantida."
      ],
      [
        "Limiar informacional",
        "Valor de λ no qual muda a cobertura mínima das ações seguras."
      ]
    ],
    "formula": "x(t) = (λw+u)(1−e^(−t))\nB_T = 1,5/(1−e^(−T))\nN_min = 1 se λ ≤ B_T−1\nN_min = 2 se B_T−1 < λ ≤ B_T+1\nInviável se λ > B_T+1",
    "example": "Com horizonte infinito: λ≤0,5 exige 0 bit; 0,5<λ≤2,5 exige 1 bit; λ>2,5 é inviável. Com T=ln 2, os limiares se deslocam para 2 e 4. Adicionar a ação neutra u=0 reduz a informação requerida em alguns regimes.",
    "finding": "Cada configuração possui um único equilíbrio globalmente estável, com autovalor −1. Não existe bifurcação de atratores. O salto está na compatibilidade das ações diante de uma exigência de segurança.",
    "bigger": "T1 separa transições físicas de transições informacionais para controle. Ele é o caso determinístico que T2 generaliza com falhas estocásticas.",
    "next": "Investigar sensores imperfeitos, intervenção tardia e restrições de recurso; conectar o limiar com barreiras de eventos raros.",
    "limits": "A ação é escolhida no início e mantida constante, e a segurança é determinística. O exemplo não demonstra conhecimento adquirido espontaneamente.",
    "simulator": "Varie λ, o horizonte e o repertório de ações. A escada de memória e a paisagem de regimes mostram onde estão os limiares, enquanto as trajetórias revelam a dinâmica contínua.",
    "sources": [
      [
        "T1: prova e variantes no corpus",
        "../results/T1-threshold.md"
      ]
    ]
  },
  {
    "id": "T2",
    "number": "03",
    "title": "Barreiras, ruído e bits necessários para agir",
    "status": "Corolário assintótico · extensão aberta",
    "kind": "Resultado condicionado",
    "question": "Uma paisagem estocástica pode determinar quando um controlador precisa distinguir estados?",
    "intuition": "À medida que o ruído diminui, certas falhas tornam-se exponencialmente raras. O custo assintótico da falha separa ações aceitáveis de ações perigosas.",
    "motivation": "É a ligação rigorosa entre least action em grandes desvios, risco admissível e a geometria da informação necessária para selecionar intervenções.",
    "definitions": [
      [
        "ε",
        "Intensidade de ruído (variância na ilustração Gaussiana)."
      ],
      [
        "J(w,a)",
        "Taxa assintótica −ε log P(falha|w,a), quando existe o limite."
      ],
      [
        "c",
        "Exigência de segurança exponencial: α_ε=e^(−c/ε)."
      ],
      [
        "Ação segura",
        "P(falha) ≤ α_ε, sob risco, horizonte e modelo declarados."
      ]
    ],
    "formula": "X | w,u ~ N(λw+u, ε)\nFalha := |X|>1,5\nJ(w,u) = ½ [max(0,1,5−|λw+u|)]²\nP(falha) ~ exp(−J/ε) na escala logarítmica\nSeguro assintoticamente se J>c (fora da igualdade)",
    "example": "Mesmo com apenas dois estados e duas ações, mudar c pode alterar a menor cobertura de ações seguras: a exigência de confiabilidade modifica as distinções necessárias para decidir.",
    "finding": "Para um conjunto finito de contextos e ações, longe dos casos J=c, a relação de segurança eventualmente coincide com o limiar J>c. Combiná-la à cobertura mínima produz uma fórmula para memória de decisão. O resultado básico é uma composição de ferramentas conhecidas.",
    "bigger": "T2 liga a ação de trajetórias e as probabilidades de escape à informação operacional. A versão fisicamente rica usará difusões bistáveis e organização endógena.",
    "next": "Derivar uma taxa de falha para uma difusão bistável, comparar probabilidades exatas ou confiáveis, incorporar limites de sensor/atuador e investigar acoplamento de recursos.",
    "limits": "O painel usa uma variável Gaussiana em um instante, não um processo de escape em dois poços. O comportamento de igualdade J=c e ruído finito não é decidido apenas pelo expoente.",
    "simulator": "Compare riscos Gaussianos de ruído finito com a taxa J do limite ε→0, e veja como o número de mensagens depende do limiar de confiabilidade.",
    "sources": [
      [
        "T2: hipóteses e prova assintótica no corpus",
        "../results/T2-barrier-to-bits.md"
      ]
    ]
  },
  {
    "id": "T3",
    "number": "04",
    "title": "O custo compartilhado de perceber, agir e se manter",
    "status": "Modelo ilustrativo · teorema aberto",
    "kind": "Conjectura",
    "question": "Qual é a fronteira de viabilidade quando informação, intervenção e reparo competem pelos mesmos recursos físicos?",
    "intuition": "Um controlador excelente em observar mas incapaz de agir falha. Um atuador potente sem manutenção também falha. A organização só funciona quando seu orçamento sustenta simultaneamente vários mecanismos.",
    "motivation": "Limites separados de informação e energia não caracterizam necessariamente o que um sistema consegue realizar quando as capacidades físicas compartilham recursos.",
    "definitions": [
      [
        "i",
        "Recursos alocados para qualidade de percepção."
      ],
      [
        "u",
        "Recursos alocados para eficácia da intervenção."
      ],
      [
        "r",
        "Recursos alocados para continuidade/reparo."
      ],
      [
        "B",
        "Orçamento físico total do modelo, com i+u+r=B."
      ]
    ],
    "formula": "q(i)=1−0,5e^(−i/2)   percepção correta\nc(u)=1−e^(−u/2)     ação eficaz\nm(r)=1−e^(−r/2)     manutenção\nP(sucesso)=q(i)·c(u)·m(r)\nmax P(sucesso), sujeito a i+u+r=B",
    "example": "Na borda do triângulo de alocações, um mecanismo recebe orçamento zero e a chance de sucesso cai a zero no modelo. O ótimo aparece no interior, e seu local se desloca ao mudar B ou as escalas de custo.",
    "finding": "A visualização é um benchmark de otimização com variáveis acopladas por orçamento; não prova um teorema geral sobre autonomia. O resultado científico procurado é uma fronteira conjunta com limites mais fortes que restrições independentes.",
    "bigger": "T3 introduz o custo da própria capacidade de controlar, que falta nas definições de influência potencial e em modelos de memória decisória com atuadores fixos.",
    "next": "Substituir a fatoração pedagógica por uma dinâmica física de sensor/atuador degradáveis; derivar um limite inferior e um contraexemplo de separabilidade.",
    "limits": "Os três fatores foram escolhidos pedagogicamente, não inferidos de física fundamental. Informação de Shannon é mostrada como métrica derivada da qualidade do canal, não como equivalente ao recurso i.",
    "simulator": "Explore o simplex de três custos. Cada ponto é uma alocação possível; o tamanho e a tonalidade sinalizam sucesso, e o ótimo é encontrado por enumeração exata.",
    "sources": [
      [
        "Fox & Tishby, minimum-information control",
        "https://arxiv.org/abs/1606.01946"
      ]
    ]
  },
  {
    "id": "T4",
    "number": "05",
    "title": "Por que a decisão correta hoje pode falhar amanhã",
    "status": "Programação dinâmica conhecida · extensão aberta",
    "kind": "Pesquisa ativa",
    "question": "Como escolher intervenções quando perceber agora consome a capacidade de perceber depois?",
    "intuition": "Saber a ação certa agora não resolve todo o problema: sensores se desgastam, recursos acabam e reparar um mecanismo pode expor o sistema ao risco antes do próximo evento.",
    "motivation": "Autonomia exige sustentabilidade temporal do controle, não apenas sucesso numa decisão isolada.",
    "definitions": [
      [
        "h",
        "Número de passos ainda necessários para permanecer viável."
      ],
      [
        "z",
        "Saúde do sensor, consumida ao observar."
      ],
      [
        "r",
        "Tokens de reparo disponíveis."
      ],
      [
        "V(h,z,r)",
        "Maior probabilidade de completar h passos sem falhar."
      ]
    ],
    "formula": "V(0,z,r)=1\nV(h,z,r)=max{\n  0,5·V(h−1,z,r)                       [sem observar]\n  q·V(h−1,z−1,r)  se z>0             [observar]\n  0,5·V(h−1,min(3,z+2),r−1) se r>0 [reparar]\n}",
    "example": "O controlador possui um sensor que permite acertar uma ação com probabilidade q. Cada observação consome uma unidade de saúde; reparar devolve duas unidades, mas durante o reparo só é possível agir às cegas.",
    "finding": "O modelo permite calcular por programação dinâmica o benefício de reparar e a dependência da estratégia em relação ao horizonte. Isso não é ainda uma solução geral de POMDP com organização endógena.",
    "bigger": "T4 transforma a memória suficiente de B1 e os limites de T3 em uma condição recursiva de continuidade. Ele também estabelece o protocolo para confrontar políticas míopes e antecipatórias.",
    "next": "Passar para observação parcial do estado de sensores/atuadores, implementar memória interna limitada e provar resultados de suficiência recursiva.",
    "limits": "A saúde do sensor e o orçamento são conhecidos perfeitamente; cada evento é independente. É uma ilustração de controle com recursos, não uma demonstração de agência.",
    "simulator": "Altere horizonte, saúde do sensor, reparos e precisão. Veja o valor de sobrevivência e o mapa de políticas ótimas por tempo restante e saúde.",
    "sources": [
      [
        "Viabilidade estocástica e programação dinâmica",
        "https://doi.org/10.1016/j.sysconle.2010.07.008"
      ]
    ]
  },
  {
    "id": "T5",
    "number": "06",
    "title": "O comportamento revela quem está no controle?",
    "status": "Problema de identificação causal · aberto",
    "kind": "Hipótese",
    "question": "Duas organizações que produzem as mesmas trajetórias externas podem diferir na origem causal do seu controle?",
    "intuition": "Um dispositivo com realimentação interna e outro que reproduz uma fita de comandos podem parecer iguais. Apenas quando provocamos uma perturbação inesperada suas arquiteturas mostram diferenças.",
    "motivation": "Persistência, complexidade e movimento organizado não bastam para atribuir autonomia. Precisamos testar a arquitetura que gera e sustenta intervenções.",
    "definitions": [
      [
        "Realimentação",
        "A intervenção depende do estado atual observado."
      ],
      [
        "Replay",
        "Uma sequência de ações foi calculada antes e não muda diante da perturbação."
      ],
      [
        "Ablação",
        "Intervenção que desativa seletivamente um mecanismo causal."
      ],
      [
        "Autonomia constitutiva",
        "Hipótese de que a organização sustenta sensores, atuadores e reparo por seus próprios processos."
      ]
    ],
    "formula": "x(t+1)=0,87x(t)+d(t)+u(t)\nFeedback: u(t)=clip(−k x(t))\nReplay: u(t)=u_ref(t) [pré-calculado]\nAblado: u(t)=0 após o instante da lesão",
    "example": "Antes de uma perturbação inesperada, feedback e replay produzem trajetórias idênticas. Depois do choque, feedback reage; replay não acompanha. Desativar o controlador interno produz uma terceira trajetória.",
    "finding": "A experiência demonstra identificação de realimentação sob intervenções declaradas, não identificação universal de agência. Um controlador externo adaptativo poderia reagir também. A parte de auto-manutenção precisa de testes separados.",
    "bigger": "T5 define evidência causal mínima para diferenciar influência, regulação e capacidade de organização. Sem essa distinção, a teoria confundiria um redemoinho, um termostato e um agente.",
    "next": "Introduzir sensores que se deterioram, reparo endógeno e controladores externos observacionalmente equivalentes; formular condições necessárias e suficientes relativas a intervenções.",
    "limits": "O replay é propositalmente aberto, não um operador externo igualmente competente. Divergência após choque não prova intenção ou consciência.",
    "simulator": "Provoque um choque imprevisível e compare trajetórias de feedback, replay e ablação. A linha vertical demarca a intervenção causal.",
    "sources": [
      [
        "Barandiaran, Di Paolo & Rohde, Defining Agency",
        "https://doi.org/10.1177/1059712309343819"
      ]
    ]
  },
  {
    "id": "T6",
    "number": "07",
    "title": "Quando a seleção vira uma memória física",
    "status": "Identidade conhecida · extensão exploratória",
    "kind": "Programa aberto",
    "question": "Uma população de mecanismos pode carregar história e alterar suas próprias possibilidades de ação?",
    "intuition": "A frequência relativa de duas estratégias acumula vantagens seletivas passadas. Se as estratégias modificam o ambiente, a memória e a paisagem dinâmica passam a interagir.",
    "motivation": "Talvez representações não precisem surgir como símbolos: podem ser distribuições históricas de mecanismos físicos que modificam as respostas futuras de uma organização.",
    "definitions": [
      [
        "p",
        "Fração de mecanismos do tipo A; 1−p representa B."
      ],
      [
        "x",
        "Variável ambiental que altera a vantagem seletiva."
      ],
      [
        "βx",
        "Diferença de crescimento entre A e B."
      ],
      [
        "η e ρ",
        "Intensidade da retroação populacional e relaxação ambiental."
      ]
    ],
    "formula": "dp/dt=βp(1−p)x\ndx/dt=−ρx+η(2p−1)\nd/dt log[p/(1−p)] = βx\nlogit p(t)−logit p(0)=β∫₀ᵗ x(s)ds",
    "example": "Se o ambiente favorece A, sua fração aumenta; ao tornar-se abundante, A pode modificar o ambiente e reforçar sua própria vantagem. O sistema apresenta dois estados atratores de fronteira e um equilíbrio interior do tipo sela quando β,η,ρ>0.",
    "finding": "A identidade de log-odds e os pontos fixos são resultados matemáticos conhecidos. A hipótese CDKA é que algumas composições históricas representem distinções contrafactuais que realmente participam da regulação futura.",
    "bigger": "T6 liga seleção, memória distribuída e controle ao estudo de atratores, sem transformar toda seleção evolutiva em conhecimento.",
    "next": "Confrontar perturbações em p com desempenho de regulação, distinguir memória histórica de representação causalmente útil, e incluir custos físicos da manutenção de mecanismos.",
    "limits": "Acúmulo de histórico não é suficiente para conhecimento operacional; o sistema de duas dimensões é um toy model, não uma explicação universal da agência.",
    "simulator": "Mude estado inicial e acoplamentos; acompanhe o campo de direções, a separatriz aproximada, a convergência aos atratores e o acúmulo das razões de frequência.",
    "sources": [
      [
        "Weitz et al. (2016), replicador com feedback ambiental",
        "https://doi.org/10.1073/pnas.1604096113"
      ]
    ]
  }
];
