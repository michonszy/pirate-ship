```
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⠤⠴⠶⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣶⣾⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠂⠉⡇⠀⠀⠀⢰⣿⣿⣿⣿⣧⠀⠀⢀⣄⣀⠀⠀ _____ _            ____  _           _             _     _       
⠀⠀⠀⢠⣶⣶⣷⠀⠀⠀⠸⠟⠁⠀⡇⠀⠀⠀⠀⠀⢹⠀⠀|_   _| |__   ___  |  _ \(_)_ __ __ _| |_ ___   ___| |__ (_)_ __  
⠀⠀⠀⠘⠟⢹⣋⣀⡀⢀⣤⣶⣿⣿⣿⣿⣿⡿⠛⣠⣼⣿⡟⠀ | | | '_ \ / _ \ | |_) | | '__/ _` | __/ _ \ / __| '_ \| | '_ \
 ⠀⣴⣾⣿⣿⣿⣿⢁⣾⣿⣿⣿⣿⣿⣿⡿⢁⣾⣿⣿⣿⠁⠀ | | | | | |  __/ |  __/| | | | (_| | ||  __/ \__ \ | | | | |_) |
⠀⠸⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⡇⢸⣿⣿⣿⠿⠇⠀⠀|_| |_| |_|\___| |_|   |_|_|  \__,_|\__\___| |___/_| |_|_| .__/ 
⠳⣤⣙⠟⠛⢻⠿⣿⠸⣿⣿⣿⣿⣿⣿⣿⣇⠘⠉⠀⢸⠀⢀⣠⠀                                                         |_|    
⠀⠈⠻⣷⣦⣼⠀⠀⠀⢻⣿⣿⠿⢿⡿⠿⣿⡄⠀⠀⣼⣷⣿⣿⠀⠀⠀Automated Kubernetes hacking tool 
⠀ ⠀⠈⣿⣿⣿⣶⣄⡈⠉⠀⠀⢸⡇⠀⠀⠉⠂⠀⣿⣿⣿⣧⠀⠀⠀   
⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣷⣤⣀⣸⣧⣠⣤⣴⣶⣾⣿⣿⣿⡿⠀⠀⠀
⠀⠀⠀ ⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀
⠀⠀⠀ ⠀⠀⠘⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠟⠛⠉⠀⠀⠀⠀
⠀⠀⠀⠀⠀  ⠀⠀⠀⠈⠉⠉⠉⠉⠉⠉⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
```

## ☠️ The Pirate Ship
Kubernetes Penetration Testing Tool

If Kubernetes is a fleet of container ships, this tool is your pirate ship, ready to attack.

A real ship can't sail without a crew. You’re the captain—but now you have a Large Language Model specially trained in the art of container exploitation to assist you in your conquest.

## 🏴‍☠️ Overview
Pirate Ship is an experimental AI-powered Kubernetes penetration testing tool. It leverages structured attack trees and a fine-tuned GPT-4 model to simulate realistic attacks in Kubernetes clusters.

* Attack tree-driven testing logic

* RAG integration for LLM guidance

* Realistic, command-line–only assistant

* Designed for red teamers and CTF challenges

## ⚙️ Features
* Structured attack automation via YAML-defined attack trees

* Multi-step exploit logic with variable reuse and preconditions

* RAG-enhanced reasoning for dynamic attacks

* Fine-tuned assistant outputs only executable shell commands (no explanations, just straightforward commands)

* Integration-ready with Kubernetes clusters and containers


## 🚀 Getting Started
> Requirements: Python 3.11+, access to a Kubernetes environment

Clone the repository:
```
git clone https://github.com/michonszy/pirate-ship.git
cd pirate-ship
```

Set up your virtual environment and install dependencies:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run the assistant:
```
python main.py
```

## 📁 Structure
```
.
├── playground/        # specially prepared easy to exploit CTF based on OWASP Top 10 dor k8s
├── prompt-engineering # Prompts for prompt engineering
├── rag/               # RAG data
   |-- attack_trees/      # YAML-defined attack trees with steps to execute
├── main.py            # Entry point for running the assistant
```