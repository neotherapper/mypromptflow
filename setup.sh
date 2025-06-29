#!/bin/bash

echo "🚀 Setting up AI Knowledge Base..."

# Create directory structure
mkdir -p .claude/{commands,prompts/{meta-prompts,document-templates/{tier1,tier2,tier3,tier4}},tests}
mkdir -p ai/{knowledge/{strategic,product/{prd,epics,user-stories,acceptance-criteria,release-notes},user-experience/{research/{user-interviews,usability-testing,empathy-maps},design,journey-maps},technical/{api,database/{schemas},architecture/{c4-diagrams},security},business-analysis,quality-assurance/{test-plans,test-cases,uat-plans},compliance/{security-docs}},features/_template/{requirements,design,technical,tests,analytics,meta},context,agents/{tier-specialists,feature-specialists,orchestrator}}

# Create template files
echo "Creating configuration files..."
touch ai/context/{dependencies.yaml,document-registry.yaml,feature-registry.yaml,tier-configuration.yaml}
touch .claude/settings.json
touch .claude/tests/{document-structure-tests.yaml,dependency-validation-tests.yaml,ai-context-tests.yaml}

echo "✅ Setup complete! See README.md for next steps."