document.addEventListener("DOMContentLoaded", function() {
    const table = document.getElementById('table');
    const rows = Array.from(table.getElementsByTagName('tr'));

    let data = [];
    let currentMonth = '';

    let count=0;

    rows.forEach(row => {
        const th = row.querySelector('th');
        const tds = Array.from(row.querySelectorAll('td'));

        if (th) {
            const monthText = th.textContent.trim();
            const monthMatch = monthText.match(/No\. (\d+), (.+)/);
            if (monthMatch) {
                currentMonth = monthMatch[2]; // Extracting the month name
            }
        } else if (tds.length === 3) {
            const title = tds[0].textContent.trim();
            const author = tds[1].textContent.trim();
            const page = tds[2].textContent.trim();
            data.push({
                id:count,
                month: currentMonth,
                title: title,
                author: author,
                page: page
        
            });
            count++;
        }
    });
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
