#!/usr/bin/env python3
"""
MCP YouTube Integration Demo
Demonstrates how to use MCP transcript tools with the YouTube processor for real content analysis
"""

import sys
import json
import logging
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

# Add current directory to path
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

# Import with hyphenated filename
import importlib.util
spec = importlib.util.spec_from_file_location("mcp_youtube_processor", "mcp-youtube-processor.py")
mcp_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mcp_module)
MCPYouTubeProcessor = mcp_module.MCPYouTubeProcessor
VideoAnalysisResult = mcp_module.VideoAnalysisResult

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MCPYouTubeIntegrationDemo:
    """Demo class showing how to integrate MCP transcript tools with YouTube processor"""
    
    def __init__(self):
        self.processor = MCPYouTubeProcessor()
        self.demo_videos = self._get_demo_video_list()
    
    def _get_demo_video_list(self) -> List[Dict[str, Any]]:
        """Get list of demo videos for processing"""
        return [
            {
                'url': 'https://www.youtube.com/watch?v=airHRQL5Xtg',
                'title': 'React TypeScript Tutorial for Beginners',
                'channel': 'Programming with Mosh',
                'expected_topics': ['react', 'typescript']
            },
            {
                'url': 'https://www.youtube.com/watch?v=SqcY0GlETPk',
                'title': 'Next.js Tutorial - Build a Portfolio',
                'channel': 'Web Dev Simplified',
                'expected_topics': ['nextjs', 'react']
            },
            {
                'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                'title': 'Advanced Claude Prompt Engineering',
                'channel': 'AI Development',
                'expected_topics': ['claude', 'meta-prompting']
            }
        ]
    
    def process_video_with_mcp_transcript(self, video_url: str, title: str = "", channel: str = "") -> Optional[VideoAnalysisResult]:
        """Process video using MCP transcript integration"""
        try:
            logger.info(f"🎥 Processing video with MCP integration: {title or video_url}")
            
            # Step 1: Get transcript via MCP
            transcript = self._get_transcript_via_mcp_call(video_url)
            if not transcript:
                logger.error(f"Failed to get transcript for {video_url}")
                return None
            
            # Step 2: Process video with real transcript
            # Temporarily inject the transcript for processing
            original_method = self.processor.get_transcript_via_mcp
            
            def mock_transcript_method(url: str, lang: str = "en") -> Optional[str]:
                return transcript if url == video_url else None
            
            self.processor.get_transcript_via_mcp = mock_transcript_method
            
            try:
                result = self.processor.process_video(video_url, title, channel)
                return result
            finally:
                # Restore original method
                self.processor.get_transcript_via_mcp = original_method
                
        except Exception as e:
            logger.error(f"Error processing video with MCP: {str(e)}")
            return None
    
    def _get_transcript_via_mcp_call(self, video_url: str, lang: str = "en") -> Optional[str]:
        """Get transcript using actual MCP call - this would be replaced with real MCP integration"""
        try:
            # This is where you would make the actual MCP call
            # For demo purposes, we'll simulate different transcript types
            
            logger.info("🔄 Making MCP transcript call...")
            
            # Simulate MCP call delay
            import time
            time.sleep(0.5)
            
            # Return appropriate sample transcript based on video URL
            if 'react' in video_url.lower() or 'typescript' in video_url.lower():
                return self._get_react_typescript_sample()
            elif 'claude' in video_url.lower() or 'prompt' in video_url.lower():
                return self._get_claude_prompting_sample()
            elif 'next' in video_url.lower():
                return self._get_nextjs_sample()
            else:
                return self._get_general_programming_sample()
                
        except Exception as e:
            logger.error(f"MCP transcript call failed: {str(e)}")
            return None
    
    def _get_react_typescript_sample(self) -> str:
        """Sample React TypeScript transcript"""
        return """
        Welcome everyone to this comprehensive React TypeScript tutorial. I'm excited to walk you through building a modern web application using React with TypeScript.

        First, let's understand why TypeScript is such a game-changer in React development. TypeScript provides static type checking, which means we can catch errors at compile time rather than discovering them at runtime. This is incredibly valuable in larger applications where maintaining code quality becomes crucial.

        Let's start by setting up our development environment. I recommend using Create React App with the TypeScript template. You can set this up by running: npx create-react-app my-app --template typescript.

        Now, let's dive into components. In TypeScript, we can define interfaces for our component props. Here's a practical example of a Button component:

        interface ButtonProps {
          onClick: () => void;
          children: React.ReactNode;
          variant?: 'primary' | 'secondary' | 'danger';
          disabled?: boolean;
        }

        const Button: React.FC<ButtonProps> = ({ 
          onClick, 
          children, 
          variant = 'primary',
          disabled = false 
        }) => {
          return (
            <button 
              className={`btn btn-${variant}`}
              onClick={onClick}
              disabled={disabled}
            >
              {children}
            </button>
          );
        };

        Now let's talk about state management with hooks. The useState hook in TypeScript can be explicitly typed:

        const [count, setCount] = useState<number>(0);
        const [user, setUser] = useState<User | null>(null);
        const [loading, setLoading] = useState<boolean>(false);

        For more complex state management, we can use useReducer. Here's how to properly type a reducer:

        type CounterAction = 
          | { type: 'INCREMENT' }
          | { type: 'DECREMENT' }
          | { type: 'SET_VALUE'; payload: number }
          | { type: 'RESET' };

        interface CounterState {
          value: number;
          history: number[];
        }

        const counterReducer = (state: CounterState, action: CounterAction): CounterState => {
          switch (action.type) {
            case 'INCREMENT':
              return {
                value: state.value + 1,
                history: [...state.history, state.value + 1]
              };
            case 'DECREMENT':
              return {
                value: state.value - 1,
                history: [...state.history, state.value - 1]
              };
            case 'SET_VALUE':
              return {
                value: action.payload,
                history: [...state.history, action.payload]
              };
            case 'RESET':
              return {
                value: 0,
                history: [0]
              };
            default:
              return state;
          }
        };

        Custom hooks are incredibly powerful in TypeScript. Here's a reusable hook for API calls:

        interface UseApiResult<T> {
          data: T | null;
          loading: boolean;
          error: string | null;
          refetch: () => void;
        }

        function useApi<T>(url: string): UseApiResult<T> {
          const [data, setData] = useState<T | null>(null);
          const [loading, setLoading] = useState<boolean>(true);
          const [error, setError] = useState<string | null>(null);

          const fetchData = useCallback(async () => {
            try {
              setLoading(true);
              setError(null);
              const response = await fetch(url);
              if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
              }
              const result = await response.json();
              setData(result);
            } catch (err) {
              setError(err instanceof Error ? err.message : 'An error occurred');
            } finally {
              setLoading(false);
            }
          }, [url]);

          useEffect(() => {
            fetchData();
          }, [fetchData]);

          return { data, loading, error, refetch: fetchData };
        }

        Performance optimization is crucial. React.memo helps prevent unnecessary re-renders:

        interface UserCardProps {
          user: User;
          onEdit: (id: string) => void;
        }

        const UserCard = React.memo<UserCardProps>(({ user, onEdit }) => {
          console.log('UserCard rendering for:', user.name);
          
          return (
            <div className="user-card">
              <h3>{user.name}</h3>
              <p>{user.email}</p>
              <button onClick={() => onEdit(user.id)}>Edit</button>
            </div>
          );
        });

        For expensive computations, use useMemo:

        const expensiveValue = useMemo(() => {
          return data.reduce((acc, item) => {
            // Complex calculation
            return acc + (item.value * item.multiplier);
          }, 0);
        }, [data]);

        And useCallback for stable function references:

        const handleSubmit = useCallback((formData: FormData) => {
          // Form submission logic
          console.log('Submitting:', formData);
        }, [/* dependencies */]);

        Error boundaries are essential for production applications. Here's a TypeScript error boundary:

        interface ErrorBoundaryState {
          hasError: boolean;
          error?: Error;
          errorInfo?: React.ErrorInfo;
        }

        class ErrorBoundary extends React.Component<
          React.PropsWithChildren<{}>,
          ErrorBoundaryState
        > {
          constructor(props: React.PropsWithChildren<{}>) {
            super(props);
            this.state = { hasError: false };
          }

          static getDerivedStateFromError(error: Error): ErrorBoundaryState {
            return { hasError: true, error };
          }

          componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
            this.setState({
              error,
              errorInfo
            });
            
            // Log error to service
            console.error('Error caught by boundary:', error, errorInfo);
          }

          render() {
            if (this.state.hasError) {
              return (
                <div className="error-boundary">
                  <h2>Something went wrong.</h2>
                  <details>
                    <summary>Error details</summary>
                    <pre>{this.state.error?.toString()}</pre>
                  </details>
                </div>
              );
            }

            return this.props.children;
          }
        }

        Testing TypeScript React components with Jest and React Testing Library:

        import { render, screen, fireEvent, waitFor } from '@testing-library/react';
        import userEvent from '@testing-library/user-event';
        import { UserCard } from './UserCard';

        const mockUser: User = {
          id: '1',
          name: 'John Doe',
          email: 'john@example.com'
        };

        describe('UserCard', () => {
          test('renders user information correctly', () => {
            const handleEdit = jest.fn();
            
            render(<UserCard user={mockUser} onEdit={handleEdit} />);
            
            expect(screen.getByText('John Doe')).toBeInTheDocument();
            expect(screen.getByText('john@example.com')).toBeInTheDocument();
          });

          test('calls onEdit when edit button is clicked', async () => {
            const handleEdit = jest.fn();
            const user = userEvent.setup();
            
            render(<UserCard user={mockUser} onEdit={handleEdit} />);
            
            const editButton = screen.getByRole('button', { name: /edit/i });
            await user.click(editButton);
            
            expect(handleEdit).toHaveBeenCalledWith('1');
          });
        });

        Context API with TypeScript provides excellent type safety for global state:

        interface AppContextType {
          user: User | null;
          theme: 'light' | 'dark';
          updateUser: (user: User) => void;
          toggleTheme: () => void;
        }

        const AppContext = React.createContext<AppContextType | undefined>(undefined);

        export const useAppContext = (): AppContextType => {
          const context = useContext(AppContext);
          if (!context) {
            throw new Error('useAppContext must be used within AppProvider');
          }
          return context;
        };

        This comprehensive guide covers the essential patterns for React TypeScript development. The key benefits are type safety, excellent IDE support, refactoring confidence, and self-documenting code through types. Remember to adopt TypeScript gradually and focus on readable, maintainable code over complex type gymnastics.
        """
    
    def _get_claude_prompting_sample(self) -> str:
        """Sample Claude prompting transcript"""
        return """
        Welcome to this advanced guide on Claude prompt engineering and meta-prompting techniques. I'm going to share some powerful strategies that can dramatically improve your AI interactions.

        Let's start with the fundamentals. Claude responds best to clear, specific instructions. Instead of saying "help me code," try "help me create a React component that handles user authentication with TypeScript types and error handling."

        Meta-prompting is about teaching Claude how to think about problems. Here's a powerful pattern - the Chain of Thought approach:

        "Let's think through this step by step:
        1. First, analyze the requirements
        2. Then, consider the constraints
        3. Next, explore potential solutions
        4. Finally, implement the best approach"

        Constitutional AI principles are built into Claude. You can leverage this by asking Claude to consider ethical implications, security concerns, and best practices. For example:

        "Please review this code for security vulnerabilities, accessibility issues, and maintainability concerns. Provide specific recommendations for each area."

        Role-based prompting is incredibly effective. Instead of generic requests, assign Claude a specific role:

        "Act as a senior software architect. Design a microservices architecture for an e-commerce platform. Consider scalability, security, and maintainability."

        Few-shot prompting provides examples to guide Claude's responses:

        "Here are examples of good API documentation:
        Example 1: [detailed example]
        Example 2: [detailed example]
        
        Now, create documentation for this new API endpoint following the same pattern."

        Iterative refinement is key. Start with a basic prompt, then refine based on Claude's response:

        Initial: "Create a React component"
        Refined: "Create a reusable React component with TypeScript, proper error handling, and accessibility features"
        Further refined: "Create a reusable React form component with TypeScript, Zod validation, proper error handling, ARIA attributes, and comprehensive tests"

        Context management is crucial for longer conversations. Regularly summarize what's been accomplished and what comes next:

        "So far we've created the component structure and added basic functionality. Next, let's add comprehensive error handling and write tests for edge cases."

        Prompt chaining allows you to break complex tasks into smaller, manageable pieces:

        Step 1: "Analyze the requirements for this feature"
        Step 2: "Design the architecture based on the requirements"
        Step 3: "Implement the core functionality"
        Step 4: "Add error handling and edge cases"
        Step 5: "Write comprehensive tests"

        System prompts and instructions can set the context for entire conversations:

        "You are an expert in modern web development. For all code examples, use TypeScript, follow React best practices, include proper error handling, and explain your architectural decisions."

        Constraint-based prompting helps focus responses:

        "Create a solution that:
        - Uses only built-in React hooks
        - Has no external dependencies
        - Maintains under 100 lines of code
        - Includes comprehensive error handling"

        Socratic prompting encourages deeper thinking:

        "What would happen if this component received invalid props? How would you handle that scenario? What are the trade-offs of different approaches?"

        Template-based prompting ensures consistency:

        "For each solution, provide:
        1. Problem analysis
        2. Approach explanation
        3. Implementation with TypeScript
        4. Testing strategy
        5. Potential improvements"

        Verification prompting helps catch errors:

        "Please review this code and check for:
        - Type safety issues
        - Performance concerns
        - Accessibility problems
        - Security vulnerabilities
        - Best practice violations"

        Advanced techniques include:

        Perspective taking: "From a junior developer's perspective, explain this concept"
        Analogical reasoning: "Explain this programming concept using a real-world analogy"
        Adversarial thinking: "What could go wrong with this approach?"
        Optimization focus: "How could we make this more efficient?"

        The key to effective Claude prompting is being specific, providing context, and iterating on your approach. Remember that Claude can help you refine your prompts - don't hesitate to ask "How could I improve this prompt to get better results?"

        Quality prompting is about creating a collaborative relationship with Claude where you guide the conversation toward your goals while leveraging Claude's capabilities for analysis, creativity, and problem-solving.
        """
    
    def _get_nextjs_sample(self) -> str:
        """Sample Next.js transcript"""
        return """
        Welcome to this comprehensive Next.js tutorial. We're going to build a full-stack web application using Next.js 14 with the new App Router.

        Next.js is a React framework that provides server-side rendering, static site generation, and many other powerful features out of the box. The App Router introduced in Next.js 13 brings significant improvements to routing, layouts, and data fetching.

        Let's start by setting up our project:

        npx create-next-app@latest my-portfolio --typescript --tailwind --eslint --app

        The App Router uses a file-system based routing where folders define routes. Here's the basic structure:

        app/
          layout.tsx          # Root layout
          page.tsx           # Home page
          about/
            page.tsx         # About page
          blog/
            page.tsx         # Blog listing
            [slug]/
              page.tsx       # Individual blog post

        Root layout is shared across all pages:

        export default function RootLayout({
          children,
        }: {
          children: React.ReactNode
        }) {
          return (
            <html lang="en">
              <body>
                <header>
                  <nav>Navigation</nav>
                </header>
                <main>{children}</main>
                <footer>Footer</footer>
              </body>
            </html>
          )
        }

        Server Components are the default in the App Router. They run on the server and can directly access databases:

        async function getData() {
          const res = await fetch('https://api.example.com/posts')
          if (!res.ok) {
            throw new Error('Failed to fetch data')
          }
          return res.json()
        }

        export default async function BlogPage() {
          const posts = await getData()
          
          return (
            <div>
              <h1>Blog Posts</h1>
              {posts.map((post: any) => (
                <article key={post.id}>
                  <h2>{post.title}</h2>
                  <p>{post.excerpt}</p>
                </article>
              ))}
            </div>
          )
        }

        Client Components are needed for interactivity:

        'use client'
        
        import { useState } from 'react'
        
        export default function Counter() {
          const [count, setCount] = useState(0)
          
          return (
            <div>
              <p>Count: {count}</p>
              <button onClick={() => setCount(count + 1)}>
                Increment
              </button>
            </div>
          )
        }

        API Routes in the App Router use Route Handlers:

        // app/api/posts/route.ts
        import { NextRequest, NextResponse } from 'next/server'
        
        export async function GET() {
          const posts = await fetch('https://jsonplaceholder.typicode.com/posts')
          const data = await posts.json()
          
          return NextResponse.json(data)
        }
        
        export async function POST(request: NextRequest) {
          const body = await request.json()
          
          // Process the data
          const newPost = {
            id: Date.now(),
            ...body
          }
          
          return NextResponse.json(newPost, { status: 201 })
        }

        Dynamic routes use square brackets:

        // app/blog/[slug]/page.tsx
        interface PageProps {
          params: {
            slug: string
          }
        }
        
        export default async function BlogPost({ params }: PageProps) {
          const post = await getPostBySlug(params.slug)
          
          return (
            <article>
              <h1>{post.title}</h1>
              <div dangerouslySetInnerHTML={{ __html: post.content }} />
            </article>
          )
        }

        Loading UI and Error handling:

        // app/blog/loading.tsx
        export default function Loading() {
          return <div>Loading blog posts...</div>
        }
        
        // app/blog/error.tsx
        'use client'
        
        export default function Error({
          error,
          reset,
        }: {
          error: Error
          reset: () => void
        }) {
          return (
            <div>
              <h2>Something went wrong!</h2>
              <button onClick={() => reset()}>Try again</button>
            </div>
          )
        }

        Metadata API for SEO:

        import { Metadata } from 'next'
        
        export const metadata: Metadata = {
          title: 'My Blog',
          description: 'A blog about web development',
          openGraph: {
            title: 'My Blog',
            description: 'A blog about web development',
            images: ['/og-image.jpg'],
          },
        }

        Image optimization with Next.js Image component:

        import Image from 'next/image'
        
        export default function Profile() {
          return (
            <Image
              src="/profile.jpg"
              alt="Profile picture"
              width={500}
              height={500}
              priority
            />
          )
        }

        Middleware for authentication and redirects:

        // middleware.ts
        import { NextResponse } from 'next/server'
        import type { NextRequest } from 'next/server'
        
        export function middleware(request: NextRequest) {
          if (request.nextUrl.pathname.startsWith('/admin')) {
            // Check authentication
            const token = request.cookies.get('token')
            
            if (!token) {
              return NextResponse.redirect(new URL('/login', request.url))
            }
          }
        }

        Static Site Generation (SSG) with generateStaticParams:

        export async function generateStaticParams() {
          const posts = await fetch('https://api.example.com/posts').then((res) =>
            res.json()
          )
         
          return posts.map((post: any) => ({
            slug: post.slug,
          }))
        }

        Streaming with Suspense:

        import { Suspense } from 'react'
        
        export default function Dashboard() {
          return (
            <div>
              <h1>Dashboard</h1>
              <Suspense fallback={<div>Loading stats...</div>}>
                <Stats />
              </Suspense>
              <Suspense fallback={<div>Loading charts...</div>}>
                <Charts />
              </Suspense>
            </div>
          )
        }

        This covers the essential Next.js patterns for modern web development. The App Router provides excellent developer experience with server components, streaming, and built-in optimizations for performance and SEO.
        """
    
    def _get_general_programming_sample(self) -> str:
        """Sample general programming transcript"""
        return """
        Welcome to this programming fundamentals course. Today we'll cover essential concepts that every developer should understand, regardless of the programming language they choose.

        Let's start with clean code principles. Clean code is readable, maintainable, and expressive. It tells a story and makes the developer's intent clear. Here are key principles:

        1. Meaningful names: Choose descriptive names for variables, functions, and classes
        2. Small functions: Functions should do one thing well
        3. Clear comments: Comment why, not what
        4. Consistent formatting: Use consistent indentation and spacing

        Data structures are fundamental to programming. Understanding when to use arrays, objects, maps, sets, and other structures is crucial for writing efficient code.

        Arrays are ordered collections:
        - Use for sequential data
        - Good for iteration
        - Access by index is O(1)

        Objects/Maps are key-value pairs:
        - Use for associative data
        - Good for lookups
        - Access by key is typically O(1)

        Algorithm complexity matters. Big O notation helps us understand performance:
        - O(1): Constant time - hash table lookups
        - O(log n): Logarithmic time - binary search
        - O(n): Linear time - array iteration
        - O(n²): Quadratic time - nested loops

        Error handling is not optional. Always anticipate what can go wrong and handle errors gracefully:
        - Validate input data
        - Handle network failures
        - Provide meaningful error messages
        - Log errors for debugging

        Testing ensures code quality:
        - Unit tests verify individual functions
        - Integration tests verify component interactions
        - End-to-end tests verify complete workflows
        - Write tests before fixing bugs

        Version control with Git is essential:
        - Commit frequently with meaningful messages
        - Use branches for features and experiments
        - Review code before merging
        - Keep a clean commit history

        Database fundamentals apply to most applications:
        - Understand CRUD operations (Create, Read, Update, Delete)
        - Learn about relationships between data
        - Understand indexing for performance
        - Consider data consistency and transactions

        API design principles:
        - RESTful endpoints are predictable
        - Use appropriate HTTP methods
        - Return consistent response formats
        - Include proper error status codes
        - Document your APIs thoroughly

        Security should be built in, not bolted on:
        - Validate and sanitize all input
        - Use parameterized queries to prevent SQL injection
        - Implement proper authentication and authorization
        - Keep dependencies updated
        - Follow the principle of least privilege

        Performance optimization strategies:
        - Profile before optimizing
        - Cache expensive operations
        - Minimize database queries
        - Optimize critical paths first
        - Consider lazy loading for resources

        Code organization and architecture:
        - Separate concerns into different modules
        - Use dependency injection for flexibility
        - Follow SOLID principles
        - Consider design patterns for common problems
        - Keep business logic separate from presentation

        Debugging is a skill that improves with practice:
        - Use debugging tools effectively
        - Read error messages carefully
        - Isolate problems systematically
        - Reproduce issues consistently
        - Document solutions for future reference

        Continuous learning is essential in programming:
        - Stay updated with industry trends
        - Practice coding regularly
        - Contribute to open source projects
        - Learn from code reviews
        - Teach others to reinforce your knowledge

        These fundamentals apply across languages and frameworks. Master these concepts, and you'll be able to adapt to any technology stack.
        """
    
    def run_demo(self):
        """Run the full MCP YouTube integration demo"""
        print("🚀 MCP YouTube Integration Demo")
        print("=" * 60)
        
        results = []
        
        for i, video_info in enumerate(self.demo_videos, 1):
            print(f"\n📹 Processing Video {i}/{len(self.demo_videos)}")
            print(f"   Title: {video_info['title']}")
            print(f"   Channel: {video_info['channel']}")
            print(f"   Expected Topics: {video_info['expected_topics']}")
            
            result = self.process_video_with_mcp_transcript(
                video_info['url'],
                video_info['title'],
                video_info['channel']
            )
            
            if result:
                results.append(result)
                self.processor.save_analysis_result(result)
                
                print(f"   ✅ Success!")
                print(f"   📊 Unified Score: {result.unified_score:.3f}")
                print(f"   🔍 Detected Topics: {result.priority_topics}")
                print(f"   💡 Programming Concepts: {len(result.programming_concepts)}")
                
                # Show top concepts
                if result.programming_concepts:
                    top_concepts = result.programming_concepts[:5]
                    print(f"   🎯 Top Concepts: {', '.join(top_concepts)}")
            else:
                print(f"   ❌ Failed to process video")
        
        # Generate comprehensive report
        if results:
            print(f"\n📊 Generating Processing Report...")
            report = self.processor.generate_processing_report(results)
            
            print(f"\n🎉 Demo Complete!")
            print(f"   Total Videos Processed: {len(results)}")
            print(f"   Average Score: {report['processing_summary']['average_unified_score']:.3f}")
            print(f"   High-Value Videos: {report['processing_summary']['high_value_videos']}")
            
            if report.get('topic_analysis', {}).get('most_common_topics'):
                top_topics = [t[0] for t in report['topic_analysis']['most_common_topics'][:3]]
                print(f"   Top Detected Topics: {', '.join(top_topics)}")
            
            print(f"\n📁 Results saved to: {self.processor.knowledge_vault_path}")
            print(f"📄 Report saved to: {self.processor.knowledge_vault_path}/mcp_processing_report_*.json")
        
        return results

def main():
    """Main entry point for the demo"""
    demo = MCPYouTubeIntegrationDemo()
    
    print("This demo shows how to integrate MCP transcript tools with YouTube content analysis.")
    print("In a real Claude Code environment, the MCP calls would fetch actual transcripts.")
    print("For this demo, we're using realistic sample transcripts to show the analysis capabilities.\n")
    
    results = demo.run_demo()
    
    if results:
        print(f"\n🔍 Sample Analysis Results:")
        for result in results[:2]:  # Show first 2 results
            print(f"\n📝 {result.title}")
            print(f"   Score: {result.unified_score:.3f}")
            print(f"   Topics: {result.priority_topics}")
            print(f"   Concepts: {result.programming_concepts[:8]}")  # First 8 concepts
            
            # Show a snippet of the content summary
            summary_lines = result.content_summary.split('\n')[:5]
            print(f"   Summary: {' '.join(summary_lines).strip()[:150]}...")

if __name__ == "__main__":
    main()