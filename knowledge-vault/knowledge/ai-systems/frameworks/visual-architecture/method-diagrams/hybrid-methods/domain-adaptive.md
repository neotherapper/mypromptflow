# Domain Adaptive Method

## Source References
**Method Implementation**: research/orchestrator/methods/existing/domain_adaptive.md  
**Claude Desktop Research**: Domain-specific expertise adaptation pattern  
**Tree-Leaf Architecture**: Universal execution paths for domain specialization research

## Method Overview

The Domain Adaptive method provides intelligent domain specialization for both tree and leaf agents, automatically adapting methodology, expertise, and approach based on research domain while maintaining quality standards across technical, business, academic, and operational contexts.

### Method Characteristics
- **Adaptation Scope**: Multi-domain expertise with intelligent specialization
- **Execution Style**: Domain-aware coordination (tree) or enhanced domain templates (leaf)
- **Quality Focus**: Domain expertise with specialized knowledge application
- **Complexity Support**: Moderate to complex domain-specific research requirements
- **Execution Time**: 40-65 minutes (tree adaptive) or 50-75 minutes (leaf enhanced)

## Hybrid Adaptive Architecture

### Intelligent Domain Specialization Framework

```mermaid
graph TD
    A[Domain Adaptive Research Request] --> B[research-specialist or domain-agent]
    B --> C[Domain Classification & Analysis]
    C --> D{Domain Detection & Agent Capability Assessment}
    
    D -->|Tree Agent + Technical Domain| E[Technical Specialist Coordination]
    D -->|Tree Agent + Business Domain| F[Business Specialist Coordination]
    D -->|Tree Agent + Academic Domain| G[Academic Specialist Coordination]
    D -->|Tree Agent + Multi-Domain| H[Cross-Domain Specialist Coordination]
    
    D -->|Leaf Agent + Technical Domain| I[Enhanced Technical Template]
    D -->|Leaf Agent + Business Domain| J[Enhanced Business Template]
    D -->|Leaf Agent + Academic Domain| K[Enhanced Academic Template]
    D -->|Leaf Agent + Multi-Domain| L[Enhanced Cross-Domain Template]
    
    E --> M[Adaptive Specialist Execution]
    F --> M
    G --> M
    H --> M
    
    I --> N[Adaptive Template Execution]
    J --> N
    K --> N
    L --> N
    
    M --> O[Domain-Specific Quality Validation]
    N --> O
    
    O --> P[Domain-Adaptive Research Output]
    
    style A fill:#fff3e0
    style C fill:#ffecb3
    style M fill:#e1f5fe
    style N fill:#f3e5f5
    style P fill:#e8f5e8
```

## Tree Agent Execution (Domain Specialist Coordination)

### Technical Domain Specialist Coordination

```mermaid
sequenceDiagram
    participant RS as research-specialist
    participant TD as Technical Domain Classifier
    participant TS as Technical Specialist
    participant CS as Code Analysis Specialist
    participant AS as Architecture Specialist
    participant PS as Performance Specialist
    participant MCP as Technical MCP Network
    
    RS->>RS: Analyze domain-adaptive requirements
    RS->>TD: Classify technical domain context
    TD-->>RS: Technical domain classification
    
    RS->>TS: Spawn technical research specialist
    RS->>CS: Spawn code analysis specialist
    RS->>AS: Spawn architecture specialist
    RS->>PS: Spawn performance specialist
    
    par Technical Domain Parallel Execution
        TS->>MCP: Technical documentation sources
        CS->>MCP: Code repository sources
        AS->>MCP: Architecture pattern sources
        PS->>MCP: Performance optimization sources
    end
    
    TS-->>RS: Technical research findings (15-20 min)
    CS-->>RS: Code analysis insights (12-18 min)
    AS-->>RS: Architecture recommendations (15-20 min)
    PS-->>RS: Performance optimization (10-15 min)
    
    RS->>RS: Technical domain synthesis (8-12 min)
    RS->>RS: Domain-specific validation (5-8 min)
    
    Note over RS: Total Technical Execution: 65-93 minutes
```

