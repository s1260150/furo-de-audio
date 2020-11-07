const { Client } = require('pg')
const client = new Client ({
  user: "postgres",
  password: "pg5936",
  host: "172.27.0.2",
  port: "5432",
  database: "db"
})

let rows;

client.connect()
.then(() => console.log("Connected successfuly"))
.then(() => client.query("select * from testtable"))
.then(results => {rows = results.rows; console.table(results.rows)})
.catch((e => console.log(e)))
.finally((() => client.end()))

var express = require('express');
var app = express();

// HTTPリクエストを受け取る部分
app.get('/', function (req, res) {
    console.log("GET Method");
  let msg = 'Hello World!\n';
  if(rows)
    for(const r of rows) msg += JSON.stringify(r) + "\n";
  res.send(msg);
});

// サーバーを起動する部分
var server = app.listen(3000, function () {
  var host = server.address().address;
  var port = server.address().port;
  console.log('Example app listening at http://%s:%s', host, port);
});