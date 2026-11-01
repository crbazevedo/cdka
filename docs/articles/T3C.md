# T3.C — O reparo que apaga o conhecimento necessário para agir

**Status científico:** contraexemplo exato, derivado de ferramentas conhecidas; ainda não demonstra agência nem originalidade matemática.

> Como um sistema pode ter um sensor perfeito, um atuador reparável e energia suficiente, mas falhar ao agir?

## Intuição

O sistema identifica corretamente uma situação, mas precisa reinicializar seu controlador para disponibilizar o atuador. O reparo apaga a memória. No momento decisivo, as duas ações estão disponíveis, mas a informação necessária para selecionar uma delas desapareceu.

A organização foi *fisicamente reparada*, porém perdeu sua *competência operacional*.

## Motivação e papel no CDKA

Este é o primeiro contraexemplo explícito contra o raciocínio que soma capacidades de perceber, agir e reparar medidas separadamente. Conhecimento operacional não é quantidade de bits observados em qualquer momento: depende de o sinal correto chegar ao mecanismo de atuação antes do prazo, atravessando as transformações da própria organização.

É uma ponte entre B1 (compatibilidade estado–ação), T3 (recursos e intervenção) e T4 (suficiência temporal).

## Definições mínimas

| Variável | Significado |
|---|---|
| W∈{0,1} | Contexto que determina qual intervenção é correta |
| Y | Leitura sensorial inicial, eventualmente com erro η |
| M | Memória volátil; ⊥ significa informação apagada |
| Z | Organização física: atuador, sensor e estados materiais potencialmente informativos |
| ρ | Probabilidade de apagamento de memória por reparo não protegido |
| ν | Probabilidade de o ambiente mudar durante reparo |
| n | Número de reparos obrigatórios antes da ação |
| B | Orçamento inteiro: cada reparo custa 1, protegê-lo custa mais 1 |
| α | Probabilidade máxima de falha admitida |

## Formulação e resultado

Com dois mundos equiprováveis e duas ações mutuamente incompatíveis, o valor de uma informação terminal fisicamente acessível C é

\`\`\`text
P*(sucesso) = [1 + TV(P(C|W=0), P(C|W=1))] / 2.
\`\`\`

Se todos os meios acessíveis forem apenas a memória após um reparo que a apagou, TV=0 e sucesso máximo=50%, apesar de o sensor inicial ter produzido 1 bit perfeito.

No modelo de n reparos com orçamento B≥n, sensores simétricos e cronograma de proteção independente do contexto:

\`\`\`text
k = min(n, B-n)       reparos protegidos
P* = 1/2 [ 1 + (1-2η)(1-2ν)^n (1-ρ)^(n-k) ].
\`\`\`

Para B<n o atuador permanece indisponível e P*=0.

## Exemplo

Com η=ν=0 e ρ=1, qualquer reparo sem proteção destrói o bit. Há um limiar de recurso: B<n é inviável; n≤B<2n entrega apenas 50% de sucesso; B≥2n permite proteger todos os reparos e alcançar 100%.

Com ρ=1/2, η=ν=0, n=3 e B=3, a probabilidade é 56,25%. Com B=4 sobe para 62,5%; B=5, 75%; B=6, 100%.

### Um segundo contraexemplo: compatibilidade em pares não basta

Considere três contextos com ações seguras {a,b}, {b,c} e {a,c}. Todos os pares compartilham uma ação. Mesmo assim, nenhuma intervenção serve para os três contextos simultaneamente. Se um reparo os torna indistinguíveis, o melhor sucesso sob distribuição uniforme é 2/3, e o controle com garantia absoluta é impossível. Essa é uma estrutura de compatibilidade de ordem superior, relacionada a complexos de Dowker.


## O que o simulador revela

- Mapa de regimes de viabilidade versus número de reparos e orçamento.
- Convergência temporal da capacidade de distinguir estados.
- Comparação de informação inicial e informação no instante da decisão.
- Um teste adversarial: registrar o mundo na configuração física Z torna o bit novamente acessível, mesmo quando M é apagada.

## Limitações e próximo passo

Não é um teorema novo: teste binário Bayesiano, Blackwell, memória finita e contração em variação total já são conhecidos. A proteção é pré-programada e não pode codificar o mundo em seu próprio padrão de ações. Em controladores reais, o estado do atuador, recursos, horários e ambiente podem guardar informações — é preciso incluir esses canais no corte causal completo.

**Próximo alvo:** políticas que recuperam ou criam seus próprios canais de memória por intervenções e reparos, com viabilidade recorrente e orçamento endógeno.

## Fontes e prova

- [Demonstração e condições completas](../results/T3C-temporal-causal-cut.md).
- [Engenharia reversa do contraexemplo](../strategy/finite-counterexample-synthesis-v1.md).
- [Controladores de estados finitos para POMDPs](https://proceedings.mlr.press/r16/junges18a.html).
- [Blackwell (1953)](https://doi.org/10.1214/aoms/1177729032).
- [Informação implícita através de ações](https://users.ece.cmu.edu/~pgrover/files/EncyclopediaWitsenhausen.pdf).
