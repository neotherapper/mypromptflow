#!/usr/bin/env python3
"""
YouTube Integration Manager
Connects RSS monitoring with MCP transcript processing and Universal Topic Intelligence

This script manages the complete workflow:
1. RSS monitoring → 2. Video queueing → 3. MCP transcript extraction → 4. Intelligence processing
"""

import json
import subprocess
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import logging

@dataclass
class ProcessingJob:
    """Video processing job structure"""
    video_url: str
    video_id: str
    title: str
    channel: str
    channel_rating: float
    topics: List[str]
    priority: str
    queued_at: str
    status: str = "pending"
    transcript: Optional[str] = None
    insights: Optional[Dict[str, Any]] = None
    processed_at: Optional[str] = None
    error: Optional[str] = None

class YouTubeIntegrationManager:
    """Manages YouTube RSS monitoring and MCP integration"""
    
    def __init__(self):
        self.logger = self._setup_logging()
        self.queue_file = "transcript-processing-queue.json"
        self.completed_file = "completed-processing-jobs.json"
        self.results_file = "youtube-processing-results.json"
        
        # MCP command templates
        self.mcp_transcript_command = 'claude'  # Using Claude Code CLI
        
    def _setup_logging(self) -> logging.Logger:
        """Set up logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('youtube-integration.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)
    
    def load_processing_queue(self) -> List[ProcessingJob]:
        """Load pending processing jobs"""
        if not Path(self.queue_file).exists():
            return []
        
        try:
            with open(self.queue_file, 'r') as f:
                data = json.load(f)
                return [ProcessingJob(**job) for job in data if job.get('status') == 'pending']
        except Exception as e:
            self.logger.error(f"Error loading processing queue: {e}")
            return []
    
    def save_processing_queue(self, jobs: List[ProcessingJob]):
        """Save processing queue"""
        try:
            job_data = [job.__dict__ for job in jobs]
            with open(self.queue_file, 'w') as f:
                json.dump(job_data, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving processing queue: {e}")
    
    def extract_transcript_via_mcp(self, video_url: str) -> Optional[str]:
        """Extract transcript using MCP Docker tool via Claude Code CLI"""
        try:
            # Create a temporary prompt file for Claude Code
            prompt = f'''
Extract the transcript from this YouTube video using the MCP get_transcript tool:

Video URL: {video_url}

Please use the mcp__MCP_DOCKER__get_transcript tool to extract the full transcript.
Return only the transcript text, no additional formatting or commentary.
'''
            
            # Use Claude Code to process the transcript extraction
            result = subprocess.run([
                'claude',
                '--print', prompt
            ], capture_output=True, text=True, timeout=300)  # 5-minute timeout
            
            if result.returncode == 0:
                transcript = result.stdout.strip()
                if len(transcript) > 100:  # Minimum viable transcript length
                    return transcript
                else:
                    self.logger.warning(f"Transcript too short for {video_url}: {len(transcript)} chars")
                    return None
            else:
                self.logger.error(f"Claude Code failed for {video_url}: {result.stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            self.logger.error(f"Transcript extraction timeout for {video_url}")
            return None
        except Exception as e:
            self.logger.error(f"Error extracting transcript for {video_url}: {e}")
            return None
    
    def process_transcript_insights(self, transcript: str, job: ProcessingJob) -> Dict[str, Any]:
        """Process transcript for insights using existing pipeline"""
        try:
            # Import the existing processor
            import sys
            sys.path.append(str(Path("../scripts").resolve()))
            from youtube_transcript_processor import YouTubeTranscriptProcessor
            
            processor = YouTubeTranscriptProcessor()
            
            # Calculate relevance score
            relevance_score = processor.calculate_relevance_score(transcript, job.channel_rating)
            
            if relevance_score < 0.5:
                return {
                    "relevance_score": relevance_score,
                    "summary": "Content relevance too low for detailed processing",
                    "key_takeaways": [],
                    "tools_mentioned": [],
                    "code_examples": [],
                    "timestamps": {}
                }
            
            # Extract insights
            insights = {
                "relevance_score": relevance_score,
                "summary": processor.generate_summary(transcript),
                "key_takeaways": processor.extract_key_takeaways(transcript),
                "tools_mentioned": processor.extract_tools_mentioned(transcript),
                "code_examples": processor.extract_code_examples(transcript),
                "timestamps": processor.extract_timestamps(transcript)
            }
            
            return insights
            
        except Exception as e:
            self.logger.error(f"Error processing transcript insights: {e}")
            return {
                "error": str(e),
                "relevance_score": 0.0,
                "summary": "Processing failed",
                "key_takeaways": [],
                "tools_mentioned": [],
                "code_examples": [],
                "timestamps": {}
            }
    
    def save_to_knowledge_vault(self, job: ProcessingJob) -> str:
        """Save processed job to knowledge vault structure"""
        try:
            # Create knowledge vault path
            base_path = Path("../knowledge-vault/youtube-content")
            base_path.mkdir(parents=True, exist_ok=True)
            
            channel_slug = job.channel.lower().replace(' ', '_').replace('-', '_')
            date_str = datetime.now().strftime('%Y-%m-%d')
            
            channel_path = base_path / channel_slug / date_str
            channel_path.mkdir(parents=True, exist_ok=True)
            
            # Generate content files
            video_slug = job.title.lower().replace(' ', '_').replace('-', '_')
            video_slug = ''.join(c for c in video_slug if c.isalnum() or c == '_')[:50]  # Limit length
            
            transcript_file = channel_path / f"{video_slug}_transcript.md"
            insights_file = channel_path / f"{video_slug}_insights.md"
            metadata_file = channel_path / f"{video_slug}_metadata.json"
            
            # Create transcript file
            transcript_content = f"""# {job.title}

