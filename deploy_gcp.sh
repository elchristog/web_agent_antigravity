#!/bin/bash
export PATH="/home/elchristog/agente_antigravity/google-cloud-sdk/bin:/home/elchristog/agente_antigravity/node_env/bin:$PATH"

echo "=== Compilando Proyecto Astro ==="
cd /home/elchristog/agente_antigravity/template_alfred/alfred-main
npm run build

echo "=== Sincronizando a Google Cloud Storage (gs://enfermerausa.com y gs://www.enfermerausa.com) ==="
gcloud storage rsync -r /home/elchristog/agente_antigravity/template_alfred/alfred-main/dist gs://enfermerausa.com --delete-unmatched-destination-objects
gcloud storage rsync -r /home/elchristog/agente_antigravity/template_alfred/alfred-main/dist gs://www.enfermerausa.com --delete-unmatched-destination-objects

echo "=== Configurando Permisos Públicos y Página de Inicio ==="
gcloud storage buckets add-iam-policy-binding gs://enfermerausa.com --member=allUsers --role=roles/storage.objectViewer
gcloud storage buckets update gs://enfermerausa.com --web-main-page-suffix=index.html --web-error-page=404.html
gcloud storage buckets add-iam-policy-binding gs://www.enfermerausa.com --member=allUsers --role=roles/storage.objectViewer
gcloud storage buckets update gs://www.enfermerausa.com --web-main-page-suffix=index.html --web-error-page=404.html

echo "=== Despliegue Completado con Éxito ==="
