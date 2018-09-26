//Set up requirements
var express = require("express");
var Request = require('request');
var bodyParser = require('body-parser');
var _ = require('underscore');
var config = require('./expt_generation/experiment_data.json');
var creds = require('./credentials.json');

//Create an 'express' object
var app = express();

//Set up the views directory
app.set("views", __dirname + '/views');
//Set EJS as templating language WITH html as an extension
app.engine('.html', require('ejs').__express);
app.set('view engine', 'html');
//Add connection to the public folder for css & js files
app.use(express.static(__dirname + '/public'));

// Enable json body parsing of application/json
app.use(bodyParser.json());

/*---------------
//DATABASE CONFIG
----------------*/
var cloudant_USER = creds.cloudant_USER;
var cloudant_DB = creds.cloudant_DB;
var cloudant_KEY = creds.cloudant_KEY;
var cloudant_PASSWORD = creds.cloudant_PASSWORD;

var cloudant_URL = "https://" + cloudant_USER + ".cloudant.com/" + cloudant_DB;

/*-----
ROUTES
-----*/

//Main Page Route - Show ALL data VIEW
app.get("/", function(req, res){
	res.render('index');
});

app.get("/practice", function(req, res){
	res.render('practice.html');
});

app.get("/experiment", function(req, res){
	res.render('experiment.html');
});

app.get("/data", function(req, res){
	res.json(config);
});

//SAVE an object to the db
app.post("/save", function(req,res){
	//Get the data from the body
	var data = req.body;
	//Send the data to the db
	Request.post({
		url: cloudant_URL,
		auth: {
			user: cloudant_KEY,
			pass: cloudant_PASSWORD
		},
		json: true,
		body: data
	});
});

// Start the server
app.listen(8000);
console.log('Express started on port 8000');
