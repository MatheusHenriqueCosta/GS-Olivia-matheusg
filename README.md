# GS-Olivia-matheusg

# 🚀 Pipeline CI/CD Automatizado - Python no Azure

Este projeto implementa um fluxo completo de Integração e Entrega Contínua (CI/CD) para aplicações Python, integrando Jenkins, SonarQube e Azure App Service.

## 🌐 Visão Geral

Pipeline automatizado que realiza:
- ✅ Análise estática de código com SonarQube
- ✅ Testes automatizados com cobertura
- ✅ Deploy contínuo no Azure App Service
- ✅ Monitoramento básico com alertas

## ⚙️ Pré-requisitos

### Infraestrutura
- Servidor Jenkins (v2.319+)
- Instância SonarQube (v8.9+)
- Conta Azure com permissões de Contributor

### Plugins Jenkins
- SonarQube Scanner
- Azure App Service
- Pipeline

### Ferramentas
- Python 3.9+
- Azure CLI
- Git

## 🛠️ Configuração

### 1. Credenciais no Jenkins
| Tipo            | ID              | Descrição                     |
|----------------|----------------|------------------------------|
| Secret Text     | `sonarqube-token` | Token do SonarQube           |
| Username/Password | `azure-sp`    | Service Principal do Azure   |

### 2. Variáveis de Ambiente
Configure no Jenkins:
```bash
AZURE_APP_NAME="meu-app-python"
AZURE_RG="GS_olivia"
AZURE_TENANT_ID="11dbbfe2-89b8-4549-be10-cec364e59551"

### 🔄 Fluxo do Pipeline
Build:
  Cria ambiente virtual Python
  Instala dependências (requirements.txt)

Testes:
  Executa testes unitários
  Gera relatório de cobertura (coverage.xml)

Análise de Código:
  Envia métricas para SonarQube
  Valida Quality Gate

Deploy:
  Empacota aplicação (app.zip)
  Faz deploy no Azure App Service

Monitoramento:
  Configura alertas básicos (CPU, HTTP 500)

### 🚧 Melhorias Futuras

Implementar canary deployment
Adicionar testes de integração
Dashboard detalhado no Azure Monitor
Notificações no Slack
