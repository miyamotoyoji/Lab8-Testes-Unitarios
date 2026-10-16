# Checkout: cálculo de frete — versão 2

## Requisitos EARS

- **REQ-01 (ubíquo):** O sistema deve calcular o total do pedido somando o frete padrão de R$15,00 ao subtotal do carrinho, respeitando a isenção prevista em REQ-02.
- **REQ-02 (condicional):** Se o subtotal do carrinho for maior ou igual a R$250,00, então o sistema deve aplicar frete grátis (R$0,00).

## Alteração do exercício 6.3

O limite anterior era R$200,00. Nesta versão, R$200,00 e R$249,99 pagam R$15,00; R$250,00 e valores superiores recebem isenção. REQ-01 e o contrato permanecem iguais. Esta especificação foi atualizada antes dos testes e do código.

## Contrato e escopo

Entradas: subtotal numérico não negativo, finito, em reais, com até duas casas decimais. O chamador é responsável por fornecer valores dentro desse domínio; validações de entrada não fazem parte desta tarefa.

`calcular_frete(subtotal)` devolve 15.00 ou 0.00; `calcular_total(subtotal)` devolve subtotal + frete. O carrinho de valor zero pertence ao domínio e tem frete padrão. Testes usam comparação aproximada para números decimais em ponto flutuante.

Sem cupons, interface ou banco de dados. A evolução regional abaixo é autorizada pelo laboratório 8; os exemplos regionais divergentes do laboratório 6 não são usados.

## Evolução do laboratório 8

- **REQ-03:** Se a região for "Norte" ou "Nordeste" e o subtotal for menor ou igual a R$300,00, então o sistema deve acrescentar R$10,00 ao frete base de REQ-01/REQ-02. Se o subtotal for superior a R$300,00, então o frete deve permanecer grátis.
- **REQ-04:** Quando confirmar um frete, o sistema deve consultar a taxa no ServicoLogisticaAPI e, após a consulta bem-sucedida, chamar enviar_notificacao_rastreio exatamente uma vez com o ID do pedido no ServicoNotificacao. Se a consulta falhar, não deve notificar. A sessão recebida é reservada, sem uso na lógica atual.

Interpretação literal de "sobre a taxa base": Norte/Nordeste pagam 25 abaixo de 250, 10 de 250 até 300 inclusive e zero acima de 300. Outras regiões preservam a regra base. A região é opcional para compatibilidade com a aula anterior e usa os nomes exatos do enunciado. O total também recebe a região. O fluxo externo é uma unidade separada com dependências injetadas; os testes não fazem chamadas reais.
