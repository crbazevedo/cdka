# T3.D — Um reparo que apaga pode também escrever

**Status:** proposições demonstradas com ferramentas conhecidas; originalidade não estabelecida.

## Motivação

Dizer que cada modo de reparo apaga a memória não basta para concluir que o controlador perde o conhecimento. O próprio modo escolhido pode escrever um novo registro físico da informação anterior. Precisamos analisar o canal completo: memória → escolha de ação → nova organização.

## Definições mínimas

- **C:** tudo que o mecanismo de decisão consegue ler fisicamente.
- **K(c'|c,a):** transformação da organização sob a ação a.
- **Política pi(a|c):** regra que usa C, não estados ocultos ou lembranças apagadas.
- **Variação total:** distância que indica quão distinguíveis são dois sinais probabilísticos.

## Resultado

Se as ações de cada estado observável podem ser escolhidas independentemente, a maior capacidade do canal fechado de preservar diferenças é a maior distância entre duas linhas físicas obtidas por escolhas de ações em entradas diferentes.

Isso permite calcular o limite por extremos de conjuntos convexos, sem otimizar todas as políticas aleatórias. Para sinais binários, a geometria é um retângulo: a diagonal representa sinais indistinguíveis; os vértices mais distantes dela representam as melhores regras de escrita.

## Exemplo

Um reparo sempre escreve 0. Outro sempre escreve 1. Cada modo isolado destrói a informação anterior. Mas selecionar o primeiro quando o bit é 0 e o segundo quando é 1 conserva o bit perfeitamente. Não há informação criada do nada: a ação apenas transfere uma distinção que já existia.

## Um segundo cuidado: quem sobreviveu não é toda a população

Imagine mil sistemas. Só um sobrevive ao reparo, mas esse sobrevivente possui memória perfeita. Medir apenas sua memória mostra 100% de acerto. Medir a viabilidade da organização mostra 0,1% de sucesso.

A análise correta conserva a probabilidade das trajetórias que falharam. Não podemos renormalizar os sobreviventes e chamar sua precisão de confiabilidade global.

## Papel no programa e próximo passo

T3.D substitui o corte passivo de T3.C por um corte dependente da política. Também fornece a medida que T4.C precisa propagar ao longo de vários reparos: probabilidade de continuidade **e** informação utilizável, não apenas uma delas.

A generalização ainda aberta é incorporar restrições físicas que impeçam escolher separadamente qualquer ação em qualquer linha do canal: custos de reconfiguração, circuitos limitados e recursos compartilhados.

## Simulador, prova e antecedentes

[Laboratório interativo](../lab/policy_cuts.html#channel) · [Prova completa](../results/T3D-policy-aware-cuts.md).

Antecedentes: coeficiente de Dobrushin e sinalização através de ações em controle. Os exemplos não demonstram intenção ou consciência.
