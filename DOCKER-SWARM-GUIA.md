# Guía Completa de Docker Swarm

## 📋 Índice
1. [¿Qué es Docker Swarm?](#qué-es-docker-swarm)
2. [Conceptos Básicos](#conceptos-básicos)
3. [Comandos Principales](#comandos-principales)
4. [Ejemplos Prácticos](#ejemplos-prácticos)
5. [Diferencias con Docker Compose](#diferencias-con-docker-compose)
6. [Mejores Prácticas](#mejores-prácticas)

---

## ¿Qué es Docker Swarm?

Docker Swarm es la herramienta nativa de orquestación de contenedores de Docker que permite:

- ✅ **Clustering**: Agrupar múltiples hosts Docker en un cluster
- ✅ **Alta Disponibilidad**: Servicios siempre disponibles
- ✅ **Escalado Automático**: Crear múltiples réplicas de servicios
- ✅ **Balanceo de Carga**: Distribuir tráfico entre réplicas
- ✅ **Rolling Updates**: Actualizaciones sin downtime
- ✅ **Service Discovery**: Los servicios se encuentran por nombre
- ✅ **Secrets Management**: Gestión segura de contraseñas y claves

---

## Conceptos Básicos

### Componentes Principales

- **Service (Servicio)**: Definición de una aplicación a ejecutar
  
- **Task (Tarea)**: Un contenedor en ejecución de un servicio

- **Stack**: Grupo de servicios relacionados (conjunto de servicios que trabajan juntos)

- **Overlay Network**: Red virtual para comunicación entre servicios

- **Réplicas**: Múltiples instancias del mismo servicio para alta disponibilidad

---

## Comandos Principales

### 🚀 Inicialización del Swarm

```bash
# Inicializar Swarm en la máquina actual
docker swarm init

# Inicializar con IP específica
docker swarm init --advertise-addr 192.168.1.100

# Ver información del Swarm
docker info | grep Swarm
```


### 📦 Despliegue de Stacks

```bash
# Desplegar un stack
docker stack deploy -c stack.yml <NOMBRE-STACK>

# Desplegar con múltiples archivos
docker stack deploy -c base.yml -c prod.yml <NOMBRE-STACK>

# Listar stacks
docker stack ls

# Ver servicios de un stack
docker stack services <NOMBRE-STACK>

# Ver tareas de un stack
docker stack ps <NOMBRE-STACK>

# Ver tareas incluyendo las detenidas
docker stack ps --no-trunc <NOMBRE-STACK>

# Eliminar un stack
docker stack rm <NOMBRE-STACK>
```

### 🔧 Gestión de Servicios

```bash
# Crear servicio
docker service create --name web --replicas 3 nginx:latest

# Listar servicios
docker service ls

# Ver detalles de un servicio
docker service inspect <SERVICIO>
docker service inspect --pretty <SERVICIO>

# Ver tareas de un servicio
docker service ps <SERVICIO>

# Ver logs de un servicio
docker service logs <SERVICIO>
docker service logs -f <SERVICIO>                    # Seguir logs
docker service logs --tail 100 <SERVICIO>            # Últimas 100 líneas

# Escalar servicio
docker service scale <SERVICIO>=5
docker service scale web=3 api=5 db=1                # Múltiples servicios

# Actualizar servicio
docker service update --image nginx:alpine <SERVICIO>
docker service update --env-add VAR=value <SERVICIO>
docker service update --replicas 5 <SERVICIO>

# Rollback a versión anterior
docker service rollback <SERVICIO>

# Forzar actualización (recrear contenedores)
docker service update --force <SERVICIO>

# Eliminar servicio
docker service rm <SERVICIO>
```

### 🌐 Gestión de Redes

```bash
# Crear red overlay
docker network create --driver overlay <RED>

# Crear red overlay encriptada
docker network create --driver overlay --opt encrypted <RED>

# Crear red con subnet específica
docker network create --driver overlay \
  --subnet 10.0.0.0/24 \
  --gateway 10.0.0.1 \
  <RED>

# Listar redes
docker network ls
docker network ls --filter driver=overlay

# Ver detalles de una red
docker network inspect <RED>

# Conectar servicio a red
docker service update --network-add <RED> <SERVICIO>

# Desconectar servicio de red
docker service update --network-rm <RED> <SERVICIO>

# Eliminar red
docker network rm <RED>
```

### 🔒 Secrets (Gestión de Secretos)

```bash
# Crear secret desde archivo
docker secret create db_password ./password.txt

# Crear secret desde stdin
echo "mi-password" | docker secret create db_password -

# Listar secrets
docker secret ls

# Ver detalles de secret (NO muestra el contenido)
docker secret inspect db_password

# Usar secret en servicio
docker service create \
  --name db \
  --secret db_password \
  --env POSTGRES_PASSWORD_FILE=/run/secrets/db_password \
  postgres:latest

# Agregar secret a servicio existente
docker service update --secret-add db_password <SERVICIO>

# Remover secret de servicio
docker service update --secret-rm db_password <SERVICIO>

# Eliminar secret
docker secret rm db_password
```

### ⚙️ Configs (Configuraciones)

```bash
# Crear config desde archivo
docker config create nginx.conf ./nginx.conf

# Crear config desde stdin
cat config.json | docker config create app.json -

# Listar configs
docker config ls

# Ver detalles de config
docker config inspect nginx.conf

# Usar config en servicio
docker service create \
  --name web \
  --config source=nginx.conf,target=/etc/nginx/nginx.conf \
  nginx:latest

# Agregar config a servicio existente
docker service update --config-add nginx.conf <SERVICIO>

# Eliminar config
docker config rm nginx.conf
```

### 💾 Volúmenes

```bash
# Crear volumen
docker volume create datos

# Listar volúmenes
docker volume ls

# Ver detalles de volumen
docker volume inspect datos

# Usar volumen en servicio
docker service create \
  --name db \
  --mount type=volume,source=datos,target=/var/lib/mysql \
  mysql:latest

# Eliminar volumen
docker volume rm datos

# Limpiar volúmenes no usados
docker volume prune
```

### 📊 Monitoreo

```bash
# Ver uso de recursos de contenedores
docker stats

# Ver uso sin streaming
docker stats --no-stream

# Ver eventos del swarm en tiempo real
docker events
docker events --filter 'type=service'
docker events --filter 'service=web'

# Ver top de procesos en servicios
docker service ps <SERVICIO>
```

### 🧹 Limpieza

```bash
# Limpiar contenedores detenidos
docker container prune

# Limpiar imágenes no usadas
docker image prune
docker image prune -a                    # Todas las no usadas

# Limpiar redes no usadas
docker network prune

# Limpiar volúmenes no usados
docker volume prune

# Limpieza completa del sistema
docker system prune
docker system prune -a                   # Incluir todas las imágenes
docker system prune -a --volumes         # Incluir volúmenes
```

---

## Ejemplos Prácticos

### Ejemplo 1: Servicio Web Simple (Nginx)

**Archivo: example_1/stack.yml**
```yaml
version: '3.8'

services:
  web:
    image: nginx:latest
    ports:
      - "8080:80"
    deploy:
      replicas: 2
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
      resources:
        limits:
          cpus: '0.5'
          memory: 256M
        reservations:
          cpus: '0.25'
          memory: 128M
      update_config:
        parallelism: 1
        delay: 10s
        failure_action: rollback
```

**Despliegue:**
```bash
# 1. Inicializar swarm
docker swarm init

# 2. Desplegar stack
cd example_1
docker stack deploy -c stack.yml web-stack

# 3. Ver servicios
docker stack services web-stack

# 4. Escalar a 5 réplicas
docker service scale web-stack_web=5

# 5. Ver distribución
docker stack ps web-stack

# 6. Acceder
curl http://localhost:8080

# 7. Remover
docker stack rm web-stack
```

---

### Ejemplo 2: Múltiples Servicios Web

**Archivo: example_2/stack.yml**
```yaml
version: '3.8'

services:
  web:
    image: nginx:latest
    ports:
      - "8080:80"
    deploy:
      replicas: 2

  web2:
    image: nginx:latest
    ports:
      - "8081:80"
    deploy:
      replicas: 2
```

**Despliegue:**
```bash
cd example_2
docker stack deploy -c stack.yml multi-web

# Ver ambos servicios
docker stack services multi-web

# Escalar independientemente
docker service scale multi-web_web=4
docker service scale multi-web_web2=3

# Acceder
curl http://localhost:8080
curl http://localhost:8081
```

---

### Ejemplo 3: Stack con Base de Datos (PostgreSQL + pgAdmin)

**Archivo: example_3/stack.yml**
```yaml
version: '3.8'

services:
  postgres_db:
    image: postgres:latest
    ports:
      - "5432:5432"
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data
    deploy:
      replicas: 1

  pgadmin:
    image: dpage/pgadmin4:latest
    ports:
      - "8081:80"
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@example.com
      PGADMIN_DEFAULT_PASSWORD: password
    volumes:
      - pgadmin_data:/var/lib/pgadmin
    deploy:
      replicas: 1

volumes:
  postgres_data:
  pgadmin_data:
```

**Despliegue:**
```bash
cd example_3
docker stack deploy -c stack.yml db-stack

# Ver servicios
docker stack services db-stack

# Ver logs de PostgreSQL
docker service logs db-stack_postgres_db

# Acceder a pgAdmin
# http://localhost:8081
# Email: admin@example.com
# Password: password

# Conectar a PostgreSQL desde pgAdmin:
# Host: postgres_db
# Port: 5432
# User: postgres
# Password: postgres
```

---

### Ejemplo 4: Microservicios (Node.js + Python)

**Archivo: example_4/stack.yml** (Versión simplificada)
```yaml
version: '3.8'

services:
  nodejs:
    image: nodejs-app:latest  # Construir primero
    ports:
      - "3000:3000"
    deploy:
      replicas: 2

  python_app:
    image: python-app:latest  # Construir primero
    ports:
      - "8000:8000"
    deploy:
      replicas: 2

networks:
  default:
    driver: overlay
```

**Preparación y Despliegue:**
```bash
cd example_4

# 1. Construir imágenes
docker build -t nodejs-app:latest ./app_node
docker build -t python-app:latest ./app_python

# 2. Desplegar stack
docker stack deploy -c stack.yml app-stack

# 3. Ver servicios
docker stack services app-stack

# 4. Probar comunicación
curl http://localhost:8000/          # Python FastAPI
curl http://localhost:8000/nodejs    # Python llama a Node.js
curl http://localhost:3000/          # Node.js Express

# 5. Escalar servicios
docker service scale app-stack_nodejs=3
docker service scale app-stack_python_app=4

# 6. Ver logs
docker service logs -f app-stack_python_app
```

---

## Diferencias con Docker Compose

| Característica | Docker Compose | Docker Swarm |
|----------------|----------------|--------------|
| **Uso** | Desarrollo local | Producción/Cluster |
| **Comando** | `docker-compose up` | `docker stack deploy` |
| **Build** | ✅ Soporta `build` | ❌ Solo imágenes |
| **Múltiples Hosts** | ❌ Solo un host | ✅ Cluster de hosts |
| **Réplicas** | Manual (scale) | Automático |
| **Alta Disponibilidad** | ❌ No | ✅ Sí |
| **Rolling Updates** | ❌ No | ✅ Sí |
| **Rollback** | ❌ No | ✅ Sí |
| **Load Balancing** | Básico | Avanzado (automático) |
| **Service Discovery** | Limitado | Completo (DNS) |
| **Secrets** | ❌ Solo env vars | ✅ Gestión nativa |
| **Health Checks** | Básico | Avanzado |
| **Placement** | ❌ No | ✅ Constraints |
| **Volúmenes** | Local | Distribuidos |

### Conversión de docker-compose.yml a stack.yml

**Docker Compose:**
```yaml
services:
  web:
    build: ./web
    ports:
      - "8080:80"
```

**Docker Swarm:**
```yaml
services:
  web:
    image: miusuario/web:latest  # Debe ser imagen, no build
    ports:
      - "8080:80"
    deploy:
      replicas: 3
      restart_policy:
        condition: on-failure
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
```

---

## Mejores Prácticas

### 🎯 Configuración Inicial

1. **Inicializar Swarm en una sola máquina** (para desarrollo/testing)
   ```bash
   docker swarm init
   ```

2. **Verificar estado del Swarm**
   ```bash
   docker info | grep Swarm
   docker service ls
   ```

### 🔒 Seguridad

1. **Usar Secrets para Datos Sensibles**
   ```bash
   # ❌ MAL - Variable de entorno
   docker service create --env DB_PASS=123456 mysql
   
   # ✅ BIEN - Secret
   echo "123456" | docker secret create db_pass -
   docker service create \
     --secret db_pass \
     --env MYSQL_ROOT_PASSWORD_FILE=/run/secrets/db_pass \
     mysql
   ```

2. **Redes Encriptadas**
   ```bash
   docker network create --driver overlay --opt encrypted secure-net
   ```


### 🚀 Despliegue

1. **Health Checks**
   ```yaml
   services:
     web:
       image: nginx
       healthcheck:
         test: ["CMD", "curl", "-f", "http://localhost"]
         interval: 30s
         timeout: 10s
         retries: 3
         start_period: 40s
   ```

2. **Rolling Updates**
   ```yaml
   services:
     web:
       deploy:
         update_config:
           parallelism: 2          # Actualizar 2 a la vez
           delay: 10s              # Esperar 10s entre grupos
           failure_action: rollback # Rollback si falla
           monitor: 30s            # Monitorear 30s
           max_failure_ratio: 0.3  # Máximo 30% fallos
   ```

3. **Recursos Definidos**
   ```yaml
   services:
     web:
       deploy:
         resources:
           limits:
             cpus: '1.0'
             memory: 512M
           reservations:
             cpus: '0.5'
             memory: 256M
   ```


### 💾 Almacenamiento

1. **Volúmenes Persistentes**: Usar drivers distribuidos en producción
   - NFS
   - GlusterFS
   - Ceph
   - AWS EFS
   - Azure Files

2. **Backups Regulares**
   ```bash
   # Backup de volumen
   docker run --rm \
     -v mydata:/data \
     -v $(pwd):/backup \
     alpine tar czf /backup/backup.tar.gz /data
   ```

### 📊 Monitoreo

1. **Implementar Stack de Monitoreo**
   - Prometheus (métricas)
   - Grafana (visualización)
   - cAdvisor (métricas de contenedores)

2. **Logs Centralizados**
   - ELK Stack (Elasticsearch, Logstash, Kibana)
   - Fluentd
   - Loki

---

## 🛠️ Troubleshooting Común

### Problema: Servicio no inicia

```bash
# 1. Ver tareas fallidas
docker service ps <SERVICIO> --no-trunc

# 2. Ver logs
docker service logs <SERVICIO>

# 3. Inspeccionar servicio
docker service inspect <SERVICIO>

# 4. Ver eventos
docker events --filter 'type=service'
```

### Problema: Servicios no se comunican

```bash
# 1. Verificar que estén en la misma red
docker network inspect <RED>

# 2. Probar DNS interno
docker service exec <SERVICIO> nslookup <OTRO-SERVICIO>

# 3. Verificar firewall y seguridad de red
```

### Problema: Actualización falló

```bash
# Hacer rollback
docker service rollback <SERVICIO>

# Ver historial de cambios
docker service inspect <SERVICIO> --pretty

# Verificar imágenes disponibles
docker service ps <SERVICIO>
```

---

## 📚 Comandos Rápidos de Referencia

```bash
# === INICIALIZACIÓN ===
docker swarm init                          # Iniciar swarm

# === STACKS ===
docker stack deploy -c stack.yml <NAME>    # Desplegar stack
docker stack ls                            # Listar stacks
docker stack services <NAME>               # Servicios del stack
docker stack ps <NAME>                     # Tareas del stack
docker stack rm <NAME>                     # Eliminar stack

# === SERVICIOS ===
docker service ls                          # Listar servicios
docker service ps <SERVICE>                # Tareas del servicio
docker service logs -f <SERVICE>           # Ver logs
docker service scale <SERVICE>=5           # Escalar servicio
docker service update --image <IMG> <SVC>  # Actualizar imagen
docker service rollback <SERVICE>          # Rollback

# === MONITOREO ===
docker stats                               # Uso de recursos
docker events                              # Eventos en tiempo real
docker system df                           # Uso de disco

# === LIMPIEZA ===
docker system prune -a                     # Limpiar todo
docker volume prune                        # Limpiar volúmenes
```

---

## 🎓 Recursos Adicionales

- **Documentación Oficial**: https://docs.docker.com/engine/swarm/
- **Docker Swarm Tutorial**: https://docs.docker.com/engine/swarm/swarm-tutorial/
- **Best Practices**: https://docs.docker.com/develop/dev-best-practices/

---

## ✅ Checklist para Producción

- [ ] Inicializar Docker Swarm
- [ ] Configurar health checks en todos los servicios
- [ ] Usar secrets para datos sensibles (contraseñas, tokens, etc.)
- [ ] Definir recursos (limits y reservations) para cada servicio
- [ ] Configurar rolling updates con rollback automático
- [ ] Implementar monitoreo (Prometheus + Grafana)
- [ ] Configurar logs centralizados
- [ ] Usar volúmenes persistentes para datos importantes
- [ ] Configurar backups automáticos de volúmenes
- [ ] Documentar arquitectura y procedimientos
- [ ] Probar estrategias de actualización y rollback
- [ ] Configurar alertas para servicios críticos
- [ ] Implementar CI/CD pipeline
- [ ] Definir políticas de restart para servicios

