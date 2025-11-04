const express = require("express");
const app = express();
const port = 3000;

app.get("/", (req, res) => {
  res.send(`<!doctype html>
  <html lang="es">
    <head>
      <meta charset="utf-8"/>
      <meta name="viewport" content="width=device-width,initial-scale=1"/>
      <title>Hola Mundo - Express</title>
    </head>
    <body>
      <h1>Hola mundo desde Express!</h1>
      <p>Andres, esto es HTML servido por Express.</p>
    </body>
  </html>`);
});

app.listen(port, () => {
  console.log(`Express escuchando en http://localhost:${port}`);
});
