# T4.I — O diagnóstico precisa atravessar a máquina

**Status:** resultados exatos de uma família finita; instrumentos de decisão bayesiana conhecidos. Sem reivindicação de originalidade.

## Pergunta e motivação

O sistema mediu a própria saúde. Mas o bit ainda estará disponível depois do reparo? E o mecanismo que lê esse bit consegue realmente selecionar a intervenção correta?

É possível ter informação verdadeira na memória e ainda assim obter um resultado pior ao tentar usá-la. Esse problema conecta R11 (diagnóstico e memória física) a R14 (implementação e manutenção do seletor).

## Definições mínimas

H é a saúde oculta do corretor. M é o diagnóstico armazenado. S é a saúde oculta de um **outro** componente: o seletor que converte M em comando. A memória pode apagar ou inverter o bit. O seletor também pode falhar. A política lê somente M — nunca H, S ou um posterior calculado pelo pesquisador.

Duas intervenções são possíveis: manter o registro ou obter uma nova observação. Usar a segunda opção num corretor degradado é mais prejudicial do que seu benefício quando saudável.

## Formulação

Se g é o ganho de atualizar com saúde boa, l é a perda de atualizar com saúde ruim, e é o erro efetivo do diagnóstico, a é a chance de o bit sobreviver e theta é o erro do seletor:

    U = max(0, g-e(g+l))
    V_diagnóstico = V_base - theta(l-g)/2 + a(1-2theta)U/2

A expressão supõe o modelo simétrico e independente, e um seletor cuja falha **inverte** o comando. Diagnósticos com risco próprio multiplicam essa expressão pela chance de sobreviver ao procedimento.

## Exemplo e resultado

Um programa custa uma unidade por reparo, uma para medir, uma para instalar o seletor e reserva duas para a intervenção terminal — até um comando errado pode gastar as duas. Proteger a memória ou fazer manutenção do seletor custa uma unidade adicional no caso de um reparo.

No exemplo, a memória ainda contém 0,2854 bit, mas ativar seu seletor falível dá sobrevivência de 87,6541%, abaixo dos 88,3319% da intervenção fixa. Com mais uma unidade, o melhor é **reparar o seletor**, não proteger a memória: sobe para 88,8049%. Com recurso para ambos, chega a 89,8773%.

O reparo do seletor não é mágico: sua saúde permanece oculta e a manutenção só funciona com probabilidade 80%. Essa transição foi enumerada no modelo físico.

## O que o simulador revela

Memória perdida e ação errada não são equivalentes. Apagar um bit com um sinal explícito permite usar uma ação de reserva. Inverter o comando pode destruir a própria ação de reserva. Um seletor que falha sempre para HOLD tem outra fórmula e pode permitir ganho onde o seletor que inverte não permite.

O programa deve especificar **como** um componente falha, não somente sua taxa média de acerto.

## O que habilita em seguida

A fórmula oferece um certificado de quanto vale gastar em preservar a memória versus reparar quem a utiliza. Um resultado complementar mostra que, para uma única decisão, pode bastar codificar o sinal do benefício da ação em um bit antes do armazenamento ruidoso.

Mas esse bit não é necessariamente suficiente amanhã. O alvo seguinte é identificar qual estado físico adicional torna a suficiência recursiva, sem conceder histórico ou crenças gratuitos ao controlador.

## Limites

Há dois estados de saúde, duas ações e custos declarados. Diagnóstico, proteção e manutenção são programas previamente escolhidos; ainda não resolvemos a política recorrente que diagnostica e repara seus próprios seletores. Não estamos medindo energia em joules nem demonstrando a origem de finalidades.

## Simulador, prova e referências

[Laboratório](../lab/diagnostic_transport.html) · [Provas e contratos](../results/T4I-diagnosis-through-repair.md) · [Próximas obrigações](../strategy/proof-engine-v8.md).

Antecedentes centrais: decisão bayesiana, Blackwell e [síntese de controladores finitos de POMDPs](https://proceedings.mlr.press/r16/junges18a.html).
