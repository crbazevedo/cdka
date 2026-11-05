# T4.R — Guardar os bits não conserva o diagnóstico

**Status:** resultado exato de uma família finita; síntese conjunta e redução estocástica verificadas.

## Pergunta e motivação

Uma organização que decide quando se reparar deve sempre proteger o diagnóstico antigo ou adquirir um novo? A resposta depende de sua própria dinâmica: as ações podem modificar o que a informação antiga diz sobre os estados que permanecem possíveis.

## Definições mínimas

O dispositivo tem um banco falível de seis portas, três células diagnósticas, saúde oculta e quatro níveis de recurso. O mesmo banco seleciona sua manutenção e executa a tarefa que repõe recursos. Manter os bits é perfeito; observar de novo é ruidoso. Os dois serviços usam o mesmo preço declarado para isolar suas consequências.

## Exemplo e resultado

Com o mesmo controlador, sobreviver a oito ciclos tem probabilidade91,7477% renovando sempre e89,5875% retendo a leitura inicial. Renovar só depois da manutenção produz88,7486%; renovar depois de não fazer manutenção produz91,6492%.

Uma leitura antiga de 'saudável' desestimula manutenção. Se somente a manutenção permite obter uma nova leitura, uma degradação posterior pode ficar sem evidência atualizada. A falibilidade do próprio seletor ainda pode provocar manutenção, mas isso não equivale a obter um diagnóstico correto.

A comparação completa reotimiza64 programas; seu melhor permanece a renovação constante. Os valores são específicos da biblioteca e dos custos declarados.

## Formulação

A renovação independente permite fatorar o processo em operação A e emissão E:

    K=A E; M=E A; E K=M E.

Ao reter a memória, ações, falhas e saldos selecionam as palavras. Demonstramos que a distribuição resultante pode sair de toda a família de emissões anteriores, mesmo sem mudança de saúde. Uma descrição física reduzida de48 estados, por sua vez, continua exata.

## Papel no CDKA e próximo passo

Conhecimento operacional depende da manutenção das condições que tornam uma representação utilizável. O próximo problema é selecionar a observação por uma política física custosa — sem consultar gratuitamente a condição real que se pretende diagnosticar.

## Simulador

[Explorar renovar, reter e temporizar a aquisição](../lab/memory_renewal.html). O gráfico preserva a massa original de sobrevivência. O segundo painel mostra a seleção de memórias, e o terceiro localiza as contribuições temporais ao ganho.

## Limites

Roteamento e guarda de recursos permanecem primitivas comuns. Retenção e aquisição têm preço igual somente no contrato desse experimento. A interface de48 estados pertence ao avaliador; não revela a saúde ao controlador. Há risco fatal uniforme por tarefa; nenhum resultado de sobrevivência infinita é alegado.

[Provas e dados](../results/T4R-renewal-and-selected-memory.md).
