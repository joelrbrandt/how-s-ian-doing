<?php
require_once('twitteroauth/twitteroauth.php');

function getConnectionWithAccessToken($oauth_token, $oauth_token_secret) {
  $CONSUMER_KEY="CONSUMER_KEY";
  $CONSUMER_SECRET="CONSUMER_SECRET";

  $connection = new TwitterOAuth($CONSUMER_KEY, $CONSUMER_SECRET, $oauth_token, $oauth_token_secret);
  return $connection;
}

try {
  $msg = $argv[1];
  $connection = getConnectionWithAccessToken("OAUTH_TOKEN", "OAUTH_TOKEN_SECRET");
  $response = $connection->post('statuses/update', array('status' => $msg,));
  if (!($response->text != '')) {
    throw new Exception("didn't work");
  }
  echo "OK\n";
  exit(0);
} catch (Exception $e) {
  echo "ERROR\n";
  echo $e;
  exit(-1);
}
exit(-2);

?>
