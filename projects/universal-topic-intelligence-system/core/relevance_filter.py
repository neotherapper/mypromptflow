#!/usr/bin/env python3
"""
Relevance Filter for Universal Topic Intelligence System
Filters out irrelevant content based on configurable rules
"""

import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class RelevanceConfig:
    """Configuration for relevance filtering"""
    
    # Topics we care about
    relevant_topics = [
        "claude", "anthropic", "opus", "sonnet", "haiku",
        "claude code", "claude desktop", "constitutional ai",
        "react", "typescript", "javascript", "next.js", "vue", "svelte",
        "frontend", "ui", "ux", "components", "hooks",
        "ai coding", "cursor", "copilot", "github copilot",
        "prompt engineering", "prompting", "few shot", "chain of thought",
        "llm", "language model", "gpt", "gemini", "mistral",
        "ai development", "ai tools", "ai applications",
        "mcp", "model context protocol", "integration",
        "langchain", "llamaindex", "rag", "retrieval augmented",
        "api", "rest", "graphql", "websocket",
        "developer productivity", "development tools"
    ]
    
    # Topics we DON'T care about
    irrelevant_topics = [
        # Hardware & Infrastructure
        "voltage scaling", "power efficiency", "hpc", "high performance computing",
        "quantum computing", "quantum algorithms", "qubits",
        "gpu optimization", "cuda", "tensor cores", "hardware acceleration",
        "distributed computing", "cluster computing", "supercomputer",
        "fpga", "asic", "chip design", "semiconductor",
        
        # Crypto & Blockchain
        "cryptocurrency", "bitcoin", "ethereum", "blockchain",
        "nft", "web3", "defi", "smart contracts", "mining",
        "token", "ico", "dao", "metamask", "wallet",
        
        # Security (unless AI/Claude related)
        "cve", "vulnerability", "exploit", "zero day", "patch tuesday",
        "penetration testing", "ethical hacking", "malware",
        
        # Academic/Theoretical (unless practical AI)
        "theoretical computer science", "computational complexity",
        "np complete", "turing machine", "lambda calculus",
        "category theory", "type theory", "formal verification",
        
        # Other
        "gaming", "game development", "unity", "unreal engine",
        "embedded systems", "iot", "arduino", "raspberry pi",
        "devops", "kubernetes", "docker", "ci/cd", "jenkins"
    ]
    
    # High-value keywords that boost relevance
    high_value_keywords = [
        "claude opus 4", "opus 4.1", "claude 4.0",
        "anthropic announcement", "anthropic release",
        "claude code update", "claude desktop",
        "react 19", "next.js 15", "typescript 5",
        "new claude feature", "claude api",
        "prompt engineering guide", "prompting best practices",
        "ai coding assistant", "cursor update",
        "mcp server", "model context protocol"
    ]


