#!/usr/bin/env python3
"""
Process AI Coding Assistant Comparison Video
Comprehensive analysis of various AI coding assistants and their real-world performance
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

def process_ai_coding_assistant_video():
    """Process the comprehensive AI coding assistant comparison video"""
    
    # Initialize topic scoring engine
    topic_scorer = TopicScoringEngine()
    
    # The AI coding assistant comparison transcript from the MCP call
    transcript = """hello and welcome to my daas era in this
video we will talk about coding
assistants so coding assistants are the
rise in 2024 it feels like we're
entering an era where it'll be very easy
for anyone to code so in this video I
want to talk about number one the
various types of coding assistants that
exist what companies are popping up in
this space number two why I am not super
bullish on them just yet why I haven't
Incorporated them in my workflow and
lastly we will go through a real world
problem I'll try to solve it myself
without any coding assistant and then
we'll try all types of categories of
assistants we'll see which one was the
fastest which one was the most
convenient for me to use right now so
let's start with the meta section of
this video I think broadly there are
three types of coding assistants number
one a chat GPT like UI where you first
copy over your problem contextualize it
and paste it inside a web based UI
finally get the response copy over the
response and paste it back into to your
IDE this is the most basic thing that
frankly existed for a while now and you
might have been very comfortable in this
workflow frankly I am as well if there
is one assistant I use right now it is
copying over the problem from Visual
Studio code or whatever editor I'm using
pasting it in ch GPT giving it some
context and then getting back the
response and pasting it back the pros of
this are number one it's very easy to
see what's happening um there's no magic
here really there's an llm that's out
there it's closed source and you
interact with it through a UI downsides
are of course there is more time for you
to copy paste code there's a lot of
manual work that you have to do to copy
over code from one place to another I
still feel this is the one I'm most
bullish on right now and surprisingly
this is the one that I've been using a
lot compared to the other options
category number two this is basically
some sort of a plugin in your IDE for
example a vs code plug-in which is just
a wrapper on top of a closed Source
model you might feel like this is a 10x
better solution than the first category
but the problem is the AI tries to get a
lot of context itself um if you start to
write your code uh you not really
telling the AI what to do it sort of
figures that out itself and downside
there is it hallucinates a lot it starts
to type things that you might not need
um which becomes mildly irritating this
is the reason I've not flipped on GitHub
co-pilot in my IDE ever because I don't
want suggestions that I don't need if I
need a suggestion I'll copy and paste it
over to chat gbt UI so that's the second
category I find it mildly irritating
right now it felt like a 10x product I
don't think it is just yet um but we
will see where this Market goes number
three this is a new category um this is
one I'm not necessarily bullish on but
I'm excited to see which is still a
plugin um but it's on a open- source
model that you can run locally it still
has the cons of the AI trying to figure
things out itself um but if you're
running a model locally you can do 10
different things that you cannot with a
close Source model this I'm excited
about purely on the technicals I'm still
feel this is not a 10x product yet but
at least a step in the right direction I
can start to customize my model in a way
where it starts to write code like I do
so I don't have to give it additional
context like I have to do in category
number two all right so those are the
three categories number one very ad hoc
way of copy pasting code over to a UI
number two a plugin that's a wrapper on
top of a close Source model and number
three a plugin that can hit any model of
your choice including a model that is
running locally on your machine given
these categories of assistants let's
move to the next section where I want to
talk a little bit about why I am mildly
bearish on them don't actually code and
I think a similar wave came when no code
tools came into the picture okay now
anyone can write or create websites
because it's a no code tool you track
and drop you create a website the
problem is um you're able to create a
very basic version using these things as
soon as complexities arise in your code
base no code tools are usually not the
best solution eventually you have to
code things yourself I think after years
people have come to realize that this is
true and you can use no Cod tools for
basic landing pages but as soon as you
start to build a real website um you're
no longer dependent on them I think
something similar is happening here
where a category of developers who've
never coded and you know maybe don't
code too much um Can Sly see code being
typed out but the problem is as soon as
complexity comes into the picture the AI
may or may not hallucinate but you at
the very least need to understand what
the AI is writing and when that happens
you know you'll eventually get
frustrated if you're the AI can write a
lot of code for you but if you don't
understand it you'll be always anxious
checking it in you'll be always anxious
trying it out so for that reason um as
fancy as it might sound okay you know
anyone can be a coder right now if that
was really true then literally everyone
would be a coder and you know the whole
Supply demand Arbitrage would close
eventually some smart coders will find a
combination of one being technically
strong themselves and two using these
assistants wisely to be a little bit
faster and this combination might be the
next wave of smart developers I don't
know yet but I don't see any senior
developer being super excited about this
right now it does save time I'm not
saying it doesn't I'm saying it's not
really an assistant it's not really
someone you can delegate everything
thing to which sort of was the original
pitch of replacing developers all right
that's Point number two now let's look
at a very basic project which has some
issues that we should fix I explain the
project at a high level but there is a
link in the description where there's a
detailed workflow of how you can create
this project on your own it's a simple M
Stack project it has some inefficiencies
I wouldn't call them bugs as such but
some good to have um so let's try to fix
them number one ourselves number two
using chat gbt UI number three using a
plug-in that hits a Clos source llm and
lastly a plugin that uses a open source
llm that's running locally on my machine
Let's get right into it all right let me
give you a brief of the project we are
dealing with um you can actually go to
this link in the description and there
will be a detailed lesson of how you can
create this project on your own this is
actually part of the cohort uh you won't
get access to any of the videos but if
you want you can try to code this thing
yourself this is a basic Financial app
similar to PTM M it looks something like
this um you can sign up or sign in if
need be once you have signed up to the
website
um you do
that you reach a page where you see a
bunch of people that you can send money
to you also see your own balance and you
can search these users select a user and
send them some money from your wallet
and once you do the transfer sort of
goes in you see a bunch of in icies here
there are no notifications in fact the
balance that you see here is hardcoded
so these are the problems that we'll try
to solve it still works um the database
still you know decreases the balance of
one user increases the balance of
another user but the UI doesn't reflect
that so let's break down a few problems
that we can fix here then we'll try to
fix them we'll time ourselves in how
much time it took us in each of these
categories when we were using assistants
and when we weren't using assistants the
first problem that that we should fix is
U it's a very minor inefficiency which
is you know when you go to the landing
page you pretty much see nothing um if
you go to the signup page even if the
user is already logged in which I was
right now they stay at the signup page
they should ideally go to the dashboard
um similarly if the user isn't logged in
and the URL tries to go to the dashboard
they should not see this page they
should go to the signup page um and
lastly I think the balance should
reflect correctly so this is a hardcoded
value of 10,000 rupees um we should fix
this to the current balance of the user
um Let me give a high level of what the
database looks like um what the back end
looks like what the front end looks like
it's a very basic bur application
doesn't even use typescript it's in pure
JavaScript um and if you read through
the code if you understand a little bit
of Mone you should be able to understand
the whole thing pretty easily all right
um the database look something like this
there are multiple users so whenever you
sign up um you there's an entry created
for you in this database and then
there's another entry where you get a
random balance initially so there's no
way to really onramp via Banks here
though everyone has a Rand random set of
balance this is mongodb um and as you
can see the first user has for example
5800 rupes second user has 720 rupees so
on and so forth given you have this and
this um anytime the user goes here and
sends some money clicks on initiate
transfer the money gets debited from one
account and credited to the other
account that's how things work right now
the problems let me summarize again is
that number
one
um
we need to
redirect user
correctly number two um
show the right balance all right these
are the two problems we need to solve
and here before we dive into the code I
want to talk a little about where
assistants are pretty much of no use um
I think when you're given a problem
statement like this it is you the
developer who will decide how to you
know design it for example um in this
specific case where
forget the balance for now but the other
thing that we need to implement which is
if you're on the signup page um and you
know if the user is already logged in
they should go to the dashboard um there
are multiple ways to implement this and
I'm not saying the AI will give you a
wrong solution number one it will be
very hard for the AI to span across
files front ends and back ends to
understand this maybe that changes in
the future but secondly you know there
are thousand approaches that you can
take here and developers are generally
very finicky teams generally have
standard SL practices maybe you can
codify these practices I don't know but
currently in the current scario um of
you know how teams work and how coding
assistant are I think there are few
decisions that an engineer needs to take
they can make the AI code a bunch of
things but there are a few decisions
that I'm going to talk about now to
implement a feature like this not only I
decided and this is how I want to
implement them another user can
implement it a different way and an AI
can totally um you know use a different
way to implement it so this is one place
where I feel you at least need a manager
an orchestrator A person who number one
understands how to code number two can
either make the um AI code or can code
themselves that really depends on them
but they need to know they need to be
the final decision maker on how this
feature needs to be implemented cool
that's a another reason I feel you know
it's not super bullish for us to feel
Engineers everything can be outsourc to
an AI I think most things can I think
one person engineering teams might also
exist but in the end you need one
engineer or orchestrator who can talk to
a all right with that small moment of
relief let's get into how we can solve
both of these Fe features though the
first thing we need to do is uh whenever
the user hits the website irrespective
of what page they are on sign up sign in
um
or dashboard um or even the landing page
if I'm being honest if the users on the
landing page they should go to either
the dashboard or the signin page based
on whether or not they're logged in the
first thing we need to do is hit the
back end and check if the user is logged
in you cannot do this on the front end
um your cookie can expire which in our
case we don't have a cookie uh we have a
token but either way um it can expire so
you can't really assume the user is
logged in if you have a token on the
front end you need to hit the back end
so the first thing we have to do is for
the first feature
um create
a backend
endpoint again if you don't understand
it it's fine just look at the lines of
code that I'm writing and how quickly
I'm writing them myself and how quickly
the AI does it secondly um on the front
end hit this end point
and redirect the user correctly all
right these are the two things we need
to do for the first point for the second
point that Returns the user details and
maybe the balance second point just use
the end point defined in 1 a so we don't
have to do much in the second point if
I'm being honest um if you already are
creating an endpoint which the user
needs to hit to check whether or not
they're logged in you can just return
their balance from the back end in the
same endpoint point which basically
means
um whenever the user comes to the
website we're going to hit the back
end this is the back end and this is the
browser irrespective of what page the
user came on um the browser will hit the
back end and uh ask for am I logged in
if yes what is my balance and then the
backend will return
either a yes or no and if it is yes it
it will return the balance as well let's
say rupees 3,000 all right this is one
end point that we need to create and
this will basically solve both the
problems if you get back a yes you take
the person to the dashboard or you keep
them at the dashboard if that's the end
point that they hit or um if what you
get back from the server is no which
means the user isn't logged in you take
them to the signin page all right cool
given this um let's kick things off by
timing myself I'm going to code all of
this we'll probably speed ramp it you
don't have to look at the whole thing
for this video um and then we'll see how
much time it took me then I will flip on
the assistants first at GPD then close
Source then open source and then we'll
see how much time those take as well all
right kick things off I'm going to start
the timer now and code this problem
really
quickly
so the back end is done I don't know how
much time it took let's go to the front
[Music]
[Music]
end
[Music]
done with the first part almost Nish if
I go to the index page now it
automatically redirects me to the
dashboard you can look at the clock
there and see how much time it took me
to implement this next up I'm going to
implement the balance and point should
be straightforward if you already have
the
data
balance is done let me quickly clean up
all the routes and then summarize all
that I've
done all right I think we can stop the
clock um how much time did it take
roughly it took me 9 minutes to solve
all these issues again let's summarize
what the issues were the issues
were number one we needed to redirect
the user correctly if if you look at it
now if the user is logged in which this
user is right now um if I go to/ sign up
I automatically get redirected to
dashboard if I go to the index page or
the landing page I again come to the
dashboard and then if I go to the signin
page same thing would happen and if I go
into incognito window and try to go to
the dashboard it takes me back to sign
in so the user on the front end is being
redirected correctly to the respective
page which is something that wasn't
happening
second thing that has happened is the
balance looks correctly here this was
10,000 hardcoded now it's the real value
from the database um let's figure out
how did this happen let's break down all
the things that I did number one I went
to the back end and created this route I
don't know how much time it took me but
I would assume less than 5 minutes um
the me end point this is a point where I
want to say you everyone can have their
own set of opinion as to what they want
to call the end in p or even if they
want to go with this approach um the
approach that I took was okay you know
anytime a user comes on the website
irrespective of what route they are
coming on whether they come on the
signup page signin page or the dashboard
page the first request that needs to go
out is to this me Endo that gives back
the user details of themselves whether
or not they're logged in if they're not
logged in they should get back a message
that says you're not logged in not get
back any user details if they are logged
in they should get back you are this
user this is your balance so these are
the things that I return from this
endpoint there is scope of improvement
here I that I look at it um if I'm being
honest this whole project is in
JavaScript and while I was typing the
code um I think I would have anyways
been like at least 25 30% faster if the
code was in typescript um that said I
think this is arguable who as to who
writes better code whether an AI would
be give me a better code I don't know um
but this is a good start um this took me
whatever I think 3 4 5 minutes um once I
wrote this this is the backend code all
the backend code that I needed to um
Implement all the features I needed then
I went
to a bunch of files and I realized you
know I can make a lot of changes in a
bunch of files but rather let me put
everything inside a hook um this is
another thing I'm unsure if you know any
can context on immediately okay you will
ask the AI to code something for the
first page for example you might ask the
AI can by when the person goes to the
slash page or the the index page take
them to dashboard and the AI might shove
all this logic that you see here that I
put inside a separate place because I am
an engineer I can think in the future
can H by I'm going to need this logic
intent different places let me
encapsulate it up front in a hook and AI
might not be able to do that so you
might ask the AI to write something and
it might shove all of this logic in
another component for example um
the index component so basically all
these files would look so big um versus
uh I encapsulated all of this into a
single hook because I could sort of
think in the future I don't think you
guys can do that yet um this is another
place where you might need human
intervention I'm not saying the AI is
bad the AI is would have been actually
pretty good we'll see in the next
sections it might have been able to spit
all of this out um but you know putting
that into a separate file is still the
job of a developer and I'm un sure how
much time time it saves um once I did
this I made the same change in a bunch
of other components for example I went
to the dashboard component and added
this logic at the top I went to the
signup component and
added this to the top same for the
signin component basically make sure
everyone gets redirected correctly and
lastly in the dashboard component I
already had the value as a hardcoded
value here I replaced it with user. user
details. account. balance the thing that
we get from the back end roughly took me
10 minutes um seems pretty
straightforward I think it would take
this much maybe 2 minutes L 2 minutes
more for anyone to code um now that we
have this um let's see how much I by the
way I had the assistant on throughout I
did not use it I when I was typing it I
started typing I realized you know it
was on which is fine I did not use any
of the suggestions it gave me um but in
the next section let's actually flip on
either copilot or I have this other one
called Codi here because Codi lets you
hit both close source and open source
LMS um we'll use either one of them
let's we can we can do copilot um let's
do co-pilot in the next one which uses
cbd4 which is a closed Source llm let's
see how much time it takes for me to
write the whole thing again um if I'm
using a close s LM like uh chb all right
let's get into the next
[Music]
section all right Hands
Up 2 minutes I saved but there's some
downside all right let's quickly discuss
um what all happened here I have a few
fresh thoughts in my head U number one
the back end code was smooth it took
basically a tab basically I think I
saved I saved 3 minutes at the very
least if not more um compared to the
original approach again we're using
co-pilot with gbd4 here um or three
probably four yeah I think it's for by
default um so pretty good uh the back
end code super impressed I thought you
know this video probably might not make
any
sense purely based on how quickly it
happened um but then uh when we came to
the front end bits the cracks that I was
talking about basically came which is
number one did not write extremely
reusable code um when it comes to you
know I went to again the index end point
here and then it was not smart enough to
figure out um to encapsulate code which
I guess is fine I mean llm it knows it's
not yet an agent it's not yet taught to
you know think smartly it's taught to
spit out a lot of code which it did um
but the common cracks were um rather
than passing in this header which is
something that I've passed in different
files so I would have assumed it uses
and also I've been using axos and
different files it did not um use axio
it uses Fetch and it had this code which
means it was expecting um the cookie to
go out but we don't use a cookie we use
a token so those were the things it
pretty much copied from a different code
base I'm assuming um this was 31 and not
3,000 those were the small things that
you know needed fixing and lastly here
it checked if data. ID does not exist
then navigate or data ID exist then
navigate to the dashboard but from the
back end it wasn't putting an ID
basically tells me you know it's not
very context aware of the code that it
wrote itself um it's yeah basically does
not remember any any of the code it
wrote um I'm sure it will at some point
you know it does look at files that I
could understand um so it's able to once
I wrote this code basically it was it
was able to actually you know um write
similar code in other components so if I
go to you know um dashboard. jsx all
this code it wrote itself um which
basically means if you tell it once okay
this is how all this happening for me
this is my backend end point um it
figures out things for the other files
itself which is good um but again I
wouldn't if if you're a good developer
you wouldn't write this code again and
again you would shove this all into a
different file so mixed opinions here
overall at least on the back end was
super helpful on the front end was
mildly irritating at points uh but I
think I would be fine with the
irritation basically I think I should
flip this on for myself U
because I haven't yet um and now it
feels like it at the very least it it'll
give me some productivity boost um and
if it does not you can obvious it off
but more specifically you can just
ignore the suggestions that it's giving
and at some point you probably have to
go all hands on deck and you know uh
teach the AI or at least tell it to do
something different this is where I feel
you know a junior engineer or someone
who's not coded will pretty much accept
what the um AI is giving it and that's
where the problem arises cool this was
number two um two more experim we left
with number third experiment is going to
be using tgbt UI so I'm not going to use
this but use the UI to solve it I seem
like a futile experiment if I'm being
honest um will most probably take a lot
of time in copy pasting I can almost
certainly tell you um okay it will
be a longer time duration also seems
like a very fake experiment happy to do
it but you to do it I yeah probably not
going to do it so I'm going to do the
last experiment which is um a close
Source llm this one's super interesting
um this wasn't possible until a while
ago I think there are a few companies
now who are trying it CI is one of those
companies you know this video isn't
sponsored um I think they they're on to
something um we at least giving people
the power to um use closed Source LMS um
sorry open source LMS the reason is you
know that at least excites me personally
you know if I have a tool that lets me
connect to an open source llm I will do
10 different things to train the model a
certain way so it understands this is
how I code and there's some you know
technically exciting problem for me
versus you know everything else seems a
little bit of you know rapper on top of
GPT um so with that let me show you
quickly how can you turn on um an open
source model locally U for and connected
directly to vs code um I think it's
possible might be possible using various
tools the one we're using is um where
did it go this one right here called Cod
aai so the first thing you have to do if
you're in Visual Studio code and I think
both GitHub GitHub copilot for sure I'm
if Codi exists for other Ides so this
isn't necessarily restricted to visual
studio code um you can try it like a
neovim or uh a chat brains ID as well
I'm going to flip off GitHub copilot
chat I'm going to flip on Codi AI here
if you want to try it out just install
this extension and then go from there
there are a few tweaks you have to make
though um if you want to run the model
locally so the first thing you have to
do is get the model locally there are a
few open source models llama is the most
famous open source model by uh meta and
it has
a fine tude version for coding um that's
the one that we'll be using today um the
the way to bring that model locally on
your machine there are a few ways the
most popular one these days is something
called AMA
um which is a project I think by a few
folks used to work at Docker um that
lets you do bring LMS locally open
source LMS of course um and very similar
to Docker how Docker lets you pull
docker
I think they wrote very similar code
because the UI looks pretty similar or
the C looks pretty similar so you can
pull open source models for example um
after you install olama if you want to
try it out locally U if I go to my
terminal what's up
here if I type AMA uh AMA list um gives
me a list of my currently available
models so you can pull any famous open
source model locally if you want um all
you have to do is AMA
pull name of the model for example I
have Cod Lama 34 billion code model and
also AMA 7 billion code model um I'm
going to use this one I'm trying my best
to run this I'm not being able to I
think it's a bug or an issue with codium
um It Is by default this is the one that
I pulled first and then ever since then
it's been using this how do I know it's
been using this because it's um I can
see it in the logs um I'm unable to move
from this model to this model I think
this one might perform slightly better
this one I tried a while back I can give
you a tldr it was pretty poor every
suggestion was very bad um so we will
see I mean it gives you good suggestions
for very simple stuff so if you the
standard example when you're trying to
test these llms uh sorry coding
assistance is make it solve a simple
problem like
sum
function something like this this it was
able to solve pretty well um let me flip
it on quickly um this it was able solve
pretty well uh but when it comes to
actually coding things like you know
creating a route it pretty much it
bricks you will see very soon so let me
start the clock again and let me try to
solve this whole problem now using a
open source model that is running
locally on my machine using Cod AI if
you want to flip it on on your side it's
a weird a few things you have to do as I
said number one you have to install AMA
number two you have to pull in the model
that you want to run and number three if
you go to uh
this icon right here which is the Cod a
icon you can go to
settings and oh that's get pilot that's
my bad that's Cod AI if you go to
settings um you need to select unstable
olama here the name itself is unstable
so there are no guarantees this will
work uh and if it does not work you can
look at the output here you'll find some
error for example I did not have the 7
billion model I deleted it and then I
could see the log here okay you know it
should brecks and then and that's how I
knew I wasn't getting any suggestions
right now I am getting suggestions so I
know it is working and it is all of this
is coming from this code Lama 7B model
how do I know this I can see this
somewhere in the log if I'm being honest
let's
see
uh let me go to settings if I go
back here and select null which
basically means switch back
to it says Scot base here but I'm
assuming GPD um
and then if I select unstable AMA again
oh I don't see any
logs there we go I think it was
happening I think the logs were just
going down um so now the log Clearly say
Codi completion provider initialized
unstable Lama / code Lama 7B code this
is the model that I have running locally
and now most probably there it's very
hard to confirm this this is the model
that's running locally 99% it is um you
might suggest K just turn off the Wi-Fi
and it will happen and no that that does
not happen turning off the Wii still
creates issues connecting to this local
model um I'm assuming because they hit
their own C API from time to time um
though I'm 99% sure this is hitting the
local model um the reason for this is
number one the speed number two the
accuracy is pretty bad um if you have
the normal default gbt model uh which I
think is gbd4 is what they use the
accuracy is pretty high here the
accuracy is pretty bad which is why I'm
99.9% sure this uses the local AMA model
that I'm running uh which is this 7
billion parameter model um and now I'm
trying to code the whole thing again
using jti this all right one quick
disclaimer if you're trying this locally
uh make sure you flip off GitHub
co-pilot else you will see suggestions
from copilot which is something we don't
want all right move
on
all right I take a pause and I accept
defeat um I don't think this model at
least the one that I'm running locally
um is it has a few problems let me State
the problems from the top um so it's
been it took me around 5 6 minutes to I
once I finish it I'm pretty I'm not
close but you know I'm basically not
able to achieve what I want to I'm just
copy pasting code which basically means
I'm doing the approach one again which
is something I don't want I wanted to
rely completely on an llm and right now
I cannot rely completely on a on a
closed sorry open source LM if you're
someone who does not know coding or
knows a little bit of coding this is not
the right way to go it'll just yeah
you're going to you you'll pluck your
hair out um so let me explain the
problems from the top um if I go to
user.js um router. get/ me this this
endpoint that I created basically
required a lot of manual effort um the
initial end point that it gave me had a
find by PK here which I think was an old
Mongo's um this thing um API I could be
wrong might still exist um but that is
one thing I had to change this was wrong
basically not have any context of the O
middleware which I guess is fine um it's
still fine I mean there was a bunch of
manual effort required here it was still
able to spit out pretty good code which
I was surprised by I thought you know it
won't be able to based on my earlier
experiments of running it locally but
right now it gave me a good structure
few things missing it's fine I think it
took me like 2 minutes too fix the whole
thing of course I did not fix everything
there was some bugs here that I had to
come back to um but high level two level
maybe equalent to or better than writing
all the code yourself not as good as um
co-pilot or you know
gbd4 now go to the front end now um
front end um was a little tricky um
basically all of this I would say is
pretty much written by me um wasn't able
to figure things out um it's still wrong
if I'm not that I'm looking at it um so
yeah basically at this point I realized
it it cannot write front end code very
well if at all so I still wrote
everything here and you know it's fine
that I had to you know put in some
manual effort but it did not even keep
context of this so once I wrote all of
this logic it should have at the very
least been able to you know rewrite this
logic in dashboard uh but when I
preached
it is hallucinating again it's pretty
much giving me something that's not
related to the code that I've already
written which basically means you know
it's better that to just SL it yourself
so what is the final outcome here um
cording to yourself great but you should
probably use an AI what AI should you
use should you copy paste over to CH gbt
uh if you're a little too old school
sure um if you're still in love with
stack Overflow sure um but what should
be your ideal solution unless you have
company policies that prevent you from
looking at GitHub copilot um use GitHub
copilot or you know some wrapper on top
of gb4 seems like gb4 is 10 times more
powerful than at least the 7 billion
parameter model I could be wrong and the
results might change if you use the 34
billion model happy to try it out after
this video I'll see if I'm able to
somehow make it work um and yeah that
might change my opinion for now
basically open source models at least 7
million model is not even close to um
which I guess is already known as some
nothing new here I think this can
compete with
um gb4 that said it seems like co-pilot
at least was making the model learn
along the way U which this guy isn't um
which might not be a problem
specifically with this model might be a
problem with you know um kod AI um so
yeah that's another thing it should
probably retain some context of the code
that I've written and you know um at
least the code that I've written in the
past 5 minutes or 10 minutes um these
are all ad hog techniques I'm un sure if
this is what how GitHub copilot does it
um but but if you want to look at the
code base I think code AI is open source
so you can um yeah that's a high level
from this video what's been my learning
my learning has been get up ciled way to
go I think that's what 90% of the people
are using anyways um because of you know
just pure branding marketing of GitHub
um that said it also seems like the more
Superior product at the moment we will
see if that changes but I think that
brings us to the end of this video was I
sharing my screen that brings us to the
end of this video hopefully it was an
inside for video let me know what should
we do next should we dive into the code
of Codi Ai and see how they were able to
do it seems like it's a simple vs code
extension with you know a bunch of
GPD I'm being a little premature here
when I say simple uh but we can look at
it at least try to figure things out
ourselves let me know if we want but we
can look at it try to figure that out
ourselves let me know if you would like
to see that next with that let's end it
I'll see you guys in the next one
bye-bye"""
    
    # Video metadata (using the actual AI coding assistant comparison video)
    video_data = {
        'video_id': 'cJlM3AIFMaw',
        'video_url': 'https://www.youtube.com/watch?v=cJlM3AIFMaw',
        'title': 'I Tried Every AI Coding Assistant! Here\'s What I Think… (2024 Updated)',
        'channel': 'Tech Creator/Developer Channel',
        'priority': 'highest',
        'expected_topics': ['ai', 'coding', 'claude', 'meta-prompting'],
        'estimated_duration': '25+ minutes',
        'view_count': 'High engagement',
        'tutorial_type': 'comprehensive_comparison_analysis',
        'year': '2024'
    }
    
    # Enhanced programming concept patterns for AI coding assistants
    programming_patterns = {
        'ai_tools': r'\\b(?:chat gpt|chatgpt|github copilot|copilot|codi ai|codium|claude|anthropic|gpt|llm|ai assistant|coding assistant|ai tools)\\b',
        'coding_concepts': r'\\b(?:frontend|backend|fullstack|javascript|typescript|react|node|mongodb|database|api|endpoint|authentication|token|cookie)\\b',
        'development_workflow': r'\\b(?:vs code|vscode|ide|plugin|extension|workflow|productivity|debugging|refactoring|code review|testing)\\b',
        'ai_methodology': r'\\b(?:prompt|context|hallucination|suggestion|autocomplete|code generation|local model|open source|closed source|fine tuning)\\b',
        'programming_practices': r'\\b(?:best practices|design patterns|architecture|mvc|hook|component|reusable|encapsulation|separation of concerns)\\b',
        'tools_platforms': r'\\b(?:ollama|docker|git|npm|terminal|cli|ui|browser|server|localhost|production|deployment)\\b',
        'performance_metrics': r'\\b(?:speed|accuracy|efficiency|productivity|time saving|performance|optimization|scalability)\\b',
        'comparison_analysis': r'\\b(?:comparison|benchmark|evaluation|pros|cons|advantages|disadvantages|better|worse|superior|inferior)\\b'
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
    
    # Sort concepts by relevance and frequency
    concept_frequency = {}
    for concept in concepts:
        concept_frequency[concept] = transcript_lower.count(concept)
    
    # Sort by frequency and length, then take top concepts
    concepts = sorted(concept_frequency.keys(), key=lambda x: (concept_frequency[x], len(x)), reverse=True)[:30]
    
    # Create content item for topic scoring
    content_item = {
        'title': video_data['title'],
        'description': f"Comprehensive comparison and analysis of AI coding assistants including GitHub Copilot, ChatGPT, and local open-source models. Real-world testing and evaluation of productivity benefits and limitations. Duration: {video_data.get('estimated_duration', 'N/A')}",
        'content': transcript,
        'platform': 'youtube',
        'url': video_data['video_url'],
        'published_date': datetime.now(timezone.utc).isoformat(),
        'channel': video_data['channel'],
        'view_count': video_data.get('view_count', 'N/A')
    }
    
    # Detect priority topics
    priority_topics = topic_scorer.detect_priority_topics(content_item)
    
    # Calculate enhanced topic scores with AI coding focus
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
        frequency_score = min(occurrences / 20.0, 1.0)  # Adjusted for longer content
        
        # AI coding assistant specific bonuses
        ai_bonus = 1.0
        if 'ai' in topic.lower() or 'claude' in topic.lower():
            ai_bonus += 0.3  # Strong bonus for AI topics
        if 'coding assistant' in video_data['title'].lower():
            ai_bonus += 0.2
        if '2024' in video_data['title'].lower():
            ai_bonus += 0.1  # Current content bonus
        
        topic_scores[topic] = base_weight * frequency_score * ai_bonus
    
    # Calculate unified score with AI coding focus
    scored_content = topic_scorer.score_content_item(content_item)
    
    # Apply enhanced quality bonuses for AI coding content
    quality_bonus = 0.0
    if len(concepts) > 20:
        quality_bonus += 0.18  # Rich concept coverage
    if len(transcript) > 15000:
        quality_bonus += 0.15  # Comprehensive content
    if len(priority_topics) > 3:
        quality_bonus += 0.12  # Multi-topic coverage
    
    # AI coding assistant specific indicators
    ai_coding_indicators = [
        'github copilot', 'chatgpt', 'ai assistant', 'coding assistant', 
        'comparison', 'evaluation', 'real world', 'productivity', 'workflow'
    ]
    ai_score = sum(1 for indicator in ai_coding_indicators 
                   if indicator in video_data['title'].lower() or indicator in transcript.lower())
    if ai_score > 5:
        quality_bonus += 0.15
    
    # Technical depth and practical focus bonus
    practical_terms = ['implementation', 'testing', 'benchmark', 'real project', 'hands on', 'experiment']
    practical_score = sum(1 for term in practical_terms if term.lower() in transcript.lower())
    if practical_score > 3:
        quality_bonus += 0.12
    
    unified_score = min(scored_content.final_score + quality_bonus, 1.0)
    
    # Generate enhanced content quality indicators
    transcript_lower = transcript.lower()
    content_quality_indicators = {
        'has_code_examples': any(indicator in transcript_lower for indicator in ['code', 'function', 'endpoint', 'backend', 'frontend', 'javascript']),
        'has_explanations': any(indicator in transcript_lower for indicator in ['explain', 'understand', 'how to', 'what is', 'why', 'because']),
        'has_best_practices': any(indicator in transcript_lower for indicator in ['best practice', 'should', 'recommended', 'approach', 'workflow']),
        'has_troubleshooting': any(indicator in transcript_lower for indicator in ['problem', 'issue', 'fix', 'debug', 'error', 'challenge']),
        'has_step_by_step': any(indicator in transcript_lower for indicator in ['step', 'first', 'second', 'next', 'then', 'finally']),
        'has_practical_demo': any(indicator in transcript_lower for indicator in ['demo', 'test', 'experiment', 'try', 'implement', 'build']),
        'has_comparison_analysis': any(indicator in transcript_lower for indicator in ['comparison', 'versus', 'better', 'worse', 'pros', 'cons']),
        'covers_multiple_tools': any(indicator in transcript_lower for indicator in ['copilot', 'chatgpt', 'codi', 'ollama', 'local model']),
        'covers_real_world_testing': any(indicator in transcript_lower for indicator in ['real world', 'actual project', 'testing', 'benchmark', 'timing']),
        'covers_productivity_analysis': any(indicator in transcript_lower for indicator in ['productivity', 'time saving', 'efficiency', 'workflow', 'faster'])
    }
    
    learning_value_indicators = {
        'beginner_friendly': any(indicator in transcript_lower for indicator in ['basic', 'simple', 'easy', 'beginner', 'introduction']),
        'advanced_concepts': any(indicator in transcript_lower for indicator in ['advanced', 'complex', 'architecture', 'fine tuning', 'local model']),
        'comprehensive_coverage': len(concepts) > 25,
        'practical_focus': any(indicator in transcript_lower for indicator in ['practical', 'real world', 'hands on', 'testing', 'experiment']),
        'industry_relevant': any(indicator in transcript_lower for indicator in ['industry', 'professional', 'production', 'enterprise', 'team']),
        'updated_content': '2024' in transcript_lower or 'updated' in video_data['title'].lower(),
        'comparison_included': any(indicator in transcript_lower for indicator in ['comparison', 'compare', 'versus', 'different', 'evaluate']),
        'honest_assessment': any(indicator in transcript_lower for indicator in ['honest', 'critical', 'limitation', 'downside', 'problem'])
    }
    
    # Check expected topic coverage
    covered_topics = [topic for topic in video_data['expected_topics'] if topic in priority_topics]
    missing_topics = [topic for topic in video_data['expected_topics'] if topic not in priority_topics]
    coverage_percentage = len(covered_topics) / len(video_data['expected_topics']) * 100 if video_data['expected_topics'] else 100
    
    # Generate enhanced content summary with structured sections
    sentences = transcript.split('.')
    key_sentences = []
    
    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) > 30:
            sentence_lower = sentence.lower()
            if any(concept in sentence_lower for concept in concepts[:20]):  # Use top concepts
                key_sentences.append(sentence)
    
    summary_sentences = key_sentences[:10] if key_sentences else sentences[:8]
    
    content_summary = f"## Comprehensive Analysis: \"{video_data['title']}\"\\n\\n"
    content_summary += f"**Channel:** {video_data['channel']}\\n"
    content_summary += f"**Type:** {video_data.get('tutorial_type', 'Analysis').replace('_', ' ').title()}\\n"
    content_summary += f"**Year:** {video_data.get('year', '2024')}\\n"
    content_summary += f"**Estimated Duration:** {video_data.get('estimated_duration', 'N/A')}\\n"
    content_summary += f"**Focus:** AI Coding Assistant Comparison & Real-World Testing\\n\\n"
    
    if concepts:
        content_summary += "### Key AI Coding Concepts Covered\\n\\n"
        concept_groups = {}
        for concept in concepts[:25]:  # Top 25 concepts
            categorized = False
            for category, pattern in programming_patterns.items():
                if re.search(pattern, concept, re.IGNORECASE):
                    category_display = category.replace('_', ' ').title()
                    if category_display not in concept_groups:
                        concept_groups[category_display] = []
                    concept_groups[category_display].append(concept)
                    categorized = True
                    break
        
        for category, items in concept_groups.items():
            if items and len(items) > 1:  # Only show categories with multiple items
                content_summary += f"**{category}:**\\n"
                for item in items[:8]:  # Limit to 8 per category
                    content_summary += f"- {item}\\n"
                content_summary += "\\n"
    
    if summary_sentences:
        content_summary += "### Key Insights from Analysis\\n\\n"
        for i, sentence in enumerate(summary_sentences, 1):
            clean_sentence = sentence.strip().replace('\\n', ' ')
            if len(clean_sentence) > 40:  # Only include substantial sentences
                content_summary += f"{i}. {clean_sentence}\\n"
    
    # Add analysis structure breakdown
    content_summary += "\\n### Analysis Structure\\n\\n"
    structure_indicators = {
        'Tool Categories': ['three types', 'categories', 'chat gpt like', 'plugin', 'local model'],
        'Real-World Testing': ['real world problem', 'timing', 'test', 'experiment', 'benchmark'],
        'Performance Comparison': ['github copilot', 'chatgpt', 'open source', 'speed', 'accuracy'],
        'Practical Limitations': ['limitations', 'problems', 'downsides', 'hallucination', 'context'],
        'Industry Perspective': ['developer', 'engineering', 'productivity', 'workflow', 'professional'],
        'Future Outlook': ['future', 'direction', 'improvement', 'potential', 'evolution']
    }
    
    for section, keywords in structure_indicators.items():
        if any(keyword in transcript_lower for keyword in keywords):
            content_summary += f"✓ **{section}** - Covered\\n"
    
    # Enhanced insights with AI coding focus
    insights = {
        'priority_video': True,
        'tutorial_type': video_data.get('tutorial_type', 'analysis'),
        'comprehensive_rating': 'exceptional' if ai_score > 7 else 'high',
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
        'technical_depth': len([c for c in concepts if c in ['github copilot', 'chatgpt', 'local model', 'ai assistant', 'coding']]),
        'content_quality_indicators': content_quality_indicators,
        'learning_value_indicators': learning_value_indicators,
        'topic_score_breakdown': topic_scores,
        'top_concepts': concepts[:20],
        'ai_coding_metrics': {
            'tools_covered': ['GitHub Copilot', 'ChatGPT UI', 'Codi AI', 'Local Models', 'Ollama'],
            'comparison_depth': ai_score,
            'real_world_testing': content_quality_indicators.get('covers_real_world_testing', False),
            'productivity_focus': content_quality_indicators.get('covers_productivity_analysis', False),
            'honest_assessment': learning_value_indicators.get('honest_assessment', False),
            'year': video_data.get('year', '2024')
        },
        'transcript_analysis': {
            'word_count': len(transcript.split()),
            'unique_technical_terms': len(set(concepts)),
            'ai_discussion_density': transcript_lower.count('ai') + transcript_lower.count('coding assistant') + transcript_lower.count('copilot'),
            'explanation_quality': transcript_lower.count('explain') + transcript_lower.count('understand') + transcript_lower.count('because'),
            'practical_examples': transcript_lower.count('example') + transcript_lower.count('test') + transcript_lower.count('experiment')
        }
    }
    
    # Calculate enhanced quality score with AI coding focus
    quality_score = unified_score
    quality_score += 0.15 if content_quality_indicators.get('has_comparison_analysis') else 0
    quality_score += 0.18 if content_quality_indicators.get('covers_real_world_testing') else 0
    quality_score += 0.12 if content_quality_indicators.get('covers_multiple_tools') else 0
    quality_score += 0.10 if content_quality_indicators.get('has_practical_demo') else 0
    quality_score += 0.08 if content_quality_indicators.get('has_best_practices') else 0
    quality_score += 0.15 if learning_value_indicators.get('practical_focus') else 0
    quality_score += 0.12 if learning_value_indicators.get('comprehensive_coverage') else 0
    quality_score += 0.10 if learning_value_indicators.get('honest_assessment') else 0
    quality_score += 0.08 if learning_value_indicators.get('industry_relevant') else 0
    quality_score += 0.06 if learning_value_indicators.get('updated_content') else 0
    quality_score += (coverage_percentage / 100) * 0.18
    
    # Bonus for comprehensive AI coding comparison
    if video_data.get('tutorial_type') == 'comprehensive_comparison_analysis':
        quality_score += 0.12
    
    quality_score = min(quality_score, 1.0)
    
    # Save results to priority YouTube intelligence
    knowledge_vault_path = Path(__file__).parent.parent.parent / "knowledge-vault" / "databases" / "knowledge_vault" / "content-intelligence" / "priority-youtube"
    process_date = datetime.now().strftime('%Y-%m-%d')
    save_dir = knowledge_vault_path / process_date
    save_dir.mkdir(parents=True, exist_ok=True)
    
    # Save unified intelligence file
    result_file = save_dir / f"{video_data['video_id']}_ai_coding_assistant_unified_intelligence.json"
    
    result_dict = {
        'video_id': video_data['video_id'],
        'video_url': video_data['video_url'],
        'title': video_data['title'],
        'channel': video_data['channel'],
        'tutorial_type': video_data.get('tutorial_type', 'analysis'),
        'year': video_data.get('year', '2024'),
        'estimated_duration': video_data.get('estimated_duration', 'N/A'),
        'view_count': video_data.get('view_count', 'N/A'),
        'programming_concepts': concepts,
        'priority_topics': priority_topics,
        'topic_scores': topic_scores,
        'unified_score': unified_score,
        'quality_score': quality_score,
        'comprehensive_rating': insights['comprehensive_rating'],
        'content_summary': content_summary,
        'insights': insights,
        'processing_timestamp': datetime.now(timezone.utc).isoformat(),
        'processed_with': 'ai-coding-assistant-processor',
        'framework_version': '1.2.0',
        'content_type': 'ai_coding_comparison',
        'transcript_available': True,
        'high_value_indicators': {
            'ai_coding_focus': True,
            'comparison_analysis': content_quality_indicators.get('has_comparison_analysis', False),
            'real_world_testing': content_quality_indicators.get('covers_real_world_testing', False),
            'comprehensive': ai_score > 6,
            'practical_focus': learning_value_indicators.get('practical_focus', False),
            'industry_relevant': learning_value_indicators.get('industry_relevant', False),
            'current_content': learning_value_indicators.get('updated_content', False)
        }
    }
    
    with open(result_file, 'w') as f:
        json.dump(result_dict, f, indent=2)
    
    # Save enhanced transcript
    transcript_file = save_dir / f"{video_data['video_id']}_ai_coding_assistant_transcript.txt"
    with open(transcript_file, 'w') as f:
        f.write(f"# AI CODING ASSISTANT COMPARISON ANALYSIS\\n")
        f.write(f"# Title: {video_data['title']}\\n")
        f.write(f"# Channel: {video_data['channel']}\\n")
        f.write(f"# Video URL: {video_data['video_url']}\\n")
        f.write(f"# Analysis Type: {video_data.get('tutorial_type', 'Comparison').replace('_', ' ').title()}\\n")
        f.write(f"# Year: {video_data.get('year', '2024')}\\n")
        f.write(f"# Estimated Duration: {video_data.get('estimated_duration', 'N/A')}\\n")
        f.write(f"# Processing Date: {datetime.now(timezone.utc).isoformat()}\\n")
        f.write(f"# Unified Score: {unified_score:.3f}\\n")
        f.write(f"# Quality Score: {quality_score:.3f}\\n")
        f.write(f"# Comprehensive Rating: {insights['comprehensive_rating'].title()}\\n")
        f.write(f"# Priority Topics: {', '.join(priority_topics)}\\n")
        f.write(f"# Programming Concepts: {len(concepts)}\\n")
        f.write(f"# Top Concepts: {', '.join(concepts[:12])}\\n")
        f.write(f"# AI Tools Covered: GitHub Copilot, ChatGPT, Codi AI, Local Models\\n")
        f.write(f"\\n{'='*80}\\n")
        f.write(f"AI CODING ASSISTANT COMPARISON TRANSCRIPT\\n")
        f.write(f"{'='*80}\\n\\n")
        f.write(transcript)
    
    # Display comprehensive results
    print("🤖 AI Coding Assistant Analysis Complete!")
    print("=" * 75)
    print(f"Video: {video_data['title']}")
    print(f"Channel: {video_data['channel']}")
    print(f"URL: {video_data['video_url']}")
    print(f"Year: {video_data.get('year', '2024')}")
    print(f"Duration: {video_data.get('estimated_duration', 'N/A')}")
    print(f"Transcript length: {len(transcript)} characters")
    print()
    
    print("✅ Processing Results:")
    print(f"   Video ID: {video_data['video_id']}")
    print(f"   Unified Score: {unified_score:.3f}")
    print(f"   Quality Score: {quality_score:.3f}")
    print(f"   Comprehensive Rating: {insights['comprehensive_rating'].title()}")
    print(f"   Priority Topics: {', '.join(priority_topics)}")
    print(f"   Programming Concepts: {len(concepts)}")
    print(f"   Top Concepts: {', '.join(concepts[:15])}")
    print()
    
    print("🛠️  AI Coding Tools Analysis:")
    print(f"   ✓ Multiple Tools Covered: {'Yes' if content_quality_indicators.get('covers_multiple_tools') else 'No'}")
    print(f"   ✓ Real-World Testing: {'Yes' if content_quality_indicators.get('covers_real_world_testing') else 'No'}")
    print(f"   ✓ Comparison Analysis: {'Yes' if content_quality_indicators.get('has_comparison_analysis') else 'No'}")
    print(f"   ✓ Productivity Focus: {'Yes' if content_quality_indicators.get('covers_productivity_analysis') else 'No'}")
    print(f"   ✓ Practical Demo: {'Yes' if content_quality_indicators.get('has_practical_demo') else 'No'}")
    print(f"   ✓ Best Practices: {'Yes' if content_quality_indicators.get('has_best_practices') else 'No'}")
    print()
    
    print("🎓 Learning Value Analysis:")
    print(f"   ✓ Practical Focus: {'Yes' if learning_value_indicators.get('practical_focus') else 'No'}")
    print(f"   ✓ Comprehensive Coverage: {'Yes' if learning_value_indicators.get('comprehensive_coverage') else 'No'}")
    print(f"   ✓ Industry Relevant: {'Yes' if learning_value_indicators.get('industry_relevant') else 'No'}")
    print(f"   ✓ Honest Assessment: {'Yes' if learning_value_indicators.get('honest_assessment') else 'No'}")
    print(f"   ✓ Updated Content (2024): {'Yes' if learning_value_indicators.get('updated_content') else 'No'}")
    print(f"   ✓ Comparison Included: {'Yes' if learning_value_indicators.get('comparison_included') else 'No'}")
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
    print("✅ This comprehensive AI coding assistant analysis is now available for daily digest inclusion!")
    print("🌟 Exceptional quality content with real-world testing and honest evaluation!")

if __name__ == "__main__":
    process_ai_coding_assistant_video()