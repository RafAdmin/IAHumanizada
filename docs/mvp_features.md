# Funcionalidades Essenciais para o MVP da Plataforma IA Humanizada

Com base na análise da plataforma stammer.ai (documentação e screenshots) e nos requisitos definidos, as seguintes funcionalidades são propostas como essenciais para o Produto Mínimo Viável (MVP) da IA Humanizada:

## 1. Gestão de Contas e Autenticação

*   **Cadastro e Login de Usuários:** Permitir que novos usuários (tanto individuais quanto agências) se cadastrem e acessem a plataforma de forma segura.
*   **Gerenciamento Básico de Perfil:** Opção para usuários atualizarem informações básicas da conta (nome, email, senha).

## 2. Criação e Gerenciamento de Agentes de IA

*   **Listagem e Criação de Agentes:** Interface para visualizar os agentes criados e adicionar novos agentes.
*   **Editor de Prompt Simplificado:** Um formulário guiado para definir a identidade central do agente, incluindo:
    *   Nome do Agente
    *   Objetivo Principal (O que o agente deve fazer?)
    *   Tom/Personalidade Básica (Ex: Amigável, Profissional, Formal)
    *   Instruções Iniciais (Um prompt base inicial, possivelmente com um template padrão editável).
*   **Base de Conhecimento (RAG - Básico):**
    *   Upload de Arquivos: Permitir upload de arquivos de texto simples (.txt) e PDF para treinar o agente.
    *   Inserção de Texto: Área para colar ou digitar diretamente informações para a base de conhecimento.
*   **Integração com LLM:** Suporte inicial a um modelo de linguagem grande (LLM) principal (ex: Gemini ou API do OpenAI via chave do usuário) para processar as conversas.

## 3. Implantação Básica do Agente

*   **Widget de Chat Web Incorporável:** Geração automática de um snippet de código (script/iframe) para que o usuário possa incorporar o agente de chat em seu próprio site.
    *   Customização Básica: Permitir alterar cores primárias do widget e o nome exibido.
*   **Link de Compartilhamento:** Geração de uma URL única para cada agente, permitindo testes e compartilhamento direto sem necessidade de incorporação.

## 4. Funcionalidades Básicas para Agências (Fundação)

*   **Estrutura de Subcontas (Simplificada):** Possibilidade de uma conta principal (agência) gerenciar múltiplos agentes, talvez com um sistema de tags ou pastas para organizar por cliente (sem isolamento completo de dados ou permissões granulares no MVP).
*   **Whitelabeling Básico:** Permitir que contas de agência façam upload de seu próprio logotipo para ser exibido dentro do painel de gerenciamento (aplicado à interface da agência, não necessariamente ao widget do cliente final no MVP).

## 5. Essenciais da Plataforma

*   **Interface Web Responsiva:** O painel de controle deve ser acessível e funcional em diferentes tamanhos de tela (desktop, tablet).
*   **Suporte a Idiomas (Agente):** O agente de IA deve ser capaz de interagir em múltiplos idiomas, aproveitando a capacidade multilíngue do LLM subjacente. A interface da plataforma será inicialmente em Português Brasileiro.
*   **Documentação/Ajuda Básica:** Uma seção inicial com guias simples sobre como criar e implantar um agente.

## Funcionalidades Excluídas do MVP (Fases Futuras)

*   Editor de prompt avançado (Cadeia de Pensamento, Regras Negativas, Exemplos).
*   Base de conhecimento avançada (Web Scraping, Q&A, sugestões de treino).
*   Construtor visual de fluxos (Drag-and-drop).
*   Integrações avançadas (Zapier, Google Agenda, CRMs específicos, APIs externas, Banco de Dados).
*   Sistema completo de faturamento SaaS e gestão de assinaturas.
*   Marketplace nativo para agentes e templates.
*   Whitelabeling completo (domínio personalizado, CSS customizado, branding de email).
*   Recursos avançados de agente (Voz, multimodalidade, emoção, avatares).
*   Analytics detalhados (NPS, CSAT).
*   Suporte a múltiplos LLMs simultaneamente ou modelos open-source.
*   Funcionalidades assistidas por IA na plataforma.
*   Coleta de leads e agendamento.
*   Modo de depuração para usuários.

