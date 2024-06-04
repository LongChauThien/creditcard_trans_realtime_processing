var socket = new WebSocket('ws://localhost:8000/ws/realtime_trans/')

socket.onmessage = function(e){
    const djangoData = JSON.parse(e.data);
    console.log(djangoData);

    const time = Object.values(djangoData.time);
    const amount = Object.values(djangoData.amount);
    const class_field = Object.values(djangoData.class_field);
    const current_refresh_time = Object.values(djangoData.current_refresh_time);

    const n = 10;
    table = document.getElementById('creditcard-table')
    for (let i = 0; i < n; i++) {
        var row = table.insertRow(1);
        if (class_field[i]!=0){
            row.className = 'table-danger';}
        var cell1 = row.insertCell(0);
        var cell2 = row.insertCell(1);
        var cell3 = row.insertCell(2);
        cell1.innerHTML = time[i];
        cell2.innerHTML = amount[i];
        cell3.innerHTML = class_field[i];
        
    }
    while (table.rows.length > n+1) {
        table.deleteRow(n+1);
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
});