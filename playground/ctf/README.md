### How to run?

Docker part:
[frontend image](https://hub.docker.com/repository/docker/michonszy/k8s-ctf-frontend)
[backend image](https://hub.docker.com/repository/docker/michonszy/k8s-ctf-backend)
```
docker build -t michonszy/k8s-ctf-backend:v1 -f backend-Dockerfile .
docker push michonszy/k8s-ctf-backend:v1
docker build -t michonszy/k8s-ctf-frontend:v1 -f frontend-Dockerfile .
docker push michonszy/k8s-ctf-frontend:v1

```


Kubernetes part:

```
k apply -f Kubernetesfile.yaml

sudo kubectl port-forward -n vulnerable-app svc/frontend-service 80:80

kubectl get all -n vulnerable-app
```
and now you should be able to access the webpage:
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

### CHALLENGES:
All challenges are based on [K8S OWASP TOP 10](https://github.com/OWASP/www-project-kubernetes-top-ten?tab=readme-ov-file#owasp-kubernetes-top-10)

1. Insecure Workload Configurations

Implementation Status: ✅

Details:
Frontend pod with privileged: true
Containers with excessive capabilities (add: ["ALL"])
hostPath mount to / exposing the entire host filesystem
Containers running as root (runAsUser: 0)
Writable filesystems (readOnlyRootFilesystem: false)
allowPrivilegeEscalation: true in backend pod


Flag Locations:
FLAG{insecure_workload_config} in challenge-flags ConfigMap
FLAG{node_compromise_via_hostpath} accessible via hostPath mount at /host/tmp/k8s-node-flag.txt
FLAG{privileged_admin_pod} in admin-tools pod at /root/flag.txt



2. Supply Chain Vulnerabilities

Implementation Status: ✅ 

Details:
Vulnerable Docker images with backdoors (from previous implementation)
No image signature verification
No vulnerability scanning enforced
Images potentially containing malicious code


Flag Locations:
FLAG{supply_chain_vulnerability} in challenge-flags ConfigMap

Additional flags in Docker images from previous implementation:
FLAG{backdoor_in_maintenance_script}
FLAG{docker_image_history_leak}





3. Overly Permissive RBAC Configurations

Implementation Status: ✅

Details:
ServiceAccount vulnerable-sa with excessive permissions
ClusterRole with broad access to pods, secrets, deployments
ClusterRoleBinding giving vulnerable-sa admin-level access
Dashboard with cluster-admin privileges


Flag Locations:
FLAG{overly_permissive_rbac} in challenge-flags ConfigMap
Access to otherwise restricted resources containing flags



4. Lack of Network Segmentation Controls

Implementation Status: ✅

Details:
No NetworkPolicies defined at all
All pods can communicate with each other
No segmentation between frontend, backend, and database
External access to services that should be internal


Flag Locations:
FLAG{missing_network_policy} in challenge-flags ConfigMap
Flags accessible by accessing services that should be restricted


5. Inadequate Logging and Monitoring

Implementation Status: ✅

Details:
No logging or monitoring resources defined
DEBUG mode enabled on applications
No audit logging configuration


Flag Locations:
FLAG{inadequate_logging} in challenge-flags ConfigMap
Players must find ways to exploit the lack of logging to access flags



6. Broken Authentication

Implementation Status: ✅

Details:
Weak authentication in applications
Exposed admin interfaces
API keys in environment variables
Credentials in ConfigMaps


Flag Locations:
FLAG{broken_authentication} in challenge-flags ConfigMap
Access to protected resources using discovered credentials



7. Missing Security Context

Implementation Status: ✅

Details:
Missing proper securityContext constraints
Containers with default security settings
No seccomp or AppArmor profiles
No pod security policies


Flag Locations:
FLAG{missing_security_context} in challenge-flags ConfigMap
FLAG{insecure_k8s_deployment} in backend pod environment


8. Secrets Management Failures

Implementation Status: ✅

Details:
Credentials in ConfigMaps instead of Secrets
Secrets not encrypted at rest
Sensitive data in environment variables
Plaintext passwords and connection strings


Flag Locations:
FLAG{secrets_badly_managed} in application-secrets Secret
FLAG{sensitive_data_in_configmap} in db-credentials ConfigMap
FLAG{secret_management_failures} in challenge-flags ConfigMap



9. Misconfigured Cluster Components

Implementation Status: ✅

Details:
Exposed Kubernetes Dashboard with admin privileges
Missing admission controllers (represented through ConfigMap)
Directly exposed services without proper ingress


Flag Locations:
FLAG{misconfigured_dashboard} in challenge-flags ConfigMap
FLAG{missing_admission_controls} in admission-control-config ConfigMap



10. Outdated and Vulnerable Kubernetes Components

Implementation Status: ✅

Details:
This is represented conceptually since we can't actually deploy outdated K8s components
Can be demonstrated by container images with known vulnerabilities


Flag Locations:
FLAG{outdated_components} in challenge-flags ConfigMap