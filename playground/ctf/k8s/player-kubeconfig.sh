#!/bin/bash

set -e

NAMESPACE="vulnerable-app"
SA_NAME="player"
SECRET_NAME="player-sa-token"
KUBECONFIG_OUTPUT="kubeconfig-player.yaml"

echo "[*] Ensuring ServiceAccount '$SA_NAME' exists in namespace '$NAMESPACE'..."
kubectl get sa "$SA_NAME" -n "$NAMESPACE" >/dev/null 2>&1 || kubectl create sa "$SA_NAME" -n "$NAMESPACE"

echo "[*] Checking if token Secret '$SECRET_NAME' exists..."
if ! kubectl get secret "$SECRET_NAME" -n "$NAMESPACE" >/dev/null 2>&1; then
  echo "[*] Creating token Secret '$SECRET_NAME' for ServiceAccount '$SA_NAME'..."
  cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Secret
metadata:
  name: $SECRET_NAME
  namespace: $NAMESPACE
  annotations:
    kubernetes.io/service-account.name: $SA_NAME
type: kubernetes.io/service-account-token
EOF
else
  echo "[*] Token Secret already exists."
fi

echo "[*] Waiting for token to be populated in the Secret..."
while true; do
  TOKEN=$(kubectl get secret "$SECRET_NAME" -n "$NAMESPACE" -o jsonpath="{.data.token}" 2>/dev/null || echo "")
  if [[ -n "$TOKEN" ]]; then
    break
  fi
  sleep 1
done

PLAYER_TOKEN=$(echo "$TOKEN" | base64 -d)

echo "[*] Getting cluster information..."
CLUSTER_NAME=$(kubectl config view -o jsonpath='{.contexts[?(@.name=="'$(kubectl config current-context)'")].context.cluster}')
CLUSTER_SERVER=$(kubectl config view -o jsonpath="{.clusters[?(@.name==\"$CLUSTER_NAME\")].cluster.server}")

echo "[*] Writing kubeconfig to $KUBECONFIG_OUTPUT"

cat <<EOF > "$KUBECONFIG_OUTPUT"
apiVersion: v1
kind: Config
clusters:
- cluster:
    server: $CLUSTER_SERVER
    insecure-skip-tls-verify: true
  name: $CLUSTER_NAME
contexts:
- context:
    cluster: $CLUSTER_NAME
    user: $SA_NAME
    namespace: $NAMESPACE
  name: player-context
current-context: player-context
users:
- name: $SA_NAME
  user:
    token: $PLAYER_TOKEN
EOF

echo
echo "[✔] Done!"
echo "👉 To test as the player:"
echo
echo "   export KUBECONFIG=\$PWD/$KUBECONFIG_OUTPUT"
echo "   kubectl get pods"
echo "   kubectl get configmaps"
echo "   kubectl describe pod <name>  # ❌ should be forbidden"
