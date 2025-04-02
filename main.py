import warnings
import os
import subprocess
import re
import yaml
import sys
from dotenv import load_dotenv
from openai import OpenAI
import chromadb

load_dotenv()
TOOL_NAMES = ["trivy"]
CHROMA_PATH = "chroma_db"
NUM_RESULTS = 1
warnings.filterwarnings("ignore")

art=r"""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⠤⠴⠶⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣶⣾⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠂⠉⡇⠀⠀⠀⢰⣿⣿⣿⣿⣧⠀⠀⢀⣄⣀⠀⠀⠀⠀⠀⠀  _____ _            ____  _           _             _     _       
⠀⠀⠀⠀⠀⠀⢠⣶⣶⣷⠀⠀⠀⠸⠟⠁⠀⡇⠀⠀⠀⠀⠀⢹⠀⠀⠀⠀⠀⠀ |_   _| |__   ___  |  _ \(_)_ __ __ _| |_ ___   ___| |__ (_)_ __  
⠀⠀⠀⠀⠀⠀⠘⠟⢹⣋⣀⡀⢀⣤⣶⣿⣿⣿⣿⣿⡿⠛⣠⣼⣿⡟⠀⠀⠀⠀   | | | '_ \ / _ \ | |_) | | '__/ _` | __/ _ \ / __| '_ \| | '_ \ 
⠀⠀⠀⠀⠀⣴⣾⣿⣿⣿⣿⢁⣾⣿⣿⣿⣿⣿⣿⡿⢁⣾⣿⣿⣿⠁⠀⠀⠀⠀   | | | | | |  __/ |  __/| | | | (_| | ||  __/ \__ \ | | | | |_) |
⠀⠀⠀⠀⠸⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⡇⢸⣿⣿⣿⠿⠇⠀⠀⠀⠀   |_| |_| |_|\___| |_|   |_|_|  \__,_|\__\___| |___/_| |_|_| .__/ 
⠀⠀⠀⠳⣤⣙⠟⠛⢻⠿⣿⠸⣿⣿⣿⣿⣿⣿⣿⣇⠘⠉⠀⢸⠀⢀⣠⠀⠀⠀                                                            |_|    
⠀⠀⠀⠀⠈⠻⣷⣦⣼⠀⠀⠀⢻⣿⣿⠿⢿⡿⠿⣿⡄⠀⠀⣼⣷⣿⣿⠀⠀⠀   Kubernetes hacking tool ☸🏴‍☠️
⠀⠀⠀⠀⠀⠀⠈⣿⣿⣿⣶⣄⡈⠉⠀⠀⢸⡇⠀⠀⠉⠂⠀⣿⣿⣿⣧⠀⠀⠀     by Szymon Michoń
⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣷⣤⣀⣸⣧⣠⣤⣴⣶⣾⣿⣿⣿⡿⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠘⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠟⠛⠉⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠉⠉⠉⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
      
"""

def get_kube_prompt():
    try:
        # Get current context
        context = subprocess.run(
            ["kubectl", "config", "current-context"],
            check=True, capture_output=True, text=True
        ).stdout.strip()

        # Get current namespace
        namespace = subprocess.run(
            ["kubectl", "config", "view", "--minify", "--output", "jsonpath={..namespace}"],
            check=True, capture_output=True, text=True
        ).stdout.strip()

        if not namespace:
            namespace = "default"

        return f"{context}:{namespace}"
    
    except subprocess.CalledProcessError:
        print("\n❌ No Kubernetes context is currently active or you are not logged into any cluster.\n")
        print("🔐 Please log into a cluster first. Here are common options:\n")
        print("👉 1. Start a local cluster using Rancher Desktop, Minikube, or Kind")
        print("👉 2. Connect to a cloud cluster:")
        print("     • AWS:      aws eks update-kubeconfig --name <cluster-name>")
        print("     • GCP:      gcloud container clusters get-credentials <cluster-name>")
        print("     • Azure:    az aks get-credentials --name <cluster-name>")
        print("👉 3. Authenticate with your provider (if using SSO/OIDC)")
        print("👉 4. Check config:  kubectl config get-contexts")
        print("👉 5. Set a context: kubectl config use-context <name>\n")
        print("💡 Once connected, re-run this tool.\n")
        sys.exit(1)
        

