# Comandos de Docker Swarm

## Conceptos Básicos

Docker Swarm es la herramienta nativa de orquestación de contenedores de Docker. Permite:
- Clustering de múltiples hosts Docker
- Balanceo de carga automático
- Alta disponibilidad
- Rolling updates
- Escalado de servicios

---

## Inicialización del Swarm

### Crear un Swarm
```bash
# Inicializar un nuevo swarm (el nodo actual se convierte en manager)
docker swarm init

# Inicializar con una IP específica (útil si tienes múltiples interfaces)
docker swarm init --advertise-addr <IP>

# Inicializar especificando puerto
docker swarm init --advertise-addr <IP>:2377

# Ver información del swarm
docker info
```

### Unir Nodos al Swarm
```bash
# Obtener token para unir workers
docker swarm join-token worker

# Obtener token para unir managers
docker swarm join-token manager

# Rotar token de workers
docker swarm join-token --rotate worker

# Unir un nodo al swarm (ejecutar en el nodo que quieres unir)
docker swarm join --token <TOKEN> <MANAGER-IP>:2377
```

### Salir del Swarm
```bash
# Salir del swarm (ejecutar en el nodo worker)
docker swarm leave

# Forzar salida del swarm
docker swarm leave --force

# Remover un nodo desde el manager
docker node rm <NODE-ID>

# Forzar remoción de un nodo
docker node rm --force <NODE-ID>
```

---

## Gestión de Nodos

### Listar y Ver Nodos
```bash
# Listar todos los nodos del swarm
docker node ls

# Ver información detallada de un nodo
docker node inspect <NODE-ID>

# Ver información en formato JSON
docker node inspect --pretty <NODE-ID>

# Ver tareas ejecutándose en un nodo
docker node ps <NODE-ID>

# Ver todas las tareas de todos los nodos
docker node ps
```

### Promover y Degradar Nodos
```bash
# Promover un worker a manager
docker node promote <NODE-ID>

# Degradar un manager a worker
docker node demote <NODE-ID>
```

### Disponibilidad de Nodos
```bash
# Hacer que un nodo esté activo (puede recibir tareas)
docker node update --availability active <NODE-ID>

# Pausar un nodo (no recibe nuevas tareas pero mantiene las existentes)
docker node update --availability pause <NODE-ID>

# Drenar un nodo (mover todas las tareas a otros nodos)
docker node update --availability drain <NODE-ID>
```

### Etiquetas de Nodos
```bash
# Agregar etiqueta a un nodo
docker node update --label-add <key>=<value> <NODE-ID>

# Ejemplo: marcar nodo como producción
docker node update --label-add environment=production <NODE-ID>

# Remover etiqueta de un nodo
docker node update --label-rm <key> <NODE-ID>
```

---

## Despliegue de Stacks

### Desplegar Stacks
```bash
# Desplegar un stack desde archivo
docker stack deploy -c stack.yml <STACK-NAME>

# Desplegar usando múltiples archivos
docker stack deploy -c docker-compose.yml -c docker-compose.prod.yml <STACK-NAME>

# Desplegar con variables de entorno
docker stack deploy -c stack.yml --with-registry-auth <STACK-NAME>

# Resolver imagenes antes de desplegar
docker stack deploy -c stack.yml --resolve-image always <STACK-NAME>
```

### Listar y Ver Stacks
```bash
# Listar todos los stacks
docker stack ls

# Ver servicios de un stack
docker stack services <STACK-NAME>

# Ver tareas de un stack
docker stack ps <STACK-NAME>

# Ver tareas incluyendo las detenidas
docker stack ps --no-trunc <STACK-NAME>

# Filtrar tareas por estado
docker stack ps --filter "desired-state=running" <STACK-NAME>
```

### Remover Stacks
```bash
# Eliminar un stack completo
docker stack rm <STACK-NAME>

# Eliminar múltiples stacks
docker stack rm stack1 stack2 stack3
```

---

