const dotenv   = require('dotenv');
const express  = require('express');
const logger   = require('morgan');
const passport = require('passport');

dotenv.config({ silent: true });

const auth = require('./auth.js');

const app  = express();
const PORT = process.argv[2] || process.env.PORT || 3000;

app.use(logger('dev'));

auth(passport);
app.use(passport.initialize());

app.get('/', (req, res) => {
    res.json({
        status: 'session cookie not set'
    });
});

app.get('/auth/google', passport.authenticate('google', {
    scope: ['https://www.googleapis.com/auth/userinfo.profile']
}));

app.get('/auth/google/callback',
    passport.authenticate('google', {
        failureRedirect: '/'
    }),
    (req, res) => {}
);

app.listen(PORT, () => console.log(`Server is listening on port ${PORT}`));
