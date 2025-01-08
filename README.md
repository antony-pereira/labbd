# Projeto Final LabBD

Este é um sistema de gerenciamento escolar desenvolvido com Streamlit, integrado a um banco de dados MySQL, com foco na exibição de informações organizadas e personalizadas. O projeto apresenta páginas dinâmicas que permitem consultas otimizadas, como listagem de escolas, turmas e docentes, com funcionalidades como ordenação de tabelas, exibição de disciplinas em formato compacto e filtros personalizados. 

Além disso, há integração com um sistema de login para controle de acesso, as páginas da pasta "pages" ficam ocultas na barra lateral até que o usuario faça login, feito o login a página principal é atualizada e novas abas aparecem na esquerda. Existe também uma lógica de permissão de usuario, o cadastro pode ser feito com um perfil "aberto" ou "gerencial", para o gerencial uma senha de autenticação é requisitada, ao fazer login com um perfil gerencial novas abas e funcionalidades aparecem, como por exemplo opção de bookmark em escolas, um botão de download de arquivo .csv em cada tabela, e uma nova página aparece na barra lateral para CRUD de bookmark de escolas.

A organização do código utiliza o arquivo app.py como principal e a maioria da lógica passa por ele, o arquivo menu.py cuida de mostrar/esconder as páginas baseado no login, e dentro da pasta pages temos cada página, com diferentes funcionalidades. 

O deploy foi feito no streamlit cloud, fiz toda a configuração e integração com o banco de dados usando Aiven como database. 

O site pode ser acessado aqui: https://labbdantony.streamlit.app/