CLUSTER_IP = get_kube_prompt()
HACK_NAME = "example_hack"

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
def validate_attack_tree(attack_tree):
    # Try both flat and nested formats
    if "steps" in attack_tree and isinstance(attack_tree["steps"], list):
        return "flat"
    elif "attack" in attack_tree and "steps" in attack_tree["attack"] and isinstance(attack_tree["attack"]["steps"], list):
        return "nested"
    else:
        raise ValueError("❌ Error: Invalid attack tree format. No valid 'steps' list found.")

def execute_attack_tree(attack_tree):
    """
    Execute a structured attack tree with support for nested 'attack' block.
    Dynamically captures any FLAG{...} patterns found in command outputs.
    """
    format_type = validate_attack_tree(attack_tree)

    if format_type == "nested":
        attack_tree = attack_tree["attack"]

    steps = {step["id"]: step for step in attack_tree["steps"]}
    visited = set()
    variables = {var["name"]: var["value"] for var in attack_tree.get("variables", [])}
    captured_flags = []  # Stores only actually found flags
    outputs = []

    def substitute_variables(text):
        for var, val in variables.items():
            text = text.replace(f"${{{var}}}", val)
        return text

    def execute_step(step_id):
        if step_id in visited:
            print(f"⚠️ Step {step_id} already executed. Skipping.")
            return
        visited.add(step_id)

        step = steps.get(step_id)
        if not step:
            print(f"❌ No step with ID: {step_id}")
            return

        print(f"\n➡️ Executing step: {step.get('name', step_id)}")

        command = substitute_variables(step.get("command", ""))
        print(f"🔄 Running: {command}")
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                check=True,
                capture_output=True,
                text=True,
                timeout=60
            )
            output = result.stdout.strip()
            out = "Command: "+ str(command)+" \n Output: "+output
            outputs.append(out)
            print(f"✅ Output:\n{output}")
            # Dynamic flag capture from command output
            found_flags = re.findall(r'FLAG\{[^}]+\}', output)
            for flag in found_flags:
                if flag not in captured_flags:
                    captured_flags.append(flag)
                    print(f"🏴 Captured flag: {flag}")

            # Handle on_success actions (excluding YAML flag declarations)
            if step.get("on_success"):
                for action in step["on_success"]:
                    if isinstance(action, dict) and "remediate" in action:
                        print(f"💡 Suggested fix: {action['remediate']}")
                    elif isinstance(action, dict) and "next" in action:
                        execute_step(action["next"])

        except subprocess.TimeoutExpired:
            print(f"⏰ Command timed out after 60 seconds: {command}")
            output = f"Command timed out after 60 seconds: {command}"
            raise subprocess.CalledProcessError(1, command, output)

        except subprocess.CalledProcessError as e:
            output = e.output.strip() if e.output else e.stderr.strip()
            print(f"❌ Command failed:\n{output}")

            # Also check for flags in error output
            found_flags = re.findall(r'FLAG\{[^}]+\}', output)
            for flag in found_flags:
                if flag not in captured_flags:
                    captured_flags.append(flag)
                    print(f"🏴 Captured flag in error output: {flag}")

            # Failure handling
            if step.get("on_failure"):
                for action in step["on_failure"]:
                    if isinstance(action, dict) and "next" in action:
                        print(f"⏭️ Proceeding to next step after failure: {action['next']}")
                        execute_step(action["next"])
                    elif isinstance(action, dict) and "remediate" in action:
                        print(f"💡 Suggested fix: {action['remediate']}")
            elif step.get("next"):
                print(f"⏭️ Proceeding to next step: {step['next']}")
                execute_step(step["next"])

    root_step_id = attack_tree.get("start") or attack_tree["steps"][0]["id"]
    execute_step(root_step_id)

    print("\n🎯 Attack tree execution complete.")
    if "recon" in attack_tree.get("name", "").lower():
        print("\n🎯 Attack tree execution complete.")
        f = open('recon_output.txt','w+')
        print(outputs,file=f)
        f.close()
        print("\n🧠 Recon Summary in recon_output.txt")
        print("\n🎯 Recon complete.")
    else:
        print("\n🎯 Attack tree execution complete.")
        if captured_flags:
            print("✅ Flags captured:")
            for flag in captured_flags:
                print(f"🏁 {flag}")
        else:
            print("No flags were captured during execution.")


