# Example 4 - Docker Swarm

## Descripción
Stack con aplicación Node.js (Express) y Python (FastAPI) comunicándose entre sí.

## Archivos
- `docker-compose.yml` - Para desarrollo local con Docker Compose
- `stack.yml` - Para despliegue en producción con Docker Swarm

## ⚠️ IMPORTANTE: Preparación para Swarm

Docker Swarm **NO soporta** la directiva `build`. Debes construir las imágenes primero y, idealmente, subirlas a un registry.

### Opción 1: Usar Imágenes Locales (Desarrollo/Testing)
```bash
# Construir las imágenes
docker build -t nodejs-app:latest ./app_node
docker build -t python-app:latest ./app_python

# Modificar stack.yml para usar estas imágenes:
# Cambiar 'image: node:18-alpine' por 'image: nodejs-app:latest'
# Cambiar 'image: python:3.14-slim' por 'image: python-app:latest'
```

### Opción 2: Usar Docker Registry (Producción)
```bash
# 1. Construir y tagear imágenes
docker build -t usuario/nodejs-app:latest ./app_node
docker build -t usuario/python-app:latest ./app_python

# 2. Subir al registry (Docker Hub, AWS ECR, etc.)
docker push usuario/nodejs-app:latest
docker push usuario/python-app:latest

# 3. Actualizar stack.yml con las imágenes del registry
# image: usuario/nodejs-app:latest
# image: usuario/python-app:latest
```

## Uso con Docker Swarm

### 1. Inicializar Swarm (solo primera vez)
```bash
docker swarm init
```

### 2. Construir imágenes (Opción 1 - Local)
```bash
# Construir imagen Node.js
docker build -t nodejs-app:latest ./app_node

# Construir imagen Python
docker build -t python-app:latest ./app_python
```

### 3. Actualizar stack.yml
Edita `stack.yml` y cambia las líneas de `image`:
```yaml
# Para nodejs
image: nodejs-app:latest

# Para python_app
image: python-app:latest
```

Y elimina o comenta las secciones `command` y `volumes` para producción.

### 4. Desplegar el Stack
```bash
docker stack deploy -c stack.yml example4
```

### 5. Verificar el despliegue
```bash
# Ver servicios
docker stack services example4

# Ver tareas/contenedores
docker stack ps example4

# Ver logs de Node.js
docker service logs -f example4_nodejs

# Ver logs de Python
docker service logs -f example4_python_app
```

### 6. Probar la aplicación

#### Python FastAPI (puerto 8000)
```bash
# Página principal de Python
curl http://localhost:8000/

# Endpoint que llama a Node.js
curl http://localhost:8000/nodejs
```

#### Node.js Express (puerto 3000)
```bash
# Página principal de Node.js
curl http://localhost:3000/
```

### 7. Escalar servicios
```bash
# Escalar Node.js a 3 réplicas
docker service scale example4_nodejs=3

# Escalar Python a 4 réplicas
docker service scale example4_python_app=4

# Ver distribución de réplicas
docker service ps example4_nodejs
docker service ps example4_python_app
```

### 8. Actualizar servicios (Rolling Update)
```bash
# Reconstruir imagen con cambios
docker build -t python-app:v2 ./app_python

# Actualizar servicio (sin downtime)
docker service update --image python-app:v2 example4_python_app

# Ver progreso de la actualización
docker service ps example4_python_app
```

### 9. Remover el stack
```bash
docker stack rm example4
```

## Características del Stack

### Servicio Node.js
- **Puerto**: 3000
- **Réplicas**: 2 por defecto
- **Recursos**:
  - Límite: 0.5 CPU, 512MB RAM
  - Reserva: 0.25 CPU, 256MB RAM

### Servicio Python
- **Puerto**: 8000
- **Réplicas**: 2 por defecto
- **Recursos**:
  - Límite: 1.0 CPU, 512MB RAM
  - Reserva: 0.5 CPU, 256MB RAM
- **Dependencia**: Puede llamar al servicio `nodejs` internamente

### Red
- **Tipo**: Overlay network
- **Comunicación**: Los servicios se comunican usando sus nombres
- **Balanceo**: Automático entre réplicas

## Arquitectura

```
┌─────────────────────┐
│   Python FastAPI    │
│    (puerto 8000)    │
│   2+ réplicas       │
└──────────┬──────────┘
           │
           │ HTTP Request
           │ http://nodejs:3000
           │
           ▼
┌─────────────────────┐
│   Node.js Express   │
│    (puerto 3000)    │
│   2+ réplicas       │
└─────────────────────┘
```

## Stack.yml para Producción

Para producción, el `stack.yml` debería:

1. **Usar imágenes del registry** en lugar de montar código con volúmenes
2. **Eliminar `--reload`** de los comandos
3. **Usar secrets** para datos sensibles
4. **Configurar health checks**
5. **Definir estrategias de update más robustas**

Ejemplo optimizado:
```yaml
services:
  nodejs:
    image: usuario/nodejs-app:1.0.0
    ports:
      - "3000:3000"
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
        failure_action: rollback
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
    healthcheck:
      test: ["CMD", "wget", "--spider", "-q", "http://localhost:3000"]
      interval: 30s
      timeout: 10s
      retries: 3

  python_app:
    image: usuario/python-app:1.0.0
    ports:
      - "8000:8000"
    environment:
      - PYTHONUNBUFFERED=1
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
        failure_action: rollback
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
    healthcheck:
      test: ["CMD", "python", "-c", "import requests; requests.get('http://localhost:8000')"]
      interval: 30s
      timeout: 10s
      retries: 3

networks:
  default:
    driver: overlay
```

## Troubleshooting

### Servicios no se comunican
```bash
# Verificar que estén en la misma red
docker network inspect example4_default

# Probar resolución DNS desde un contenedor
docker exec $(docker ps -q -f name=example4_python) nslookup nodejs
```

### Ver logs detallados
```bash
# Logs de un contenedor específico
docker service logs --tail 100 example4_python_app

# Logs en tiempo real
docker service logs -f example4_nodejs
```

### Reiniciar un servicio
```bash
# Forzar recreación de contenedores
docker service update --force example4_nodejs
```