## Gestión de Servicios

### Crear Servicios
```bash
# Crear un servicio simple
docker service create --name <SERVICE-NAME> <IMAGE>

# Crear servicio con réplicas
docker service create --name web --replicas 3 nginx:latest

# Crear servicio con puerto publicado
docker service create --name web --publish 8080:80 nginx:latest

# Crear con variables de entorno
docker service create --name web --env VAR=value nginx:latest

# Crear con restricciones de placement
docker service create --name web \
  --constraint 'node.role==worker' \
  nginx:latest

# Crear con límites de recursos
docker service create --name web \
  --limit-cpu 0.5 \
  --limit-memory 512M \
  --reserve-cpu 0.25 \
  --reserve-memory 256M \
  nginx:latest

# Crear servicio global (una réplica en cada nodo)
docker service create --name monitor --mode global nginx:latest

# Crear con red específica
docker service create --name web --network my-network nginx:latest
```

### Listar y Ver Servicios
```bash
# Listar todos los servicios
docker service ls

# Ver detalles de un servicio
docker service inspect <SERVICE-NAME>

# Ver detalles en formato legible
docker service inspect --pretty <SERVICE-NAME>

# Ver tareas/contenedores de un servicio
docker service ps <SERVICE-NAME>

# Ver logs de un servicio
docker service logs <SERVICE-NAME>

# Ver logs en tiempo real
docker service logs -f <SERVICE-NAME>

# Ver últimas N líneas
docker service logs --tail 100 <SERVICE-NAME>
```

### Actualizar Servicios
```bash
# Actualizar imagen de un servicio
docker service update --image nginx:alpine <SERVICE-NAME>

# Escalar un servicio
docker service scale <SERVICE-NAME>=5

# Escalar múltiples servicios
docker service scale web=3 api=5 db=1

# Agregar puerto publicado
docker service update --publish-add 8080:80 <SERVICE-NAME>

# Remover puerto publicado
docker service update --publish-rm 8080 <SERVICE-NAME>

# Actualizar variables de entorno
docker service update --env-add NEW_VAR=value <SERVICE-NAME>
docker service update --env-rm OLD_VAR <SERVICE-NAME>

# Actualizar restricciones
docker service update --constraint-add 'node.labels.disk==ssd' <SERVICE-NAME>

# Actualizar con rollback automático en caso de fallo
docker service update \
  --update-failure-action rollback \
  --update-max-failure-ratio 0.3 \
  --image nginx:alpine \
  <SERVICE-NAME>

# Configurar rolling update
docker service update \
  --update-parallelism 2 \
  --update-delay 10s \
  --image nginx:alpine \
  <SERVICE-NAME>

# Forzar actualización (recrear contenedores aunque la configuración no cambió)
docker service update --force <SERVICE-NAME>
```

### Rollback de Servicios
```bash
# Hacer rollback a la configuración anterior
docker service rollback <SERVICE-NAME>

# Rollback automático configurado en update
docker service update \
  --rollback-parallelism 2 \
  --rollback-monitor 20s \
  --rollback-max-failure-ratio 0.3 \
  <SERVICE-NAME>
```

### Remover Servicios
```bash
# Eliminar un servicio
docker service rm <SERVICE-NAME>

# Eliminar múltiples servicios
docker service rm service1 service2 service3
```

---

## Gestión de Redes

### Crear Redes
```bash
# Crear red overlay (para comunicación entre servicios)
docker network create --driver overlay <NETWORK-NAME>

# Crear red con subnet específica
docker network create --driver overlay \
  --subnet 10.0.0.0/24 \
  <NETWORK-NAME>

# Crear red encriptada
docker network create --driver overlay \
  --opt encrypted \
  <NETWORK-NAME>

# Crear red attachable (permite contenedores standalone)
docker network create --driver overlay \
  --attachable \
  <NETWORK-NAME>
```

