var stocksLabel = []
var stocksData = []
var backgroundColorList = []
var userId = null
var fundId = null


async function donutChart() {
    userId = sessionStorage.getItem("user_id");
    fundId = sessionStorage.getItem("fund_id");
	await getFundStocksData()

new Chart("piechart", {
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
                    console.log(dataArr)
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
	// this.userId = sessionStorage.getItem("userId");
	// this.fundId = sessionStorage.getItem("fundId");
    userId = sessionStorage.getItem("user_id");
    fundId = sessionStorage.getItem("fund_id");
  	let response = await axios
	.get('http://localhost:5001/fund_stocks/user/' + this.fundId + '/' + this.userId)
	.then((response) => {
		var tempdata = response.data.data.fundsSettlement;
		for (stock in tempdata){
			stocksData.push(tempdata[stock]["allocation"]);
			stocksLabel.push(tempdata[stock]["stock_name"]);
			backgroundColorList.push(dynamicColors());
		}
	});
}