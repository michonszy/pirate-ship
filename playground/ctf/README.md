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

### 1. 🛠️ Insecure Workload Configurations
Goal: Show how misconfigured containers (privileged, hostPath, etc.) lead to host compromise.

Flags:
```
FLAG{node_compromise_via_hostpath} — via hostPath

FLAG{privileged_admin_pod} — in admin-tools pod
```

How to get:

```
kubectl exec admin-tools -n vulnerable-app -- cat /root/flag.txt
kubectl exec <any-pod> -n vulnerable-app -- cat /host/tmp/k8s-node-flag.txt
```
Checks:
* Verify that admin-tools is running privileged
* Check /host/tmp/k8s-node-flag.txt is placed via the job

### 2. 🔗 Supply Chain Vulnerabilities
Goal: Show how unverified/backdoored images leak data.


Flags:
```
FLAG{backdoor_in_maintenance_script}

FLAG{docker_image_history_leak}
```
How to get:

Pull image:
```
docker pull michonszy/k8s-ctf-backend:v1
docker history michonszy/k8s-ctf-backend:v1
```
Run container & inspect:
```
docker run -it michonszy/k8s-ctf-backend:v1 sh
```
Checks:
* One flag should be exposed in docker history
* Another should be inside a file in /opt/ or entrypoint.sh

### 3. 🔓 Overly Permissive RBAC
Goal: Show how excessive permissions lead to privilege escalation.


Flag:
```
FLAG{overly_permissive_rbac} — annotation in ServiceAccount
```
How to get:
```
kubectl get sa vulnerable-sa -n vulnerable-app -o yaml | grep FLAG
```
Checks:
* Ensure ClusterRoleBinding exists and grants cluster-admin to vulnerable-sa

### 4. 🌐 Lack of Network Segmentation
Goal: Show how missing NetworkPolicies allow lateral movement.

Flag:
```
FLAG{missing_network_policy} — only visible from internal pod access
```
How to get:
```
kubectl exec backend-xxxx -n vulnerable-app -- curl http://backend-service:5000/internal/admin
```
Checks:
/internal/admin endpoint returns flag and is only reachable because of missing NetworkPolicy

## 5. 📉 Inadequate Logging and Monitoring
Goal: Show that blind-spot activities (privileged pod logs) go unnoticed.

Flag:
```
FLAG{inadequate_logging} — in simulated syslog on host
```

How to get:
```
kubectl exec host-inspector -n vulnerable-app -- grep FLAG /host/var/log/syslog
```
Checks:
* Confirm stealthy-job ran and wrote to /host/var/log/syslog
* host-inspector should have hostPath to read it

### 6. 🔑 Broken Authentication
Goal: Show weak or leaked credentials can bypass protection.

Flag:
```
FLAG{broken_authentication} — visible after admin login
```

How to get:
```
kubectl expose backend
curl -X POST http://<backend-url>:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"super_admin_password"}'
```
Checks:
* Flag is only returned for valid login
* Credentials are leaked in frontend HTML/JS

### 7. 🔐 Missing Security Context
Goal: Show insecure container defaults allow risk.

Flag:
```
FLAG{insecure_k8s_deployment} — stored in backend pod’s env var
```
How to get:
```
kubectl exec backend-xxxx -n vulnerable-app -- printenv FLAG
```
Checks:
* No securityContext, seccomp, AppArmor, etc.
* Flag stored only in runtime, not in manifest

### 8. 🧾 Secrets Management Failures
Goal: Show improper handling of sensitive data.


Flags:
```
FLAG{sensitive_data_in_configmap} — in db-credentials ConfigMap
FLAG{secrets_badly_managed} — in application-secrets Secret
```

How to get (ConfigMap):
```
kubectl get configmap db-credentials -n vulnerable-app -o yaml | grep FLAG
```
Secret should be inaccessible to player via command line

Checks:
* Player role allows access to ConfigMaps only
* application-secrets contains base64-encoded flag

### 9. ⚙️ Misconfigured Cluster Components
Goal: Show misconfig exposes full control via Dashboard.

Flag:
```
FLAG{misconfigured_dashboard} — stored in dashboard-flag Secret, visible via Dashboard UI
```
How to get:
```
Forward Dashboard: kubectl port-forward -n vulnerable-app svc/kubernetes-dashboard 9090:9090
Open: http://localhost:9090
```

Use full admin access to navigate to: Secrets > dashboard-flag

Checks:
* Dashboard runs as cluster-admin SA
* No auth is required (NodePort exposed)

### 10. 🧟‍♂️ Outdated Kubernetes Components
Goal: Show risk of running outdated base images with known CVEs.

Flag:
```
FLAG{outdated_components} — hidden in outdated Docker image
```
How to get:
```
docker pull michonszy/k8s-ctf-frontend:v1
docker history michonszy/k8s-ctf-frontend:v1 | grep FLAG
```
Or check within container:
```
docker run -it michonszy/k8s-ctf-frontend:v1 sh
```
Checks:
* Image uses old Alpine or Python version
* Flag embedded in layer or image label



## User
You are running this challenge with those privilages:
| Command                          | Expected | Notes                                  |
|----------------------------------|----------|----------------------------------------|
| `kubectl auth can-i list pods`   | ✅       | Can list pod names                     |
| `kubectl auth can-i get pods`    | ❌       | Prevents `kubectl get pod -o yaml`     |
| `kubectl auth can-i describe pods` | ❌       | Also uses get under the hood           |
| `kubectl auth can-i create pods/exec` | ✅ | Allows `kubectl exec`                 |
| `kubectl auth can-i create pods/log` | ✅  | Allows `kubectl logs`                 |
| `kubectl auth can-i get configmaps` | ✅    | Allows viewing leaked data in configmaps |
| `kubectl auth can-i list configmaps` | ✅   | Can enumerate all configmaps           |
| `kubectl auth can-i get secrets` | ❌       | Prevents reading any secrets           |
| `kubectl auth can-i list secrets` | ❌      | Prevents secret enumeration            |
| `kubectl auth can-i get namespaces` | ❌    | Can't see cluster-wide info            |
| `kubectl auth can-i get events`  | ❌       | Prevents snooping runtime events/logs  |

LOGIN AS ONE:
```
chmod +x player-kubeconfig.sh
./player-kubeconfig.sh
export KUBECONFIG=$PWD/kubeconfig-player.yaml
```
and you will see
```
╰─➤  kubectl get pods

Error from server (Forbidden): pods is forbidden: User "system:serviceaccount:vulnerable-app:player" cannot list resource "pods" in API group "" in the namespace "vulnerable-app"
```

to get back to admin just use:
```
unset KUBECONFIG
```