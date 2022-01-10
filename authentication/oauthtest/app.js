#!/usr/bin/env node
//Principale
require('dotenv').config()
const express = require('express')
const passport = require('passport')

const session = require('express-session')
const GoogleStrategy = require('passport-google-oauth20').Strategy

const app = express();
const PORT = 9999;
app.use(session({
	secret: 'test',
	saveUninitialized: true,
	resave: true,
	// using store session on MongoDB using express-session + connect

}));

// Protocollo Oauth + funzione di logout
app.use(passport.initialize());
app.use(passport.session());
passport.serializeUser(function (user, done) {
	done(null, user);
});

passport.deserializeUser(function (user, done) {
	done(null, user);
});

//Impostiamo la GoogleStrategy per passport
passport.use(new GoogleStrategy({
	clientID: "18356018425-c6r05qhceb0g4iitc8prchlgf0d8pfr6.apps.googleusercontent.com",
	clientSecret: "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",
	callbackURL: 'http://localhost:' + PORT + '/auth/google/callback',
	scope: ['email', 'profile'],
}, (accessToken, refreshToken, profile, cb) => {
	//console.log('Our user authenticated with Google, and Google sent us back this profile info identifying the authenticated user:', profile);
	// Save token

	return cb(null, profile, accessToken);
}));

// La sessione dell'utente viene creata, ma se NON viene creato un campo allora l'utente non viene salvato nel database
// questo facilita il controllo sui dati
app.get('/auth/google/callback', passport.authenticate('google', { failureRedirect: '/', session: true }), (req, res) => {
	//console.log('we authenticated, here is our user object:', req.user);
	//console.log('The access token is: ', req.authInfo)
	user_info = {
		name: req.user.name.givenName,
		surname: req.user.name.familyName,
		email: req.user.emails[0].value,
		accessToken: req.authInfo
	}


	//res.send("L'email dell'user è " + umail + req.isAuthenticated());
	//res.sendFile(__dirname + "/" + "authcall.html");
	res.send(user_info)
});
app.get('/', function (req, res) {
	res.sendFile(__dirname + "/" + "home.html");
})


app.get('/isauthenticated', function (req, res) {
	var auth = req.isAuthenticated();
	res.send("User authenticated : " + auth);
})

// Avvio del server
var server = app.listen(PORT, function () {
	console.log('[i] Provaapp su http://localhost:%s', PORT);
	console.log("[+] Premere ctrl+c per terminare");

});