def hack(hack_name):
    """
    Everything setted up? Let's execute this!
    """
    print(f"Executing hack: {hack_name}")
    
    yaml_file = f"rag/attack-trees/{hack_name}.yml"
    if not os.path.isfile(yaml_file):
        yaml_file_alt = f"{hack_name}.yml"
        if os.path.isfile(yaml_file_alt):
            yaml_file = yaml_file_alt
        else:
            print(f"❌ Error: No .yaml or .yml file found for this hack.")
            return True

    try:
        with open(yaml_file, "r") as file:
            attack_tree = yaml.safe_load(file)
    except yaml.YAMLError as e:
        print(f"❌ Error: Failed to parse YAML file '{yaml_file}': {e}")
        return True

    try:
        validate_attack_tree(attack_tree)
        execute_attack_tree(attack_tree)
    except Exception as e:
        print(f"❌ Error: while executing attack: {e}")
        return True

    print(f"✅ Successfully executed hack: {hack_name}")
    return True


def list_hacks():
    """
    Lists all available hack JSON files in the specified directory
    and allows the user to select one dynamically.
    """
    global HACK_NAME
    directory = 'rag/attack-trees'
    hack_files = [f for f in os.listdir(directory) if f.endswith(".yaml") or f.endswith(".yml")]

    if not hack_files:
        print("❌ No hack files (.yaml/.yml) found in the directory.")
        return True

    print("🔍 Available Hacks:")
    for i, file in enumerate(hack_files, start=1):
        print(f"  {i}. {file}")

    while True:
        try:
            choice = input("\nEnter the number of the hack to select (or 'q' to cancel): ")
            if choice.lower() == 'q':
                print("❌ Hack selection canceled.")
                return True

            choice_index = int(choice) - 1
            if 0 <= choice_index < len(hack_files):
                HACK_NAME = os.path.splitext(hack_files[choice_index])[0]
                print(f"✅ Hack selected: {HACK_NAME}")
                return True
            else:
                print("⚠️ Invalid choice. Please select a valid number.")
        except ValueError:
            print("⚠️ Invalid input. Please enter a number or 'q'.")

def hello():
    """Greet the user."""
    print("Hello, user! How can I help you?")
    return True

def exit():
    """Exit the application."""
    print("Goodbye! Exiting the app...")
    return False

