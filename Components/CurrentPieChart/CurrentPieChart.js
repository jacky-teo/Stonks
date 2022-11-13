var currentStocksLabel = []
var currentStocksData = []
var backgroundColorList = []
var userId = null
var fundId = null 

async function currentDonutChart() {
    userId = sessionStorage.getItem("user_id");
    fundId = sessionStorage.getItem("fund_id");
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

function compare( a, b ) {
	if ( a.stock_name < b.stock_name ){
		return -1;
	}
	if ( a.stock_name > b.stock_name ){
		return 1;
	}
	return 0;
}

var dict = {};
async function getFundStocksData() {
	this.userId = sessionStorage.getItem("user_id");
	this.fundId = sessionStorage.getItem("fund_id");
    await axios
        .get('http://localhost:5001/current_funds_stocks/' + this.fundId + '/' + this.userId)
	.then((response) => {
		var currentData = response.data.data;
        currentData.sort( this.compare );

        for (stock in currentData){
            currentStocksData.push(currentData[stock]["allocation"]);
            this.currentStocksLabel.push(currentData[stock]["stock_name"]);
			this.backgroundColorList.push(dynamicColors());
		}
	});
}