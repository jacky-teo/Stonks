var stocksLabels = []
var stocksHistory = []

var ctx = document.getElementById("linechart").getContext("2d");
var myChart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: stocksLabels,
    datasets: stocksHistory
  },
  options: {
    plugins: {
      datalabels: {
        display: false
      }
    }
  }
  
});

getStockHistoryData();

function dynamicColors() {
  var r = Math.floor(Math.random() * 255);
  var g = Math.floor(Math.random() * 255);
  var b = Math.floor(Math.random() * 255);
  return "rgb(" + r + "," + g + "," + b + ")";
};

function getStockHistoryData() {
  
    var userID = "Z312312";
    var PIN = "148986";
    var fund_id = sessionStorage.getItem("fund_id");
    var numDays = 30;
  
    axios.get(`http://localhost:5001/fund_stocks/stock_history/${fund_id}/${userID}/${PIN}`).then(response => {
      // console.log(response.data.data);
      var dates = 1;
      for ([stock_name, stock_data] of Object.entries(response.data.data)) {
        price_data = [];
        for (let i = 0; i < numDays; i++ ) {

          price_data.push(parseFloat(stock_data.prices[i].high));
          if (dates < numDays+1) {
  
            let myDate = new Date(parseInt(stock_data.prices[i].date) * 1000);
            let dateStr = myDate.getFullYear() + "/" + (myDate.getMonth() + 1) + "/" + myDate.getDate()
            
            stocksLabels.push(dateStr);
            dates++;
          }
        }
        obj = {
          label: stock_name,
          data: price_data,
          fill: false,
          borderColor: dynamicColors(),
          tension: 0.1
        }
        stocksHistory.push(obj);
        // console.log(stocksHistory);
        myChart.update();
      }
  
  }).catch(error => {
      // Handle error
      console.log(error);
  });
}