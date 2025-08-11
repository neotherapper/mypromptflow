#!/usr/bin/env python3
"""
Test Enhanced Topic Scoring with Claude Intelligence
"""

import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.append(str(Path(__file__).parent))

try:
    # Import with the correct filename (hyphenated)
    import importlib.util
    spec = importlib.util.spec_from_file_location("topic_scoring_engine", 
                                                str(Path(__file__).parent / "topic-scoring-engine.py"))
    topic_scoring_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(topic_scoring_module)
    TopicScoringEngine = topic_scoring_module.TopicScoringEngine
    print("✅ Successfully imported TopicScoringEngine")
except ImportError as e:
    print(f"❌ Failed to import TopicScoringEngine: {e}")
    sys.exit(1)

def test_enhanced_scoring():
    """Test the enhanced scoring system with Claude intelligence"""
    
    # Initialize the enhanced scorer
    config_path = str(Path(__file__).parent / "priority-topics.json")
    scorer = TopicScoringEngine(config_path)
    
    # Test content items
    test_content = [
        {
            'title': 'Advanced Claude Code Workflows for AI-Assisted Development',
            'description': 'Learn how to use Claude Code for automated development workflows with meta-prompting techniques',
            'content': '''
            # Claude Code Development Workflow
            
            This guide demonstrates end-to-end Claude Code workflows for AI-assisted development.
            
            ## Constitutional AI Principles
            Claude Code follows Constitutional AI principles to ensure responsible AI assistance.
            
            ```python
            # Example Claude Code automation
            def automated_development_workflow():
                claude_response = claude_api.complete(
                    prompt="Generate optimal React component structure",
                    context="Following best practices and safety considerations"
                )
                return claude_response
            ```
            ''',
            'source': 'claude.ai',
            'url': 'https://claude.ai/docs/workflows',
            'author': 'Anthropic Team',
            'platform': 'documentation',
            'score': 95,
            'comments': 45,
            'views': 5000,
            'published_date': '2025-07-31T10:00:00Z',
            'metadata': {'official': True, 'verified': True}
        },
        {
            'title': 'React TypeScript Best Practices',
            'description': 'Modern React development with TypeScript patterns',
            'content': 'Learn advanced React patterns with TypeScript for better type safety',
            'source': 'reactjs.org',
            'url': 'https://reactjs.org/docs/best-practices',
            'author': 'React Team',
            'platform': 'documentation',
            'score': 80,
            'comments': 30,
            'views': 3000,
            'published_date': '2025-07-30T14:00:00Z'
        },
        {
            'title': 'Meta-prompting Techniques with Claude AI',
            'description': 'Advanced prompt engineering and chain of thought reasoning',
            'content': '''
            # Meta-Prompting with Claude
            
            This guide covers advanced meta-prompting techniques for Claude AI:
            
            - Chain of thought reasoning
            - Few-shot prompting examples
            - Constitutional prompting methods
            - Workflow automation patterns
            ''',
            'source': 'community',
            'url': 'https://example.com/meta-prompting',
            'author': 'AI Researcher',
            'platform': 'blog',
            'score': 85,
            'comments': 25,
            'views': 2500,
            'published_date': '2025-07-31T08:00:00Z'
        }
    ]
    
    print("\n🧪 Testing Enhanced Topic Scoring with Claude Intelligence")
    print("=" * 70)
    
    for i, content in enumerate(test_content, 1):
        print(f"\n📝 Content {i}: {content['title'][:50]}...")
        
        try:
            scored_content = scorer.score_content_item(content)
            
            print(f"🎯 Final Score: {scored_content.final_score:.3f}")
            print(f"📊 Base Score: {scored_content.base_score:.3f}")
            print(f"🚀 Priority Score: {scored_content.priority_score:.3f}")
            print(f"🏷️  Detected Topics: {scored_content.detected_priority_topics}")
            
            # Display Claude enhancement details if available
            claude_enhancement = scored_content.score_breakdown.get('claude_enhancement')
            if claude_enhancement:
                print(f"🤖 Claude Intelligence:")
                print(f"   Category: {claude_enhancement.get('topic_category', 'N/A')}")
                print(f"   Multiplier: {claude_enhancement.get('topic_multiplier', 1.0):.2f}x")
                print(f"   Quality Tier: {claude_enhancement.get('quality_tier', 'N/A')}")
                print(f"   Confidence: {claude_enhancement.get('claude_confidence', 0.0):.2f}")
                
                bonuses = claude_enhancement.get('bonuses', {})
                if any(bonuses.values()):
                    print(f"   Bonuses:")
                    for bonus_type, value in bonuses.items():
                        if value > 0:
                            print(f"     {bonus_type}: +{value:.3f}")
            else:
                print(f"🤖 Claude Intelligence: Not applicable")
            
            print(f"📈 Calculation: {scored_content.score_breakdown.get('calculation', 'N/A')}")
            
        except Exception as e:
            print(f"❌ Error scoring content: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n✅ Enhanced scoring test completed!")

if __name__ == "__main__":
    test_enhanced_scoring()