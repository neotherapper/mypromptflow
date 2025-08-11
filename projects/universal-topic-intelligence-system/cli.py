#!/usr/bin/env python3
"""
Universal Topic Intelligence System - CLI Interface
Interactive command-line interface for monitoring topics of interest
"""

import asyncio
import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, List
import logging
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.live import Live
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.markdown import Markdown
from rich import print as rprint

# Configure logging
logging.basicConfig(
    level=logging.WARNING,  # Reduce noise in CLI
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from core import ContentPriority, SourceMonitorFactory, SourceType
from sources.rss_monitor import RSSSourceMonitor
from agents.queen_agent import QueenAgent, ResourceAllocationStrategy
from agents.architect_agents import ArchitectCoordinator

console = Console()


class TopicMonitorCLI:
    """CLI interface for the Universal Topic Intelligence System"""
    
    def __init__(self):
        self.queen = None
        self.config_dir = Path("configs/topics")
        self.running = False
        self.monitor_task = None
        
    async def initialize(self):
        """Initialize the monitoring system"""
        with console.status("[bold green]Initializing Topic Intelligence System..."):
            # Register monitors
            SourceMonitorFactory.register_monitor(SourceType.RSS, RSSSourceMonitor)
            
            # Initialize Queen Agent
            self.queen = QueenAgent(config_dir=str(self.config_dir))
            
            await asyncio.sleep(1)  # Brief pause for effect
        
        console.print("[bold green]✅ System initialized successfully![/bold green]")
        console.print(f"[cyan]Loaded {len(self.queen.topics)} topics:[/cyan]")
        
        for topic_slug, state in self.queen.topics.items():
            console.print(f"  • {state.topic_name} ([yellow]{state.priority_level}[/yellow] priority)")
    
    async def monitor_topics(self, 
                           topics: Optional[List[str]] = None,
                           continuous: bool = False,
                           interval: int = 60):
        """
        Monitor specified topics
        
        Args:
            topics: List of topic slugs to monitor (None for all)
            continuous: Whether to monitor continuously
            interval: Interval between monitoring cycles (seconds)
        """
        self.running = True
        
        while self.running:
            try:
                # Create progress display
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    console=console
                ) as progress:
                    task = progress.add_task("Monitoring topics...", total=None)
                    
                    # Run orchestration
                    result = await self.queen.orchestrate(force_topics=topics)
                    
                    progress.update(task, completed=True)
                
                # Display results
                self._display_results(result)
                
                if not continuous:
                    break
                
                # Wait for next cycle
                console.print(f"\n[dim]Next scan in {interval} seconds... (Press Ctrl+C to stop)[/dim]")
                await asyncio.sleep(interval)
                
            except KeyboardInterrupt:
                console.print("\n[yellow]Monitoring stopped by user[/yellow]")
                self.running = False
                break
            except Exception as e:
                console.print(f"[red]Error during monitoring: {str(e)}[/red]")
                if not continuous:
                    break
    
    def _display_results(self, result):
        """Display monitoring results in a formatted way"""
        # Header
        console.print("\n" + "=" * 80)
        console.print(f"[bold cyan]📊 Monitoring Results - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/bold cyan]")
        console.print("=" * 80)
        
        # Summary stats
        summary_table = Table(show_header=True, header_style="bold magenta")
        summary_table.add_column("Metric", style="cyan")
        summary_table.add_column("Value", style="green")
        
        summary_table.add_row("Topics Monitored", str(len(result.topics_monitored)))
        summary_table.add_row("Total Items", str(result.total_items_collected))
        summary_table.add_row("Critical Items", str(len(result.critical_items)))
        summary_table.add_row("Processing Time", f"{result.performance_metrics.get('orchestration_duration', 0):.2f}s")
        
        console.print(Panel(summary_table, title="Summary", border_style="blue"))
        
        # Critical items
        if result.critical_items:
            console.print("\n[bold red]🔴 Critical Items:[/bold red]")
            for i, item in enumerate(result.critical_items[:5], 1):
                console.print(f"\n{i}. [bold]{item.title}[/bold]")
                console.print(f"   [dim]Source: {item.source_id} | Topics: {', '.join(item.topics[:3])}[/dim]")
                if item.url:
                    console.print(f"   [link]{item.url}[/link]")
        
        # Cross-topic insights
        if result.cross_topic_insights:
            console.print("\n[bold cyan]🔗 Cross-Topic Insights:[/bold cyan]")
            for insight in result.cross_topic_insights[:3]:
                insight_type = insight.get("type", "unknown")
                console.print(f"\n• [yellow]{insight_type.replace('_', ' ').title()}[/yellow]")
                
                if insight_type == "topic_overlap":
                    for overlap in insight.get("data", [])[:3]:
                        topics = overlap.get("topics", [])
                        count = overlap.get("count", 0)
                        console.print(f"  - {' & '.join(topics)}: {count} co-occurrences")
                elif insight_type == "temporal_pattern":
                    for pattern in insight.get("data", [])[:3]:
                        console.print(f"  - Hour {pattern.get('hour', 0)}: {pattern.get('items', 0)} items")
        
        # Resource usage
        console.print("\n[bold yellow]💰 Resource Allocation:[/bold yellow]")
        resource_table = Table(show_header=True, header_style="bold yellow")
        resource_table.add_column("Topic", style="cyan")
        resource_table.add_column("Resources", style="green")
        resource_table.add_column("Items", style="white")
        
        for topic_slug, resources in result.resource_usage.items():
            state = self.queen.topics.get(topic_slug)
            if state:
                resource_table.add_row(
                    state.topic_name[:30],
                    f"{resources:.1f} units",
                    str(state.items_collected)
                )
        
        console.print(resource_table)
    
    async def show_status(self):
        """Display current system status"""
        if not self.queen:
            console.print("[red]System not initialized[/red]")
            return
        
        status = self.queen.get_status()
        
        # Status panel
        status_table = Table(show_header=False, box=None)
        status_table.add_column("Metric", style="cyan")
        status_table.add_column("Value", style="green")
        
        status_table.add_row("Total Orchestrations", str(status["orchestration_count"]))
        status_table.add_row("Total Items Processed", str(status["total_items_processed"]))
        status_table.add_row("Topics Managed", str(status["topics_managed"]))
        status_table.add_row("Active Topics", str(len(status["active_topics"])))
        status_table.add_row("Shared Sources", str(status["shared_sources"]))
        status_table.add_row("Known Relationships", str(status["known_relationships"]))
        status_table.add_row("Resource Strategy", status["allocation_strategy"])
        
        console.print(Panel(status_table, title="System Status", border_style="cyan"))
        
        # Active topics
        if status["active_topics"]:
            console.print("\n[bold green]Active Topics:[/bold green]")
            for topic in status["active_topics"]:
                state = self.queen.topics.get(topic)
                if state:
                    console.print(f"  • {state.topic_name} - {state.items_collected} items collected")
    
    async def configure_topic(self, topic_slug: str):
        """Configure or view a specific topic"""
        if not self.queen:
            console.print("[red]System not initialized[/red]")
            return
        
        if topic_slug not in self.queen.topics:
            console.print(f"[red]Topic '{topic_slug}' not found[/red]")
            console.print("\nAvailable topics:")
            for slug in self.queen.topics:
                console.print(f"  • {slug}")
            return
        
        state = self.queen.topics[topic_slug]
        config = self.queen.topic_configs.get(topic_slug, {})
        
        # Display topic configuration
        console.print(f"\n[bold cyan]📋 Topic: {state.topic_name}[/bold cyan]")
        console.print("=" * 60)
        
        config_table = Table(show_header=False, box=None)
        config_table.add_column("Property", style="cyan")
        config_table.add_column("Value", style="white")
        
        config_table.add_row("Slug", topic_slug)
        config_table.add_row("Priority", state.priority_level)
        config_table.add_row("Monitoring Frequency", state.monitoring_frequency)
        config_table.add_row("Last Monitored", 
                           state.last_monitored.strftime("%Y-%m-%d %H:%M") if state.last_monitored else "Never")
        config_table.add_row("Items Collected", str(state.items_collected))
        config_table.add_row("Critical Items", str(state.critical_items))
        config_table.add_row("Error Count", str(state.error_count))
        
        console.print(config_table)
        
        # Show sources
        source_mapping = config.get("source_mapping", {})
        total_sources = 0
        
        for tier in ["tier_1_official", "tier_2_community", "tier_3_aggregators"]:
            sources = source_mapping.get(tier, {}).get("sources", [])
            total_sources += len(sources)
        
        console.print(f"\n[yellow]Sources:[/yellow] {total_sources} configured")
        
        # Show relationships
        relationships = []
        for (t1, t2), rel in self.queen.topic_relationships.items():
            if t1 == topic_slug:
                relationships.append(f"{t2} ({rel.value})")
        
        if relationships:
            console.print(f"[yellow]Relationships:[/yellow] {', '.join(relationships)}")
    
    async def set_strategy(self, strategy: str):
        """Set resource allocation strategy"""
        if not self.queen:
            console.print("[red]System not initialized[/red]")
            return
        
        try:
            self.queen.allocation_strategy = ResourceAllocationStrategy[strategy.upper()]
            console.print(f"[green]✅ Resource allocation strategy set to: {strategy}[/green]")
        except KeyError:
            console.print(f"[red]Invalid strategy: {strategy}[/red]")
            console.print("Available strategies:")
            for s in ResourceAllocationStrategy:
                console.print(f"  • {s.value}")


