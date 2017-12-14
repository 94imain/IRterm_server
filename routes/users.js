var express = require('express');
var router = express.Router();

var PythonShell = require('python-shell');

/* GET users listing. */

var options ={
    mode : 'text',
    pythonPath: '/Library/Frameworks/Python.framework/Versions/3.5/bin/python3.5',
    pythonOptions: ['-u'],
    scriptPath:'',
    args:['value1','val2','val3']
};
router.get('/', function(req, res, next) {
  res.send('respond with a resource');
  PythonShell.run('coretest.py',options,function (err, results) {
      if(err) throw err;

      console.log("result : %j", results);

    });
});


router.post('/signup', function (req,res) {
  var message = req.body.inputmessage;
  var output = "default";
    console.log("ok its coming"+req.body.inputmessage);
    console.log(message);
    options.args=[message];
    PythonShell.run('main.py',options,function (err, results) {
      if(err) throw err;

      console.log("result : %j", results);
      console.log(results.toString());
      output=results.toString();


    res.setHeader('Content-Type', 'application/json');
    res.write(JSON.stringify({ inputmessage: output }, null, 3));
    res.end();
    });
});

module.exports = router;
