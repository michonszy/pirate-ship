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