### Listar y Ver Redes
```bash
# Listar todas las redes
docker network ls

# Ver detalles de una red
docker network inspect <NETWORK-NAME>

# Filtrar redes por driver
docker network ls --filter driver=overlay
```

### Conectar y Desconectar Servicios
```bash
# Conectar un servicio a una red
docker service update --network-add <NETWORK-NAME> <SERVICE-NAME>

# Desconectar un servicio de una red
docker service update --network-rm <NETWORK-NAME> <SERVICE-NAME>
```

### Remover Redes
```bash
# Eliminar una red
docker network rm <NETWORK-NAME>

# Eliminar redes no utilizadas
docker network prune
```

---

## Secrets (Gestión de Secretos)

### Crear Secrets
```bash
# Crear secret desde un archivo
docker secret create <SECRET-NAME> <FILE-PATH>

# Crear secret desde stdin
echo "mi-password-secreto" | docker secret create <SECRET-NAME> -

# Crear secret desde stdin con heredoc
docker secret create mysql_password <<EOF
mi-password-muy-secreto
EOF

# Etiquetar un secret
docker secret create --label env=prod <SECRET-NAME> <FILE-PATH>
```

### Listar y Ver Secrets
```bash
# Listar todos los secrets
docker secret ls

# Ver detalles de un secret (no muestra el contenido)
docker secret inspect <SECRET-NAME>
```

### Usar Secrets en Servicios
```bash
# Crear servicio con secret
docker service create --name mysql \
  --secret mysql_password \
  --env MYSQL_ROOT_PASSWORD_FILE=/run/secrets/mysql_password \
  mysql:latest

# Agregar secret a servicio existente
docker service update --secret-add mysql_password <SERVICE-NAME>

# Remover secret de servicio
docker service update --secret-rm mysql_password <SERVICE-NAME>

# Usar secret con nombre personalizado dentro del contenedor
docker service create --name app \
  --secret source=mysql_password,target=db_pass \
  myapp:latest
```

### Remover Secrets
```bash
# Eliminar un secret
docker secret rm <SECRET-NAME>

# Eliminar múltiples secrets
docker secret rm secret1 secret2 secret3
```

---

## Configs (Configuraciones)

### Crear Configs
```bash
# Crear config desde archivo
docker config create <CONFIG-NAME> <FILE-PATH>

# Crear config desde stdin
echo "configuracion" | docker config create <CONFIG-NAME> -

# Etiquetar una config
docker config create --label env=prod <CONFIG-NAME> <FILE-PATH>
```

### Listar y Ver Configs
```bash
# Listar todas las configs
docker config ls

# Ver detalles de una config
docker config inspect <CONFIG-NAME>
```

### Usar Configs en Servicios
```bash
# Crear servicio con config
docker service create --name web \
  --config nginx.conf \
  nginx:latest

# Agregar config a servicio existente
docker service update --config-add nginx.conf <SERVICE-NAME>

# Remover config de servicio
docker service update --config-rm nginx.conf <SERVICE-NAME>

# Usar config con target personalizado
docker service create --name web \
  --config source=nginx.conf,target=/etc/nginx/nginx.conf \
  nginx:latest
```

### Remover Configs
```bash
# Eliminar una config
docker config rm <CONFIG-NAME>

# Eliminar múltiples configs
docker config rm config1 config2 config3
```

---

## Volúmenes en Swarm

### Crear Volúmenes
```bash
# Crear volumen
docker volume create <VOLUME-NAME>

# Crear volumen con driver específico
docker volume create --driver local <VOLUME-NAME>

# Crear volumen con opciones
docker volume create \
  --driver local \
  --opt type=nfs \
  --opt o=addr=192.168.1.1,rw \
  --opt device=:/path/to/dir \
  <VOLUME-NAME>
```

