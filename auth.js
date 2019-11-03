const passportGoogle = require('passport-google-oauth');

const googleStrategy = passportGoogle.OAuth2Strategy;

function googleCallback(token, refreshToken, profile, done) {
  return done(null, {
    profile: profile,
    token: token
  });
}

module.exports = (passport) => {
  const { CLIENT_ID, CLIENT_SECRET, CALLBACK_URL } = process.env;

  const googleOptions = {
    clientID: CLIENT_ID,
    clientSecret: CLIENT_SECRET,
    callbackURL: CALLBACK_URL
  };

  passport.serializeUser((user, done) => {
    done(null, user);
  });

  passport.deserializeUser((user, done) => {
    done(null, user);
  });

  passport.use(new googleStrategy(googleOptions, googleCallback));
};