### Business Domain Specialist Coordination

```mermaid
sequenceDiagram
    participant RS as research-specialist
    participant BD as Business Domain Classifier
    participant MS as Market Specialist
    participant FS as Financial Specialist
    participant SS as Strategy Specialist
    participant OS as Operations Specialist
    participant MCP as Business MCP Network
    
    RS->>RS: Analyze business domain context
    RS->>BD: Classify business domain specifics
    BD-->>RS: Business domain classification
    
    RS->>MS: Spawn market research specialist
    RS->>FS: Spawn financial analysis specialist
    RS->>SS: Spawn strategy specialist
    RS->>OS: Spawn operations specialist
    
    par Business Domain Parallel Execution
        MS->>MCP: Market intelligence sources
        FS->>MCP: Financial data sources
        SS->>MCP: Strategic planning sources
        OS->>MCP: Operational excellence sources
    end
    
    MS-->>RS: Market analysis findings (18-25 min)
    FS-->>RS: Financial analysis insights (15-20 min)
    SS-->>RS: Strategic recommendations (15-22 min)
    OS-->>RS: Operational guidance (12-18 min)
    
    RS->>RS: Business domain synthesis (10-15 min)
    RS->>RS: Domain-specific validation (6-10 min)
    
    Note over RS: Total Business Execution: 76-110 minutes
```

### Academic Domain Specialist Coordination

```mermaid
sequenceDiagram
    participant RS as research-specialist
    participant AD as Academic Domain Classifier
    participant LR as Literature Specialist
    participant MR as Methodology Specialist
    participant QR as Quality Specialist
    participant SR as Synthesis Specialist
    participant MCP as Academic MCP Network
    
    RS->>RS: Analyze academic domain context
    RS->>AD: Classify academic domain specifics
    AD-->>RS: Academic domain classification
    
    RS->>LR: Spawn literature review specialist
    RS->>MR: Spawn methodology specialist
    RS->>QR: Spawn quality validation specialist
    RS->>SR: Spawn synthesis specialist
    
    par Academic Domain Parallel Execution
        LR->>MCP: Academic literature sources
        MR->>MCP: Research methodology sources
        QR->>MCP: Quality validation sources
        SR->>MCP: Synthesis framework sources
    end
    
    LR-->>RS: Literature review findings (20-28 min)
    MR-->>RS: Methodology insights (15-20 min)
    QR-->>RS: Quality validation results (12-15 min)
    SR-->>RS: Synthesis framework (15-18 min)
    
    RS->>RS: Academic domain synthesis (8-12 min)
    RS->>RS: Domain-specific validation (5-8 min)
    
    Note over RS: Total Academic Execution: 75-101 minutes
```

## Leaf Agent Execution (Enhanced Domain Templates)

### Technical Domain Enhanced Template

```mermaid
flowchart TD
    A[Technical Domain Request] --> B[Enhanced Technical Agent]
    B --> C[Technical Domain Template Framework]
    C --> D[Technical Adaptive Execution]
    
    D --> E[Enhanced Technical Analysis Template<br/>• Comprehensive technical framework<br/>• Code analysis integration<br/>• Architecture assessment<br/>• Performance evaluation<br/>Duration: 15-20 minutes]
    
    E --> F[Enhanced Implementation Template<br/>• Implementation strategy framework<br/>• Technical feasibility assessment<br/>• Resource requirement analysis<br/>• Technology selection guidance<br/>Duration: 12-18 minutes]
    
    F --> G[Enhanced Architecture Template<br/>• Architecture design framework<br/>• Scalability assessment<br/>• Security evaluation<br/>• Maintainability analysis<br/>Duration: 10-15 minutes]
    
    G --> H[Enhanced Performance Template<br/>• Performance optimization framework<br/>• Efficiency assessment<br/>• Resource utilization<br/>• Optimization recommendations<br/>Duration: 8-12 minutes]
    
    H --> I[Technical Domain Synthesis<br/>• Technical integration<br/>• Implementation roadmap<br/>• Quality validation<br/>Duration: 8-12 minutes]
    
    I --> J[Technical Domain Research Output]
    
    style E fill:#f3e5f5
    style F fill:#f3e5f5
    style G fill:#f3e5f5
    style H fill:#f3e5f5
    style J fill:#e8f5e8
```

