### Uso

```
É autorizado a utilização e modificação dos arquivos deste repositório para uso livre, 
contanto que os créditos ao seu criador estejam explícitos, 
de preferência expondo seu GitHub pessoal:
github.com/henriquelmeeee
```

### Instalação

Para instalar a Harvi Cloud no seu computador pessoal ou em um serviço de hospedagem especializado, você deve fazer algumas configurações.

> :warning: **Aviso**: O script abaixo irá baixar os arquivos para a **versão 1** do projeto.

<br>Primeiro, você deve copiar os arquivos para seu computador/servidor:
```console
root@server:~# mkdir /app
root@server:~# cd /app
root@server:/app# gh repo clone henriquelmeeee/harvicloud 
root@server:/app# rm -rf ./v2/ ./v1/src/README.md README.md && mv ./v1/src/* .
```

Após isso, você deve executar ```requirements.sh``` para baixar todas as dependências do projeto. Observe que o processo de instalação poderá demorar mais, em especial caso você esteja baixando as dependências da **API**.

```console
root@server:/app# chmod +x ./v1/requirements.sh
root@server:/app# ./requirements.sh
```

Quando todas as dependências estiverem instaladas, é hora de configurar algumas variáveis para o código.<br> Observe que cada diretório (api.harvicloud.com, harvicloud.com, etc) tem um arquivo chamado **config.py**. Nele, estará armazenado todos os valores que o site irá usar para funcionar. Você deverá configurar qual o domínio/ip para a **API**, por exemplo.<br>Não se preocupe, cada variável terá um comentário exemplificando o que ela faz. Veja um exemplo abaixo.

```
ADMIN_USER_NAME = 'admin' # Nome de usuário do administrador
ADMIN_PASSWORD = 'admin' # Senha do administrador

DOCS_DOMAIN: 'http://docs.harvicloud.com/' # Domínio/IP em que a documentação está registrada
API_DOMAIN: 'http://api.harvicloud.com/' # Domínio/IP em que a API está registrada
...
```

Após isso, **Harvi Cloud** estará pronto para uso. Você pode editar livremente o código fonte, **sempre lembrando de deixar os créditos em algum lugar da página inicial do site**.
