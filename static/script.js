    // Sample data for the pie chart
    var data = {
        labels: ['Low', 'Mid', 'High'],
        datasets: [{
            data: [20, 30, 50], // Replace with your actual data
            backgroundColor: ['#FF6384', '#FFCE56', '#36A2EB'], // Specify colors
            hoverBackgroundColor: ['#FF6384', '#FFCE56', '#36A2EB']
        }]
    };

    // Get the canvas element
    var ctx = document.getElementById('pieChart').getContext('2d');

    // Create the pie chart
    var myPieChart = new Chart(ctx,{
        type: 'pie',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
        
    });


    
document.addEventListener('DOMContentLoaded', function() {
    // Get the canvas element
    var ctxColumn = document.getElementById('columnChart').getContext('2d');

    // Sample data for the column chart
    var dataColumn = {
        labels: ['Category 1', 'Category 2', 'Category 3'],
        datasets: [{
            label: 'Column Chart',
            backgroundColor: 'rgba(75, 192, 192, 0.6)', // Adjust color and opacity
            borderColor: 'rgba(75, 192, 192, 1)', // Adjust color
            borderWidth: 1,
            data: [10, 20, 30] // Sample data values
        }]
    };

    // Chart configuration
    var configColumn = {
        type: 'bar', // Set chart type to bar for column chart
        data: dataColumn,
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    };

    // Create the column chart
    var myColumnChart = new Chart(ctxColumn, configColumn);
});