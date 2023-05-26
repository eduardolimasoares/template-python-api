# Nome da Aplicação

Desafio FastAPI

## Instalação

Certifique-se de ter o Docker instalado em sua máquina. Em seguida, siga os passos abaixo para executar a aplicação:

1. Clone este repositório para o seu ambiente local.
2. Navegue até o diretório raiz da aplicação.

## Configuração

Antes de executar a aplicação, você precisa configurar algumas variáveis de ambiente. Siga os passos abaixo:

1. Verifique se o arquivo `docker-env` estão setadas as variáveis.

## Executando a Aplicação

Para executar a aplicação, siga os passos abaixo:

1. Abra um terminal e navegue até o diretório raiz da aplicação.
2. Execute o seguinte comando para construir as imagens do Docker e iniciar os contêineres:

   ```bash
   docker-compose -f docker-compose-api.yaml up --build -d

3. Aguarde até que os contêineres sejam iniciados com sucesso.
4. Acesse a aplicação em seu navegador utilizando o seguinte endereço: http://localhost:8000.
5. A documentação está em http://127.0.0.1:8000/docs

## Testes

1. Para rodar os testes vá até a rais do projeto e rode o comando:
   ```bash
   pytest