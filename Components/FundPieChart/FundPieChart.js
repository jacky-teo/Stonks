const fundpiechart = Vue.createApp({
	data() {
		return {
			stockList: [],
			stockTitle: ["Name", "Allocation", "Volume", "Price (SGD)", "Value (SGD)"],
			userId: 1,
			fundId: 1,
		};
	},
	async created() {
		await this.getUsersFunds();
		console.log(this.stockList);
	},
	methods: {
		getUsersFunds() {
			// this.userId = sessionStorage.getItem("userId");
			// this.fundId = sessionStorage.getItem("fundId");
			axios.get('http://localhost:5001/fund_stocks/user/' + this.fundId + '/' + this.userId)
				.then(response => {
					this.stockList = response.data.data.fundsSettlement;
					console.log(response.data.data.stocks);
				})
				.catch(error => {
					console.log(error);
				});
		}
  	},
	template: `
	<div class="shadow-lg p-3 mb-5 bg-white rounded">

		<h1 class="text-center mb-4">Fund {{userId}} Stocks</h1>

		<div class="row d-flex justify-content-center align-content-center">
			<canvas id="piechart" style="width:100%;max-width:700px"></canvas>
		</div>

		<div class="row d-flex justify-content-center align-content-center mx-3 mt-3">
			<table class="table table-sm table-bordered table-hover">
				<thead>
				<tr>
					<th scope="col" v-for="(value, key) in stockTitle" v-bind:key="key">{{value}}</th>
				</tr>
				</thead>

				<tbody>
				<tr v-for="(value, key) in stockList" v-bind:key="key">
					<td>{{value.stock_name}}</td>
					<td>{{value.allocation}}</td>
					<td>{{value.volume}}</td>
					<td>{{value.stock_price}}</td>
					<td>{{(value.volume * value.stock_price).toFixed(2)}}</td>
				</tr>
				</tbody>
			</table>
		</div>

	</div>`
})
fundpiechart.mount('#fundpiechart')

