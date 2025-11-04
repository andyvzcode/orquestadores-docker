# Comandos de Docker Compose

## Comandos Básicos

### Iniciar servicios
```bash
# Iniciar todos los servicios definidos en docker-compose.yml
docker-compose up

# Iniciar servicios en segundo plano (detached mode)
docker-compose up -d

# Iniciar un servicio específico
docker-compose up <nombre_servicio>

# Forzar recreación de contenedores
docker-compose up --force-recreate

# Construir imágenes antes de iniciar
docker-compose up --build
```

### Detener servicios
```bash
# Detener servicios en ejecución
docker-compose stop

# Detener un servicio específico
docker-compose stop <nombre_servicio>

# Detener y eliminar contenedores, redes, volúmenes e imágenes
docker-compose down

# Eliminar también los volúmenes
docker-compose down -v

# Eliminar también las imágenes
docker-compose down --rmi all
```

## Gestión de Contenedores

### Ver estado
```bash
# Listar contenedores en ejecución
docker-compose ps

# Listar todos los contenedores (incluso detenidos)
docker-compose ps -a

# Ver logs de todos los servicios
docker-compose logs

# Ver logs de un servicio específico
docker-compose logs <nombre_servicio>

# Ver logs en tiempo real (follow)
docker-compose logs -f

# Ver últimas N líneas de logs
docker-compose logs --tail=100
```

### Ejecutar comandos
```bash
# Ejecutar un comando en un servicio en ejecución
docker-compose exec <nombre_servicio> <comando>

# Ejemplo: abrir bash en un contenedor
docker-compose exec <nombre_servicio> bash

# Ejecutar comando en un nuevo contenedor
docker-compose run <nombre_servicio> <comando>

# Ejecutar sin crear dependencias
docker-compose run --no-deps <nombre_servicio> <comando>

# Ejecutar sin publicar puertos
docker-compose run --no-ports <nombre_servicio> <comando>
```

## Construcción y Imágenes

### Build
```bash
# Construir o reconstruir servicios
docker-compose build

# Construir un servicio específico
docker-compose build <nombre_servicio>

# Construir sin usar caché
docker-compose build --no-cache

# Construir con parámetros de build
docker-compose build --build-arg <key>=<value>

# Forzar pull de imágenes base
docker-compose build --pull
```

### Imágenes
```bash
# Listar imágenes utilizadas por los servicios
docker-compose images

# Descargar imágenes sin iniciar contenedores
docker-compose pull

# Descargar imagen de un servicio específico
docker-compose pull <nombre_servicio>

# Push de imágenes a un registry
docker-compose push
```

## Control de Servicios

### Pausar y reanudar
```bash
# Pausar servicios en ejecución
docker-compose pause

# Pausar un servicio específico
docker-compose pause <nombre_servicio>

# Reanudar servicios pausados
docker-compose unpause

# Reanudar un servicio específico
docker-compose unpause <nombre_servicio>
```

### Reiniciar
```bash
# Reiniciar servicios
docker-compose restart

# Reiniciar un servicio específico
docker-compose restart <nombre_servicio>

# Reiniciar con timeout personalizado (segundos)
docker-compose restart -t 30 <nombre_servicio>
```

### Escalar
```bash
# Escalar servicios (crear múltiples instancias)
docker-compose up -d --scale <nombre_servicio>=3

# Escalar múltiples servicios
docker-compose up -d --scale servicio1=2 --scale servicio2=3
```

## Configuración y Validación

### Validar y ver configuración
```bash
# Validar y ver el archivo compose
docker-compose config

# Ver configuración de un servicio específico
docker-compose config --services

# Ver volúmenes definidos
docker-compose config --volumes

# Resolver rutas de volumen
docker-compose config --resolve-image-digests

# Validar sin ejecutar
docker-compose config --quiet
```

### Archivos de configuración
```bash
# Usar un archivo compose específico
docker-compose -f docker-compose.yml up

# Usar múltiples archivos (se fusionan)
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up

# Especificar nombre del proyecto
docker-compose -p mi_proyecto up
```

