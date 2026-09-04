# 📋 README Completo do Sistema de Cadastro de Pessoas

---

## 🌟 Sistema de Cadastro de Pessoas

Sistema desktop desenvolvido em **Python** com **PySide6** para cadastro e gerenciamento de pessoas físicas e jurídicas, com validação de documentos, consulta automática de CEP e interface moderna e intuitiva.

---

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Funcionalidades](#funcionalidades)
3. [Tecnologias Utilizadas](#tecnologias-utilizadas)
4. [Pré-requisitos](#pré-requisitos)
5. [Instalação e Execução](#instalação-e-execução)
6. [Estrutura do Projeto](#estrutura-do-projeto)
7. [Como Usar](#como-usar)
8. [Validações Implementadas](#validações-implementadas)
9. [Integração com API ViaCEP](#integração-com-api-viacep)
10. [Banco de Dados](#banco-de-dados)
11. [Personalização](#personalização)
12. [Solução de Problemas](#solução-de-problemas)
13. [Próximos Passos](#próximos-passos)
14. [Licença](#licença)

---

## 🎯 Visão Geral

O **Sistema de Cadastro de Pessoas** é uma aplicação desktop completa que oferece:

- ✅ Cadastro de pessoas físicas e jurídicas
- ✅ Validação automática de CPF, CNPJ, e-mail, celular e CEP
- ✅ Consulta de endereço via API ViaCEP com preenchimento automático
- ✅ Gerenciamento completo (listar, editar, excluir, pesquisar)
- ✅ Interface moderna, responsiva e com feedback visual
- ✅ Banco de dados SQLite para armazenamento local

---

## ✨ Funcionalidades

### 📝 Cadastro de Pessoas
| Campo | Descrição |
|-------|-----------|
| **Tipo de Pessoa** | Física ou Jurídica |
| **Nome Completo** | Mínimo: nome + sobrenome |
| **CPF/CNPJ** | Com validação de dígitos verificadores |
| **E-mail** | Validação de formato |
| **Celular** | Formato (XX) XXXXX-XXXX com validação de DDD |
| **CEP** | Consulta automática ao digitar 8 dígitos |
| **Logradouro** | Preenchido automaticamente pela API |
| **Número** | Campo obrigatório |
| **Complemento** | Opcional |
| **Bairro** | Preenchido automaticamente pela API |
| **Cidade** | Preenchido automaticamente pela API |
| **Estado** | Seleção em combobox, preenchido automaticamente pela API |

### 🔍 Consulta de CEP
- **Integração**: API ViaCEP (gratuita e sem autenticação)
- **Preenchimento**: Automático de logradouro, bairro, cidade e estado
- **Auto-consulta**: Ao digitar 8 dígitos no campo CEP
- **Botão manual**: Consultar para consulta explícita
- **Tratamento de erros**: 
  - CEP não encontrado
  - Timeout de conexão
  - Erro de rede
  - Resposta inválida da API

### 📊 Gerenciamento de Dados
| Funcionalidade | Descrição |
|----------------|-----------|
| **Listar** | Exibe todos os registros em tabela |
| **Pesquisar** | Em tempo real por nome ou CPF/CNPJ |
| **Editar** | Carrega dados para edição com cancelamento |
| **Excluir** | Com confirmação de segurança |
| **Atualizar** | Botão para recarregar a lista |

### 🎨 Interface do Usuário
- **Abas**: Organização em "Cadastro" e "Lista de Usuários Cadastrados"
- **Design Moderno**: Gradientes, sombras, cantos arredondados
- **Ícones**: Em todos os campos, botões e abas
- **Feedback Visual**: 
  - ✅ Borda verde para campos válidos
  - ❌ Borda vermelha para campos inválidos
- **Responsivo**: Adapta-se a diferentes tamanhos de tela
- **Indicadores**: Status de conexão, contagem de registros

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Versão | Finalidade |
|------------|--------|------------|
| **Python** | 3.8+ | Linguagem de programação |
| **PySide6** | 6.0.0+ | Interface gráfica (Qt para Python) |
| **Requests** | 2.28.0+ | Requisições HTTP para API ViaCEP |
| **SQLite3** | Integrado | Banco de dados local |
| **Regex** | Integrado | Validação de padrões |

---

## 📦 Pré-requisitos

Antes de executar o sistema, certifique-se de ter instalado:

### 1. Python 3.8 ou superior
```bash
# Verificar versão do Python
python --version
# ou
python3 --version