const updateFund = Vue.createApp({})

updateFund.component("updatefunds", {
    data() {
        return {
            fund_id: null,
            user_id: 1,
            before_fund: {},
            after_fund: {},
            stocks: {},
            msgAllocationAlert: "❌ Allocation must add up to 100%! ❌",
            showAllocationAlert: false,
            msgNameAlert: "❌ Fund name cannot be empty! ❌",
            showNameAlert: false,
            msgIntervalAlert: "❌ Fund interval cannot be empty & must be a whole number! ❌",
            showIntervalAlert: false,
            msgUpdateAlert: "",
            showUpdateAlert: false,
            beforeLabel: [],
            beforeData: [],
            beforeChart: null,
            afterLabel: [],
            afterData: [],
            afterChart: null
        }
    },
    created() {
        let urlParams = new URLSearchParams(window.location.search);
    
        if (urlParams.has("fund_id")) {
            this.fund_id = urlParams.get("fund_id");
        }
    },
    async mounted() {
        // this.user_id = sessionStorage.getItem("user_id");
        var fundDetails = await this.getFundDetails();
        var fundStocks = await this.getFundStocks();
        var allStocks = await this.getStocks();

        this.before_fund = {
            "fund_id": this.fund_id,
            "fund_name": fundDetails.fund_name,
            "fund_investment_amount": fundDetails.fund_investment_amount,
            "fund_creation_date": fundDetails.fund_creation_date,
            "fund_interval": fundDetails.fund_interval,
            "allocations": fundStocks
        }
        this.after_fund = JSON.parse(JSON.stringify(this.before_fund))
        this.all_stocks = allStocks

    },
    methods: {
        getFundDetails() {
            return new Promise((resolve, reject) => {
                axios.get('http://localhost:5000/funds/' + this.fund_id)
                .then((response) => {
                    var data = response.data.data
                    console.log("getFundDetails", data)
                    resolve(data)
                }).catch((error) => {
                    reject(error)
                })
            })
        },
        getFundStocks() {
            return new Promise((resolve, reject) => {
                axios.get('http://localhost:5001/a_fund_stocks/' + this.fund_id)
                .then((response) => {
                    var data = response.data.data.allocation
                    var allocations = []
                    for (allocation of data) {
                        var to_push = {}
                        to_push["stock_id"] = allocation.stock_id
                        to_push["allocation"] = allocation.allocation*100
                        allocations.push(to_push)
                    }
                    // console.log("getFundStocks", allocations)
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
        outputTotal() {
            var total = 0;
            var allocations = this.after_fund.allocations
            allocations.forEach((item) => {
                if (item.allocation) {
                    total += item.allocation
                } else {
                    total += 0
                }
            })
            this.showAllocationAlert = total !== 100
        },
        validateName() {
            this.showNameAlert = this.after_fund.fund_name === ""
        },
        validateInterval() {
            this.showIntervalAlert = this.after_fund.fund_interval === "" || !Number.isInteger(this.after_fund.fund_interval)
        },
        updateChart() {
            this.msgUpdateAlert = ""
            this.showUpdateAlert = false

            if (this.beforeChart) {
                this.beforeChart.destroy()
            }

            if (this.afterChart) {
                this.afterChart.destroy()
            }

            this.beforeLabel = []
            this.beforeData = []
            for (allocation of this.before_fund.allocations) {
                var stock_id = parseInt(allocation.stock_id)
                var stock_symbol = this.all_stocks[stock_id].stock_symbol
                var stock_name = this.all_stocks[stock_id].stock_name
                this.beforeLabel.push("[" + stock_symbol + "] " + stock_name)
                this.beforeData.push(allocation.allocation/100)
            }

            const beforeData = {
                labels: this.beforeLabel,
                datasets: [{
                label: 'Before changes',
                backgroundColor: [
                    '#F2E4BB',
                    '#BAB3BA',  // color for data at index 0
                    '#C1D5E0',  // color for data at index 1
                    '#FFF8B1',  // color for data at index 2
                    '#A5CC93',  // color for data at index 3
                    '#B7CACC',  // color for data at index 4
                    '#BC798A',  // color for data at index 5
                    '#C8B6C6',  // color for data at index 6
                    '#ECCECE',
                    '#F09AAE'
                    //...
                ],
                // borderColor: 'rgb(255, 99, 132)',
                data: this.beforeData,
                }]
            };
    
            const beforeConfig = {
                type: 'doughnut',
                data: beforeData,
                options: {
                    plugins: {
                        legend: {
                            display: false
                        }
                    }
                }
            };
    
            this.beforeChart = new Chart(
                document.getElementById('beforeChart'), beforeConfig
            );

            this.afterLabel = []
            this.afterData = []
            for (allocation of this.after_fund.allocations) {
                var stock_id = parseInt(allocation.stock_id)
                var stock_symbol = this.all_stocks[stock_id].stock_symbol
                var stock_name = this.all_stocks[stock_id].stock_name
                this.afterLabel.push("[" + stock_symbol + "] " + stock_name)
                this.afterData.push(allocation.allocation/100)
            }
            
            const afterData = {
                labels: this.afterLabel,
                datasets: [{
                label: 'After changes',
                backgroundColor: [
                    '#FCBBB1',  // color for data at index 0
                    '#A5D0C6',  // color for data at index 1
                    '#FF787B',  // color for data at index 2
                    '#EFE8E2',  // color for data at index 3
                    '#FFC2AA',  // color for data at index 4
                    '#D8BACC',  // color for data at index 5
                    '#C1D5E0',  // color for data at index 6
                    '#EDFCED',
                    '#E0BCE0',
                    '#F38D4A'
                    //...
                ],
                // borderColor: 'rgb(255, 99, 132)',
                data: this.afterData,
                }]
            };
    
            const afterConfig = {
                type: 'doughnut',
                data: afterData,
                options: {
                    plugins: {
                        legend: {
                            display: false
                        }
                    }
                }
            };
    
            this.afterChart = new Chart(document.getElementById('afterChart'), afterConfig)
        },
        async processUpdateFund() {
            var isUpdated = false

            if (this.before_fund.fund_name !== this.after_fund.fund_name || this.before_fund.fund_interval !== this.after_fund.fund_interval) {
                var updatedFund = {
                    "fund_id": this.after_fund.fund_id,
                    "fund_name": this.after_fund.fund_name,
                    "fund_interval": this.after_fund.fund_interval
                }
                var fundPromise = await this.callUpdateFund(updatedFund)

                isUpdated = true
            }

            if (JSON.stringify(this.before_fund.allocations) !== JSON.stringify(this.after_fund.allocations)) {
                var allocationsRatio = []
                for (allocation of this.after_fund.allocations){
                    var newAllocation = JSON.parse(JSON.stringify(allocation))
                    newAllocation.allocation = allocation.allocation/100
                    allocationsRatio.push(newAllocation)
                }
                var updatedFundStock = {
                    "fund_id": this.after_fund.fund_id,
                    "allocations": allocationsRatio
                }
                var fundStockPromise = await this.callUpdateFundStock(updatedFundStock)

                isUpdated = true
            }

            if (!isUpdated) {
                this.msgUpdateAlert = "There was no changes made, please make some changes before confirming your update!"
                this.showUpdateAlert = true
            } else {
                Swal.fire({icon: 'success',title: 'Success',text: 'Fund successfully updated!'}).then((result) => {
                    if (result.isConfirmed) {
                        window.location.href = "update-fund.html?fund_id=" + this.fund_id
                    }
                })
            }

        },
        callUpdateFund(updatedFund) {
            return new Promise((resolve, reject) => {
                axios.put("http://localhost:5000/funds/update", updatedFund)
                .then((response) => {
                    resolve(response.data.data)
                }).catch((error) => {
                    reject(error)
                })
            })
        },
        callUpdateFundStock(updatedFundStock) {
            return new Promise((resolve, reject) => {
                axios.post("http://localhost:5001/funds_stocks/update_allocation", updatedFundStock)
                .then((response) => {
                    resolve(response.data.data)
                }).catch((error) => {
                    reject(error)
                })
            })
        }
    },
    template: `
    <div class="container my-5">
        <div class="row mb-5">
            <h1>
                Update my fund
            </h1>
            <h2 class="fst-italic">{{ before_fund.fund_name }}</h2>
        </div>
        <div v-if="showNameAlert" class="alert alert-danger alert-dismissible fade show" role="alert">
            <strong>{{ msgNameAlert }}</strong>
        </div>
        <div v-if="showIntervalAlert" class="alert alert-danger alert-dismissible fade show" role="alert">
            <strong>{{ msgIntervalAlert }}</strong>
        </div>
        <div v-if="showAllocationAlert" class="alert alert-danger alert-dismissible fade show" role="alert">
            <strong>{{ msgAllocationAlert }}</strong>
        </div>
        <div class="row">
            <h4>
                Edit fund details / allocation
            </h4>
            <div class="form-floating mb-3 mt-3 ml-auto gx-1">
                <input type="text" class="form-control" id="floatingName" placeholder="Enter New Fund Name Here" v-model="after_fund.fund_name" @change="validateName">
                <label for="floatingName">Fund Name</label>
            </div>
            <div class="form-floating mb-3 mt-3 ml-auto gx-1">
                <input type="number" step="1" class="form-control" id="floatingInterval" placeholder="Enter Fund Interval Here" v-model="after_fund.fund_interval" @change="validateInterval">
                <label for="floatingInterval">Fund Interval (Days)</label>
            </div>
        </div>
        <div class=row>
            <table class="table table-hover">
                <thead>
                    <tr>
                        <th scope="col">Stock ID</th>
                        <th scope="col">Stock Name</th>
                        <th scope="col">Allocation</th>
                    </tr>
                </thead>
                
                <tbody>
                    <tr v-if="after_fund.allocations" v-for="(allocation, index) in after_fund.allocations">
                        <td>
                            {{ all_stocks[allocation.stock_id].stock_symbol }}
                        </td>
                        <td>
                            {{ all_stocks[allocation.stock_id].stock_name }}
                        </td>
                        <td>
                            <div class="input-group mb-3">
                                <input type="number" class="form-control" aria-label="Allocation percentage" v-model="allocation.allocation" @change="outputTotal">
                                <span class="input-group-text">%</span>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div class="row">
            <div class="d-grid gap-2">
                <button class="btn btn-success" type="button" :disabled="showNameAlert || showAllocationAlert || showIntervalAlert || same" data-bs-toggle="modal" data-bs-target="#comfimationModal" @click="updateChart">Update Fund</button>
            </div>
        </div>

        <div class="modal fade" id="comfimationModal" tabindex="-1" aria-labelledby="confirmationModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-xl modal-dialog-centered modal-dialog-scrollable">
                <div class="modal-content">
                    <div class="modal-header">
                        <h1 class="modal-title fs-4" id="confirmationModalLabel">Review & confirm changes?</h1>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <div class="row  mx-5" v-if="showUpdateAlert" >
                            <div class="alert alert-danger alert-dismissible fade show" role="alert">
                                <strong>{{ msgUpdateAlert }}</strong>
                            </div>
                        </div>
                        <div class="row align-items-center">
                            <div class="col-md-5">
                                <div class="row text-center">
                                    <h3 class="text-danger">
                                        Before
                                    </h3>
                                </div>
                                <div class="row">
                                    <div class="card border-danger w-75 mx-auto">
                                        <div class="card-body">
                                            <h5 class="card-title">{{ before_fund.fund_name }}</h5>
                                            <h6 class="card-subtitle mb-2 text-muted">Rebalances every {{ before_fund.fund_interval }} day(s)</h6>
                                            <canvas id="beforeChart"></canvas>
                                        </div>
                                        <ul class="list-group list-group-flush">
                                            <li class="list-group-item" v-for="(allocation, index) in before_fund.allocations">
                                                {{ all_stocks[allocation.stock_id].stock_symbol }}, {{ all_stocks[allocation.stock_id].stock_name }}: {{ allocation.allocation }}%
                                            </li>
                                        </ul>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-2 text-center fs-1">
                                <div class="align-items-center">
                                    <span>&#10132;</span>
                                </div>
                            </div>
                            <div class="col-md-5">
                                <div class="row text-center">
                                    <h3 class="text-success">
                                        After
                                    </h3>
                                </div>
                                <div class="row">
                                    <div class="card border-success w-75 mx-auto">
                                        <div class="card-body">
                                            <h5 class="card-title">{{ after_fund.fund_name }}</h5>
                                            <h6 class="card-subtitle mb-2 text-muted">Rebalances every {{ after_fund.fund_interval }} day(s)</h6>
                                            <canvas id="afterChart"></canvas>
                                        </div>
                                        <ul class="list-group list-group-flush">
                                            <li class="list-group-item" v-for="(allocation, index) in after_fund.allocations">
                                                {{ all_stocks[allocation.stock_id].stock_symbol }}, {{ all_stocks[allocation.stock_id].stock_name }}: {{ allocation.allocation }}%
                                            </li>
                                        </ul>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="row">
                            <div class="">
                            
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button type="button" class="btn btn-success" @click="processUpdateFund">Confirm</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
    `
})

updateFund.mount("#updatefund")