<?php
// Get the JSON data sent from the client
$jsonData = file_get_contents('php://input');

// Decode the JSON data into a PHP associative array
$data = json_decode($jsonData, true);

// Handle the JSON data as needed (e.g., store it in a file, database, etc.)
// For example, store JSON data in a file named data.json
file_put_contents('data.json', $jsonData);

// Send a response back to the client (optional)
echo "JSON data received and stored successfully.";
?>