**Channel:** {job.channel}
**URL:** {job.video_url}
**Processing Date:** {job.processed_at}
**Relevance Score:** {job.insights.get('relevance_score', 0.0):.2f}

## Full Transcript

{job.transcript}
"""
            
            with open(transcript_file, 'w', encoding='utf-8') as f:
                f.write(transcript_content)
            
            # Create insights file
            insights_content = f"""# {job.title} - Analysis

**Channel:** {job.channel} ({job.channel_rating}⭐)
**URL:** {job.video_url}
**Processing Date:** {job.processed_at}

## Summary
{job.insights.get('summary', 'No summary available')}

## Key Takeaways
{chr(10).join(f"- {takeaway}" for takeaway in job.insights.get('key_takeaways', []))}

## Tools & Technologies Mentioned
{chr(10).join(f"- {tool}" for tool in job.insights.get('tools_mentioned', []))}

## Code Examples
{chr(10).join(f"```{chr(10)}{example}{chr(10)}```" for example in job.insights.get('code_examples', []))}

## Important Timestamps
{chr(10).join(f"- **{time}**: {desc}" for time, desc in job.insights.get('timestamps', {}).items())}

## Relevance Assessment
- **Score:** {job.insights.get('relevance_score', 0.0):.2f}
- **Priority:** {job.priority}
- **Topics:** {', '.join(job.topics)}
"""
            
            with open(insights_file, 'w', encoding='utf-8') as f:
                f.write(insights_content)
            
            # Create metadata file
            metadata = {
                "video_id": job.video_id,
                "video_url": job.video_url,
                "title": job.title,
                "channel": job.channel,
                "channel_rating": job.channel_rating,
                "topics": job.topics,
                "priority": job.priority,
                "processing_date": job.processed_at,
                "relevance_score": job.insights.get('relevance_score', 0.0),
                "tools_mentioned": job.insights.get('tools_mentioned', []),
                "key_takeaways_count": len(job.insights.get('key_takeaways', [])),
                "code_examples_count": len(job.insights.get('code_examples', [])),
                "file_paths": {
                    "transcript": str(transcript_file),
                    "insights": str(insights_file),
                    "metadata": str(metadata_file)
                }
            }
            
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2)
            
            self.logger.info(f"Saved to knowledge vault: {channel_path}")
            return str(channel_path)
            
        except Exception as e:
            self.logger.error(f"Error saving to knowledge vault: {e}")
            return ""
    
    def process_single_job(self, job: ProcessingJob) -> ProcessingJob:
        """Process a single video job through the complete pipeline"""
        self.logger.info(f"Processing: {job.title} ({job.channel})")
        
        try:
            # Step 1: Extract transcript
            job.status = "extracting_transcript"
            transcript = self.extract_transcript_via_mcp(job.video_url)
            
            if not transcript:
                job.status = "failed"
                job.error = "Failed to extract transcript"
                return job
            
            job.transcript = transcript
            
            # Step 2: Process insights
            job.status = "processing_insights"
            insights = self.process_transcript_insights(transcript, job)
            job.insights = insights
            
            # Step 3: Save to knowledge vault
            job.status = "saving_to_vault"
            vault_path = self.save_to_knowledge_vault(job)
            
            # Step 4: Complete
            job.status = "completed"
            job.processed_at = datetime.now().isoformat()
            
            self.logger.info(f"✅ Completed processing: {job.title}")
            return job
            
        except Exception as e:
            job.status = "failed"
            job.error = str(e)
            self.logger.error(f"❌ Failed processing {job.title}: {e}")
            return job
    
    def process_queue(self, max_jobs: int = 5) -> Dict[str, Any]:
        """Process pending jobs in the queue"""
        queue = self.load_processing_queue()
        
        if not queue:
            self.logger.info("No jobs in processing queue")
            return {"processed": 0, "failed": 0, "results": []}
        
        self.logger.info(f"Processing {min(len(queue), max_jobs)} jobs from queue of {len(queue)}")
        
        # Sort by priority
        priority_order = {"high": 0, "medium": 1, "low": 2}
        queue.sort(key=lambda x: priority_order.get(x.priority, 1))
        
        processed_jobs = []
        failed_jobs = []
        
        for i, job in enumerate(queue[:max_jobs]):
            result = self.process_single_job(job)
            
            if result.status == "completed":
                processed_jobs.append(result)
            else:
                failed_jobs.append(result)
            
            # Add delay between jobs to avoid overwhelming systems
            if i < len(queue) - 1:
                time.sleep(5)
        
        # Save results
        self._save_processing_results(processed_jobs, failed_jobs)
        
        # Update queue (remove processed jobs)
        remaining_queue = [job for job in queue[max_jobs:]]
        remaining_queue.extend(failed_jobs)  # Keep failed jobs for retry
        self.save_processing_queue(remaining_queue)
        
        return {
            "processed": len(processed_jobs),
            "failed": len(failed_jobs),
            "results": processed_jobs + failed_jobs
        }
    
    def _save_processing_results(self, processed: List[ProcessingJob], failed: List[ProcessingJob]):
        """Save processing results for reporting"""
        results = {
            "run_timestamp": datetime.now().isoformat(),
            "processed_count": len(processed),
            "failed_count": len(failed),
            "processed_jobs": [job.__dict__ for job in processed],
            "failed_jobs": [job.__dict__ for job in failed]
        }
        
        # Load existing results
        if Path(self.results_file).exists():
            with open(self.results_file, 'r') as f:
                existing_results = json.load(f)
                if not isinstance(existing_results, list):
                    existing_results = [existing_results]
        else:
            existing_results = []
        
        existing_results.append(results)
        
        # Keep only last 10 runs
        existing_results = existing_results[-10:]
        
        with open(self.results_file, 'w') as f:
            json.dump(existing_results, f, indent=2)
    
    def run_complete_workflow(self) -> Dict[str, Any]:
        """Run complete YouTube monitoring and processing workflow"""
        self.logger.info("Starting complete YouTube workflow")
        
        try:
            # Step 1: Run RSS monitoring
            self.logger.info("Step 1: Running RSS monitoring")
            rss_monitor_result = subprocess.run([
                'python3', 'rss-youtube-monitor.py'
            ], capture_output=True, text=True, cwd=Path(__file__).parent)
            
            if rss_monitor_result.returncode != 0:
                self.logger.error(f"RSS monitoring failed: {rss_monitor_result.stderr}")
                return {"success": False, "error": "RSS monitoring failed"}
            
            # Step 2: Process transcript queue
            self.logger.info("Step 2: Processing transcript queue")
            processing_result = self.process_queue(max_jobs=3)  # Limit to 3 jobs per run
            
            # Step 3: Generate summary report
            report = self._generate_workflow_report(processing_result)
            
            self.logger.info("✅ Complete workflow finished successfully")
            return {
                "success": True,
                "rss_monitoring": rss_monitor_result.stdout,
                "transcript_processing": processing_result,
                "report": report
            }
            
        except Exception as e:
            self.logger.error(f"Workflow failed: {e}")
            return {"success": False, "error": str(e)}
    
    def _generate_workflow_report(self, processing_result: Dict[str, Any]) -> str:
        """Generate summary report of workflow execution"""
        report = [
            "=== YouTube Integration Workflow Report ===",
            f"Execution time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "📊 Processing Results:",
            f"  ✅ Successfully processed: {processing_result['processed']} videos",
            f"  ❌ Failed processing: {processing_result['failed']} videos",
            ""
        ]
        
        if processing_result['results']:
            report.append("📋 Processed Videos:")
            for job in processing_result['results']:
                if hasattr(job, 'status') and job.status == 'completed':
                    relevance = job.insights.get('relevance_score', 0.0) if job.insights else 0.0
                    report.append(f"  ✅ {job.title} ({job.channel}) - Relevance: {relevance:.2f}")
                else:
                    error = job.error if hasattr(job, 'error') else 'Unknown error'
                    report.append(f"  ❌ {job.title} ({job.channel}) - Error: {error}")
            report.append("")
        
        report.extend([
            "🔗 Integration Status:",
            "  • RSS monitoring: Active",
            "  • MCP transcript extraction: Active", 
            "  • Knowledge vault storage: Active",
            "  • Universal Topic Intelligence: Ready for integration",
            "",
            "📂 Output Locations:",
            "  • Knowledge vault: ../knowledge-vault/youtube-content/",
            "  • Processing logs: youtube-integration.log",
            "  • Results archive: youtube-processing-results.json"
        ])
        
        return "\n".join(report)

def main():
    """Main execution function"""
    manager = YouTubeIntegrationManager()
    
    print("YouTube Integration Manager")
    print("=" * 50)
    
    # Check for existing queue
    queue = manager.load_processing_queue()
    print(f"Pending jobs in queue: {len(queue)}")
    
    if queue:
        print("\nRunning transcript processing for queued videos...")
        result = manager.process_queue(max_jobs=3)
        print(f"✅ Processed: {result['processed']}")
        print(f"❌ Failed: {result['failed']}")
    else:
        print("No pending jobs. Running complete workflow...")
        result = manager.run_complete_workflow()
        
        if result['success']:
            print("✅ Workflow completed successfully")
            print(result['report'])
        else:
            print(f"❌ Workflow failed: {result['error']}")

if __name__ == "__main__":
    main()