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
        placeMarketOrder(tBankUID, tBankPin, tBankSettlementAccount, allocation){
            var data = {
				"userID": tBankUID,
				"PIN": tBankPin, 
				"additionalInvest": 0,
				"allocation": JSON.stringify(allocation),
				"settlement_account": tBankSettlementAccount,
			}
			return new Promise((resolve, reject) => {
				axios.post("http://localhost:5010/rebalance", data).then((response) => {
					resolve(response);
				}).catch(error => {
					reject(error);
				});
			})
        },
		returnAllocationsBasedOnPlaceMarketOrderFormat(items) {
			var allocations = {}
			items.forEach((item) => {
				allocations[item.stock_symbol] = (item.stock_allocation/100)
			})
			return allocations
		},
		getFundStocks() {
            return new Promise((resolve, reject) => {
                axios.get('http://localhost:5001/a_fund_stocks/' + this.fundId)
                .then((response) => {
                    var data = response.data.data.allocation
					var allocations = {}
					data.forEach((item) => {
						allocations[item.stock_id] = item.allocation
					})
                    resolve(allocations)
                }).catch((error) => {
                    reject(error)
                })
            })
        },
        getStocks() {
            return new Promise((resolve, reject) => {
                axios.get('http://localhost:5003/stocks')
                .then((response) => {
                    var data = response.data.data.stocks
                    var stocks = {}
                    for (stock of data) {
                        var stockId = stock.stock_id
                        var stockName = stock.stock_name
                        var stockSymbol = stock.stock_symbol
                        stocks[stockId] = {
                            "stock_name": stockName,
                            "stock_symbol": stockSymbol
                        }
                    }
                    // console.log("getStocks", stocks)
                    resolve(stocks)
                }).catch((error) => {
                    reject(error)
                })
            })
        },
		getUser() {
            return new Promise((resolve, reject) => {
                axios.get('http://localhost:5005/user_info/user/' + this.userId)
                .then((response) => {
                    var data = response.data.data
                    console.log(data)
                    resolve(data)
                }).catch((error) => {
                    reject(error)
                })
            })
        },
        async rebalance(){
			var user = await this.getUser();
			var response = await this.placeMarketOrder(user.user_acc_id, user.user_pin, user.settlement_acc, this.allocations);
			
			if (response.data.code == 200) {
                Swal.fire({icon: 'success',title: 'Success',text: 'Fund successfully rebalanced!'}).then((result) => {
                    if (result.isConfirmed) {
                        window.location.href = "mystocks.html"
                    }
                })
            } else {
                Swal.fire({icon: 'error',title: 'Note',text: 'Something went wrong while rebalancing, please try again later.'})
            }
        }
  	},
    async created() {
        await this.getUsersFunds();
        this.userId = sessionStorage.getItem("user_id");
        this.fundId = sessionStorage.getItem("fund_id");

		var allocations = await this.getFundStocks();
		var allStocks = await this.getStocks();

		var cleanedAllocations = {};
		for (key in allocations) {
			cleanedAllocations[allStocks[key]["stock_symbol"]] = allocations[key]
		}

		this.allocations = cleanedAllocations
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
            <button type="button" class="btn btn-success float-end" data-bs-toggle="modal" data-bs-target="#comfimationModal">Rebalance Fund</button>
		</div>

		<div class="modal fade" id="comfimationModal" tabindex="-1" aria-labelledby="confirmationModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-lg modal-dialog-centered modal-dialog-scrollable">
                <div class="modal-content">
                    <div class="modal-header">
                        <h1 class="modal-title fs-4" id="confirmationModalLabel">Confirm rebalance current fund to target allocation?</h1>
                    </div>
                    <div class="modal-body">
                        <div class="row align-items-center">
                            <div class="">
								Are you sure you would like to rebalance your current fund?
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button type="button" class="btn btn-success" @click="rebalance()">Confirm</button>
                    </div>
                </div>
            </div>
        </div>

	</div>`
})
currentfundpiechart.mount('#currentfundpiechart')

