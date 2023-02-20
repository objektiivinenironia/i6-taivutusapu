<html>
<body>
<pre>

<?php
$input=$_POST['in'];
$mon=$_POST['mon'];

if (isset($mon)) $command = 'python3 tee.py -r -m "' . $input . '"';

else $command = 'python3 tee.py -r "' . $input . '"';
$python = `$command`;
echo $python;
//echo shell_exec("python3 testi.py" 'hellopython');
//echo shell_exec("python3 testi.py" 'hello');
?>
</pre>
<body>
<html>
