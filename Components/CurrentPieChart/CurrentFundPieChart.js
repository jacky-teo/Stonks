const currentfundpiechart = Vue.createApp({
	data() {
		return {
			stockList: [],
			stockTitle: ["Name", "Allocation", "Volume", "Price (SGD)", "Value (SGD)"],
			userId: 1,
			fundId: 1,
		};
	},
	methods: {
		getUsersFunds() {
			this.userId = sessionStorage.getItem("user_id");
            
			this.fundId = sessionStorage.getItem("fund_id");
			axios.get('http://localhost:5001/current_funds_stocks/' + this.fundId + '/' + this.userId)
				.then(response => {
                    console.log(response)
					this.stockList = response.data.data;
					console.log(response.data.data);
				})
				.catch(error => {
					console.log(error);
				});
		}
  	},
    async created() {
        await this.getUsersFunds();
        console.log(this.stockList);
    },
	template: `
	<div class="shadow-lg p-3 mb-5 bg-white rounded">

		<h1 class="text-center mb-4">Current Fund {{userId}} Stocks</h1>

		<div class="row d-flex justify-content-center align-content-center">
			<canvas id="currentpiechart" style="width:100%;max-width:700px"></canvas>
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
currentfundpiechart.mount('#currentfundpiechart')