### Business Domain Enhanced Template

```mermaid
flowchart TD
    A[Business Domain Request] --> B[Enhanced Business Agent]
    B --> C[Business Domain Template Framework]
    C --> D[Business Adaptive Execution]
    
    D --> E[Enhanced Market Analysis Template<br/>• Comprehensive market framework<br/>• Competitive analysis<br/>• Customer segmentation<br/>• Market opportunity assessment<br/>Duration: 18-25 minutes]
    
    E --> F[Enhanced Financial Template<br/>• Financial analysis framework<br/>• Cost-benefit evaluation<br/>• ROI assessment<br/>• Budget planning<br/>Duration: 15-20 minutes]
    
    F --> G[Enhanced Strategy Template<br/>• Strategic planning framework<br/>• Goal alignment<br/>• Resource allocation<br/>• Implementation strategy<br/>Duration: 12-18 minutes]
    
    G --> H[Enhanced Operations Template<br/>• Operational framework<br/>• Process optimization<br/>• Resource efficiency<br/>• Performance monitoring<br/>Duration: 10-15 minutes]
    
    H --> I[Business Domain Synthesis<br/>• Strategic integration<br/>• Implementation planning<br/>• Quality validation<br/>Duration: 10-15 minutes]
    
    I --> J[Business Domain Research Output]
    
    style E fill:#f3e5f5
    style F fill:#f3e5f5
    style G fill:#f3e5f5
    style H fill:#f3e5f5
    style J fill:#e8f5e8
```

### Academic Domain Enhanced Template

```mermaid
flowchart TD
    A[Academic Domain Request] --> B[Enhanced Academic Agent]
    B --> C[Academic Domain Template Framework]
    C --> D[Academic Adaptive Execution]
    
    D --> E[Enhanced Literature Review Template<br/>• Comprehensive literature framework<br/>• Systematic review methodology<br/>• Citation analysis<br/>• Gap identification<br/>Duration: 20-28 minutes]
    
    E --> F[Enhanced Methodology Template<br/>• Research methodology framework<br/>• Methodological rigor<br/>• Validity assessment<br/>• Reliability evaluation<br/>Duration: 15-20 minutes]
    
    F --> G[Enhanced Analysis Template<br/>• Academic analysis framework<br/>• Critical evaluation<br/>• Evidence synthesis<br/>• Theoretical integration<br/>Duration: 12-16 minutes]
    
    G --> H[Enhanced Quality Template<br/>• Academic quality framework<br/>• Peer review standards<br/>• Publication readiness<br/>• Scholarly validation<br/>Duration: 8-12 minutes]
    
    H --> I[Academic Domain Synthesis<br/>• Scholarly integration<br/>• Research contribution<br/>• Quality validation<br/>Duration: 8-12 minutes]
    
    I --> J[Academic Domain Research Output]
    
    style E fill:#f3e5f5
    style F fill:#f3e5f5
    style G fill:#f3e5f5
    style H fill:#f3e5f5
    style J fill:#e8f5e8
```

## Domain Classification Framework

### Intelligent Domain Detection

