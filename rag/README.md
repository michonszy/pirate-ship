## RAG Collections
I have prepared 3 collections:
### attack_paths
Purpose: Provides the assistant with pre-modeled strategies for exploiting vulnerabilities.
Value: Helps the model reason about what to try next based on known tactics or weaknesses (e.g., privilege escalation via service account token misuse).
Format: YAML
Bonus: You can connect these to OWASP Top 10 or MITRE ATT&CK mappings.

### conversation_histories
Purpose: Stores prior user-assistant interactions, including decision logic, dead ends, and successful paths.
Value: Great for case-based reasoning and helping the assistant adapt its responses based on similar past scenarios.
FORMAT: JSON

### tools_documentation
Purpose: Gives detailed, up-to-date reference for using tools. Till now I have seen model struggling with some tools wasting iterations to properly use obtained values in a command (ex. crane).
Value: Helps the model to craft valid command syntaxes without hallucinating.
FORMAT: Markdown

## How They Work Together
When the model gets a prompt like:
```
“Here’s the output of kubectl get pods -A, what should I do next?”
```

You can:
Retrieve attack_paths relevant to suspicious pod names or namespaces.
Search conversation_histories for similar scenarios and their next steps.
Pull tool tips from tools_documentation if next step involves scanning or exploitation.

### Data for my RAG
https://github.com/google/go-containerregistry/tree/main/cmd/crane/doc
