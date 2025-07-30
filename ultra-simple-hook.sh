#!/bin/bash
# Ultra simple hook - just create a file to prove it was called
touch /Users/georgiospilitsoglou/Developer/projects/mypromptflow/HOOK_WAS_CALLED_$(date +%s).txt
echo '{"action": "allow"}' 
exit 0