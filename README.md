# Nyx Bot
Um bot de Discord desenvolvido para tocar músicas e playlists diretamente do YouTube. O bot utiliza a interface moderna do Discord através de Slash Commands (comandos de barra).
## Funcionalidades
Reprodução do YouTube: Suporte para tocar músicas diretamente de links ou buscas do YouTube.

Suporte a Playlists: Capacidade de carregar e enfileirar playlists completas do YouTube.

Slash Commands: Interação nativa com o Discord digitando /, o que facilita a visualização dos comandos disponíveis sem a necessidade de prefixos customizados.

Fila de Músicas: Sistema de gerenciamento de fila (pular, pausar, retomar, parar).

## Como Configurar e Usar
Siga os passos abaixo para registrar o seu bot no Discord, configurar as credenciais e executá-lo no seu servidor.

### 1. Criar o Bot no Discord Developer Portal
Para que o bot funcione, você precisa de um aplicativo registrado no Discord.

Acesse o Discord Developer Portal.

Clique no botão New Application no canto superior direito.

Dê um nome ao seu bot, aceite os termos e clique em Create.

No menu lateral esquerdo, vá até a aba Bot.

(Opcional, mas recomendado) Na seção Privileged Gateway Intents, ative as opções Message Content Intent e Server Members Intent, depois salve as alterações.

Na seção Token, clique em Reset Token e depois em Copy para copiar a chave do seu bot. Nunca compartilhe esta chave publicamente.

### 2. Convidar o Bot para o seu Servidor
Você precisa gerar um link de convite com as permissões corretas para adicionar o bot ao seu servidor.

Ainda no Developer Portal, vá até a aba OAuth2 e depois em URL Generator no menu lateral.

Na seção Scopes, marque as seguintes caixas:
```
bot

applications.commands (Essencial para os Slash Commands funcionarem)
```
Uma nova seção chamada Bot Permissions aparecerá logo abaixo. Marque as permissões mínimas necessárias:
```
Text Permissions: Send Messages, Read Message History, Use Slash Commands.

Voice Permissions: Connect, Speak.
```
Copie a URL gerada no final da página.

Cole a URL no seu navegador, selecione o servidor desejado e autorize o bot.

### 3. Configurar o Arquivo .env
Com o bot no servidor e o Token em mãos, configure o ambiente de desenvolvimento local.

Clone este repositório para a sua máquina local.

Na raiz da pasta do projeto, crie um arquivo chamado exatamente .env.

Abra o arquivo .env e adicione a seguinte linha, colando o token que você copiou no Passo 1:
```
DISCORD_TOKEN="sua_bot_key_aqui"
```
### 4. Executar o Bot
Com as variáveis de ambiente configuradas, você já pode iniciar o sistema.

Certifique-se de ter instalado as dependências necessárias do projeto.

Execute o arquivo principal da aplicação.

```
python main.py
```
