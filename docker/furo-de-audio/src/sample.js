const { Client } = require('pg')
const client = new Client ({
  user: "postgres",
  password: "pg5936",
  host: "172.20.0.3",
  port: "5432",
  database: "db"
})

client.connect()
.then(() => console.log("Connected successfuly"))
.then(() => client.query("select * from testdb"))
.then(results => console.table(results.rows))
.catch((e => console.log(e)))
.finally((() => client.end()))