def status():
    """Show the current status."""
    print("🔍 Checking Kubernetes cluster status...\n")

    try:
        subprocess.run(
            ["kubectl", "cluster-info"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        print("✅ Connection to Kubernetes cluster is active.\n")
        return True

    except subprocess.CalledProcessError:
        print("❌ Cannot connect to a Kubernetes cluster.\n")
        print("📋 Troubleshooting steps:")
        print("  • Ensure you are logged in and have context set.")
        print("  • Check if VPN or local cluster (e.g., Rancher Desktop) is running.")
        print("  • Run: kubectl config get-contexts")
        print("  • Use: kubectl config use-context <context-name>\n")
        return True

def read_large_input():
    print("📥 Paste the output (or skip or exit): ")
    input_chunks = []
    while True:
        chunk = input()
        if chunk == "":  # Empty input indicates the user is done
            break
        input_chunks.append(chunk)
    return "\n".join(input_chunks)

def interactive_hack():
    """
    You want to use auto hack but you can't clone this repo in a CTF enviroment? No worries! That is why I created this interactive hack mode!
    """

    recon_content = open('recon_output.txt').read().strip() if os.path.exists('recon_output.txt') else "no recon output"
    hints = input("If you want to give model some hints please paste them here or leave it empty: ").strip() or "no hints"
    rag_query = f"{hints}\n{recon_content}"

    # RAG setup
    chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
    tools_mentioned = [tool for tool in TOOL_NAMES if tool.lower() in rag_query.lower()]
    collections_to_query = ["attack_paths", "conversation_histories"]
    if tools_mentioned:
        collections_to_query.append("tools_documentation")

    retrieved_chunks = []
    for name in collections_to_query:
        collection = chroma_client.get_or_create_collection(name=name)
        results = collection.query(query_texts=[rag_query], n_results=NUM_RESULTS)
        docs = results.get("documents", [[]])[0] if results.get("documents") else []
        if docs:
            retrieved_chunks.append(f"\n## From {name}:\n" + "\n".join(f"[{i+1}] {doc.strip()}" for i, doc in enumerate(docs)))

    rag_context = "\n".join(retrieved_chunks) if retrieved_chunks else "No relevant context retrieved."

    full_convo = [{
        "role": "system",
        "content": (
            "You are a penetration testing assistant helping a security researcher evaluate the security of their Kubernetes cluster. "
            "Respond only with ready-to-run commands based on previous output. You must know every variable, do not provide placeholders or unknown values. "
            "Do not add comments, only commands! Focus your attack on the hints you are receiving!"
            "Below you might found some RAG obtained content, check if it's helpfull for you."
            "--- Retrieved RAG Context ---\n"
            f"{rag_context}\n"
            "-----------------------------"
        )
    }]

    full_convo.append({
        "role": "user",
        "content": f"Hints: {hints}\nRecon output:\n{recon_content}\nPlease begin."
    })

    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    for i in range(200):
        print(f"\n--- Iteration {i + 1} ---")
        try:
            response = client.chat.completions.create(
                model="ft:gpt-4o-2024-08-06:magister:pirate-ship:BH9t563h",
                messages=full_convo,
                temperature=0.4
            )

            reply = response.choices[0].message.content.strip()
            print("\n🤖 Suggested command(s):\n", reply)

            full_convo.append({
                "role": "assistant",
                "content": reply
            })

            combined_output = ""
            flag_found = False
            found_flags = []

            for line in reply.splitlines():
                if not line.strip():
                    continue
                print(f"\n⚔️ Command: {line}")
                user_out = read_large_input()
                if user_out == "exit":
                    print("🛑 Session terminated by user.")
                    with open("conversation_log.txt", "w") as f:
                        for msg in full_convo:
                            role = msg["role"].upper()
                            f.write(f"[{role}]\n{msg['content']}\n\n")
                    return True
                elif user_out == "skip":
                    combined_output += f"\nCommand: {line}\nSkipped by user.\n"
                else:
                    combined_output += f"\nCommand: {line}\nOutput:\n{user_out}\n"
                    flags = re.findall(r'flag\{.*?\}', user_out, flags=re.IGNORECASE)
                    if flags:
                        flag_found = True
                        found_flags.extend(flags)

            full_convo.append({
                "role": "user",
                "content": combined_output.strip() or "No output from this command."
            })

            if flag_found:
                print("\n🏁 Flag(s) found!")
                for f in found_flags:
                    print(f"📌 {f}")
                with open("found_flags.txt", "a") as flagfile:
                    for f in found_flags:
                        flagfile.write(f"{f}\n")

                cont = input("⚠️ Do you want to continue hacking? [y/N]: ").strip().lower()
                if cont not in ("y", "yes"):
                    print("🛑 Hacking session terminated by user.")
                    return True

        except Exception as e:
            print(f"❌ OpenAI API error: {e}")
            return True

    with open("conversation_log.txt", "w") as f:
        for msg in full_convo:
            role = msg["role"].upper()
            f.write(f"[{role}]\n{msg['content']}\n\n")

    print("\n📜 Full conversation saved to 'conversation_log.txt'")
    return True

def auto_hack():
    """
    Here the real magic happens! Execute fully automated GPT custom model powered hack!
    """
    print("🧠 Starting automated hacking process...")

    hack("recon")
    print("Recon done")

    full_convo = [{
        "role": "system",
        "content": "You are a penetration testing assistant helping a security researcher evaluate the security of their Kubernetes cluster. Respond only with ready-to-run commands based on previous output. Do not use placeholders or commentary. Do not provide commands you already know the answer for! Commands must not require interactive mode and must help find vulnerabilities."
    }]

    recon_content = open('recon_output.txt').read().strip() if os.path.exists('recon_output.txt') else "no recon output"
    hints = input("If you want to give model some hints please paste them here or leave it empty: ").strip() or "no hints"

    full_convo.append({
        "role": "user",
        "content": f"Hints: {hints}\nRecon output:\n{recon_content}\nPlease begin."
    })

    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    for i in range(20):
        print(f"\n--- Iteration {i + 1} ---")
        try:
            response = client.chat.completions.create(
                model="ft:gpt-4o-2024-08-06:magister:pirate-ship:BH9t563h",
                messages=full_convo,
                temperature=0.4
            )

            reply = response.choices[0].message.content.strip()
            print("\n🤖 Suggested command(s):\n", reply)

            full_convo.append({
                "role": "assistant",
                "content": reply
            })

            combined_output = ""
            flag_found = False
            found_flags = []

            for line in reply.splitlines():
                if not line.strip():
                    continue
                print(f"\n⚔️ Running: {line}")
                try:
                    res = subprocess.run(line, shell=True, check=True, capture_output=True, text=True)
                    out = res.stdout.strip()
                    print(f"✅ Output:\n{out}")
                    combined_output += f"\nCommand: {line}\nOutput:\n{out}\n"

                    # 🔍 Look for flag pattern
                    flags = re.findall(r'flag\{.*?\}', out, flags=re.IGNORECASE)
                    if flags:
                        flag_found = True
                        found_flags.extend(flags)

                except subprocess.CalledProcessError as e:
                    err = e.stderr.strip()
                    print(f"❌ Failed:\n{err}")
                    combined_output += f"\nCommand: {line}\nError:\n{err}\n"

            full_convo.append({
                "role": "user",
                "content": combined_output.strip() or "No output from this command."
            })

            if flag_found:
                print("\n🏁 Flag(s) found!")
                for f in found_flags:
                    print(f"📌 {f}")
                with open("found_flags.txt", "a") as flagfile:
                    for f in found_flags:
                        flagfile.write(f"{f}\n")

                cont = input("⚠️ Do you want to continue hacking? [y/N]: ").strip().lower()
                if cont not in ("y", "yes"):
                    print("🛑 Hacking session terminated by user.")
                    break

        except Exception as e:
            print(f"❌ OpenAI API error: {e}")
            break

    with open("conversation_log.txt", "w") as f:
        for msg in full_convo:
            role = msg["role"].upper()
            f.write(f"[{role}]\n{msg['content']}\n\n")

    print("\n📜 Full conversation saved to 'conversation_log.txt'")
    return True


def setup():
    """Setup tool"""
    print("Current setup")
    print(f"Victim ip: {CLUSTER_IP}")
    print(f"Hack name: {HACK_NAME}")
    print("Mode: recognition")
    print("Attak type: AI")
    chg = input("Do you want to change it? [Y/N] : ")
    if chg.lower() == 'y':
        print("Change mode")
    else:
        print("No changes were made")
    return True

def help():
    print("\nAvailable commands:")
    for command in COMMANDS:
        print(f"{command} - {COMMANDS[command].__doc__}")
    print()
    return True

COMMANDS = {
    "hello": hello,
    "exit": exit,
    "status": status,
    "help": help,
    "setup": setup,
    "hack": lambda: hack(HACK_NAME),
    "list": list_hacks,
    "auto": auto_hack,
    'interactive_ai': interactive_hack

}

def handle_command(command):
    command_func = COMMANDS.get(command.lower())
    if command_func:
        return command_func() 
    else:
        print(f"Unknown command")
        return True
    
def main():
    print(art) 
    running = True
    while running:
        command = input(f"╭─ "+bcolors.WARNING+CLUSTER_IP+ bcolors.ENDC+" > "+bcolors.FAIL+HACK_NAME+ bcolors.ENDC+" \n╰─➤ ")
        running = handle_command(command)

if __name__ == "__main__":
    main()
