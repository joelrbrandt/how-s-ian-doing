<?php
header("Content-Type: application/xml; charset=ISO-8859-1");

function parse($l) {
       $r = explode(" ", $l);
       $r[0] = intval($r[0]);
       $r[1] = intval($r[1]);
       return $r;
}
function getData() {
	 $a = file('log.txt');
	 $b = array_map(parse, $a);
	 $c = Array();
	 $last = 0;
	 for ($i = 0 ; $i < count($b) ; $i++) {
	     if ($b[$i][1] != $last) {
	     	$last = $b[$i][1];
		$c[] = $b[$i];
	     }
	 }	
	 return $c;
}

$thedata = getData();

?>

<rss version="2.0">

<channel>
<title>Ian's Dissertation Length</title>
<description>Tracks Ian's Dissertation Length</description>
<link>http://joelbrandt.org/howsiandoing/</link>
<lastBuildDate><?= strftime("%a, %d %b %Y %H:%M:%S %z", $thedata[count($thedata)-1][0]) ?></lastBuildDate>
<pubDate><?= strftime("%a, %d %b %Y %H:%M:%S %z", $thedata[count($thedata)-1][0]) ?></pubDate>

<?php
for ($i = count($thedata)-1; $i >= 0; $i--) {
?>

<item>
<title><?= $thedata[$i][1] ?></title>
<description>
<p>There are now <?= $thedata[$i][1] ?> words.</p>
<?php
$IMAGE_DIRECTORY = "/home/jbrandt/joelbrandt.org/howsiandoing/i";
$IMAGE_URL_BASE = "http://joelbrandt.org/howsiandoing/i";
if (file_exists($IMAGE_DIRECTORY . "/" . $thedata[$i][0] . ".png")) {
  echo "<p><img src='" . $IMAGE_URL_BASE . "/" . $thedata[$i][0] . ".png"  . "' /></p>";
}

?>
</description>
<link>http://joelbrandt.org/howsiandoing/</link>
<guid><?= $thedata[$i][0] ?></guid>
<pubDate><?= strftime("%a, %d %b %Y %H:%M:%S %z", $thedata[$i][0]) ?></pubDate>
</item>

<?php
}
?>

</channel>
</rss>