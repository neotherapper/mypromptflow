#!/bin/bash

# Create directory structure
mkdir -p .claude/{commands,prompts/{meta-prompts,document-templates/{tier1,tier2,tier3,tier4}},tests}
mkdir -p ai/{knowledge/{strategic,product/{prd,epics,user-stories,acceptance-criteria,release-notes},user-experience/{research/{user-interviews,usability-testing,empathy-maps},design,journey-maps},technical/{api,database/schemas,architecture/c4-diagrams,security},business-analysis,quality-assurance/{test-plans,test-cases,uat-plans},compliance/security-docs},features/{_template/{requirements,design,technical,tests,analytics,meta},user-authentication},context,agents/{tier-specialists,feature-specialists,orchestrator},prompts/{document-templates/{tier1,tier2,tier3,tier4},meta-prompts,meta},scratchpads,tests}