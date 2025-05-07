# Etapas de Desenvolvimento da Plataforma IA Humanizada

Este documento descreve as fases propostas para o desenvolvimento da plataforma IA Humanizada (www.iahumanizada.com.br), começando com um Produto Mínimo Viável (MVP) e evoluindo progressivamente para incorporar funcionalidades avançadas, inspiradas na plataforma stammer.ai e nos requisitos definidos.

## Fase 1: MVP - Fundação Essencial (Foco: Criação e Implantação Básica)

**Objetivo:** Lançar rapidamente uma versão funcional que permita aos usuários criar agentes de IA simples, treiná-los com texto/documentos e implantá-los via widget web. Incluir funcionalidades básicas para agências iniciarem.

**Funcionalidades Principais (Detalhes em `mvp_features.md`):**

1.  **Gestão de Contas:** Cadastro, login, perfil básico.
2.  **Criação de Agentes:** Listagem, criação, editor de prompt simplificado (nome, objetivo, tom, instruções iniciais).
3.  **Base de Conhecimento (RAG Básico):** Upload de TXT/PDF, inserção de texto.
4.  **Integração LLM:** Suporte inicial a um LLM principal (via chave do usuário ou modelo padrão).
5.  **Implantação:** Widget web incorporável (customização básica de cor/nome), link de compartilhamento.
6.  **Agências (Fundação):** Estrutura de subcontas simplificada (organização), whitelabeling básico (logo no painel da agência).
7.  **Plataforma:** Interface responsiva (Português-BR), suporte multilíngue do agente (via LLM), documentação básica.

**Tecnologias Sugeridas (MVP):**

*   **Frontend:** Next.js (React) para responsividade e performance.
*   **Backend:** Python (Flask ou FastAPI) para integração com LLMs e lógica de negócios.
*   **Banco de Dados:** PostgreSQL ou MongoDB para armazenar dados de usuários, agentes e bases de conhecimento.
*   **LLM:** Integração inicial com API do Google Gemini ou OpenAI.

## Fase 2: Expansão de Funcionalidades e Integrações

**Objetivo:** Aprimorar a criação de agentes, adicionar integrações chave e melhorar a experiência do usuário.

**Novas Funcionalidades:**

*   **Editor de Prompt Avançado:** Adicionar campos para Cadeia de Pensamento, Regras Negativas, Exemplos (conforme documentação stammer.ai).
*   **Base de Conhecimento Avançada:** Implementar Web Scraping (extração de texto de URLs) e formato Q&A.
*   **Integrações Iniciais:**
    *   Zapier (via Webhooks) para conectar com outros apps.
    *   Google Agenda para funcionalidade básica de agendamento.
*   **Coleta de Leads:** Formulário pré-chat e extração de dados da conversa (com webhook para envio).
*   **Customização do Widget:** Mais opções de aparência (fonte, ícone, placeholders).
*   **Analytics Básicos:** Contagem de interações, visualização de conversas.
*   **Suporte a Múltiplos LLMs:** Permitir ao usuário escolher entre diferentes provedores (ex: Gemini, OpenAI, Claude) via chave de API.

## Fase 3: Recursos para Agências e Monetização

**Objetivo:** Fortalecer a oferta para agências, introduzir modelos de monetização e o marketplace.

**Novas Funcionalidades:**

*   **Sistema SaaS Completo:** Planos de assinatura, gerenciamento de créditos (mensagens, armazenamento), faturamento automático (integração com Stripe).
*   **Whitelabeling Completo:** Domínio personalizado para agências, opções avançadas de CSS, branding de emails.
*   **Gestão de Subcontas Avançada:** Permissões granulares, isolamento de dados entre clientes da agência.
*   **Marketplace Nativo (v1):**
    *   Agências podem publicar templates de agentes.
    *   Usuários podem navegar e usar templates (inicialmente gratuitos ou com modelo simples).
*   **API da Plataforma:** Expor endpoints para gerenciamento programático de agentes e conversas.
*   **Modo de Depuração:** Disponibilizar o modo de depuração para usuários avançados/agências.

## Fase 4: Inteligência Artificial Avançada e Experiência Aprimorada

**Objetivo:** Incorporar recursos de IA mais sofisticados e melhorar a humanização dos agentes.

**Novas Funcionalidades:**

*   **Construtor Visual de Fluxos (Drag-and-Drop):** Interface gráfica para desenhar fluxos de conversa complexos.
*   **IA Nativa na Plataforma:**
    *   Assistente para criação de prompts.
    *   Sugestões de treinamento para base de conhecimento.
    *   Interpretação de documentação de API para integrações personalizadas.
*   **Recursos Multimodais:** Suporte a entrada/saída de voz (integração com TTS/STT), possivelmente avatares (inicialmente simples).
*   **Detecção de Emoção:** Análise de sentimento nas conversas.
*   **Analytics Avançados:** Métricas como NPS, CSAT, tempo médio de atendimento.
*   **Testes A/B:** Para prompts e configurações de agentes.
*   **Suporte a Modelos Open-Source:** Integração com LLMs self-hosted ou via APIs como Ollama.

## Fases Futuras e Evolução Contínua

*   Expansão do Marketplace (modelos pagos, avaliações).
*   Integrações mais profundas (CRMs específicos, bancos de dados externos via credenciais).
*   Recursos de colaboração em equipe.
*   Otimizações de performance e escalabilidade.
*   Novos canais de implantação (WhatsApp via APIs como Evolution, Messenger, etc.).
*   Melhorias contínuas na UI/UX com base no feedback dos usuários.

**Observação:** Este roadmap é uma proposta inicial e pode ser ajustado com base no feedback do usuário, nas prioridades de negócio e nas descobertas durante o desenvolvimento de cada fase.
