var ctx = document.getElementById('myChart').getContext('2d');
var myChart = new Chart(ctx, {
    type: 'scatter',
    options: {
        plugins: {
            title: {
              display: true,
              text: 'Real-time CreditCard Transactions' // Replace with your desired title
            }
        },
        scales: {
            x: {
                type: 'linear',
                title: {
                    display: true,
                    text: 'Time'
                }
            },
            y: {
                title: {
                    display: true,
                    text: 'Amount'
                }
            }
        }
    }
});

var chart_socket = new WebSocket('ws://localhost:8000/ws/realtime_chart/')
chart_socket.onmessage = function(e){
    const chartData = JSON.parse(e.data);
    // console.log(chartData);
    // Update the chart data.
    myChart.data.datasets = chartData.datasets;

    // Refresh the chart.
    myChart.update();

}

var statistics_socket = new WebSocket('ws://localhost:8000/ws/realtime_statistic/')

class0_count = document.getElementById('class0-count')
class1_count = document.getElementById('class1-count')
class0_avg = document.getElementById('class0-avg')
class1_avg = document.getElementById('class1-avg')
class0_recent = document.getElementById('class0-recent')
class1_recent = document.getElementById('class1-recent')
statistics_socket.onmessage = function(e){
    const statisticsData = JSON.parse(e.data);
    console.log(statisticsData);
    class0_count.innerText = statisticsData.class0_count;
    class1_count.innerText = statisticsData.class1_count;
    class0_avg.innerText = statisticsData.class0_avg;
    class1_avg.innerText = statisticsData.class1_avg;
    class0_recent.innerText = 'Id: ' + statisticsData.class0_recent.id + '\r\n' + 'Time: ' + statisticsData.class0_recent.time;
    class1_recent.innerText = 'Id: ' + statisticsData.class1_recent.id + '\r\n' + 'Time: ' + statisticsData.class1_recent.time;
}



var data_socket = new WebSocket('ws://localhost:8000/ws/realtime_trans/')

data_socket.onmessage = function(e){
    const djangoData = JSON.parse(e.data);
    // console.log(djangoData);

    const id = djangoData.id;
    const time = djangoData.time;
    const amount = djangoData.amount;
    const class_field = djangoData.class_field;
    const current_refresh_time = djangoData.current_refresh_time;

    table = document.getElementById('creditcard-table');
    // tbody = document.getElementById('creditcard-table-body');
    var row = table.insertRow(1);
    if (class_field!=0){
        row.className = 'table-danger text-center';}
    else {
        row.className = 'table-light text-center';
    }
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);
    var cell4 = row.insertCell(3);
    cell1.innerHTML = id;
    // cell1.className = 'col-3'
    cell2.innerHTML = time;
    cell3.innerHTML = amount;
    cell4.innerHTML = class_field;
    
    while (table.rows.length > 11) {
        table.deleteRow(11);
    }
    divElement = document.querySelector('#current_refresh_time')
    if(typeof divElement !== null && divElement !== 'undefined' ) {
      document.querySelector('#current_refresh_time').innerText = current_refresh_time;
    }
}
$(document).ready(function() {
    $('#start-kafka-producer').click(function() {
        $.ajax({
            url: '/run_kafka_producer/',
            type: 'POST',
            success: function(response) {
                alert(response.status);
            },
            error: function(xhr) {
                alert('Error: ' + xhr.responseJSON.message);
            }
        });
    });

    $('#start-spark-processing').click(function() {
        $.ajax({
            url: '/run_spark_processing/',
            type: 'POST',
            success: function(response) {
                alert(response.status);
            },
            error: function(xhr) {
                alert('Error: ' + xhr.responseJSON.message);
            }
        });
    });

    $('#stop-kafka-producer').click(function() {
        $.ajax({
            url: '/stop_kafka_producer/',
            type: 'POST',
            success: function(response) {
                alert(response.status);
            },
            error: function(xhr) {
                alert('Error: ' + xhr.responseJSON.message);
            }
        });
    });

    $('#stop-spark-processing').click(function() {
        $.ajax({
            url: '/stop_spark_processing/',
            type: 'POST',
            success: function(response) {
                alert(response.status);
            },
            error: function(xhr) {
                alert('Error: ' + xhr.responseJSON.message);
            }
        });
    });

    $('#transaction-form').on('submit',function(e) {
        e.preventDefault();
        $.ajax({
            url: '/query/',
            type: 'POST',
            data: $('#transaction-form').serialize(),
            success: function(response) {
                    var results = $('#idResults');
                    results.empty();
                    if (response.transaction_data.length == 0) {
                        results.append('<li class="list-group-item list-group-item border border-primary">No transaction found</li>');
                    }
                    else {
                    response.transaction_data.forEach(function(transaction) {
                        results.append('<li class="list-group-item list-group-item border border-primary"> '+transaction.id+' </li>');
                    })};
            },
            error: function(xhr) {
                alert('Error: ' + xhr.responseJSON.message);
            }
        });
    });

    $('#search-by-id').on('submit',function(e) {
        e.preventDefault();
        $.ajax({
            url: '/search_by_id/',
            type: 'POST',
            data: $('#search-by-id').serialize(),
            success: function(response) {
                    var results = $('#transactionResult');
                    results.empty();
                    if (response.transaction_data == null) {
                        results.append('<li class="list-group-item list-group-item border border-primary>No transaction found</li>');
                    }
                    else {
                        results.append('<li class="list-group-item list-group-item border border-primary"> '+'Time: '+ response.transaction_data.time + '    Amount: ' + response.transaction_data.amount + ' Class: ' + response.transaction_data.class_field  + ' </li>');
                    };
            },
            error: function(xhr) {
                alert('Error: ' + xhr.responseJSON.message);
            }
        });
    });
});