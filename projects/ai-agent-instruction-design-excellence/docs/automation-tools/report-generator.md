# Report Generation Templates

**Input Requirements**: Real assessment data from automation tools
**Output Format**: Evidence-based findings with file references
**Template Selection**: Based on assessment scope (comprehensive/quick/dimensional)

## Templates

**Template 1: Comprehensive Report**
- Executive summary with overall score and classification
- 5-dimensional breakdown with evidence
- Improvement action plan with priorities

**Template 2: Quick Assessment** 
- Overall quality score
- Top 3 critical improvements
- Implementation recommendations

**Template 3: Dimensional Analysis**
- Detailed breakdown by dimension
- Specific evidence with line references
- Priority rankings

**Template Usage Commands**:
```bash
# Generate comprehensive report
./generate-report --template comprehensive --input assessment-data.json

# Generate quick assessment
./generate-report --template quick --input assessment-data.json --sections summary,score,improvements

# Generate dimensional analysis
./generate-report --template dimensional --input assessment-data.json --include-evidence
```