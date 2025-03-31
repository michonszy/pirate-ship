# 🛡️ Kubernetes Attack Trees

Structured, machine-readable attack trees for simulating and reasoning about offensive security in Kubernetes and containerized environments.  
Perfect for use with GPT-4o, RAG systems, red team automation, CTF prep, or educational tooling.

## 📦 What’s Inside

- ✅ **YAML-based attack trees** for container escape, privilege escalation, and misconfig exploitation
- ✅ Support for conditional logic, branching, and dynamic outputs
- ✅ Designed for use with GPT-4o or other AI-based agents
- ✅ Includes a validation script to check structure and detect YAML issues

## 🧠 Format Overview

Each attack tree is written in structured YAML:

```
attack:
  name: "Kubernetes CTF Compromise"
  steps:
    - id: 1.0
      name: "Check env vars"
      command: "printenv"
      tags: ["info_leak"]
      on_success:
        - capture_flag: "FLAG{leaked_secret}"
        - remediation: "Avoid exposing secrets via environment variables"
```
✅ Supported features:
* Step IDs and names
* Commands and conditions
* on_success / on_failure handling
* Flag capture and remediation notes
* Tagging and preconditions
* Variable extraction and reuse 

sample:
```
- id: 5.0
  name: "Extract Pod Name"
  command: "kubectl get pods -n vulnerable-app -l app=admin-tools -o jsonpath='{.items[0].metadata.name}'"
  output_var: admin_pod

- id: 5.1
  name: "Use pod name to exec"
  command: "kubectl exec -n vulnerable-app ${admin_pod} -- cat /root/flag.txt"
  on_success:
    - capture_flag: "FLAG{privileged_admin_pod}"

```

## 🔧 Validation tool
```
python format_validator.py kubernetes-ctf-compromise.yaml
```
possible outputs:
```
✅ Attack tree is valid.

or

❌ YAML structure error: Duplicate key detected: 'command' at line 17

```