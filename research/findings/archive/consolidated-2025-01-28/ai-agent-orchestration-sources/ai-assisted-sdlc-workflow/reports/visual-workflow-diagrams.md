# Visual Diagrams for AI-Assisted SDLC Workflow

This document provides visual representations of the key workflows, team structures, and technical pipelines described in the AI-Assisted SDLC research.

## 1. High-Level AI-Assisted SDLC Flow

This diagram illustrates the end-to-end software development lifecycle, highlighting the key phases and the primary AI tools integrated at each step.

```mermaid
graph TD
    subgraph "Phase 1: Planning & Requirements"
        A[Business Requirement in Natural Language] -->|Claude Code / JIRA AI| B(Analyzed & Structured Requirement);
        B -->|Claude Code / JIRA AI| C{JIRA Ticket Created};
    end

    subgraph "Phase 2: Development & Implementation"
        C --> D[Sprint Planning];
        D -->|Claude Code / Gemini| E(Architecture & Design);
        E -->|Claude/Cursor/Copilot| F[Implementation & Coding];
    end

    subgraph "Phase 3: Review & Quality Assurance"
        F -->|Claude Code / AI Tools| G(Automated Code Review);
        G -->|AI-Generated Tests| H[Unit & Integration Testing];
    end

    subgraph "Phase 4: Deployment"
        H --> I[Staging Deployment];
        I -->|Playwright / AI Scripts| J(Automated E2E & UAT);
        J -->|Blue-Green Deployment| K[Production Release];
    end

    subgraph "Phase 5: Monitoring & Feedback"
        K -->|AI-Powered Monitoring| L(Real-time Performance & Business Metrics);
        L -->|AI Feedback Analysis| A;
    end

    style A fill:#f9f,stroke:#333,stroke-width:2px
    style K fill:#bbf,stroke:#333,stroke-width:2px
```

## 2. Team Interaction & Tool Ecosystem

This diagram shows the roles within the the platform team, the primary AI tools they use, and how they interact with the core development ecosystem.

```mermaid
graph TD
    subgraph "Development Team"
        HoE[Head of Engineering]
        FE[Lead Frontend Developer]
        BE[Lead Backend Developer]
        UX[UI/UX Designer]
    end

    subgraph "Primary AI Assistants"
        Claude[Claude Code Max]
        Gemini[Gemini CLI]
        Cursor[Cursor AI]
    end

    subgraph "Development Ecosystem"
        JIRA
        GitHub
        Figma
        Storybook
        CI_CD[CI/CD Pipeline]
    end

    %% Connections
    HoE ---|Architectural Decisions| Claude
    HoE ---|Large-scale Analysis| Gemini
    HoE --- JIRA & GitHub

    FE ---|Complex React Dev| Claude
    FE ---|Real-time Coding| Cursor
    FE --- Figma & Storybook & GitHub

    BE ---|Python & API Dev| Claude
    BE ---|Codebase Analysis| Gemini
    BE --- GitHub & CI_CD

    UX ---|Design-to-Code| Gemini
    UX --- Figma & Storybook

    Claude & Gemini ---|via MCP| JIRA
    Claude & Gemini ---|via MCP| GitHub
```

## 3. AI-Enhanced CI/CD Pipeline

This diagram details the Continuous Integration and Continuous Deployment pipeline, showing the specific stages where AI-powered checks and validations are integrated.

```mermaid
graph LR
    subgraph "CI: Continuous Integration"
        A[Developer Commits to GitHub] --> B{Build Triggered};
        B --> C[Build Application];
        C --> D("AI Security Scan (SonarQube + AI)");
        D --> E("AI Quality Gate (Code Review Bot)");
        E --> F("AI-Generated Tests (Unit & Integration)");
    end

    subgraph "CD: Continuous Deployment"
        F --> G{Merge to Develop};
        G --> H[Deploy to Staging];
        H --> I("Automated E2E Tests (Playwright + AI)");
        I --> J("UAT with Stakeholders");
        J --> K{Approve for Production};
        K --> L["Deploy to Production (Blue-Green)"];
        L --> M("AI-Powered Health Monitoring");
    end

    style F fill:#9f9,stroke:#333,stroke-width:2px
    style M fill:#bbf,stroke:#333,stroke-width:2px
```
