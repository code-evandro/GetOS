# GetOS — Documentação Técnica
Sistema de Gestão de Ordens de Serviço (OS) para Secretaria de Municipal de Orçamento, Planejamento, Finanças e Tecnologia da Informação – SMPOFTI, Setor STI.
Este documento consolida visão geral, requisitos, arquitetura, instalação, operação, manutenção e roadmap.
1) Visão Geral
- Objetivo: Centralizar abertura, acompanhamento e fechamento de Ordens de Serviço de TI, melhorando rastreabilidade, tempo de resposta e qualidade do atendimento aos servidores.
- Escopo atual: Cadastro de Setores e Servidores; criação/visualização/fechamento de OS; designação de técnico; filtros por data, técnico, setor, servidor e situação; geração de PDF da OS; dashboard com indicadores básicos (OS por mês, listagens por técnico/setor, recentes).
- Público-alvo: Equipe de TI (técnicos, triagem), servidores requisitantes, e administradores do sistema.
- Contexto de uso: Rede interna da Prefeitura (ambiente Windows). Execução em host local acessível via IP interno (https://192.168.0.153:8000))
2. Requisitos:
2.1 Requisitos Funcionais (RF)
1. RF-01 Cadastrar Setor (com: nome, sigla, secretaria, ramal opcional).
2. RF-02 Cadastrar Servidor (com: nome, matrícula, setor vinculado).
3. RF-03 Autenticação de usuário (login padrão Django para técnicos/administradores).
4. RF-04 Criar Ordem de Serviço com: servidor, setor, tipo, técnico designado, data, relato.
5. RF-05 Editar/visualizar OS; finalizar OS (alterar situação aberta/finalizada).
6. RF-06 Filtrar OS por data, técnico, setor, servidor e situação.
7. RF-07 Gerar PDF da OS (impressão/arquivamento).
8. RF-08 Dashboard: contagem de OS por mês; listas por técnico, por setor e OS recentes.
9. RF-09 Mensagens de validação/erro/sucesso em formulários (feedback ao usuário).
10. RF-10 Controle básico de perfis (técnicos via auth do Django; possibilidade de superusuário/admin).
2.2 Requisitos Não Funcionais (RNF)
1. RNF-01 Usabilidade: páginas com estilo unificado (gradiente, transparências, minimalista, responsivo básico).
2. RNF-02 Performance: respostas < 2s nas ações mais comuns em rede interna.
3. RNF-03 Segurança: autenticação, sessões seguras, ocultar SECRET_KEY em produção, restringir acesso via rede interna.
4. RNF-04 Manutenibilidade: separação por apps Django (core, setores, servidores, ordens), templates organizados.
5. RNF-05 Portabilidade: execução em Windows com Python 3.x e Django; possibilidade de portar para Linux.
6. RNF-06 Observabilidade: logs de aplicação e erros; capacidade futura de exportação/backup de dados.
2.3 Regras de Negócio (RN)
1. RN-01 Uma OS deve estar sempre associada a um Servidor e a um Setor.
2. RN-02 Um Técnico deve ser designado na abertura (ou posteriormente) e pode ser alterado.
3. RN-03 Ramal do Setor é opcional (pode ficar vazio).
4. RN-04 OS finalizada não deve ser editada sem registrar novo histórico (melhoria futura).
3) Arquitetura e Tecnologias
- Framework: Django (Python 3.x)
- Apps do projeto: core, setores, servidores, ordens.
- Templates/Front-end: HTML/CSS com estilo unificado.
- Banco de Dados: SQLite (desenvolvimento). Pode migrar para PostgreSQL em produção.
- Implantação atual: Host Windows, rede interna.
Modelos de Dados (resumo):
Setor: nome, sigla, secretaria, ramal (opcional).
Servidor: nome, matricula, setor (FK Setor).
Técnico: mapeado aos usuários do Django.
OrdemDeServico: servidor (FK), setor (FK), tipo, tecnico (FK), data, relato, criado_em, atualizado_em, finalizada (bool).
4) Instalação e Configuração
- Pré-requisitos: Windows 10/11, Python 3.x, PowerShell atualizado.
- Criar ambiente virtual, instalar dependências, aplicar migrações, criar superusuário, configurar settings.py, executar servidor.
- Script .BAT para execução rápida.
5) Operação do Sistema
- Perfis: Admin/Superusuário, Técnico, Servidor.
- Fluxos principais: Cadastro básico, Abrir OS, Acompanhar/Filtrar, Finalizar OS, Gerar PDF.
- Dashboard: gráfico OS por mês, listas por técnico, setor e OS recentes.
6) Segurança, Logs e Backup
- Acesso interno restrito, autenticação via Django Auth, logs configuráveis, backup periódico.
7) Testes e Qualidade
- Testes manuais e automatizados, revisão de UI.
8) Manutenção e Suporte
- Atualizações, migrações, monitoramento.
9) Roadmap
- Histórico de alterações, permissões refinadas, PostgreSQL, relatórios exportáveis, notificações, API REST.
10) Checklist de Entrega
- Código, ambiente virtual, migrações, acesso interno, páginas funcionando, dashboard, backup e script .bat.
