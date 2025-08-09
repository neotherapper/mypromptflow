#!/usr/bin/env python3
"""
Direct Transcript Processor
Process the TypeScript/React video transcript directly using the MCP processor
"""

import os
import sys
import json
import logging
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

def process_typescript_react_video():
    """Process the TypeScript React video directly"""
    
    # Initialize topic scoring engine
    topic_scorer = TopicScoringEngine()
    
    # The real transcript from the MCP call
    transcript = """so in this video we will learn how to
use typescript with react from Basics so
to get started you first need to install
typescript on your machine which you can
do using npm install hyphen G type
script
and you need to mention the version that
you want to install so the current
latest version X 5.2.2
you can also mention latest if you want
to install the latest version but I will
go with 5.2.2 which is the latest one so
once you execute this command it will
install typescript globally so not on a
specific project but for their entire
application all the application so once
it's installed now we can create a
project using typescript
so we can use wheat JS to create the
typescript project so we can say npm
create
so it will ask you the project name I
can say react type script demo
now select react and for the variant I
will select typescript
now this folder is created we can CD
into that
I will open this in the current vs code
now after opening we can open the
terminal let me make this smaller
so you will see all the files you can
see the
tsconfig.json this is all the
configuration file so by default I don't
want app.css now this all the
boilerplate code I don't want I can
remove and I will create new app
component
now as we you can see there is a red
line because we don't have node modules
folder so once you create with just you
need to install the packages so just
execute npm install and it will install
all the packages from package.json so
react
react Dom and all the div dependencies
it will install those packages
now once the packages are installed you
will see that there is still a red
underline coming here so it's saying
does not take this sum error so what you
need to do is you need to press command
shift p or Ctrl shift p and you need to
select
type script version so type here type
script select this option select type
script version and you need to select
the workspace version so you need to
select that option use workspace version
5.2.2
so once you select that now you can see
there is no red underline and you will
be able to successfully able to write
typescript code so that was with vs code
vs code version typescript version is
different from what we installed once
that is done now you have this
now this
index.js I will remove all this code
and I will remove everything else
now in main this is fine
this is fine so now we can start the
application by running
npm run Dev or you can use yarn Dave
script so
can open this
you can see app is getting displayed so
this application is working now let's
see how to use typescript so this is a
normal component to make it typescript
you can add colon FC FC starts for
functional component you need to import
from react
so you add colon and then add this FC
so one thing you notice that the file
name is dot TSX not jsx so every
typescript code you write has to be in
the dot TSX extension if you are using
react if that is not a react code dot TF
is required because that is a typescript
all jsx related code you write in TSX
and without jsx you write in dot PS so
now this is a typescript version and I
can display anything so let's say for
this app component I am passing from
prop let's say from app I am passing
title
let's say title equal to
type script
foreign
now as soon as I add this prop you can
see there is a error
type title string is not assignable to
type intrinsic attribute so what this
means this means that app component
requires a title prop but you have not
mentioned that so what you can do you
can go to app component and here you
need to Define that types which are
which you are passing so all the props
that you are passing to any component
you need to mention that so you can
create the interface here
oops and here whatever props you are
passing so I am calling it title prompt
we can mention title and what the data
type of that prop that you are passing
so this is a string so I will mention it
as a string
now this app props you need to mention
it in angle brackets now what it means
is app is a component which accept these
props and now you can see there is no
red underline and there is no error so
now to access this you can use this
structuring so I can access this title
prop and I can use this title so you can
see typescript demo is getting displayed
so we are correctly able to display so
let me make it H1
so this is and we can CSS also index.css
for the H1 text align Center
now it's in the center
so now let's say I have
let's say in this app component I want
to get list of users and displays we
will create a application which using
which you can understand how to use
typescript with react so let's say there
is a random users API So Random user.me
if you go to this website here you can
get a random user their name and a
location but they all the information so
you can go to documentation and you can
read about with different API so it
accepts results query parameter gender
mail and password Etc so I will use this
random users results equal to 10. so
this so this
so this API will give me results of 10
different random users so let's first
use axios we'll install
axios
we can make API call now we can start
the application again
let me zoom out
and here I will use use effect hook
so I will add empty dependency so this
use effective hook will execute only
once
while the component is loaded now I will
create get users function
and here I will use async of it
await
xios dot get and that API URL now we are
using await so I will declare this
function as a sync and as we are using
await we need to wrap that in a try
catch so if anything goes wrong your
application will not stop
I'll print this error
and we can just lock the data to the
transfer
now this get user function I will call
it here
you can see we get the results which is
the here you can see it the data type
contains in the results property so we
correctly get the results and we have
list of 10 random users so now we can
use the these users to display on the
screen so let's say to now to store that
data we need to declare a state
I will initialize that as empty array
because this is this beta is an array
inside results property so I will log
results
we can see you get this array directly
now I will declare users
set users
equal to use it
here I will call set users
data dot free box
now let's use these users and display
them on the screen so what we will do is
let me write this in a tube
which one
users.map I will display this individual
user for individual users I will return
let's make this an order list
inside it I will return a live
for each individual Ally let's say I
want to display each user's name for
name DOT first
so I will get this user I will
and
name
user.name DOT first
user.name dot last user dot name dot
last
so if you see we are correctly printing
but here you are getting error property
name does not exist this is you can see
on type neighbor so this is typescript
specifics you need to mention what is
the type of user what property it
contains to that specifically you need
to measure so to remove this error and
to fix this error you need to specify
you can see if I Mouse over users you
see it it's type is never array so it's
not on a specific type so you need to
mention that it's an array of objects so
to specify that here you can add
angle bracket and here you need to
specify what type of this array so you
can create another interface here
let's say users
and you need to specify whatever
property you are accessing you need to
specify that so let's say user dot name
so each I need to specify name DOT first
so name is an object so here I can say
name is an object and each object has a
property so it has first and last
40 the first first is also type of
string
and last is our type of string
now which are the different properties
so now these users we can use it here so
this is not just users this is an array
of users so array of objects with this
name property now you can see there is
no error if I refry this
we are getting this key because we have
not added key so let's add a key for
each individual user property has a
unique ID so if you see login dot uuid
so we can use that as a key user Dot
Login dot PO ID
here here again now we need to specify
that user each user has a login property
so here you can say login
which is of type string
now you can see there is no error and if
I refresh this you will not see any
warning now so you can see we are
correctly able to display 10 user names
now let's display another name
so let's say email so where is email
emails comes from
direct email property so I can say user
dot email
again you need to specify that each
individual user has an email property
and which is of type string
we can see there is no error so every
time whenever you are accessing any
property you need to specify that what
is the type of that property now if you
Mouse over this users you can see you
correctly get array of users previously
it all array of Never And if you Mouse
over this you can see its users so it's
type is user so this is an array of
users and it is a individual users
property user subject now we have we are
able to correctly display this let me
make this horizontal line
so we'll see it better
so now so you can see we have lot of
properties for each individual user but
for declaring interface you don't need
to specify all the property so only
those property which you are using you
need to specify so only the properties
which you need you need to specify in
the interface you don't need to specify
everything so now you can see we are
declaring object here but instead of
like this you will mostly see it having
declared separate interface so this you
can declare name so we start every
interface with the capital letter that's
a common convention now I will declare
this
let me remove this
so now name is n here I can use name
you don't need to directly specify here
so the advantage is that if I want to
use this name somewhere else you can
easily use that so you don't have to
repeat that things again again so again
now I can create interface
it's a login
and I will add this uid property
now here I will use login
this looks much better than the previous
version so you have separate interfaces
you can instead of interface you can
also use type if you are familiar with
typescript
you can also use type so like this type
login equal to
uid
string
so this is also valid it depends on your
preference which one you use
so mostly you will see interfaces use
but you can use type also that does not
matter so you need to remember whenever
you are declaring an array in typescript
you need to specify what type of data
you are storing so each individual
property you need to specify
instead of always referring this user
you can de-structure also so here I will
destruct a login property if this Vector
name property
and email profile
now you don't need to always use user
dot user Dot
you can directly use it this is much
better than direct always referring to
so this is object destructuring we are
using now we will create a separate
component so inside SRC I will create
components folder
here I will create user dot PSX you have
to make sure it's PSX extension not jsx
I'll create a component
now whatever we are displaying here will
display in that particular user
component so I will move this inside
user component
now here what you need you need login
name and email so I will pass this as a
prop
log in name and email
so you can see you are getting an error
because whenever you pass prop you need
to specify those types of props when
using typescript so what you can do is
you can again create interface
user
oops
and here I will specify what is the type
of login login has a uuid property so
what you can do is here we have already
defined all these props so what we can
do is you can just export these
interfaces
so this we don't need the specific to
app we can export this also and Export
results
now we can directly use this here so
instead of defining this login again I
can say login
user props now name is of type name
this name is this particular interface
that we have created
email which is of type
string
and now we can declare this as a
functional component
import react and we'll specify the user
props here
now you can see there is no error now
inside this
we need to call this user component
and pass all of the values so I can pass
login equal to login
name equal to name
email equal to email
all these props we are passing and if I
refresh
you can see it still works but now we
are getting that again error of missing
key why because we have removed key so
we previously key was for individual
Ally but now we don't need that key here
we can actually remove this login and we
don't need it here
and here
we'll add that key login
Dot uoid
so now this login we don't need
so if you refresh
you can see it's still works if you want
you can also display any other
properties like gender or
phone number you can display that
information on the screen so if you see
the file is becoming quite larger so
because we have multiple interfaces
so what you can do is it's a common
convention you can use to separate out
these interface in a separate file so
this is app.tfx so you can create new
app dot types
dot PS not TSX
and we can move these interfaces inside
this types file now we also need to
export this because we will be using it
in another file
and we can import app props
from dot app slash types
import these users also
that's it now in user
remove this we need to import this name
from here
we can see now it's by better so you
have
saved some the file is not larger now
it's quite smaller and if you refresh
you can see it still works the users are
initially different and then after some
time they are changing why that is
happening because we have use effect
talk and in react 18 so if you see
package.json we are using react version
18 and in main.jsx we are using react
strict mode so whenever you are using
stick mode with react 18 use effect
execute twice so if I add
console.log here inside or you can say
calling
I'll add it here
so if you rephrase this page you can see
calling it displayed toy so use
effective executed twice so what you can
do is if you don't want to this is only
during development on production it will
execute only once but on development it
execute twice so if you don't want you
can comment out this strict mode
after commenting out if I refresh
you can see it's executed only once and
now if I add this transfer.log calling
if I refresh you can see it is displayed
only once and now you will not see this
data changing so once it's loaded it
remains same it will not change again
because that random user API always
returns different users on every time so
every time we call this API we get
different random users so while it was
calling this user Vector twice so we are
having different results always
I will add a new state
is loading so it is loading
is equal to U state it will have initial
value of 4.
while the data before making the API
call I will set is loading to true
remove this lock
and once the API is done I will set is
loading to Fox
even if there is error I will set it to
forms
and here while the data is loading so I
can display is loading
loading
when I refresh you can see loading is
displayed for some time and then you get
that data
so
if you see here we are repeating the
same code again twice so what we can do
is you can add a finally block this
finally block will always execute even
if there is success or if there is
failure
so you can add this inside directly in
only inside of finally block and you
don't need to repeat it in try and get
so if I refresh you can see you still
get that data
loading messages display and now if you
see we have not specified type of this
so This Is by default so
typescript automatically infers
depending on the data which you have
provided by the initial value it knows
that it's Boolean but in this case it's
not knowing what is the it knows that
it's Boolean but in this case it's
not knowing what is the it knows that
it's a array but it don't know what is
that data that you are storing in that
app that's why you manually need to
specify here here also you can specify a
type of Boolean that also works and you
don't get any error so if you see here
we don't have any error and data is
correctly loaded but that is redundant
code because you are not you don't need
to specify
so that is the Redundant thing so you
don't need to specify if you are
specifying the initial value
to buy this value itself it's clear that
it's Boolean so typescript automatically
infers that data type
so you don't need to specify it again
now let's say we are loading this users
initially so instead of this let's let
me add a button here
show users
I want to display these users only when
we click on this button so I will add on
click Handler
I will add an event listener here
and I'll click
if you find this
here so here I want to make that API
call so now I don't need this use effect
hook
I can directly call this here and I will
declare this function as I see
I will come in this out
now on handle click you are calling this
now when I click on show users you can
see you see that loading user
you can save every time I click you load
different set of users so users are
changing
you can see now it's different so that's
how you can use event listener now let's
say I have another input field here
that's the type equal to text
and on change of this I want to whatever
I am typing at the input field I want to
display it below so let's create a new
on change Handler handle change
and here I will call this
and that value whatever I am storing let
me declare a new state
it will have initial value of empty
username set user name
now I will set this username whenever I
change
and from where I will get I will get
that as an event object
or on change event I have added so I
will get that even but you can see we
are getting error parameter event
implicitly have any type so if I try to
set event dot Target
dot value
we are getting these error here you are
declaring any function when you are
passing anything any parameter you need
to specify what is the type of that
particular event so how can you identify
what is that type
so what you can do is you can convert
this function
into inline function
now you will pass this event and if you
Mouse over this
you can see you are getting that type so
you don't need to guess what is the type
of event or search you can directly use
this type here
and now I will change back this here
you can see now there is no error so
whenever I using event dot you can see
you will get suggestion that the
advantage of typescript so you get Auto
completion whatever properties has that
particular event because I am specifying
change event of input element that is
input element so you have access to
event.target.1 so previously before
without adding this you will not get
those suggestions so if I type dot you
can see there is nothing coming so we
don't get those suggestions that's why
it's important to specify type so only
those values you can use and type script
will automatically give your suggestions
so now you this username is set we can
display this username here
so on change of this we are creating
this username and we are displaying it
below so if I type here mic you can see
its name is automatically displayed
below so this here you are not adding
value so value is optional prop you
don't have to provide so if you want to
provide you can provide so here I can
say username
if I refresh you can see it still works
so when I say it still works but value
is optional prop you don't have to
provide but whenever you provide that
value you have to provide the on change
so it when you provide value and without
on change you will get an error you can
see
you can see we provided a value prop
without on chain Handler that is a react
warning not typescript specific
value is optional prop but if you
provide value you have to provide on
change
so now if I refresh you don't get this
error so I can type Alex
it's working fine when I click on show
users we get this list of users
so this is all about using typescript
with react"""
    
    # Video metadata
    video_data = {
        'video_id': 'KmYoJmZs3sY',
        'video_url': 'https://www.youtube.com/watch?v=KmYoJmZs3sY',
        'title': 'Introduction to TypeScript with React - Complete Tutorial 2024',
        'channel': 'Programming Tutorial Channel',
        'priority': 'high',
        'expected_topics': ['react', 'typescript']
    }
    
    # Extract programming concepts
    programming_patterns = {
        'languages': r'\b(?:python|javascript|typescript|java|rust|go|cpp|c\+\+|react|vue|angular|node\.?js|php|ruby|swift|kotlin|dart)\b',
        'frameworks': r'\b(?:next\.?js|react|vue|angular|express|django|flask|spring|rails|laravel|nest\.?js|svelte|remix)\b',
        'tools': r'\b(?:git|docker|kubernetes|webpack|vite|babel|eslint|prettier|jest|cypress|playwright|vercel|netlify|aws|gcp|azure|npm|yarn)\b',
        'concepts': r'\b(?:api|rest|graphql|microservices|serverless|devops|ci\/cd|testing|debugging|deployment|authentication|authorization|database|sql|nosql|redis|mongodb|postgresql)\b',
        'patterns': r'\b(?:component|hook|state|props|context|redux|middleware|routing|ssr|ssg|hydration|optimization|performance|accessibility|responsive|interface|type)\b',
        'ai_ml': r'\b(?:ai|artificial intelligence|machine learning|ml|neural network|deep learning|nlp|gpt|llm|claude|anthropic|openai|transformer|prompt engineering|meta-prompting)\b'
    }
    
    import re
    concepts = []
    transcript_lower = transcript.lower()
    
    for category, pattern in programming_patterns.items():
        matches = re.findall(pattern, transcript_lower, re.IGNORECASE)
        for match in matches:
            concept = match.strip().lower()
            if concept and concept not in concepts:
                concepts.append(concept)
    
    # Sort concepts by relevance
    concepts.sort(key=lambda x: (-len(x), x))
    concepts = concepts[:20]  # Top 20 concepts
    
    # Create content item for topic scoring
    content_item = {
        'title': video_data['title'],
        'description': transcript[:500],
        'content': transcript,
        'platform': 'youtube',
        'url': video_data['video_url'],
        'published_date': datetime.now(timezone.utc).isoformat()
    }
    
    # Detect priority topics
    priority_topics = topic_scorer.detect_priority_topics(content_item)
    
    # Calculate topic scores
    with open('priority-topics.json', 'r') as f:
        priority_config = json.load(f)
    
    topic_scores = {}
    for topic in priority_topics:
        topic_config = priority_config.get('priority_topics', {}).get(topic, {})
        weight = topic_config.get('weight', 1.0)
        
        # Calculate occurrence frequency
        topic_keywords = [topic] + topic_config.get('aliases', []) + topic_config.get('keywords', [])
        content_text = f"{video_data['title']} {transcript}".lower()
        
        occurrences = sum(content_text.count(keyword.lower()) for keyword in topic_keywords)
        frequency_score = min(occurrences / 10.0, 1.0)  # Normalize to 0-1
        
        topic_scores[topic] = weight * frequency_score
    
    # Calculate unified score
    scored_content = topic_scorer.score_content_item(content_item)
    
    # Apply quality bonuses
    quality_bonus = 0.0
    if len(concepts) > 10:
        quality_bonus += 0.1
    if len(transcript) > 2000:
        quality_bonus += 0.1
    if len(priority_topics) > 1:
        quality_bonus += 0.05
    
    technical_terms = ['implementation', 'architecture', 'optimization', 'performance', 'scalability']
    technical_score = sum(1 for term in technical_terms if term.lower() in transcript.lower())
    if technical_score > 2:
        quality_bonus += 0.05
    
    unified_score = min(scored_content.final_score + quality_bonus, 1.0)
    
    # Generate content quality indicators
    transcript_lower = transcript.lower()
    content_quality_indicators = {
        'has_code_examples': any(indicator in transcript_lower for indicator in ['example', 'code', 'import', 'function', 'const', 'let']),
        'has_explanations': any(indicator in transcript_lower for indicator in ['explain', 'understand', 'how to', 'what is', 'why']),
        'has_best_practices': any(indicator in transcript_lower for indicator in ['best practice', 'should', 'recommended', 'convention']),
        'has_troubleshooting': any(indicator in transcript_lower for indicator in ['error', 'fix', 'debug', 'issue', 'problem']),
        'has_step_by_step': any(indicator in transcript_lower for indicator in ['step', 'first', 'next', 'then', 'finally']),
        'has_practical_demo': any(indicator in transcript_lower for indicator in ['demo', 'build', 'create', 'implement', 'tutorial'])
    }
    
    learning_value_indicators = {
        'beginner_friendly': any(indicator in transcript_lower for indicator in ['basic', 'beginner', 'introduction', 'getting started', 'from scratch']),
        'advanced_concepts': any(indicator in transcript_lower for indicator in ['advanced', 'complex', 'architecture', 'optimization', 'performance']),
        'comprehensive_coverage': len(concepts) > 15,
        'practical_focus': any(indicator in transcript_lower for indicator in ['build', 'create', 'implement', 'project', 'application'])
    }
    
    # Check expected topic coverage
    covered_topics = [topic for topic in video_data['expected_topics'] if topic in priority_topics]
    missing_topics = [topic for topic in video_data['expected_topics'] if topic not in priority_topics]
    coverage_percentage = len(covered_topics) / len(video_data['expected_topics']) * 100 if video_data['expected_topics'] else 100
    
    # Generate content summary
    sentences = transcript.split('.')
    key_sentences = []
    
    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) > 20:
            sentence_lower = sentence.lower()
            if any(concept in sentence_lower for concept in concepts):
                key_sentences.append(sentence)
    
    summary_sentences = key_sentences[:5] if key_sentences else sentences[:3]
    
    content_summary = f"## Analysis of \"{video_data['title']}\"\n\n"
    
    if concepts:
        content_summary += "### Key Programming Concepts Mentioned\n\n"
        concept_groups = {}
        for concept in concepts:
            for category, pattern in programming_patterns.items():
                if re.search(pattern, concept, re.IGNORECASE):
                    if category not in concept_groups:
                        concept_groups[category] = []
                    concept_groups[category].append(concept)
                    break
        
        for category, items in concept_groups.items():
            if items:
                content_summary += f"**{category.replace('_', ' ').title()}:**\n"
                for item in items[:5]:
                    content_summary += f"- {item}\n"
                content_summary += "\n"
    
    if summary_sentences:
        content_summary += "### Key Points from Transcript\n\n"
        for i, sentence in enumerate(summary_sentences, 1):
            content_summary += f"{i}. {sentence.strip()}\n"
    
    # Enhanced insights
    insights = {
        'priority_video': True,
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
        'technical_depth': len([c for c in concepts if c in ['architecture', 'optimization', 'performance', 'implementation']]),
        'content_quality_indicators': content_quality_indicators,
        'learning_value_indicators': learning_value_indicators,
        'topic_score_breakdown': topic_scores,
        'top_concepts': concepts[:10],
        'transcript_analysis': {
            'word_count': len(transcript.split()),
            'unique_technical_terms': len(set(concepts)),
            'code_discussion_density': transcript_lower.count('code') + transcript_lower.count('function') + transcript_lower.count('component'),
            'explanation_quality': transcript_lower.count('because') + transcript_lower.count('reason') + transcript_lower.count('explain')
        }
    }
    
    # Calculate enhanced quality score
    quality_score = unified_score
    quality_score += 0.1 if content_quality_indicators.get('has_code_examples') else 0
    quality_score += 0.1 if content_quality_indicators.get('has_practical_demo') else 0
    quality_score += 0.08 if content_quality_indicators.get('has_step_by_step') else 0
    quality_score += 0.05 if content_quality_indicators.get('has_best_practices') else 0
    quality_score += 0.07 if learning_value_indicators.get('practical_focus') else 0
    quality_score += 0.05 if learning_value_indicators.get('comprehensive_coverage') else 0
    quality_score += (coverage_percentage / 100) * 0.15
    quality_score = min(quality_score, 1.0)
    
    # Save results
    knowledge_vault_path = Path(__file__).parent.parent.parent / "knowledge-vault" / "databases" / "knowledge_vault" / "content-intelligence" / "priority-youtube"
    process_date = datetime.now().strftime('%Y-%m-%d')
    save_dir = knowledge_vault_path / process_date
    save_dir.mkdir(parents=True, exist_ok=True)
    
    # Save unified intelligence file
    result_file = save_dir / f"{video_data['video_id']}_priority_unified_intelligence.json"
    
    result_dict = {
        'video_id': video_data['video_id'],
        'video_url': video_data['video_url'],
        'title': video_data['title'],
        'channel': video_data['channel'],
        'programming_concepts': concepts,
        'priority_topics': priority_topics,
        'topic_scores': topic_scores,
        'unified_score': unified_score,
        'quality_score': quality_score,
        'content_summary': content_summary,
        'insights': insights,
        'processing_timestamp': datetime.now(timezone.utc).isoformat(),
        'processed_with': 'direct-transcript-processor',
        'framework_version': '1.0.0',
        'content_type': 'priority_youtube_video',
        'transcript_available': True
    }
    
    with open(result_file, 'w') as f:
        json.dump(result_dict, f, indent=2)
    
    # Save transcript
    transcript_file = save_dir / f"{video_data['video_id']}_priority_transcript.txt"
    with open(transcript_file, 'w') as f:
        f.write(f"# PRIORITY VIDEO ANALYSIS\n")
        f.write(f"# Title: {video_data['title']}\n")
        f.write(f"# Channel: {video_data['channel']}\n")
        f.write(f"# Video URL: {video_data['video_url']}\n")
        f.write(f"# Processing Date: {datetime.now(timezone.utc).isoformat()}\n")
        f.write(f"# Unified Score: {unified_score:.3f}\n")
        f.write(f"# Quality Score: {quality_score:.3f}\n")
        f.write(f"# Priority Topics: {', '.join(priority_topics)}\n")
        f.write(f"# Programming Concepts: {len(concepts)}\n")
        f.write(f"\n{'='*80}\n")
        f.write(f"TRANSCRIPT\n")
        f.write(f"{'='*80}\n\n")
        f.write(transcript)
    
    # Generate and save report
    report = {
        'priority_processing_summary': {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'total_priority_videos': 1,
            'average_unified_score': round(unified_score, 3),
            'average_quality_score': round(quality_score, 3),
            'high_value_videos': 1 if unified_score > 0.8 else 0,
            'exceptional_quality_videos': 1 if quality_score > 0.9 else 0,
            'processor_version': 'direct-1.0.0'
        },
        'priority_videos_analyzed': [
            {
                'title': video_data['title'],
                'channel': video_data['channel'],
                'video_url': video_data['video_url'],
                'unified_score': unified_score,
                'quality_score': quality_score,
                'priority_topics': priority_topics,
                'concept_count': len(concepts),
                'learning_indicators': learning_value_indicators,
                'expected_coverage': coverage_percentage
            }
        ],
        'topic_analysis': {
            'priority_topics_discovered': [(topic, score) for topic, score in sorted(topic_scores.items(), key=lambda x: x[1], reverse=True)],
            'unique_topics': len(priority_topics),
            'topic_distribution': topic_scores
        },
        'concept_analysis': {
            'top_programming_concepts': [(concept, 1) for concept in concepts[:20]],  # Simplified frequency
            'unique_concepts_discovered': len(concepts)
        },
        'content_quality_metrics': {
            'videos_with_code_examples': 1 if content_quality_indicators.get('has_code_examples') else 0,
            'videos_with_practical_demos': 1 if content_quality_indicators.get('has_practical_demo') else 0,
            'comprehensive_tutorials': 1 if learning_value_indicators.get('comprehensive_coverage') else 0,
            'beginner_friendly_content': 1 if learning_value_indicators.get('beginner_friendly') else 0
        }
    }
    
    report_file = knowledge_vault_path / f"priority_processing_report_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    # Display results
    print("🎯 Direct Transcript Processing Complete!")
    print("=" * 60)
    print(f"Video: {video_data['title']}")
    print(f"URL: {video_data['video_url']}")
    print(f"Transcript length: {len(transcript)} characters")
    print()
    
    print("✅ Processing Results:")
    print(f"   Video ID: {video_data['video_id']}")
    print(f"   Unified Score: {unified_score:.3f}")
    print(f"   Quality Score: {quality_score:.3f}")
    print(f"   Priority Topics: {', '.join(priority_topics)}")
    print(f"   Programming Concepts: {len(concepts)}")
    print(f"   Top Concepts: {', '.join(concepts[:10])}")
    print()
    
    print("📊 Content Quality Analysis:")
    print(f"   ✓ Code Examples: {'Yes' if content_quality_indicators.get('has_code_examples') else 'No'}")
    print(f"   ✓ Practical Demo: {'Yes' if content_quality_indicators.get('has_practical_demo') else 'No'}")
    print(f"   ✓ Step-by-Step: {'Yes' if content_quality_indicators.get('has_step_by_step') else 'No'}")
    print(f"   ✓ Best Practices: {'Yes' if content_quality_indicators.get('has_best_practices') else 'No'}")
    print(f"   ✓ Beginner Friendly: {'Yes' if learning_value_indicators.get('beginner_friendly') else 'No'}")
    print(f"   ✓ Comprehensive: {'Yes' if learning_value_indicators.get('comprehensive_coverage') else 'No'}")
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
    print(f"   Report: {report_file.name}")
    print()
    print("✅ This video is now available for daily digest inclusion!")

if __name__ == "__main__":
    process_typescript_react_video()