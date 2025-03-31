## 🚀 How to Run the CTF Environment

### 🐳 Docker Images

Docker part:
[frontend image](https://hub.docker.com/repository/docker/michonszy/k8s-ctf-frontend)
[backend image](https://hub.docker.com/repository/docker/michonszy/k8s-ctf-backend)
```
docker build -t michonszy/k8s-ctf-backend:v1 -f backend-Dockerfile .
docker push michonszy/k8s-ctf-backend:v1
docker build -t michonszy/k8s-ctf-frontend:v1 -f frontend-Dockerfile .
docker push michonszy/k8s-ctf-frontend:v1

```


### ☸️ Kubernetes part:

```
k apply -f Kubernetesfile.yaml

sudo kubectl port-forward -n vulnerable-app svc/frontend-service 80:80

kubectl get all -n vulnerable-app
```

### 🌐 Access the app
```
─➤  curl localhost                                                        

    <!DOCTYPE html>
    <html>
    <head>
      <title>CTF Challenge</title>
    </head>
    <body>
      <h1>Welcome to the Vulnerable App</h1>
      <p>This application has multiple vulnerabilities. Can you find them all?</p>
      <!-- Note: Remove before production. Admin access at /admin with password "d3fault_adm1n_p@ss" -->
      <div id="content"></div>
      <script>
        // Vulnerable to XSS
        const urlParams = new URLSearchParams(window.location.search);
        const message = urlParams.get('message');
        if (message) {
          document.getElementById('content').innerHTML = message;
        }

        // Hidden flag in JavaScript
        function checkFlag() {
          return "FLAG{client_side_javascript_leak}";
        }
      </script>
    </body>
    </html>
  %
```

## 🏴‍☠️ Challenges Overview

All challenges are based on the [OWASP Kubernetes Top 10](https://github.com/OWASP/www-project-kubernetes-top-ten?tab=readme-ov-file#owasp-kubernetes-top-10).

Each vulnerability is deliberately implemented and has one or more flags to capture.

---

### 1. 🛠️ Insecure Workload Configurations ✅

**Details**:
- Frontend pod runs with `privileged: true`
- Containers granted excessive capabilities: `add: ["ALL"]`
- `hostPath` mount exposes entire host filesystem (`/`)
- Containers run as root (`runAsUser: 0`)
- Writable root filesystems (`readOnlyRootFilesystem: false`)
- `allowPrivilegeEscalation: true` in backend pod

**Flag Locations**:
- `FLAG{node_compromise_via_hostpath}` – via `/host/tmp/k8s-node-flag.txt`  
- `FLAG{privileged_admin_pod}` – inside `admin-tools` pod at `/root/flag.txt`  

---

### 2. 🔗 Supply Chain Vulnerabilities ✅

**Details**:
- Backdoored Docker images
- No image signature verification
- No enforced vulnerability scanning
- Malicious code included in containers

**Flag Locations**:
- `FLAG{backdoor_in_maintenance_script}` – embedded in Docker image  
- `FLAG{docker_image_history_leak}` – found in image history layers  

---

### 3. 🔓 Overly Permissive RBAC Configurations ✅

**Details**:
- `vulnerable-sa` ServiceAccount with excessive privileges
- ClusterRole grants broad access to pods, secrets, and deployments
- ClusterRoleBinding provides admin-level access
- Misconfigured Kubernetes Dashboard with `cluster-admin`

**Flag Locations**:
- `FLAG{overly_permissive_rbac}` – in annotations of service account with excessive priveleges
- Additional flags accessible via privileged role abuse  

---

### 4. 🌐 Lack of Network Segmentation ✅

**Details**:
- No `NetworkPolicies` defined
- Full mesh pod communication
- No separation between frontend, backend, and database
- Services exposed externally that should be internal-only

**Flag Locations**:
- `FLAG{missing_network_policy}` – in  `backend-service` annotations
- Flags reachable via unintended network access  

---

### 5. 📉 Inadequate Logging and Monitoring ✅

**Details**:
- Applications run in `DEBUG` mode
- No centralized logging or monitoring tools
- Absence of audit logs

**Flag Locations**:
- `FLAG{inadequate_logging}` – in `stealthy-job` job  
- Exploitable through blind spots in observability  

---

### 6. 🔑 Broken Authentication ✅

**Details**:
- Hardcoded admin credentials exposed in frontend code and environment variables.
- Admin panel exposed at `/admin` without proper access control.
- API keys stored in plaintext in ConfigMaps and environment variables.
- Backend accepts insecure tokens or uses predictable authentication.

**How to Exploit**:
- Inspect frontend JavaScript or HTML comments to discover default credentials.
- Enumerate environment variables or config maps via pod access.
- Bypass authentication by sending predictable or static tokens to the API.

**Flag Location**:
- `FLAG{broken_authentication}` – visible **only after logging into `/admin`** or calling a restricted backend API using leaked credentials.
```
╰─➤  curl -X POST http://localhost:5000/api/login \                           130 ↵
  -H "Content-Type: application/json" \
  -d '{"username":"admin", "password":"super_admin_password"}'

{
  "flag": "FLAG{broken_authentication}",
  "message": "Welcome admin",
  "success": true,
  "token": "YWRtaW46c3VwZXJfYWRtaW5fcGFzc3dvcmQ="
}
```
---

### 7. 🔐 Missing Security Context ✅

**Details**:
- No `securityContext`, seccomp, or AppArmor profiles defined
- Containers running with default security settings
- No PodSecurityPolicies applied

**Flag Locations**:
- `FLAG{insecure_k8s_deployment}` – in backend pod environment 

---

### 8. 🧾 Secrets Management Failures ✅

**Details**:
- Sensitive data stored in ConfigMaps instead of Secrets
- No encryption at rest
- Passwords and connection strings in plaintext

**Flag Locations**:
- `FLAG{secrets_badly_managed}` – in `application-secrets` Secret  
- `FLAG{sensitive_data_in_configmap}` – in `db-credentials` ConfigMap  

---

### 9. ⚙️ Misconfigured Cluster Components ✅ (NEED FIX!!!)

**Details**:
- Kubernetes Dashboard is exposed externally with **cluster-admin privileges**.
- No authentication required to access the dashboard (`ClusterRoleBinding` is wide open).
- Critical **admission controllers** (like `PodSecurityPolicy`, `LimitRanger`, `SecurityContextDeny`) are **not enabled** — simulated via ConfigMap.
- Services (e.g., dashboard, internal APIs) are exposed with `type: NodePort` or `LoadBalancer` and **lack ingress rules or authentication**.

**How to Exploit**:
- Access the **Kubernetes Dashboard** directly via NodePort (`/api/v1/namespaces/kube-system/services/https:kubernetes-dashboard:/proxy/`).
- View or modify high-privilege resources without authentication.
- Deploy privileged or misconfigured pods without any admission controller blocking you.
- Identify insecurely exposed services that allow interaction with the cluster's internals.

**Flag Locations**:
- `FLAG{misconfigured_dashboard}` – visible in the Dashboard UI or a secret accessible from the Dashboard session.

**Example Recon Tips**:
- Use `kubectl get svc -A` to discover externally exposed services.
- Access the dashboard:
  ```
  kubectl port-forward -n kube-system svc/kubernetes-dashboard 8443:443
  curl https://localhost:8443/
```
---

### 10. 🧟‍♂️ Outdated and Vulnerable Kubernetes Components ✅

**Details**:
- Containers run on outdated base images with known CVEs (e.g., `alpine:3.10`, `python:3.6`, `ubuntu:16.04`)
- No image scanning or update policy is enforced
- Simulates the risk of using deprecated components or unpatched dependencies
- Kubernetes version simulates outdated behavior (no PodSecurity admission, legacy APIs)

**How to Exploit**:
- Use `kubectl describe pod` or `kubectl get pods -o yaml` to inspect image tags
- Pull the container images locally and analyze them with tools like:
  - `trivy`, `grype`, or `docker scan` to find known vulnerabilities
- Examine image history (`docker history`) for sensitive data or backdoored layers
- Abuse outdated behaviors (e.g., insecure defaults, writable `/tmp`, known exploits in base binaries)

**Flag Locations**:
- `FLAG{outdated_components}` – embedded in vulnerable image layers or metadata
  - e.g., use `docker history` on `michonszy/k8s-ctf-backend:v1` to extract the flag