var stocksLabel = []
var stocksData = []
var backgroundColorList = []
var userId = 1
var fundId = 1 

async function donutChart() {
	await getFundStocksData()

new Chart("currentpiechart", {
	type: "doughnut",
	data: {
		labels: this.stocksLabel,
		datasets: [{
			backgroundColor: this.backgroundColorList,
			data: this.stocksData
		}]
	},
	options: {
		title: {
			display: false,
		},
		legend:{
			position: 'right',
		},
		plugins: {
			datalabels: {
				formatter: (value, ctx) => {
					let sum = 0;
					let dataArr = ctx.chart.data.datasets[0].data;
					dataArr.map(data => {
						sum += data;
					});
					let percentage = (value*100 / sum).toFixed(2)+"%";
					return percentage;
			},
				color: '#fff',
		}
		}
  	}
})}

donutChart()

function dynamicColors() {
	var r = Math.floor(Math.random() * 255);
	var g = Math.floor(Math.random() * 255);
	var b = Math.floor(Math.random() * 255);
	return "rgb(" + r + "," + g + "," + b + ")";
};

async function getFundStocksData() {
	this.userId = sessionStorage.getItem("user_id");
	this.fundId = sessionStorage.getItem("fund_id");
    await axios
        .get('http://localhost:5001/current_funds_stocks/' + this.fundId + '/' + this.userId)
	.then((response) => {
        console.log(response)
		var tempdata = response.data.data;
        
		for (stock in tempdata){
			stocksData.push(tempdata[stock]["allocation"]);
			stocksLabel.push(tempdata[stock]["stock_name"]);
			backgroundColorList.push(dynamicColors());
		}
	});
}