var currentStocksLabel = []
var currentStocksData = []
var backgroundColorList = []
var userId = 1
var fundId = 1 

async function currentDonutChart() {
	await getFundStocksData()

new Chart("currentpiechart", {
	type: "doughnut",
	data: {
        labels: this.currentStocksLabel,
		datasets: [{
			backgroundColor: this.backgroundColorList,
            data: this.currentStocksData
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
					let currentArr = ctx.chart.data.datasets[0].data;
                    console.log(currentArr)
                    currentArr.map(data => {
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

currentDonutChart()

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
		var currentData = response.data.data;
        
        for (stock in currentData){
            currentStocksData.push(currentData[stock]["allocation"]);
            currentStocksLabel.push(currentData[stock]["stock_name"]);
			backgroundColorList.push(dynamicColors());
		}
	});
}