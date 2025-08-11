#!/usr/bin/env python3
"""
Demo script for Universal Topic Intelligence System
Shows the system monitoring Claude, React, and AI topics
"""

import asyncio
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import print as rprint
import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from core import SourceMonitorFactory, SourceType, ContentItem, ContentPriority
from sources.rss_monitor import RSSSourceMonitor
from agents.queen_agent import QueenAgent

console = Console()


async def demo():
    """Run a demonstration of the Topic Intelligence System"""
    
    # Welcome message
    console.print(Panel.fit(
        "[bold cyan]Universal Topic Intelligence System Demo[/bold cyan]\n\n"
        "Monitoring your interests:\n"
        "• Claude AI & Claude Code\n"
        "• React & TypeScript Development\n"
        "• AI Prompting & Applications\n\n"
        "This demo shows the system architecture and capabilities",
        border_style="cyan"
    ))
    
    await asyncio.sleep(2)
    
    # Initialize system
    console.print("\n[bold yellow]1. System Initialization[/bold yellow]")
    console.print("=" * 60)
    
    with console.status("[green]Registering monitors and initializing agents..."):
        # Register RSS monitor
        SourceMonitorFactory.register_monitor(SourceType.RSS, RSSSourceMonitor)
        
        # Initialize Queen Agent
        queen = QueenAgent(config_dir="configs/topics")
        await asyncio.sleep(1)
    
    console.print("✅ System initialized with:")
    console.print(f"  • {len(queen.topics)} topics configured")
    console.print(f"  • {len(queen.topic_relationships)} cross-topic relationships")
    console.print(f"  • {len(queen.shared_sources)} shared sources identified")
    
    # Show topics
    console.print("\n[bold yellow]2. Configured Topics[/bold yellow]")
    console.print("=" * 60)
    
    topic_table = Table(show_header=True, header_style="bold magenta")
    topic_table.add_column("Topic", style="cyan")
    topic_table.add_column("Priority", style="yellow")
    topic_table.add_column("Frequency", style="green")
    topic_table.add_column("Sources", style="white")
    
    for topic_slug, state in queen.topics.items():
        config = queen.topic_configs.get(topic_slug, {})
        source_count = 0
        
        for tier in ["tier_1_official", "tier_2_community", "tier_3_aggregators"]:
            sources = config.get("source_mapping", {}).get(tier, {}).get("sources", [])
            source_count += len(sources)
        
        topic_table.add_row(
            state.topic_name[:40],
            state.priority_level,
            state.monitoring_frequency,
            str(source_count)
        )
    
    console.print(topic_table)
    
    # Show relationships
    console.print("\n[bold yellow]3. Cross-Topic Relationships[/bold yellow]")
    console.print("=" * 60)
    
    relationships = {}
    for (t1, t2), rel in queen.topic_relationships.items():
        if t1 not in relationships:
            relationships[t1] = []
        relationships[t1].append(f"{t2} ({rel.value})")
    
    for topic, rels in relationships.items():
        state = queen.topics.get(topic)
        if state:
            console.print(f"• {state.topic_name}:")
            for rel in rels[:3]:
                console.print(f"  → {rel}")
    
    # Demonstrate monitoring
    console.print("\n[bold yellow]4. Topic Monitoring Demonstration[/bold yellow]")
    console.print("=" * 60)
    
    with console.status("[green]Running orchestration across all topics..."):
        result = await queen.orchestrate()
        await asyncio.sleep(1)
    
    console.print(f"✅ Orchestration complete:")
    console.print(f"  • Topics monitored: {len(result.topics_monitored)}")
    console.print(f"  • Total items collected: {result.total_items_collected}")
    console.print(f"  • Processing time: {result.performance_metrics.get('orchestration_duration', 0):.2f}s")
    
    # Show resource allocation
    console.print("\n[bold yellow]5. Adaptive Resource Allocation[/bold yellow]")
    console.print("=" * 60)
    
    resource_table = Table(show_header=True, header_style="bold yellow")
    resource_table.add_column("Topic", style="cyan")
    resource_table.add_column("Allocation", style="green")
    resource_table.add_column("Strategy", style="white")
    
    for topic_slug, resources in result.resource_usage.items():
        state = queen.topics.get(topic_slug)
        if state:
            resource_table.add_row(
                state.topic_name[:40],
                f"{resources:.1f} units",
                queen.allocation_strategy.value
            )
    
    console.print(resource_table)
    
    # Demonstrate content prioritization
    console.print("\n[bold yellow]6. Content Prioritization Example[/bold yellow]")
    console.print("=" * 60)
    
    # Create sample content
    sample_items = [
        ContentItem(
            item_id="demo1",
            source_id="anthropic_blog",
            title="Claude 3.5 Sonnet: Major Performance Improvements",
            content="Anthropic announces significant improvements to Claude...",
            url="https://anthropic.com/claude-update",
            published_date=datetime.now(),
            author="Anthropic",
            topics=["claude", "ai", "announcement"],
            metadata={"priority": "critical"}
        ),
        ContentItem(
            item_id="demo2",
            source_id="react_blog",
            title="React 19 RC: Server Components are Here",
            content="The React team announces the release candidate...",
            url="https://react.dev/blog/react-19",
            published_date=datetime.now(),
            author="React Team",
            topics=["react", "release", "server-components"],
            metadata={"priority": "high"}
        ),
        ContentItem(
            item_id="demo3",
            source_id="community",
            title="Building AI Apps with Claude Code and React",
            content="Tutorial on integrating Claude Code with React apps...",
            url="https://dev.to/claude-react",
            published_date=datetime.now(),
            author="Developer",
            topics=["claude", "react", "tutorial"],
            metadata={"priority": "medium"}
        )
    ]
    
    console.print("Sample content items:")
    for i, item in enumerate(sample_items, 1):
        priority_color = {
            "critical": "red",
            "high": "yellow",
            "medium": "green"
        }.get(item.metadata.get("priority", "medium"), "white")
        
        console.print(f"\n{i}. [{priority_color}]{item.title}[/{priority_color}]")
        console.print(f"   Topics: {', '.join(item.topics)}")
        console.print(f"   Priority: [{priority_color}]{item.metadata.get('priority', 'unknown')}[/{priority_color}]")
    
    # System capabilities
    console.print("\n[bold yellow]7. System Capabilities[/bold yellow]")
    console.print("=" * 60)
    
    capabilities = [
        ("🎯", "Universal Monitoring", "Monitor ANY topic with YAML configuration"),
        ("🤖", "4-Level AI Hierarchy", "Queen → Architect → Specialist → Worker"),
        ("⚡", "Adaptive Resources", "Intelligent resource allocation across topics"),
        ("🔗", "Cross-Topic Intelligence", "Detect relationships and patterns"),
        ("🚨", "Emergency Response", "Immediate processing of critical updates"),
        ("📊", "Quality Assessment", "Constitutional AI compliance and scoring"),
        ("🔄", "Continuous Learning", "Adapt based on patterns and performance")
    ]
    
    for icon, capability, description in capabilities:
        console.print(f"{icon} [bold cyan]{capability}[/bold cyan]")
        console.print(f"   {description}")
    
    # Summary
    console.print("\n" + "=" * 60)
    console.print(Panel.fit(
        "[bold green]System Ready for Production![/bold green]\n\n"
        "The Universal Topic Intelligence System is configured to monitor:\n"
        "• Claude AI developments and Claude Code updates\n"
        "• React & TypeScript ecosystem changes\n"
        "• AI prompting techniques and applications\n\n"
        "Use the CLI interface to start real-time monitoring:\n"
        "[cyan]python cli.py[/cyan]",
        border_style="green"
    ))


if __name__ == "__main__":
    try:
        asyncio.run(demo())
    except KeyboardInterrupt:
        console.print("\n[yellow]Demo interrupted[/yellow]")
        sys.exit(0)