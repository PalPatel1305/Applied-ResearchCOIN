// When the DOM content is fully loaded, execute the following function
document.addEventListener("DOMContentLoaded", function() {
    // Get the table element with the id 'table'
    const table = document.getElementById('table');
    // Convert the HTMLCollection of table rows into an array
    const rows = Array.from(table.getElementsByTagName('tr'));

    // Initialize an empty array to store the extracted data
    let data = [];
    // Variable to track the current month being processed
    let currentMonth = '';

    // Counter variable for assigning unique IDs to each entry
    let count = 0;

    // Iterate over each table row
    rows.forEach(row => {
        // Check if the row contains a <th> element (header row)
        const th = row.querySelector('th');
        // Convert the HTMLCollection of table cells into an array
        const tds = Array.from(row.querySelectorAll('td'));

        if (th) {
            // Extract the month text from the header
            const monthText = th.textContent.trim();
            // Use regex to match the month number and name
            const monthMatch = monthText.match(/No\. (\d+), (.+)/);
            if (monthMatch) {
                // Extract the month name from the matched result
                currentMonth = monthMatch[2]; // Extracting the month name
            }
        } else if (tds.length === 3) {
            // If the row contains 3 <td> elements, extract the data
            const title = tds[0].textContent.trim();
            const author = tds[1].textContent.trim();
            const page = tds[2].textContent.trim();
            // Construct an object with the extracted data and push it to the 'data' array
            data.push({
                id: count, // Assign a unique ID
                month: currentMonth, // Assign the current month
                title: title,
                author: author,
                page: page
            });
            // Increment the counter for unique IDs
            count++;
        }
    });

    // Send the extracted data to the server using AJAX
    $.ajax({
        url: 'save_json.php', // Specify the URL of your server-side script
        type: 'POST', // Use POST method to send data
        data: JSON.stringify(data), // Convert JSON object to string
        contentType: 'application/json', // Specify content type
        success: function(response) {
            console.log('JSON data sent to server successfully');
            // Handle the response from the server if needed
        },
        error: function(xhr, status, error) {
            console.error('Error sending JSON data to server:', error);
        }
    });
});
