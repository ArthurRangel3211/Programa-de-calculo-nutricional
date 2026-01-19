# 🥗 Sistema Nutri Pro - Secure Patient Management

> **Projeto de Engenharia de Software focado em AppSec e DevSecOps.**

O **Nutri Pro** é uma aplicação web para gestão de pacientes e cálculo nutricional, desenvolvida com foco rigoroso em segurança da informação, controle de acesso e proteção de dados.

O projeto implementa práticas modernas de **Secure Coding**, incluindo autenticação robusta, criptografia de credenciais e auditoria automatizada de código.

---

## 🚀 Funcionalidades

### 🔐 Segurança e Autenticação (Destaque)
* **RBAC (Role-Based Access Control):** Sistema de permissões segregado entre **Admin** (Gestão Total) e **User** (Operacional).
* **CSPRNG (Cryptographically Secure PRNG):** Geração de senhas utilizando a biblioteca `secrets` (resistente a ataques de predição), substituindo o `random` padrão.
* **Hashing Seguro:** Senhas armazenadas utilizando SHA-256 (não salvamos texto plano).
* **Política de Primeiro Acesso:** Flag `force_change` no banco de dados obriga o usuário a redefinir a senha provisória no primeiro login.
* **Integridade de Dados:** Restrições de unicidade (`UNIQUE CONSTRAINT`) no SQLite para prevenir inconsistências e duplicidade de usuários.

### 🛠️ Funcionalidades do Sistema
* **Cadastro de Pacientes:** Registro completo com cálculo automático de IMC.
* **Gestão de Equipe (Admin):**
    * Cadastro de novos nutricionistas/funcionários.
    * Envio **automático** de credenciais por e-mail (SMTP).
    * Remoção de acesso (Revogação imediata).
* **Visualização de Dados:** Dashboard tabular para análise da base de pacientes.

---

## 🛡️ Auditoria e Qualidade (DevSecOps)

Este projeto foi auditado utilizando ferramentas de análise estática de segurança (SAST) e composição de software (SCA):

| Ferramenta | Tipo | Resultado |
| :--- | :--- | :--- |
| **Bandit** | SAST (Código) | ✅ **No issues identified** (0 vulnerabilidades) |
| **Safety CI** | SCA (Libs) | ✅ **0 vulnerabilidades** em dependências |

---

## 💻 Tecnologias Utilizadas

* **Linguagem:** Python 3.14+
* **Frontend/Framework:** Streamlit
* **Banco de Dados:** SQLite3
* **Análise de Dados:** Pandas
* **Segurança:** Hashlib, Secrets, Dotenv
* **Automação:** SMTP (Gmail Automation)

---

## ⚙️ Como Rodar o Projeto Localmente

### Pré-requisitos
* Python instalado.
* Git instalado.

### 1. Clonar o repositório
```bash
git clone [https://github.com/ArthurRangel3211/Programa-de-c-lculo-nutricional-.git](https://github.com/ArthurRangel3211/Programa-de-c-lculo-nutricional-.git)
cd Programa-de-c-lculo-nutricional-