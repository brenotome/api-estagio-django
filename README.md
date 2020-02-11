# API Teste django

Endereço da API: [https://api-teste-estagio.herokuapp.com/api/](https://api-teste-estagio.herokuapp.com/api/)

Documentação da API: [https://brenotome.github.io/api-teste-django-docs/](https://brenotome.github.io/api-teste-django-docs/)

## Autenticação
A autenticação é feita por [JWT](https://jwt.io/), a rota de cadastro de novo usuário está liberada, todas as outras só ficam acessíveis para o próprio usuário.

## Pdf
A criação de pdf somente envia o arquivo em resposta ao request de pagamento, e não o armazena em lugar nenhum, optei por fazer assim porque segundo minhas pesquisas para salvar arquivos no heroku precisaria de outros serviços.

## Locais dos métodos

Optei por sobrescrever os métodos em locais diferentes, os de leitura nos Viewsets e os de escrita nos Observables, pelas minhas pesquisas pareceu ser o mais adotado uma vez que nos Observables eu receberia os parâmetros já validados, porém não encontrei muito consenso sobre quais são as boas práticas nesse caso.
