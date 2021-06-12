const express = require('express'); // Include ExpressJS
const app = express(); // Create an ExpressJS app
const bodyParser = require('body-parser'); // Middleware 

app.use(bodyParser.urlencoded({ extended: false }));

function authenicate (username, password) {
    if (username === 'admin' && password === 'password') {
        return true;
    }
    return false;
}

// Route to Login Page
app.get('/', (req, res) => {
  res.sendFile(__dirname + '/index.html');
});

app.post('/login', (req, res) => {
    // Insert Login Code Here
    let username = req.body.username;
    let password = req.body.password;
    if(authenicate(username, password)) {
        return res.send('Login Succeessfully');
    }
    return res.send('Login failed due to incorrect username or password');
});

const port = 3000 // Port we will listen on

// Function to listen on the port
app.listen(port, () => console.log(`This app is listening on port ${port}`));