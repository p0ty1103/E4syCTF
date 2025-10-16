const express = require("express");
const bodyParser = require("body-parser");
const mysql = require("mysql2");
const cookieParser = require("cookie-parser");
const path = require("path");
const fs = require("fs");

const app = express();
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());
app.use(cookieParser());
app.use(express.static(path.join(__dirname)));

let flag_content;
try {
    flag_content = fs.readFileSync(path.join(__dirname, 'flag.txt'), 'utf8').trim();
} catch (e) {
    flag_content = "E4syCTF{File_Not_Found}";
    console.error("FLAG file (flag.txt) not found or unreadable.");
}

const db = mysql.createConnection({
  host: "web05-db",
  user: "root",
  password: "SuPeRsEcReTaDmInPaSsWoRd1234",
  database: "e4syctf"
});

const waf = (sql) => {
  const blacklist = ["--", ";"];
  const pattern = new RegExp(blacklist.join("|"), "i");
  return pattern.test(sql);
};

const submissions = [];

db.connect((err) => {
  if (err) {
    console.error('MySQL connection error:', err);
    return;
  }
  console.log('MySQL connected.');

  const queries = [
    "DROP TABLE IF EXISTS users;",
    "CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), password VARCHAR(255));",
    "DELETE FROM users;",
    "INSERT INTO users (username, password) VALUES ('admin','supersecret');",
    "INSERT INTO users (username, password) VALUES ('guest','guest');"
  ];

  const run = (i) => {
    if (i >= queries.length) { console.log('DB initialized.'); return; }
    db.query(queries[i], (e) => { if (e) { console.error('DB init error', e); } run(i+1); });
  };
  run(0);
});


app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "E4syCTF.html"));
});

app.get("/login", (req, res) => {
  res.sendFile(path.join(__dirname, "login.html"));
});

app.post("/login", (req, res) => {
  let { username, password } = req.body;
  username = String(username || '').trim();
  password = String(password || '').trim();

  const input = `${username} ${password}`;
  if (waf(input)) {
    return res.send("🚫 Invalid input detected");
  }

  const query = `SELECT * FROM users WHERE username='${username}' AND password='${password}'`;
  console.log("[SQL] " + query);

  db.query(query, (err, results) => {
    if (err) {
      console.error('DB error:', err);
      return res.status(500).send("Internal Error");
    }
    if (results && results.length > 0) {
      const row = results[0];
      
      if (row.username === "admin") {
        res.cookie("session", "admin-session", { httpOnly: true });
        return res.redirect("/admin");
      }
      res.cookie("session", "user-session", { httpOnly: true });
      return res.send("Login successful, but you are not admin.");
    } else {
      return res.send("Login failed.");
    }
  });
});

app.post("/post", (req, res) => {
  const author = (req.body.author || 'anonymous').toString();
  const content = (req.body.content || '').toString();
  const id = submissions.length + 1;
  submissions.push({ id, author, content });
  return res.send(`Post OK (id=${id})`);
});

app.get("/submissions", (req, res) => {
  res.json(submissions);
});

app.get("/admin", (req, res) => {
  const session_cookie = req.cookies.session;
  if (session_cookie !== "admin-session") {
    return res.status(403).send('Forbidden: Must be logged in as admin to view this page.');
  }
  
  res.cookie('flag', flag_content, { httpOnly: false }); 
  
  return res.sendFile(path.join(__dirname, "admin.html"));
});

app.get("/steal", (req, res) => {
  const stolen = req.query.c || '';
  console.log('[STOLEN COOKIE]', stolen);
  res.send('ok');
});

app.post("/admin/clear", (req, res) => {
  const cookie = req.cookies.session;
  if (cookie !== "admin-session") return res.status(403).send('Forbidden');
  submissions.length = 0;
  res.send('cleared');
});

const PORT = process.env.PORT || 2943;
app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));

module.exports = app;