class RelevanceFilter:
    """Filter for determining content relevance"""
    
    def __init__(self, config: Optional[RelevanceConfig] = None):
        """Initialize relevance filter with configuration"""
        self.config = config or RelevanceConfig()
        self.logger = logging.getLogger("RelevanceFilter")
        
        # Compile regex patterns for efficiency
        self._compile_patterns()
    
    def _compile_patterns(self):
        """Compile regex patterns for faster matching"""
        # Create pattern for relevant topics
        relevant_terms = "|".join(re.escape(term) for term in self.config.relevant_topics)
        self.relevant_pattern = re.compile(relevant_terms, re.IGNORECASE)
        
        # Create pattern for irrelevant topics
        irrelevant_terms = "|".join(re.escape(term) for term in self.config.irrelevant_topics)
        self.irrelevant_pattern = re.compile(irrelevant_terms, re.IGNORECASE)
        
        # Create pattern for high-value keywords
        high_value_terms = "|".join(re.escape(term) for term in self.config.high_value_keywords)
        self.high_value_pattern = re.compile(high_value_terms, re.IGNORECASE)
    
    def is_relevant(self, title: str, content: str = "", 
                   topics: List[str] = None) -> Tuple[bool, float, str]:
        """
        Determine if content is relevant
        
        Args:
            title: Content title
            content: Content body (optional)
            topics: List of topics/tags (optional)
            
        Returns:
            (is_relevant, relevance_score, reason)
        """
        combined_text = f"{title} {content[:500] if content else ''}"
        topics_text = " ".join(topics) if topics else ""
        all_text = f"{combined_text} {topics_text}"
        
        # Check for high-value content first
        high_value_matches = self.high_value_pattern.findall(all_text)
        if high_value_matches:
            self.logger.debug(f"High-value content detected: {high_value_matches[0]}")
            return True, 1.0, f"High-value: {high_value_matches[0]}"
        
        # Check for irrelevant topics (strong negative signal)
        irrelevant_matches = self.irrelevant_pattern.findall(title)
        if irrelevant_matches:
            # Check if it's actually about AI/Claude despite the keyword
            if not self._has_relevant_context(all_text):
                self.logger.debug(f"Irrelevant topic detected: {irrelevant_matches[0]}")
                return False, 0.0, f"Irrelevant: {irrelevant_matches[0]}"
        
        # Check for relevant topics
        relevant_matches = self.relevant_pattern.findall(all_text)
        if relevant_matches:
            # Calculate relevance score based on matches
            score = min(1.0, 0.5 + (len(set(relevant_matches)) * 0.1))
            self.logger.debug(f"Relevant content: {relevant_matches[0]}, score: {score}")
            return True, score, f"Relevant: {', '.join(set(relevant_matches[:3]))}"
        
        # Default: not relevant
        return False, 0.0, "No relevant keywords found"
    
    def _has_relevant_context(self, text: str) -> bool:
        """Check if text has relevant context despite irrelevant keywords"""
        # Look for AI/Claude context that overrides irrelevant keywords
        override_patterns = [
            r"claude.*\b(can|does|helps|assists)\b",
            r"ai.*\b(coding|development|assistant)\b",
            r"prompt.*\b(engineering|design|optimization)\b",
            r"react.*\b(component|hook|state)\b"
        ]
        
        for pattern in override_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        
        return False
    
    def filter_items(self, items: List[Dict]) -> List[Dict]:
        """
        Filter a list of items for relevance
        
        Args:
            items: List of content items
            
        Returns:
            Filtered list of relevant items
        """
        filtered = []
        
        for item in items:
            title = item.get('title', '')
            content = item.get('content', '')
            topics = item.get('topics', [])
            
            is_relevant, score, reason = self.is_relevant(title, content, topics)
            
            if is_relevant:
                item['relevance_score'] = score
                item['relevance_reason'] = reason
                filtered.append(item)
            else:
                self.logger.info(f"Filtered out: {title[:50]}... - {reason}")
        
        self.logger.info(f"Filtered {len(items)} items to {len(filtered)} relevant items")
        return filtered


# Example usage
def test_relevance_filter():
    """Test the relevance filter"""
    filter = RelevanceFilter()
    
    test_cases = [
        ("Claude Opus 4.1 Is Here And What It Means for AI Development", "", ["ai", "claude"]),
        ("Autonomous Dynamic Voltage Scaling via Reinforcement Learning for Power Efficiency in HPC", "", ["hpc", "computing"]),
        ("React 19 Beta: New Features and Breaking Changes", "", ["react", "frontend"]),
        ("Understanding Quantum Computing Algorithms", "", ["quantum", "algorithms"]),
        ("Building AI Agents with Claude and LangChain", "", ["ai", "claude", "langchain"]),
        ("Cryptocurrency Market Analysis 2024", "", ["crypto", "bitcoin"]),
        ("TypeScript 5.0: What's New for React Developers", "", ["typescript", "react"]),
        ("Optimizing GPU Performance for Deep Learning", "", ["gpu", "ml"]),
    ]
    
    print("Testing Relevance Filter:")
    print("-" * 60)
    
    for title, content, topics in test_cases:
        is_relevant, score, reason = filter.is_relevant(title, content, topics)
        status = "✅ KEEP" if is_relevant else "❌ FILTER"
        print(f"{status} [{score:.2f}] {title[:50]}...")
        print(f"         Reason: {reason}")
        print()


if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Run test
    test_relevance_filter()