async def interactive_mode():
    """Run in interactive mode"""
    cli = TopicMonitorCLI()
    
    # Display welcome message
    console.print(Panel.fit(
        "[bold cyan]Universal Topic Intelligence System[/bold cyan]\n\n"
        "Monitor Claude, React, TypeScript, and AI topics in real-time\n"
        "Type 'help' for available commands",
        border_style="cyan"
    ))
    
    # Initialize system
    await cli.initialize()
    
    # Interactive loop
    while True:
        try:
            command = console.input("\n[bold cyan]topic-monitor>[/bold cyan] ").strip().lower()
            
            if not command:
                continue
            
            parts = command.split()
            cmd = parts[0]
            
            if cmd == "help":
                console.print("\n[bold yellow]Available Commands:[/bold yellow]")
                console.print("  monitor [topic1 topic2...]  - Monitor specific topics (or all if none specified)")
                console.print("  continuous [interval]        - Start continuous monitoring")
                console.print("  status                       - Show system status")
                console.print("  topic <slug>                 - View topic configuration")
                console.print("  strategy <type>              - Set resource allocation strategy")
                console.print("  topics                       - List all available topics")
                console.print("  exit/quit                    - Exit the program")
                
            elif cmd == "monitor":
                topics = parts[1:] if len(parts) > 1 else None
                await cli.monitor_topics(topics, continuous=False)
                
            elif cmd == "continuous":
                interval = int(parts[1]) if len(parts) > 1 else 60
                await cli.monitor_topics(None, continuous=True, interval=interval)
                
            elif cmd == "status":
                await cli.show_status()
                
            elif cmd == "topic" and len(parts) > 1:
                await cli.configure_topic(parts[1])
                
            elif cmd == "strategy" and len(parts) > 1:
                await cli.set_strategy(parts[1])
                
            elif cmd == "topics":
                console.print("\n[bold yellow]Available Topics:[/bold yellow]")
                for slug, state in cli.queen.topics.items():
                    console.print(f"  • [cyan]{slug}[/cyan] - {state.topic_name}")
                    
            elif cmd in ["exit", "quit"]:
                console.print("[yellow]Goodbye! 👋[/yellow]")
                break
                
            else:
                console.print(f"[red]Unknown command: {cmd}[/red]")
                console.print("Type 'help' for available commands")
                
        except KeyboardInterrupt:
            console.print("\n[yellow]Use 'exit' or 'quit' to leave[/yellow]")
        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/red]")


