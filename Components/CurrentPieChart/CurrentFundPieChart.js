const currentfundpiechart = Vue.createApp({
	data() {
		return {
			stockList: [],
			stockTitle: ["Name", "Allocation", "Volume", "Price (SGD)", "Value (SGD)"],
			userId: null,
			fundId: null,
		};
	},
	methods: {
		compare( a, b ) {
			if ( a.stock_name < b.stock_name ){
				return -1;
			}
			if ( a.stock_name > b.stock_name ){
				return 1;
			}
			return 0;
		},

		getUsersFunds() {
			this.userId = sessionStorage.getItem("user_id");
            
			this.fundId = sessionStorage.getItem("fund_id");
			axios.get('http://localhost:5001/current_funds_stocks/' + this.fundId + '/' + this.userId)
				.then(response => {
					this.stockList = response.data.data;
					this.stockList.sort( this.compare );
				})
				.catch(error => {
					console.log(error);
				});
		},
        redirectBalance(){
            window.location.href = "rebalance.html?fund_id=" + this.fundId;
        }
  	},
    async created() {
        await this.getUsersFunds();
        this.userId = sessionStorage.getItem("user_id");
        this.fundId = sessionStorage.getItem("fund_id");
    },
	template: `
	<div class="shadow-lg p-3 mb-5 bg-white rounded">

		<h1 class="text-center mb-4" style="color:black;">Current Fund {{fundId}} Investment Value</h1>

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
					<td>{{value.price}}</td>
					<td>{{(value.allocation_value).toFixed(2)}}</td>
				</tr>
				</tbody>
			</table>
            <button type="button" class="btn btn-success float-end" @click="
            redirectBalance()">Rebalance Fund</button>
		</div>

	</div>`
})
currentfundpiechart.mount('#currentfundpiechart')