### Usar Volúmenes en Servicios
```bash
# Crear servicio con volumen
docker service create --name db \
  --mount type=volume,source=db-data,target=/var/lib/mysql \
  mysql:latest

# Usar volumen temporal (tmpfs)
docker service create --name web \
  --mount type=tmpfs,destination=/tmp \
  nginx:latest

# Usar bind mount (no recomendado en producción)
docker service create --name web \
  --mount type=bind,source=/host/path,target=/container/path \
  nginx:latest
```

---

## Monitoreo y Troubleshooting

### Ver Estado del Swarm
```bash
# Ver información general del swarm
docker info

# Ver nodos y su estado
docker node ls

# Ver servicios y réplicas
docker service ls

# Ver detalles de todas las tareas
docker stack ps <STACK-NAME>
```

### Logs
```bash
# Ver logs de un servicio
docker service logs <SERVICE-NAME>

# Ver logs en tiempo real
docker service logs -f <SERVICE-NAME>

# Ver logs con timestamps
docker service logs -t <SERVICE-NAME>

# Ver logs de una tarea específica
docker service logs <TASK-ID>

# Ver logs de todos los servicios de un stack
docker stack ps <STACK-NAME> --no-trunc
```

### Inspeccionar Recursos
```bash
# Inspeccionar un nodo
docker node inspect <NODE-ID>

# Inspeccionar un servicio
docker service inspect <SERVICE-NAME>

# Inspeccionar una tarea
docker inspect <TASK-ID>

# Inspeccionar una red
docker network inspect <NETWORK-NAME>
```

### Eventos en Tiempo Real
```bash
# Ver eventos del swarm en tiempo real
docker events

# Filtrar eventos por tipo
docker events --filter 'type=service'
docker events --filter 'type=node'

# Filtrar eventos por servicio
docker events --filter 'service=web'
```

---

## Limpieza y Mantenimiento

### Limpiar Recursos
```bash
# Eliminar servicios no utilizados
docker service rm $(docker service ls -q)

# Eliminar redes no utilizadas
docker network prune

# Eliminar volúmenes no utilizados
docker volume prune

# Limpieza completa del sistema
docker system prune

# Limpieza completa incluyendo volúmenes
docker system prune --volumes

# Limpieza incluyendo imágenes no usadas
docker system prune -a
```

### Actualizar el Swarm
```bash
# Actualizar configuración del swarm
docker swarm update --task-history-limit 10

# Actualizar certificados del swarm
docker swarm ca --rotate
```

---

## Ejemplos Prácticos Completos

### Ejemplo 1: Stack Web Simple
```bash
# Desplegar un stack de Nginx
docker stack deploy -c stack.yml web-stack

# Escalar el servicio
docker service scale web-stack_web=5

# Ver logs
docker service logs -f web-stack_web

# Actualizar imagen
docker service update --image nginx:alpine web-stack_web

# Remover stack
docker stack rm web-stack
```

### Ejemplo 2: Stack con Base de Datos
```bash
# Crear secrets para la base de datos
echo "mi-password" | docker secret create db_password -
echo "mi-usuario" | docker secret create db_user -

# Desplegar stack
docker stack deploy -c stack.yml db-stack

# Ver estado de servicios
docker stack services db-stack

# Ver logs de PostgreSQL
docker service logs db-stack_postgres_db

# Backup de volumen (en nodo manager)
docker run --rm -v db-stack_postgres_data:/data -v $(pwd):/backup \
  alpine tar czf /backup/db-backup.tar.gz /data
```

### Ejemplo 3: Rolling Update sin Downtime
```bash
# Crear servicio con configuración de update
docker service create \
  --name api \
  --replicas 5 \
  --update-parallelism 2 \
  --update-delay 10s \
  --update-failure-action rollback \
  --rollback-parallelism 2 \
  myapp:v1

# Actualizar a nueva versión
docker service update --image myapp:v2 api

# Si falla, hacer rollback manual
docker service rollback api
```

### Ejemplo 4: Servicio Global (Agente en Cada Nodo)
```bash
# Crear servicio de monitoreo en cada nodo
docker service create \
  --name node-exporter \
  --mode global \
  --mount type=bind,source=/proc,target=/host/proc,readonly \
  --mount type=bind,source=/sys,target=/host/sys,readonly \
  prom/node-exporter
```

