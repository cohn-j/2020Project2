console.log("Hello!")

var markersCount = 0;
    
        anychart.onDocumentReady(function () {
          // The data used in this sample can be obtained from the CDN
          // https://cdn.anychart.com/csv-data/csco-daily.js
          anychart.data.loadCsvFile(
            'assets/monthly_AAL.csv',
          function(data) {  
          // create data table on loaded data
          var dataTable = anychart.data.table();
          dataTable.addData(data); 
    
          // map data for the ohlc series
          var ohlcMapping = dataTable.mapAs({
            open: 1,
            high: 2,
            low: 3,
            close: 4
          });
    
          // map data for scroller
          var valueMapping = dataTable.mapAs({ value: 5 });
    
          // create stock chart
          var chart = anychart.stock();
    
          // create and setup ohlc series
          var plot = chart.plot(0);
          var series = plot.ohlc(ohlcMapping);
          series.name('AAL');
          series.legendItem().iconType('risingfalling');
    
          // create markers
          createMarkers(plot, 0, 33, 'green', 'Low');
          createMarkers(plot, 33, 67, 'yellow', 'Average');
          createMarkers(plot, 67, 100, 'red', 'High');
    
          // create scroller series
          chart.scroller().area(valueMapping);
    
          // set container id for the chart
          chart.container('container');
    
          // initiate chart drawing
          chart.draw();
    
          // create range picker
          var rangePicker = anychart.ui.rangePicker();
          // init range picker
          rangePicker.render(chart);
    
          // create range selector
          var rangeSelector = anychart.ui.rangeSelector();
          // init range selector
          rangeSelector.render(chart);
        });
        });
    
        function createMarkers(plot, start, end, color, text) {
          // create and setup range marker
          plot.rangeMarker(markersCount).from(start).to(end).fill(color, 0.1);
    
          // create and setup text marker
          plot
            .textMarker(markersCount)
            .zIndex(50)
            .value(start + (end - start) / 2)
            .text(text);
    
          markersCount++;
        };



