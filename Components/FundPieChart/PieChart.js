var stocksLabel = []
var stocksData = []
var backgroundColorList = []

async function dummyChart() {
   await getDummyData()

new Chart("piechart", {
  type: "doughnut",
  data: {
    labels: this.stocksLabel,
    datasets: [{
      backgroundColor: this.backgroundColorList,
      data: this.stocksData,
    }]
  },
  options: {
    title: {
      display: true,
      text: "Fund 1 Stocks"
    },
    legend:{
      position: 'right',
    }
  }
})}

dummyChart()

function dynamicColors() {
  var r = Math.floor(Math.random() * 255);
  var g = Math.floor(Math.random() * 255);
  var b = Math.floor(Math.random() * 255);
  return "rgb(" + r + "," + g + "," + b + ")";
};

async function getDummyData() {
  let response = await axios
    .get("http://localhost:5003/fund_stocks/1")
    .then((response) => {
      var tempdata = response.data.data
      for (stock in tempdata){
        stocksData.push(tempdata[stock]["volume"]);
        stocksLabel.push(tempdata[stock]["stock_name"]);
        backgroundColorList.push(dynamicColors());
      }
    });
}