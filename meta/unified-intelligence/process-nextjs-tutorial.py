#!/usr/bin/env python3
"""
Process Next.js Tutorial Video
High-value Next.js 13 tutorial with TypeScript and modern app router
"""

import os
import sys
import json
import logging
import re
from pathlib import Path
from datetime import datetime, timezone

# Add unified intelligence directory to path
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

# Import topic scoring engine directly
import importlib.util
spec = importlib.util.spec_from_file_location("topic_scoring_engine", "topic-scoring-engine.py")
topic_scoring_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(topic_scoring_module)
TopicScoringEngine = topic_scoring_module.TopicScoringEngine

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_nextjs_tutorial():
    """Process the comprehensive Next.js tutorial video"""
    
    # Initialize topic scoring engine
    topic_scorer = TopicScoringEngine()
    
    # Get the Next.js tutorial transcript (truncated for processing)
    transcript = """[Music]
foreign welcome to the ultimate nexjs
course in this course you will learn
everything you need to know about nexjs
from the basics to more advanced
concepts so by the end of the course
you'll be able to confidently build fast
and scalable applications with the xjs
if you have been searching for a
comprehensive easy to follow
well-organized and practical course that
takes you from Zero to Hero this is the
right next.js course for you you don't
need any prior knowledge of next.js to
get started everything you need is right
here so you won't need to jump back and
forth between random tutorials but
here's the catch unlike other courses
we're not just building a dummy app
we'll be building a beautiful full stack
production grade app for tracking issues
an app complete with all the features
and UI patterns you would expect in
modern applications on the home page we
have this beautiful dashboard that
displays the latest issues and their
status and all of this data is stored in
a mySQL database we can go to the issues
page we can filter issues
sort them
and go to different pages
we can click on an issue to see more
details we can assign an issue to a user
so here we have full authentication and
authorization
we can edit an issue
and here we have this beautiful markdown
editor
we can also delete an issue and here we
get this confirmation dialog box
we'll be building this application using
a Cutting Edge stack next she has 13
Tailwind Radix UI Prisma react query
reactbook forms Zod and more and don't
worry if some of these tools are alien
to you just like my other courses I will
walk you through each one explaining the
what the why and the how so if you
follow along you will master nexjs and
we'll be able to build full stack
applications with confidence
a software engineer with over 20 years
of experience and I've taught Millions
how to code and become professional
software Engineers through my YouTube
channel and online school
codewitmarsh.com if you are new here
make sure to subscribe as I upload new
videos all the time now let's jump in
and get started
[Music]
all right so what exactly do you need to
know to take this course well to take
this course you don't need any prior
knowledge of next.js because I'm going
to teach you everything from the ground
up however you need to have basic
familiarity with react and typescript
because next.js is a react framework and
if you don't know react you are not
really the right student for this course
now if you want to learn react I have a
great tutorial on my YouTube channel the
link is below this video I also have a
comprehensive course that goes way
beyond that it teaches you everything
you need to know to build modern
applications with react 18 and
typescript the full course is 14 hours
divided into two parts so you can easily
finish each part in this course you will
learn how to build this beautiful
application for discovering video games
here we have all the common UI patterns
you see in real applications like
filtering sorting infinite Scrolls and
so on again in case you are interested
the link is below this video
welcome back to our next chess course in
this section we'll be talking about the
fundamentals of nexjs first I will
explain what exactly next.js is and why
is it so popular shortly after we'll set
up our development environment and
create our first next.js project from
there we'll talk about some foundational
Concepts such as client and server
components data fetching caching as well
as static and dynamic rendering this
section is a great introduction to
next.js so let's jump in and get started
[Music]
so you might be wondering what is this
next JS thing everyone is talking about
and why should I bother with it well
next.js is an incredibly powerful
framework for building fast and search
engine friendly applications it's built
on top of react so everything you have
learned about react is still relevant
but nexjs takes web development to the
next level wild react is just a library
for creating interactive user interfaces
next.js is a comprehensive framework
think of a framework as a collection of
libraries tools and conventions that
streamline application development for
instance next.js includes its own
routing Library so we don't need to use
a separate Library like react router in
terms of tooling it comes with a
compiler for transforming and minifying
our JavaScript code a command line
interface for building and starting our
application and a node.js runtime
now you might wonder what exactly is a
node.js runtime well there are two main
ways we can execute JavaScript code
within a web browser on the client side
or within a node.js runtime on the
server so a node.js runtime is just a
fancy term for a program that can
execute JavaScript code so next JS comes
with a node.js runtime and this allows
us to do some really cool things the
first thing is that we can do full stack
development so we can write both the
front end and back-end code within the
same nyxjs project the backend code gets
executed within the node.js runtime and
the front-end code gets bundled and sent
to the client for execution within a web
browser in contrast when building
applications with react we have to
maintain a separate backend project in a
potentially different programming
language this node.js runtime also
allows us to render our components on
the server and send their content to the
client this technique is called
server-side rendering or SSR and can
make our applications faster and more
search engine friendly we'll talk about
it in detail later in the course but
wait there's more with next.js we can
pre-render certain pages and components
that have static data when we build our
application we just render them once and
serve them whenever they are needed this
technique is called Static site
generation and can make our applications
super fast
so in a nutshell next.js is a framework
for building super fast and search
engine friendly applications
[Music]
all right now let's talk about setting
up our development environment to run
next.js you should have node version
16.8 or higher
so head over to nodejs.org and download
the latest version
now in this course I will be using vs
code as my editor just like my other
courses you're welcome to use your
preferred editor but I encourage you to
use vs code because along the way I'll
be sharing a lot of tips and techniques
for writing code fast
so you can get vs code from
code.visualstudio.com
now here in vs code window let's talk
about the extensions I'm going to use in
this course
so in this panel search for es7
all right look at this extension
es7 plus react Redux and react native
this extension gives us a bunch of code
Snippets so we can quickly and easily
generate react components the next
extension is typescript
is this one here JavaScript and
typescript nightly
and the last one is
Tailwind CSS
intellisense
now if you have never worked with Telvin
before don't worry it's super easy and
I'm going to hold your hands through the
entire course
[Music]
all right to create our first nexgs
project open up a terminal window and
run npx create Dash next Dash app add
you can use the latest version but in
this course I'm going to use version
13.4 so I strongly recommend you to use
the same version so you don't have any
difficulties going through the course
let's go ahead
now it's asking if you want to install
this package create next app version
13.4.13 let's proceed
all right now it's going to ask us a
bunch of questions about our new project
the first question is the name of our
project I'm going to use next Dash app
the next question is if you want to use
typescript in this project the default
answer is yes so let's press enter to
accept it the next question is about
using eslint which is a common code
analysis tool that we can use to find
common errors like syntax errors
formatting issues and so on again we're
going to accept the default value which
is yes
the next question is about using
Tailwind CSS one more time you're going
to accept yes the next question is about
using the source directory a lot of
next.js projects don't use the source
directory so I'm going to select no here
the next question is about using the new
app router I'm going to talk about this
later in this section but very briefly
in Nexus 13 we have two types of routers
we have the new app router and the
Legacy Pages router in this course we're
going to use the new app router so let's
select yes the last question is about
customizing the default import aliens
we're going to select no
all right now it's going to install all
these dependencies so you see we have
react react on next typescript and so on
all right all of our dependencies are
installed so now let's go into this
folder
and run npm run Dev
this starts at development server on
Port 3000 so let's control and click on
this link
and this confirms that our first next.js
project is open running
[Music]
let's talk about the key files and
folders in this project so at the top we
have the app folder or this is also
called the app router this is the
container for our routing system so in
next.js our router is based on the file
system so unlike react router we don't
have to configure our routes and map
them to our components we can simply
create files and folders to represent
our routes we'll talk about them in the
next lesson so in the app folder we have
a favorite icon we have our Global CSS
file a layout file which is a basic
react component that returns an HTML and
body element this represents the common
layout for our Pages now inside the body
element we have children which is
replaced by a page dynamically at
runtime depending on where the user is
in our application
now in this folder we also have a page
file page.tsx this represents our home
page now for this demo let's delete
everything here
and
replace it
with a simple markup so we're going to
return a main element inside main we
want to add an H1 and say hello world
now back to the browser
here we have fast refresh so anytime we
make any changes to our typescript or
css files the changes are reflected
immediately now here we have a bit of
styling issue because there is a
gradient a linear gradient applied to
the body element
so let's go to our Global CSS file
down the bottom look at the Styles
applied to the body element
the background attribute is set to a
linear gradient and that is why we have
this weird style here so simply remove
the background attribute and the issue
goes away beautiful now I want to apply
a padding here so the content is not so
close to the edges of the screen
so let's add padding to
one REM
okay
that is better
so we're done with the app folder
now in this project
after that folder we have the public
folder this is where we can put our
popping assets like images in this case
we have two SVG files here which are
vector graphics one is next the other is
verisal which is the company that has
created nexjs now in the root we have a
bunch of configuration files we have one
for eslint another for next post CSS
tailwind and typescript for the most
part we don't have to touch this
configuration files but if the situation
changes in the future we'll come back
and revisit them
thank you
[Music]
all right I told you that routing in xjs
is based on the file system so here in
the app folder we can create a new
folder called users now to make this
publicly accessible here we should add a
page file in this folder so page dot now
the extension can be JS jsx or TSX or
typescript in this course we use
typescript so I'm going to go with TSX
now make sure to name this file
correctly page in lowercase because this
is one of the conventions that nexjs
looks for so the routing system in xjs
is based on convention not configuration
okay
so here we have a page file now in this
page file we should export a react
component that will be rendered when the
user is at this location slash users
earlier we installed a very useful
extension in vs code with that extension
we can generate a react component using
this shortcut r a f c e that is short
for react Arrow function component with
an export now the way I remember this is
Raf C okay
so that's generated beautiful now here
we have multiple cursors activated so we
can rename this component to something
more meaningful like users page
the name we assign here it doesn't
really matter in terms of routing this
is just for better organization of our
code okay now let's press escape to
deactivate multiple cursors so back to
the browser now let's go to slash users
and here's our new users page beautiful
now one thing you need to know about
this routing system is that if you add
any other files in this folder let's say
test.css this file is not going to be
accessible so if you go to slash users
slash test.css
look we get this not found page so this
is how the new app router is different
from the old Pages router in the pages
router if we put any files in these
folders those files would be publicly
accessible but this is not the case with
the new router okay
so let's delete this file
now here we can also create nested
routes so inside the users folder we can
add a new folder called new
and in this folder we add
a new page file so page.tsx
one more time let's create a react
component and we're going to call this
new user page
good so now we can go to users Slash new
and see this new page beautiful
now let's talk about navigation so we're
going to go back to our home page
so here we press command and P on Mac or
Ctrl mp on Windows to look up files by
their name if we type page we can see
all our page files so the first item is
our home page this is the one we are
looking for
now on this page let's add
an anchor
so here we have
an anchor we set href to slash users
and give it a label like users
now there is a problem with this way of
implementing navigation let me show you
so let's go back to our home page
all right now I'm going to open up
devtools
here in the network tab look at all the
requests sent to the server the first
one is our HTML document the second one
is a font the third one is a CSS file
and after that we have a bunch of
JavaScript files now I'm going to clear
this list
look what happens when we click on the
user's link
let's go back to the network tab look
all these resources are redownloaded
this is not the optimal way to implement
navigation because in the real
application we probably have a
navigation bar on the top the side panel
on the left so as the user navigates
from one page to another we don't want
to reload all these repetitive parts we
only want to replace the content area
right this is where we use the link
component in next.js so back to our code
we're going to replace this anchor with
a link component that is defined in next
slash link Library
okay let's replace it here as well
good now back to our home page once
again I'm going to bring up the network
Tab and clear this list
now look what happens when we click on
the user's link
look we only have two requests and these
requests are for downloading the content
of the users page so we are not
re-downloading a font a CSS file and a
bunch of JavaScript files this is what
we call client-side navigation now there
is more to navigation we have a
comprehensive section about this topic
later in the course this was just a
basic overview
[Music]
in the next rest projects we have two
environments where we can render our
components and generate HTML markup
either on the client within a web
browser or on the server within a
node.js runtime rendering components on
the client is similar to how react
applications work we refer to this
technique as client-side rendering or
CSR on the flip side we have server-side
rendering or SSR where components are
rendered on the server so what are the
differences well with client-side
rendering we have to bundle all our
components and send them to the client
for rendering this means as our
application grows so does our bundle
size because it must contain all of our
components now the larger the bundle the
more memory we need on the client to
load all these components so this
approach is resource heavy the other
problem is that search engine bot Parts
which are machines that browse and index
our websites can't view our content
because they can't execute JavaScript
code so they cannot render our
components like a web browser and last
but not least any sensitive data we have
in our components or their dependencies
like API keys will be exposed to the
client now if we render our components
on the server we can get rid of all
these problems we only send the
essential components to the client and
prevent our bundle from becoming
unnecessarily large also because the
server handles most of the rendering we
need less resources on the client plus
because rendering is done on the server
and we send the actual content to the
client search engine Bots can view and
index our pages and finally we can keep
sensitive data like API keys on the
server so these are all the great
benefits of server-side rendering
however with server-side rendering we
lose interactivity so server components
which are components that are rendered
on the server cannot listen to browser
events like Click Change submit and so
on they cannot access browser apis like
the local storage they cannot maintain
state or use effects these
functionalities are only available in
client components so in real-world
applications we often use a mixture of
server and client components we should
default to server components and use
client components only when we
absolutely need them here is an example
let's imagine we want to build a page to
show a list of products to build this
page we probably need several components
like navbar sidebar product list product
card pagination and footer now in
standard react applications we have to
package all these components and send
them to the client for rendering but in
next.js we can keep all these components
on the server and minimize the bundle
size there is just one exception to add
a product to a shopping cart we need to
handle the click event of a button
typically we implement this
functionality in the product card
component so we have to make it a client
component that's one option but there is
a better way we can keep this component
on the server and do most of the
rendering there and instead extract a
small component that only contains the
add button with this change we only ship
that tiny component to the client and
keep everything else on the server let's
see this in action back to our project
in next.js all components inside the app
folder are server components by default
so that means all the pages we have
created so far these are server
components and are rendered on the
server let me show you so back to the
browser let's bring up the network Tab
and look at the first request this is
the HTML document that we get from the
backend so look we have our content here
we have our hello world and the user's
link this is exactly what search engine
Bots see when they browse our website in
contrast if we used client-side
rendering which is how standard react
applications work search engine Bots
wouldn't be able to see our content they
would see a blank page because all
components all the content is rendered
on the client okay
so back to our project all components
inside the app folder are server
components by default now if you have
worked with nextjs before I should
mention that the pages router doesn't
support server components so going
forward you should stop using it and
switch to the new app router okay
now let's create a new folder here
called components earlier I told you
that this folder is not publicly
accessible unless we have a page file
inside it so that means we can co-locate
our project files like our components
and other building blocks with our Pages
we can put them next to each other and
this is perfectly fine so here in the
components folder let's add
a new file called Product card.tsx
here we create a basic react component
now earlier I told you that server
components cannot have interactivity so
they cannot handle browser events like
Click Change and so on so that means if
we add a button here
and handle the click event we get a
runtime error let me show you so let's
pass a basic error function
and log something on the console
and we set the label to add to cart
now let's add this component to our home
page
so we go to our first page file
and add our new product card component
now back to the browser look we got an
error saying event handlers cannot be
passed to client component props if you
need interactivity consider converting
part of this to a client component now
here we have two options one option is
to make this entire component a client
component so we go to the top
and use the client directive so in
quotes we type use client that's all we
have to do with this we tell the Nexus
compiler to include this file or this
component in our JavaScript bundle and
that means if this component is
dependent on other components those
components will automatically become
client components and will be included
in our JavaScript bundle so we don't
have to repeat this directive on every
client component okay so here's one
option now if you go back to the browser
the error is gone but there is a better
way to make our applications faster and
more search engine friendly we want to
render our components on the server as
much as possible and use client
components only when absolutely
necessary so here our product card could
have some complex markup we want to
render all that markup on the server and
move this button to the client
so I'm going to extract this button and
put it inside a separate component so
here in the components folder let's add
a new file
add to cart
again we create a basic react component
on the top
we use the client directive and then we
move
this button to our new component
like this okay so now we have a client
component and we're going to use this in
our product card
okay
with this we can remove use client from
this file so this component will be
rendered on the server and that means
where we have a client component in this
case where we have this button there is
going to be a hole or a slot where react
will later inject our client component
okay now if you go back to the home page
again we don't see any errors so this is
how we can create and use client and
server components"""
    
    # Video metadata for Next.js tutorial
    video_data = {
        'video_id': 'ZVnjOPwW4ZA',
        'video_url': 'https://www.youtube.com/watch?v=ZVnjOPwW4ZA',
        'title': 'Next js Tutorial for Beginners | Nextjs 13 (App Router) with TypeScript',
        'channel': 'Code with Mosh',
        'priority': 'highest',
        'expected_topics': ['nextjs', 'react', 'typescript'],
        'estimated_duration': '1h+',
        'tutorial_type': 'comprehensive_beginner_course',
        'covers_modern_features': True,
        'instructor_authority': 'high'  # Code with Mosh is a well-known educator
    }
    
    # Enhanced programming concept patterns for Next.js content
    programming_patterns = {
        'nextjs_core': r'\b(?:next\.?js|nextjs|app router|pages router|server components|client components|static rendering|dynamic rendering)\b',
        'nextjs_features': r'\b(?:server side rendering|ssr|static site generation|ssg|file system routing|image optimization|automatic code splitting)\b',
        'react_integration': r'\b(?:react|jsx|tsx|component|props|state|hook|useEffect|useState|react router)\b',
        'typescript_features': r'\b(?:typescript|interface|type|generic|type annotation|ts|tsx|type safety)\b',
        'web_fundamentals': r'\b(?:html|css|javascript|dom|browser|client|server|node\.?js|runtime|bundle)\b',
        'development_tools': r'\b(?:vs code|terminal|npm|npx|create next app|dev server|build|deployment)\b',
        'styling_solutions': r'\b(?:tailwind|css modules|global styles|daisy ui|utility classes|responsive design)\b',
        'data_fetching': r'\b(?:fetch|api|rest|json|database|mysql|prisma|caching|revalidate)\b',
        'modern_stack': r'\b(?:radix ui|react query|react hook forms|zod|prisma|tailwind|markdown editor)\b',
        'performance': r'\b(?:optimization|caching|static|dynamic|bundle size|memory|fast|scalable)\b'
    }
    
    # Extract enhanced programming concepts
    concepts = []
    transcript_lower = transcript.lower()
    
    for category, pattern in programming_patterns.items():
        matches = re.findall(pattern, transcript_lower, re.IGNORECASE)
        for match in matches:
            concept = match.strip().lower().replace('.', '')
            if concept and concept not in concepts and len(concept) > 2:
                concepts.append(concept)
    
    # Calculate concept frequency and sort by relevance
    concept_frequency = {}
    for concept in concepts:
        concept_frequency[concept] = transcript_lower.count(concept)
    
    # Sort by frequency and length, then take top concepts
    concepts = sorted(concept_frequency.keys(), key=lambda x: (concept_frequency[x], len(x)), reverse=True)[:30]
    
    # Create content item for topic scoring
    content_item = {
        'title': video_data['title'],
        'description': f"Ultimate Next.js course covering app router, TypeScript, server components, and modern full-stack development. Build production-grade applications with cutting-edge stack. Duration: {video_data.get('estimated_duration', 'N/A')}",
        'content': transcript,
        'platform': 'youtube',
        'url': video_data['video_url'],
        'published_date': datetime.now(timezone.utc).isoformat(),
        'channel': video_data['channel'],
        'instructor_authority': video_data.get('instructor_authority', 'medium')
    }
    
    # Detect priority topics
    priority_topics = topic_scorer.detect_priority_topics(content_item)
    
    # Calculate enhanced topic scores with Next.js specific bonuses
    with open('priority-topics.json', 'r') as f:
        priority_config = json.load(f)
    
    topic_scores = {}
    for topic in priority_topics:
        topic_config = priority_config.get('priority_topics', {}).get(topic, {})
        base_weight = topic_config.get('weight', 1.0)
        
        # Calculate occurrence frequency
        topic_keywords = [topic] + topic_config.get('aliases', []) + topic_config.get('keywords', [])
        content_text = f"{video_data['title']} {transcript}".lower()
        
        occurrences = sum(content_text.count(keyword.lower()) for keyword in topic_keywords)
        frequency_score = min(occurrences / 20.0, 1.0)  # Higher threshold for longer content
        
        # Next.js specific bonuses
        nextjs_bonus = 1.0
        if topic == 'nextjs':
            nextjs_bonus += 0.3  # Bonus for Next.js content
        if video_data.get('covers_modern_features'):
            nextjs_bonus += 0.2  # Modern features bonus
        if video_data.get('instructor_authority') == 'high':
            nextjs_bonus += 0.15  # Authority instructor bonus
        
        topic_scores[topic] = base_weight * frequency_score * nextjs_bonus
    
    # Calculate unified score with comprehensive tutorial bonuses
    scored_content = topic_scorer.score_content_item(content_item)
    
    # Apply enhanced quality bonuses for comprehensive Next.js tutorials
    quality_bonus = 0.0
    if len(concepts) > 20:
        quality_bonus += 0.15  # Rich concept coverage
    if len(transcript) > 15000:
        quality_bonus += 0.12  # Comprehensive content
    if len(priority_topics) > 2:
        quality_bonus += 0.08  # Multi-topic coverage
    
    # Next.js specific quality indicators
    nextjs_indicators = [
        'app router', 'server components', 'client components', 'typescript',
        'full stack', 'production grade', 'comprehensive', 'beginner'
    ]
    nextjs_score = sum(1 for indicator in nextjs_indicators 
                      if indicator in video_data['title'].lower() or indicator in transcript.lower())
    if nextjs_score > 5:
        quality_bonus += 0.12
    
    # Modern stack bonus
    modern_stack = ['tailwind', 'prisma', 'radix ui', 'react query', 'typescript']
    modern_score = sum(1 for tech in modern_stack if tech.lower() in transcript.lower())
    if modern_score > 3:
        quality_bonus += 0.08
    
    unified_score = min(scored_content.final_score + quality_bonus, 1.0)
    
    # Generate enhanced content quality indicators for Next.js
    transcript_lower = transcript.lower()
    content_quality_indicators = {
        'has_code_examples': any(indicator in transcript_lower for indicator in ['create', 'npm', 'tsx', 'component', 'import', 'export']),
        'has_explanations': any(indicator in transcript_lower for indicator in ['explain', 'understand', 'what is', 'why', 'how']),
        'has_best_practices': any(indicator in transcript_lower for indicator in ['should', 'recommended', 'best', 'optimize', 'performance']),
        'has_troubleshooting': any(indicator in transcript_lower for indicator in ['error', 'fix', 'debug', 'issue', 'problem']),
        'has_step_by_step': any(indicator in transcript_lower for indicator in ['step', 'first', 'next', 'now', "let's"]),
        'has_practical_demo': any(indicator in transcript_lower for indicator in ['build', 'create', 'project', 'application', 'demo']),
        'covers_modern_nextjs': any(indicator in transcript_lower for indicator in ['app router', 'server components', 'next 13', 'typescript']),
        'covers_full_stack': any(indicator in transcript_lower for indicator in ['full stack', 'backend', 'database', 'api']),
        'covers_deployment': any(indicator in transcript_lower for indicator in ['deploy', 'production', 'build', 'serve']),
        'covers_styling': any(indicator in transcript_lower for indicator in ['tailwind', 'css', 'styling', 'ui'])
    }
    
    learning_value_indicators = {
        'beginner_friendly': any(indicator in transcript_lower for indicator in ['beginner', 'basic', 'introduction', 'zero to hero', 'from scratch']),
        'advanced_concepts': any(indicator in transcript_lower for indicator in ['advanced', 'complex', 'server components', 'optimization']),
        'comprehensive_coverage': len(concepts) > 25,
        'practical_focus': any(indicator in transcript_lower for indicator in ['build', 'create', 'project', 'production grade', 'real application']),
        'industry_relevant': any(indicator in transcript_lower for indicator in ['modern', 'cutting edge', 'professional', 'production']),
        'up_to_date': any(indicator in transcript_lower for indicator in ['next 13', 'latest', 'new', 'modern']),
        'instructor_credibility': video_data.get('instructor_authority') == 'high',
        'complete_course': any(indicator in transcript_lower for indicator in ['course', 'complete', 'comprehensive', 'ultimate'])
    }
    
    # Check expected topic coverage
    covered_topics = [topic for topic in video_data['expected_topics'] if topic in priority_topics]
    missing_topics = [topic for topic in video_data['expected_topics'] if topic not in priority_topics]
    coverage_percentage = len(covered_topics) / len(video_data['expected_topics']) * 100 if video_data['expected_topics'] else 100
    
    # Generate enhanced content summary with Next.js focus
    sentences = transcript.split('.')
    key_sentences = []
    
    # Look for Next.js specific key sentences
    nextjs_keywords = ['next.js', 'server components', 'app router', 'typescript', 'full stack', 'react framework']
    
    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) > 30:
            sentence_lower = sentence.lower()
            if (any(concept in sentence_lower for concept in concepts[:20]) or 
                any(keyword in sentence_lower for keyword in nextjs_keywords)):
                key_sentences.append(sentence)
    
    summary_sentences = key_sentences[:10] if key_sentences else sentences[:6]
    
    content_summary = f"## Comprehensive Next.js Tutorial Analysis: \"{video_data['title']}\"\n\n"
    content_summary += f"**Channel:** {video_data['channel']}\n"
    content_summary += f"**Tutorial Type:** {video_data.get('tutorial_type', 'Tutorial').replace('_', ' ').title()}\n"
    content_summary += f"**Estimated Duration:** {video_data.get('estimated_duration', 'N/A')}\n"
    content_summary += f"**Instructor Authority:** {video_data.get('instructor_authority', 'Medium').title()}\n"
    content_summary += f"**Modern Features Coverage:** {'Yes' if video_data.get('covers_modern_features') else 'No'}\n\n"
    
    if concepts:
        content_summary += "### Next.js & Related Technologies Covered\n\n"
        concept_groups = {}
        for concept in concepts[:25]:  # Top 25 concepts
            categorized = False
            for category, pattern in programming_patterns.items():
                if re.search(pattern, concept, re.IGNORECASE):
                    category_display = category.replace('_', ' ').title()
                    if category_display not in concept_groups:
                        concept_groups[category_display] = []
                    if concept not in concept_groups[category_display]:
                        concept_groups[category_display].append(concept)
                    categorized = True
                    break
        
        for category, items in concept_groups.items():
            if items and len(items) > 1:  # Only show categories with multiple items
                content_summary += f"**{category}:**\n"
                for item in items[:7]:  # Limit to 7 per category
                    content_summary += f"- {item}\n"
                content_summary += "\n"
    
    if summary_sentences:
        content_summary += "### Key Tutorial Insights\n\n"
        for i, sentence in enumerate(summary_sentences, 1):
            clean_sentence = sentence.strip().replace('\n', ' ')
            if len(clean_sentence) > 40:  # Only include substantial sentences
                content_summary += f"{i}. {clean_sentence}\n"
    
    # Add Next.js specific tutorial structure analysis
    content_summary += "\n### Next.js Tutorial Structure\n\n"
    structure_sections = {
        'Introduction & Setup': ['what is', 'setup', 'install', 'create next app'],
        'Core Concepts': ['app router', 'server components', 'client components', 'routing'],
        'TypeScript Integration': ['typescript', 'interface', 'type', 'tsx'],
        'Styling Solutions': ['tailwind', 'css', 'styling', 'ui'],
        'Data Fetching': ['fetch', 'api', 'data', 'caching'],
        'Full Stack Development': ['full stack', 'backend', 'database', 'production'],
        'Performance & Optimization': ['optimization', 'static', 'dynamic', 'performance']
    }
    
    for section, keywords in structure_sections.items():
        if any(keyword in transcript_lower for keyword in keywords):
            content_summary += f"✓ **{section}** - Covered\n"
    
    # Enhanced insights with Next.js specific metrics
    insights = {
        'priority_video': True,
        'tutorial_type': video_data.get('tutorial_type', 'standard'),
        'nextjs_version': 'Next.js 13',
        'modern_features_covered': video_data.get('covers_modern_features', False),
        'instructor_authority': video_data.get('instructor_authority', 'medium'),
        'expected_topics_covered': {
            'expected': video_data['expected_topics'],
            'found': priority_topics,
            'covered': covered_topics,
            'missing': missing_topics,
            'coverage_percentage': coverage_percentage
        },
        'concept_count': len(concepts),
        'transcript_length': len(transcript),
        'topic_diversity': len(priority_topics),
        'technical_depth': len([c for c in concepts if c in ['server components', 'app router', 'typescript', 'full stack']]),
        'content_quality_indicators': content_quality_indicators,
        'learning_value_indicators': learning_value_indicators,
        'topic_score_breakdown': topic_scores,
        'top_concepts': concepts[:15],
        'nextjs_specific_metrics': {
            'covers_app_router': 'app router' in transcript_lower,
            'covers_server_components': 'server components' in transcript_lower,
            'typescript_integration': 'typescript' in transcript_lower,
            'modern_nextjs_features': nextjs_score,
            'full_stack_coverage': content_quality_indicators.get('covers_full_stack', False),
            'production_ready': 'production' in transcript_lower or 'deploy' in transcript_lower
        },
        'tutorial_completeness': {
            'estimated_duration': video_data.get('estimated_duration', 'N/A'),
            'channel_authority': video_data['channel'],
            'beginner_friendly': learning_value_indicators.get('beginner_friendly', False),
            'practical_focus': learning_value_indicators.get('practical_focus', False),
            'up_to_date': learning_value_indicators.get('up_to_date', False)
        },
        'transcript_analysis': {
            'word_count': len(transcript.split()),
            'unique_technical_terms': len(set(concepts)),
            'nextjs_mentions': transcript_lower.count('next.js') + transcript_lower.count('nextjs'),
            'code_examples': transcript_lower.count('create') + transcript_lower.count('import') + transcript_lower.count('component'),
            'explanation_quality': transcript_lower.count('explain') + transcript_lower.count('understand') + transcript_lower.count('why')
        }
    }
    
    # Calculate enhanced quality score with Next.js specific weightings
    quality_score = unified_score
    quality_score += 0.15 if content_quality_indicators.get('covers_modern_nextjs') else 0
    quality_score += 0.12 if content_quality_indicators.get('has_practical_demo') else 0
    quality_score += 0.10 if content_quality_indicators.get('has_step_by_step') else 0
    quality_score += 0.08 if content_quality_indicators.get('has_best_practices') else 0
    quality_score += 0.15 if learning_value_indicators.get('practical_focus') else 0
    quality_score += 0.12 if learning_value_indicators.get('comprehensive_coverage') else 0
    quality_score += 0.10 if learning_value_indicators.get('beginner_friendly') else 0
    quality_score += 0.08 if learning_value_indicators.get('up_to_date') else 0
    quality_score += 0.10 if learning_value_indicators.get('instructor_credibility') else 0
    quality_score += 0.06 if content_quality_indicators.get('covers_full_stack') else 0
    quality_score += (coverage_percentage / 100) * 0.15
    
    # Bonus for comprehensive Next.js course
    if video_data.get('tutorial_type') == 'comprehensive_beginner_course':
        quality_score += 0.12
    
    quality_score = min(quality_score, 1.0)
    
    # Save results to priority YouTube intelligence
    knowledge_vault_path = Path(__file__).parent.parent.parent / "knowledge-vault" / "databases" / "knowledge_vault" / "content-intelligence" / "priority-youtube"
    process_date = datetime.now().strftime('%Y-%m-%d')
    save_dir = knowledge_vault_path / process_date
    save_dir.mkdir(parents=True, exist_ok=True)
    
    # Save unified intelligence file
    result_file = save_dir / f"{video_data['video_id']}_nextjs_tutorial_unified_intelligence.json"
    
    result_dict = {
        'video_id': video_data['video_id'],
        'video_url': video_data['video_url'],
        'title': video_data['title'],
        'channel': video_data['channel'],
        'tutorial_type': video_data.get('tutorial_type', 'standard'),
        'nextjs_version': 'Next.js 13',
        'estimated_duration': video_data.get('estimated_duration', 'N/A'),
        'instructor_authority': video_data.get('instructor_authority', 'medium'),
        'modern_features_covered': video_data.get('covers_modern_features', False),
        'programming_concepts': concepts,
        'priority_topics': priority_topics,
        'topic_scores': topic_scores,
        'unified_score': unified_score,
        'quality_score': quality_score,
        'content_summary': content_summary,
        'insights': insights,
        'processing_timestamp': datetime.now(timezone.utc).isoformat(),
        'processed_with': 'nextjs-tutorial-processor',
        'framework_version': '1.2.0',
        'content_type': 'comprehensive_nextjs_tutorial',
        'transcript_available': True,
        'high_value_indicators': {
            'modern_nextjs': content_quality_indicators.get('covers_modern_nextjs', False),
            'comprehensive_course': learning_value_indicators.get('complete_course', False),
            'beginner_friendly': learning_value_indicators.get('beginner_friendly', False),
            'practical_focus': learning_value_indicators.get('practical_focus', False),
            'authority_instructor': learning_value_indicators.get('instructor_credibility', False),
            'up_to_date': learning_value_indicators.get('up_to_date', False)
        }
    }
    
    with open(result_file, 'w') as f:
        json.dump(result_dict, f, indent=2)
    
    # Save enhanced transcript
    transcript_file = save_dir / f"{video_data['video_id']}_nextjs_tutorial_transcript.txt"
    with open(transcript_file, 'w') as f:
        f.write(f"# COMPREHENSIVE NEXT.JS TUTORIAL ANALYSIS\n")
        f.write(f"# Title: {video_data['title']}\n")
        f.write(f"# Channel: {video_data['channel']}\n")
        f.write(f"# Video URL: {video_data['video_url']}\n")
        f.write(f"# Tutorial Type: {video_data.get('tutorial_type', 'Standard').replace('_', ' ').title()}\n")
        f.write(f"# Next.js Version: Next.js 13 (App Router)\n")
        f.write(f"# Estimated Duration: {video_data.get('estimated_duration', 'N/A')}\n")
        f.write(f"# Instructor Authority: {video_data.get('instructor_authority', 'Medium').title()}\n")
        f.write(f"# Modern Features: {'Yes' if video_data.get('covers_modern_features') else 'No'}\n")
        f.write(f"# Processing Date: {datetime.now(timezone.utc).isoformat()}\n")
        f.write(f"# Unified Score: {unified_score:.3f}\n")
        f.write(f"# Quality Score: {quality_score:.3f}\n")
        f.write(f"# Priority Topics: {', '.join(priority_topics)}\n")
        f.write(f"# Programming Concepts: {len(concepts)}\n")
        f.write(f"# Top Concepts: {', '.join(concepts[:12])}\n")
        f.write(f"\n{'='*80}\n")
        f.write(f"NEXT.JS TUTORIAL TRANSCRIPT\n")
        f.write(f"{'='*80}\n\n")
        f.write(transcript)
    
    # Display comprehensive results
    print("🎯 Next.js Tutorial Processing Complete!")
    print("=" * 70)
    print(f"Video: {video_data['title']}")
    print(f"Channel: {video_data['channel']}")
    print(f"URL: {video_data['video_url']}")
    print(f"Duration: {video_data.get('estimated_duration', 'N/A')}")
    print(f"Next.js Version: Next.js 13 (App Router)")
    print(f"Transcript length: {len(transcript)} characters")
    print()
    
    print("✅ Processing Results:")
    print(f"   Video ID: {video_data['video_id']}")
    print(f"   Unified Score: {unified_score:.3f}")
    print(f"   Quality Score: {quality_score:.3f}")
    print(f"   Tutorial Type: {video_data.get('tutorial_type', 'Standard').replace('_', ' ').title()}")
    print(f"   Priority Topics: {', '.join(priority_topics)}")
    print(f"   Programming Concepts: {len(concepts)}")
    print(f"   Top Concepts: {', '.join(concepts[:12])}")
    print()
    
    print("📊 Next.js Content Quality Analysis:")
    print(f"   ✓ Modern Next.js Features: {'Yes' if content_quality_indicators.get('covers_modern_nextjs') else 'No'}")
    print(f"   ✓ Practical Demo: {'Yes' if content_quality_indicators.get('has_practical_demo') else 'No'}")
    print(f"   ✓ Step-by-Step Guide: {'Yes' if content_quality_indicators.get('has_step_by_step') else 'No'}")
    print(f"   ✓ Best Practices: {'Yes' if content_quality_indicators.get('has_best_practices') else 'No'}")
    print(f"   ✓ Full-Stack Coverage: {'Yes' if content_quality_indicators.get('covers_full_stack') else 'No'}")
    print(f"   ✓ Styling Solutions: {'Yes' if content_quality_indicators.get('covers_styling') else 'No'}")
    print(f"   ✓ TypeScript Integration: {'Yes' if 'typescript' in priority_topics else 'No'}")
    print()
    
    print("🎓 Learning Value Analysis:")
    print(f"   ✓ Beginner Friendly: {'Yes' if learning_value_indicators.get('beginner_friendly') else 'No'}")
    print(f"   ✓ Comprehensive Coverage: {'Yes' if learning_value_indicators.get('comprehensive_coverage') else 'No'}")
    print(f"   ✓ Practical Focus: {'Yes' if learning_value_indicators.get('practical_focus') else 'No'}")
    print(f"   ✓ Industry Relevant: {'Yes' if learning_value_indicators.get('industry_relevant') else 'No'}")
    print(f"   ✓ Up-to-Date Content: {'Yes' if learning_value_indicators.get('up_to_date') else 'No'}")
    print(f"   ✓ Instructor Credibility: {'Yes' if learning_value_indicators.get('instructor_credibility') else 'No'}")
    print()
    
    print("🎯 Expected Topic Coverage:")
    print(f"   Expected: {', '.join(video_data['expected_topics'])}")
    print(f"   Found: {', '.join(priority_topics)}")
    print(f"   Coverage: {coverage_percentage:.1f}%")
    print()
    
    print("🏆 Processing Complete!")
    print(f"   Files saved to: {save_dir}")
    print(f"   Unified intelligence: {result_file.name}")
    print(f"   Transcript: {transcript_file.name}")
    print()
    print("✅ This comprehensive Next.js tutorial is now available for daily digest inclusion!")
    print("🌟 High-authority instructor with modern Next.js 13 app router coverage!")

if __name__ == "__main__":
    process_nextjs_tutorial()