async def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Universal Topic Intelligence System - Monitor any topic intelligently"
    )
    
    parser.add_argument(
        "command",
        nargs="?",
        default="interactive",
        choices=["interactive", "monitor", "status"],
        help="Command to run (default: interactive)"
    )
    
    parser.add_argument(
        "--topics",
        nargs="+",
        help="Topics to monitor (slugs)"
    )
    
    parser.add_argument(
        "--continuous",
        action="store_true",
        help="Run continuous monitoring"
    )
    
    parser.add_argument(
        "--interval",
        type=int,
        default=60,
        help="Monitoring interval in seconds (default: 60)"
    )
    
    parser.add_argument(
        "--strategy",
        choices=["priority_based", "activity_based", "balanced", "adaptive"],
        default="adaptive",
        help="Resource allocation strategy"
    )
    
    args = parser.parse_args()
    
    if args.command == "interactive":
        await interactive_mode()
    else:
        cli = TopicMonitorCLI()
        await cli.initialize()
        
        if args.strategy:
            await cli.set_strategy(args.strategy)
        
        if args.command == "monitor":
            await cli.monitor_topics(
                topics=args.topics,
                continuous=args.continuous,
                interval=args.interval
            )
        elif args.command == "status":
            await cli.show_status()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[yellow]Program interrupted[/yellow]")
        sys.exit(0)