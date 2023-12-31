## Language Options

- [English](README.en.md)

# JaBOT Al Mossar - Bot Telegram de Cardápio

JaBOT Al Mossar é o seu assistente de refeições diárias no Telegram! Este bot oferece uma maneira conveniente de acessar o cardápio do almoço e do jantar, diretamente na palma da sua mão. Ele foi desenvolvido com carinho em Python para garantir que você e todos os alunos possam aproveitar as deliciosas opções de refeição a qualquer momento.

## Como Usar

Siga estas etapas simples para começar:

1. **Iniciar o Bot**: Abra o seu Telegram e pesquise por "@QxdJabot" ou clique [aqui](https://t.me/QxdJabot). Clique em "Iniciar" para começar a receber atualizações diárias do cardápio.

2. **Receba o Cardápio**: Todos os dias, o JaBOT irá lhe enviar o cardápio para o almoço e o jantar, diretamente no seu Telegram. É a maneira perfeita de se manter atualizado sobre as deliciosas opções de refeição disponíveis.

3. **Comandos Personalizados**: Se você quiser verificar o cardápio a qualquer momento, basta digitar `/almoco` para o almoço e `/jantar` para o jantar. O JaBOT responderá instantaneamente com as informações mais recentes.

4. **Parar a Atualização**: Se por algum motivo você quiser parar de receber as atualizações diárias, basta digitar `/parar` a qualquer momento.

## Tecnologias Utilizadas

Este projeto faz uso das seguintes tecnologias e bibliotecas:

- **Python**: Linguagem de programação utilizada para desenvolver o bot.
- **Selenium**: Automatiza a interação com o navegador para coletar dados do cardápio.
- **Beautiful Soup (bs4)**: Realiza o parsing do conteúdo HTML da página para extrair informações.
- **PyTelegramBotAPI**: Biblioteca para interagir com a API do Telegram e enviar mensagens.

## Contribuição

Se você deseja contribuir para tornar o JaBOT ainda melhor, fique à vontade para colaborar! Aceitamos contribuições que adicionem funcionalidades, façam melhorias ou corrijam problemas. Basta criar um fork do repositório e enviar um pull request.

## Licença

Este projeto é licenciado sob a [Licença MIT](LICENSE). Consulte o arquivo `LICENSE` para obter os detalhes completos da licença.

## Aproveite Suas Refeições!

A equipe do JaBOT Al Mossar deseja que você desfrute das suas refeições e que o bot facilite a sua vida no campus. **E aí? JaBOT Al Mossar?**

## Changelog - JaBOT Al Mossar

Todas as mudanças notáveis deste projeto serão documentadas nesta seção.

## [Versão 1.0.0] - 17/09/23

### Adicionado

- Início do projeto JaBOT Al Mossar.
- Implementação do scraping para obter dados do cardápio.
- Configuração do bot para o Telegram.
- Funcionalidade de iniciar e parar o menu do bot.
- Comandos para receber o cardápio do almoço e do jantar.
- Agendamento para atualização automática do cardápio em dias úteis.
- Envio automático de mensagens com o cardápio para os usuários.

## [Versão 1.1.0] - 25/10/2023

### Adicionado

- **Comando /start**: Agora os usuários podem obter informações iniciais sobre as funcionalidades do bot com o comando /start.
- **Comentários e Sugestões**: Foi adicionada a funcionalidade de enviar comentários e sugestões aos desenvolvedores diretamente pelo bot.
- **Data Atual no Cardápio**: A data atual foi incluída na mensagem do cardápio, proporcionando informações claras sobre a data da refeição.

### Corrigido

- **Tratamento de Falha no Cardápio**: Problemas ao lidar com a ausência de dados de cardápio foram corrigidos, garantindo uma experiência mais confiável para os usuários. Agora uma mensagem informando os usuários é enviada.

### Aprimorado

- **Mensagens de Erro Aprimoradas**: Mensagens de erro agora são mais informativas, melhorando a experiência do usuário.
- **Mensagens Reescritas**: As mensagens foram reescritas para melhorar a comunicação com os usuários, tornando-a mais dinâmica e confiável.
- **Desempenho e Estabilidade**: Vários aprimoramentos gerais foram implementados para melhorar o desempenho e a estabilidade do bot.