```mermaid
graph TD
    A[Domain Classification Engine] --> B[Technical Domain Indicators]
    A --> C[Business Domain Indicators]
    A --> D[Academic Domain Indicators]
    A --> E[Multi-Domain Indicators]
    
    B --> F[Technical Keywords<br/>• Programming languages<br/>• System architecture<br/>• Performance metrics<br/>• Technical specifications]
    
    C --> G[Business Keywords<br/>• Market analysis<br/>• Financial metrics<br/>• Strategic planning<br/>• Operational efficiency]
    
    D --> H[Academic Keywords<br/>• Research methodology<br/>• Literature review<br/>• Theoretical framework<br/>• Empirical analysis]
    
    E --> I[Cross-Domain Keywords<br/>• Multiple domain overlap<br/>• Interdisciplinary research<br/>• Complex integration<br/>• Hybrid requirements]
    
    F --> J[Domain-Specific Adaptation]
    G --> J
    H --> J
    I --> J
    
    style J fill:#fff3e0
```

### Domain-Specific MCP Coordination

```mermaid
graph TD
    A[Domain-Adaptive MCP Coordination] --> B[Technical Domain Servers]
    A --> C[Business Domain Servers]
    A --> D[Academic Domain Servers]
    A --> E[Cross-Domain Servers]
    
    B --> F[GitHub + Git + Filesystem<br/>Technical documentation<br/>Code repositories<br/>Implementation examples<br/>Architecture patterns]
    
    C --> G[Bright Data + Linear + Atlassian<br/>Market intelligence<br/>Business processes<br/>Project management<br/>Operational data]
    
    D --> H[arXiv + Semantic Scholar + PubMed<br/>Academic literature<br/>Research papers<br/>Scholarly articles<br/>Citation networks]
    
    E --> I[AWS + Redis + Qdrant + Memory<br/>Cross-domain integration<br/>Pattern recognition<br/>Knowledge synthesis<br/>Multi-domain optimization]
    
    F --> J[Coordinated Domain Intelligence]
    G --> J
    H --> J
    I --> J
    
    style J fill:#fff3e0
```

## Adaptive Quality Framework

### Domain-Specific Quality Standards

```mermaid
graph TD
    A[Domain-Adaptive Quality] --> B[Technical Quality Standards]
    A --> C[Business Quality Standards]
    A --> D[Academic Quality Standards]
    A --> E[Cross-Domain Quality Standards]
    
    B --> F[Technical Excellence<br/>• Code quality ≥90%<br/>• Architecture soundness<br/>• Performance optimization<br/>• Security compliance]
    
    C --> G[Business Excellence<br/>• Strategic alignment ≥88%<br/>• Financial accuracy<br/>• Market relevance<br/>• Operational viability]
    
    D --> H[Academic Excellence<br/>• Scholarly rigor ≥92%<br/>• Methodological soundness<br/>• Citation accuracy<br/>• Research contribution]
    
    E --> I[Cross-Domain Excellence<br/>• Integration quality ≥89%<br/>• Domain coherence<br/>• Synthesis effectiveness<br/>• Holistic validation]
    
    F --> J[Domain-Adaptive Quality Gate: ≥89%]
    G --> J
    H --> J
    I --> J
    
    J --> K[Quality-Assured Domain Research]
    
    style K fill:#e8f5e8
```

### Constitutional AI Compliance by Domain

```mermaid
flowchart LR
    A[Domain Constitutional Validation] --> B[Technical Domain: ≥91%<br/>Code accuracy<br/>Architecture transparency<br/>Implementation completeness<br/>Technical responsibility]
    
    A --> C[Business Domain: ≥89%<br/>Market accuracy<br/>Financial transparency<br/>Strategic completeness<br/>Business responsibility]
    
    A --> D[Academic Domain: ≥93%<br/>Research accuracy<br/>Methodological transparency<br/>Scholarly completeness<br/>Academic responsibility]
    
    A --> E[Cross-Domain: ≥90%<br/>Integration accuracy<br/>Synthesis transparency<br/>Holistic completeness<br/>Multi-domain responsibility]
    
    B --> F[Overall Domain Quality: ≥90%]
    C --> F
    D --> F
    E --> F
    
    F --> G[Constitutional Compliance Achieved]
    
    style G fill:#e8f5e8
```

