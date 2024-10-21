# AgendaDaCrianca

Agenda da Criança

A Agenda da criança é um aplicativo desenvolvido em Python usando Tkinter que permite que as atividades de uma criança sejam agendadas, recompensadas com estrelas ao serem completadas e salvas em um banco de dados para futuras consultas. O sistema também possibilita a troca dessas estrelas por recompensas personalizadas.

Funcionalidades Principais

Adicionar Atividades: Permite agendar atividades diárias com nome, data, hora, número de estrelas e uma imagem associada.
Recompensas com Estrelas: Ao completar as atividades, a criança recebe estrelas, que podem ser acumuladas e trocadas por recompensas.
Banco de Estrelas: Um banco de estrelas que contabiliza a quantidade de estrelas ganhas e gastas.

Quadro de Atividades: Um quadro para visualizar as atividades agendadas e concluídas.
Persistência de Dados: As atividades e recompensas são salvas em um banco de dados SQLite, garantindo que os dados sejam mantidos entre as sessões.

Como Usar
Pré-requisitos:

Certifique-se de ter o Python 3 instalado em seu sistema. Você pode verificar a instalação com o comando:

bash
python --version

Instalação
Clone este repositório:

bash:
Copiar código
git clone https://github.com/taticavalcanti22/AgendaDaCrianca.git

Instale os pacotes necessários:

bash:
pip install Pillow

Execute o aplicativo:

bash
python esbocoAgendaF.py

Estrutura de Arquivos

esbocoAgendaF.py: O código principal da aplicação, incluindo a interface gráfica e a lógica do banco de dados.

atividades.db: O banco de dados SQLite onde as atividades e recompensas são armazenadas.

assets/: Diretório para imagens utilizadas no app (imagens de atividades e recompensas).

Funcionalidades da Interface

Adicionar Atividade: Na tela principal, clique no botão "Adicionar Atividade" e preencha os detalhes da atividade (nome, data, hora, estrelas e imagem). Clique em "Confirmar" para salvar.

Visualizar Atividades: O quadro de atividades exibirá as atividades com os horários e estrelas associadas.

Recompensas: O quadro de recompensas mostrará as opções de recompensas, onde estrelas podem ser trocadas.

Banco de Dados
A aplicação utiliza SQLite para persistência de dados. O banco de dados atividades.db contém duas tabelas principais:

atividades: Armazena as atividades agendadas, incluindo nome, data, hora, imagem associada e o número de estrelas.

recompensas: Armazena as recompensas disponíveis, incluindo o nome, imagem e custo em estrelas.

Como Contribuir
Faça um fork deste repositório.

Crie uma nova branch com sua funcionalidade:

bash
git checkout -b minha-funcionalidade
Faça commit de suas mudanças:

bash
git commit -m 'Adiciona nova funcionalidade'
Envie para o branch original:

bash
git push origin minha-funcionalidade
Abra um pull request.

Licença
Este projeto está licenciado sob a Licença MIT - consulte o arquivo LICENSE para mais detalhes.