## Redes

```bash
# Listar redes
docker network ls

# Crear redes definidas
docker-compose up --no-start

# Inspeccionar una red
docker network inspect <nombre_red>
```

## Volúmenes

```bash
# Listar volúmenes
docker volume ls

# Eliminar volúmenes huérfanos
docker-compose down --volumes --remove-orphans

# Inspeccionar un volumen
docker volume inspect <nombre_volumen>
```

## Eventos y Monitoreo

```bash
# Ver eventos en tiempo real
docker-compose events

# Ver eventos de un servicio específico
docker-compose events <nombre_servicio>

# Ver top de procesos en contenedores
docker-compose top

# Ver uso de recursos
docker stats $(docker-compose ps -q)
```

## Comandos de Limpieza

```bash
# Eliminar contenedores detenidos
docker-compose rm

# Forzar eliminación sin confirmación
docker-compose rm -f

# Eliminar también volúmenes anónimos
docker-compose rm -v

# Eliminar contenedores huérfanos
docker-compose down --remove-orphans
```

## Variables de Entorno

```bash
# Usar archivo .env personalizado
docker-compose --env-file .env.prod up

# Ver variables de entorno de un servicio
docker-compose config
```

## Comandos de Información

```bash
# Ver versión de docker-compose
docker-compose version

# Ver ayuda general
docker-compose --help

# Ver ayuda de un comando específico
docker-compose up --help

# Ver información de configuración del proyecto
docker-compose ls
```

## Docker Compose V2 (Plugin)

Con Docker Compose V2, se usa `docker compose` (sin guión):

```bash
# Todos los comandos anteriores funcionan igual
docker compose up
docker compose down
docker compose ps
# etc...
```

## Atajos Útiles

```bash
# Ver logs en tiempo real de todos los servicios
docker-compose up | tee logs.txt

# Recrear y reconstruir todo
docker-compose up -d --force-recreate --build

# Limpiar todo (contenedores, redes, volúmenes, imágenes)
docker-compose down -v --rmi all --remove-orphans

# Ejecutar bash en un servicio
docker-compose exec <servicio> /bin/bash

# Ver logs de los últimos 100 líneas y seguir
docker-compose logs --tail=100 -f
```

## Ejemplos de Uso Común

```bash
# Desarrollo: reconstruir y reiniciar
docker-compose down && docker-compose up --build -d

# Ver qué está pasando
docker-compose ps && docker-compose logs --tail=50

# Limpiar y empezar de cero
docker-compose down -v && docker-compose up --build

# Entrar a un contenedor para debugging
docker-compose exec <servicio> sh

# Copiar archivos desde/hacia un contenedor
docker cp <container_id>:/ruta/archivo ./local
docker cp ./local <container_id>:/ruta/destino
```

## Flags Globales Comunes

```bash
-f, --file FILE          Especificar archivo compose alternativo
-p, --project-name NAME  Especificar nombre del proyecto alternativo
--verbose                Mostrar más información de salida
--log-level LEVEL        Establecer nivel de logging
-H, --host HOST          Socket del daemon a conectar
--tls                    Usar TLS
--tlsverify              Usar TLS y verificar remoto
--env-file PATH          Especificar archivo de variables de entorno
```

## Notas Importantes

1. **docker-compose vs docker compose**: La versión V2 usa `docker compose` (comando integrado en Docker CLI)
2. **docker-compose.yml**: Nombre por defecto del archivo de configuración
3. **Dependencias**: Los servicios se inician según sus dependencias definidas
4. **Redes**: Por defecto, Compose crea una red para tu aplicación
5. **Volúmenes**: Los volúmenes nombrados persisten entre recreaciones de contenedores
6. **Orden de archivos**: Cuando usas múltiples archivos `-f`, los valores del último sobrescriben a los anteriores
7. **.env**: Docker Compose carga automáticamente variables de un archivo `.env` en el mismo directorio