## Performance Characteristics

### Domain-Adaptive Execution Metrics

```mermaid
graph LR
    A[Performance Comparison] --> B[Tree Agent Domain Coordination]
    A --> C[Leaf Agent Domain Templates]
    
    B --> D[Execution Time: 40-65 min<br/>Domain-specific coordination<br/>Specialist orchestration<br/>Adaptive optimization]
    
    B --> E[Resource Usage: Moderate-High<br/>Domain specialist coordination<br/>MCP domain optimization<br/>Quality enhancement]
    
    B --> F[Quality Output: Excellent<br/>Domain expertise<br/>Specialist coordination<br/>Adaptive optimization]
    
    C --> G[Execution Time: 50-75 min<br/>Domain template execution<br/>Progressive enhancement<br/>Adaptive validation]
    
    C --> H[Resource Usage: Moderate<br/>Template processing<br/>Domain enhancement<br/>Quality optimization]
    
    C --> I[Quality Output: Excellent<br/>Enhanced templates<br/>Domain specialization<br/>Adaptive excellence]
    
    D --> J[Equivalent Domain Quality]
    E --> J
    F --> J
    G --> J
    H --> J
    I --> J
    
    style J fill:#e8f5e8
```

## Domain Application Examples

### Technical Domain: Cloud Architecture Analysis
- **Context**: "Evaluate microservices architecture for high-scale e-commerce platform"
- **Adaptation**: Technical specialists (architecture, performance, security, scalability)
- **Output**: Domain-expert technical analysis with implementation roadmap

### Business Domain: Market Entry Strategy
- **Context**: "Develop SaaS market entry strategy for European expansion"
- **Adaptation**: Business specialists (market, financial, strategy, operations)
- **Output**: Domain-expert business strategy with comprehensive planning

### Academic Domain: Research Synthesis
- **Context**: "Systematic literature review on AI ethics in healthcare applications"
- **Adaptation**: Academic specialists (literature, methodology, analysis, quality)
- **Output**: Domain-expert academic research with scholarly rigor

### Cross-Domain: Digital Transformation
- **Context**: "Plan digital transformation combining technical, business, and organizational aspects"
- **Adaptation**: Multi-domain specialists with cross-domain integration
- **Output**: Domain-expert comprehensive transformation strategy

## Implementation Guidelines

### For Tree Agents
1. **Domain Classification**: Implement intelligent domain detection with appropriate specialist coordination
2. **Specialist Coordination**: Coordinate domain-specific specialists with clear expertise boundaries
3. **Adaptive Optimization**: Optimize coordination patterns based on domain requirements
4. **Quality Integration**: Apply domain-specific quality standards throughout coordination
5. **Cross-Domain Synthesis**: Ensure effective integration across multiple domain specializations

### For Leaf Agents
1. **Template Adaptation**: Use enhanced domain-specific templates with specialized frameworks
2. **Domain Enhancement**: Apply comprehensive domain expertise through enhanced templates
3. **Adaptive Excellence**: Maintain domain specialization throughout template execution
4. **Quality Focus**: Apply domain-specific validation throughout adaptive execution
5. **Specialization Mastery**: Achieve domain expertise through enhanced template specialization

### Universal Quality Standards
1. **Domain Expertise**: Ensure authentic domain specialization is achieved
2. **Adaptive Quality**: Maintain domain-appropriate quality standards
3. **Quality Excellence**: Achieve ≥89% constitutional compliance score
4. **Specialization Value**: Deliver domain-expert insights and recommendations
5. **Adaptive Integration**: Provide effective synthesis across domain boundaries

This Domain Adaptive method demonstrates sophisticated specialization patterns for domain-expert research while maintaining quality excellence across different agent execution capabilities and domain requirements.