Accede al contenedor
```bash
docker exec -it opobot-db bash
```

Accede a la base de datos
```bash
mongosh --username root --password root_password --authenticationDatabase admin
```

Dentro de la base de datos
```bash
use opobot
```

Ver las bases de datos disponibles
```bash
show dbs
```

Ver las colecciones disponibles
```bash
show collections
```

Ver las colecciones de las oposiciones
```bash
db.opposition.find()
```

Ver las colecciones de los usuarios
```bash
db.user.find()
```