### Ejemplo 5: Drenar Nodo para Mantenimiento
```bash
# 1. Drenar el nodo (mover todas las tareas)
docker node update --availability drain node-1

# 2. Realizar mantenimiento en node-1

# 3. Reactivar el nodo
docker node update --availability active node-1

# 4. Re-balancear las tareas
docker service update --force <SERVICE-NAME>
```

---

## Diferencias entre Docker Compose y Docker Swarm

| Característica | Docker Compose | Docker Swarm |
|----------------|----------------|--------------|
| **Comando** | `docker-compose up` | `docker stack deploy` |
| **Build** | Soporta `build` | No soporta `build` (usar imágenes) |
| **Múltiples hosts** | No | Sí |
| **Escalado** | Manual | Automático |
| **High Availability** | No | Sí |
| **Rolling Updates** | No | Sí |
| **Load Balancing** | Básico | Avanzado |
| **Secrets** | No (usa env vars) | Sí |
| **Health Checks** | Básico | Avanzado |

---

## Mejores Prácticas

1. **Managers**: Usar 3, 5 o 7 managers (siempre número impar para quorum)
2. **Labels**: Usar labels en nodos para placement constraints
3. **Secrets**: Nunca usar variables de entorno para datos sensibles
4. **Updates**: Siempre configurar rollback automático
5. **Resources**: Definir límites y reservas de CPU/memoria
6. **Health Checks**: Implementar health checks en los servicios
7. **Networks**: Usar redes overlay encriptadas para datos sensibles
8. **Volúmenes**: Usar drivers de volumen distribuidos (NFS, GlusterFS) en producción
9. **Logs**: Implementar solución centralizada de logs
10. **Monitoreo**: Usar Prometheus + Grafana para monitoreo

---

## Comandos de Diagnóstico

```bash
# Ver versión de Docker y Swarm
docker version
docker info | grep Swarm

# Ver capacidad del cluster
docker node ls --format "{{.Hostname}}: {{.Status}} - {{.Availability}}"

# Ver distribución de tareas por nodo
for node in $(docker node ls -q); do
  echo "Nodo: $(docker node inspect $node --format '{{.Description.Hostname}}')"
  docker node ps $node --format "  {{.Name}}"
done

# Ver uso de recursos
docker stats --no-stream

# Ver errores en servicios
docker service ps <SERVICE-NAME> --filter "desired-state=shutdown"
```

---

## Troubleshooting Común

### Servicio no inicia
```bash
# Ver logs de tareas fallidas
docker service ps <SERVICE-NAME> --no-trunc

# Ver logs específicos
docker service logs <SERVICE-NAME>

# Inspeccionar servicio
docker service inspect <SERVICE-NAME>
```

### Nodo no se une al swarm
```bash
# Verificar conectividad de puertos (2377, 7946, 4789)
# En el manager
docker swarm join-token worker

# En el worker, verificar conectividad
telnet <MANAGER-IP> 2377
```

### Servicios no se comunican
```bash
# Verificar que estén en la misma red overlay
docker network inspect <NETWORK-NAME>

# Verificar DNS interno
docker service exec <SERVICE-NAME> nslookup <OTHER-SERVICE-NAME>
```

---

## Comandos Útiles Rápidos

```bash
# Ver todo el estado del swarm de un vistazo
docker node ls && docker service ls && docker stack ls

# Escalar todos los servicios de un stack
for service in $(docker stack services -q <STACK-NAME>); do
  docker service scale $service=3
done

# Obtener IPs de todas las tareas de un servicio
docker service ps <SERVICE-NAME> -q | \
  xargs docker inspect --format '{{.NetworksAttachments}}'

# Limpiar servicios fallidos
docker service ls --filter "replicas=0" -q | xargs docker service rm
```

