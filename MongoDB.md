# Init DB

```
mongod --port 27017 --dbpath /data/db1

mongo --port 27017

use admin
db.createUser(
  {
    user: "root",
    pwd: "123abc."
    roles: [{role: "userAdminAnyDatabase", db: "admin"}, "readWriteAnyDatabase"]
  }
)

mongod --auth --port 27017 --dbpath /data/db1

mongo --port 27017  --authenticationDatabase "admin" -u "myUserAdmin" -p

use UserPower
db.createUser({user: "mtdtest", pwd: "mtdtest123", roles: [{role: "readWrite", db: "UserPower"}, {role: "read", db: "UserPower"}]})
```
