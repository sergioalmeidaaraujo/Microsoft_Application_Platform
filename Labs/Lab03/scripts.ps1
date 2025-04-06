docker build -t blog-henrique-app:latest .

#detached mode". 
# Quando você usa essa opção, o container é executado em segundo plano (background) e o 
# terminal não fica "preso" ao processo do container. Ele retorna apenas o ID do container iniciado.


docker run -d -p 80:80 blog-henrique-app:latest

az login az l

# Create a resource group
az group create --name containerappslab03 --location eastus

# Create Container Registry
az acr create --resource-group containerappslab03 --name bloghenriqueacr --sku Basic

# Login to ACR
az acr login --name bloghenriqueacr

# Tag the image
docker tag blog-henrique-app:latest bloghenriqueacr.azurecr.io/blog-henrique-app:latest

# Push the image
docker push bloghenriqueacr.azurecr.io/blog-henrique-app:latest

#containerID = bloghenriqueacr.azurecr.io/blog-henrique-app:latest
#user =  bloghenriqueacr
#password = duzYmeARNVgFRMrndpcI91oXkqOJfC4YjrZYUDyAxQ+ACRCFxFzB

# Create Environment container app
az containerapp env create  --name blog-henrique-env --resource-group containerappslab03 --location eastus 

# Create Container App
az containerapp create --name blog-henrique-app --resource-group containerappslab03 --image bloghenriqueacr.azurecr.io/blog-henrique-app:latest --environment blog-henrique-env --target-port 80 --ingress external --registry-username bloghenriqueacr --registry-password duzYmeARNVgFRMrndpcI91oXkqOJfC4YjrZYUDyAxQ+ACRCFxFzB --registry-server bloghenriqueacr.azurecr.io


# az containerapp create \
# --name blog-henrique-app \
# --resource-group containerappslab03 \
# --location eastus \
# --image bloghenriqueacr.azurecr.io/blog-henrique-app:latest \
# --environment blog-henrique-env \
# --target-port 80 \ 
# --ingress external
# --registry-username bloghenriqueacr
# --registry-password duzYmeARNVgFRMrndpcI91oXkqOJfC4YjrZYUDyAxQ+ACRCFxFzB
# --registry-server bloghenriqueacr.azurecr.io



