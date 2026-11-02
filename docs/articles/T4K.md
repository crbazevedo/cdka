# T4.K — O código também é uma máquina

**Status:** resultados exatos de uma biblioteca finita e instrumentos conhecidos. Originalidade não estabelecida.

## Pergunta e motivação

Preservar todas as distinções de um diagnóstico é sempre a melhor maneira de controlar o futuro? A v9 disse quando uma distinção importa para duas decisões. Agora acrescentamos uma exigência: ela precisa ser representada por bits físicos sujeitos a corrupção, e o programa que a usa precisa caber na biblioteca disponível.

## Definições mínimas

O sensor produz três diagnósticos equiprováveis. O mundo e o corretor seguem a mesma dinâmica anterior. Um codificador grava cada diagnóstico em dois bits: 00, 01, 10 ou 11. Antes da primeira ação, cada bit pode inverter independentemente com probabilidade p. Depois disso, a palavra recebida é retida durante as duas decisões. O controlador lê apenas essa palavra, novos sinais físicos e o relógio declarado.

O programa completo também possui um limite: no máximo L continuações distintas podem ser instaladas para atender os quatro resultados possíveis da leitura. Não fornecemos saúde oculta, diagnóstico original ou um ponteiro de plano gratuito.

## O que a matemática revelou

Cada programa tem uma probabilidade de sobrevivência da forma a+bp+cp². Enumeramos 5.184 codificações/decodificações e certificamos, com aritmética exata, que o ótimo possui três regiões:

| Erro por bit | Melhor estrutura |
|---|---|
| Abaixo de aproximadamente 0,492129% | Preservar os três diagnósticos |
| Entre aproximadamente 0,492129% e 20,818763% | Fundir dois diagnósticos e usar palavras opostas |
| Acima de aproximadamente 20,818763% | Usar a mesma continuação, sem aproveitar o diagnóstico |

O resultado refere-se a até três planos gratuitos no experimento de transporte. Não é uma lei universal para qualquer ruído ou controlador.

## Exemplo

Com p=10%, a melhor codificação injetiva preserva três diagnósticos e entrega sobrevivência média de 81,2618%. A síntese conjunta funde dois diagnósticos, entrega 81,6650% e utiliza menos informação mútua sobre o sinal original.

Não é o ruído que ajuda. O projeto descarta uma diferença menos valiosa para separar melhor as classes cujo erro tem consequências maiores. O hardware continua sendo o mesmo registrador de dois bits; os quatro resultados de leitura continuam fisicamente possíveis.

## Por que o desenho físico importa

Sem ruído, trocar os nomes dos estados não muda o diagnóstico. Com inversões de bits, 00 e 01 são vizinhos, enquanto 00 e 11 estão a duas inversões de distância. Nem toda permutação abstrata preserva essas relações. O código precisa ser escolhido junto com o canal e com o valor das continuações.

A distância dois não corrige todo erro simples: 01 e 10 são ambíguos entre as duas palavras opostas. O decodificador escolhe uma continuação que é melhor para a tarefa nesses casos, não uma recuperação sempre correta do diagnóstico.

## Custo do programa

Em um segundo experimento, cada slot extra da biblioteca consome um token antes do diagnóstico. Com recurso total quatro, um slot deixa quatro tokens para operar; dois deixam três; três deixam dois. Mesmo sem ruído, a melhor solução compra dois slots. O programa maior consome o recurso necessário à ação seguinte.

Os preços são hipóteses de uma biblioteca concreta, não limites físicos universais. Acrescentar uma opção gratuita não prejudica o ótimo; pagar por ela pode produzir um projeto pior, e a síntese deve poder rejeitá-la.

## Papel no programa CDKA

A unidade de análise passa a ser a combinação **representação + transição física da memória + programa implementável + recursos restantes**. A teoria não pode tratar o código como informação abstrata e só depois perguntar se a organização consegue sustentá-lo.

## Próxima obrigação e limites

A atualização entre decisões ainda é retenção ideal depois do primeiro episódio de ruído. A próxima prova deve restringir o circuito que atualiza o código e compartilha recursos com o seletor. Codificação causal, atribuição de estados e compressão de POMDPs são antecedentes diretos; esta construção não estabelece prioridade nem agência espontânea.

## Simulador e prova

[Laboratório interativo](../lab/joint_compilation.html) · [Demonstração completa](../results/T4K-joint-physical-compilation.md) · [Estratégia e retomadas](../strategy/proof-engine-v10.md).
