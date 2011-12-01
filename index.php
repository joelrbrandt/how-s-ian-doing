<?php
function parse($l) {
       $r = explode(" ", $l);
       $r[0] = intval($r[0]);
       $r[1] = intval($r[1]);
       return $r;
}
function readData() {
	 $a = file('log.txt');
	 $b = array_map(parse, $a);
	 return $b;
}

function filterData($data) {
	 $output = Array();
	 for ($i = 0 ; $i < count($data) ; $i++) {
	     if ($data[$i][1] != $last) {
	     	$last = $data[$i][1];
		$output[] = $data[$i];
	     }
	 }	
	 return $output;
}


$filtered_data = filterData(readData());


?>

<html>
<head>
<link rel="alternate" type="application/rss+xml" title="RSS" href="feed.php">
<style>
body {
	font-family: sans-serif;
}
</style>
</head>

<body>
<h1>How's Ian Doing On His Dissertation?</h1>

<p>Current word count: <?= $filtered_data[count($filtered_data)-1][1] ?> </p>

<p><img src="i/current.png" /></p>

</body>
</html>
