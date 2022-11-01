const createFund = Vue.createApp({});
// Stocks Component
createFund.component("createfunds", {
  data() {
    return {
        items: [],
        user_id: 1,
        fundInfo: {
            fund_name: "",
            fund_investment_amount: 0,
        },
        fundInterval: 0,
        stocks: {},
        ourStockList: [],
        tbank_stocks: [],
        stockSelected: [],
        total_allocations: 0,
        tbankStock_loaded: false,
        stockExistInFund: false,
        isCreatedFund: false,
    };
  },
   async mounted() {
    var loadTbankStocks = await this.getCustomerStocks(this.user_id)
    var loadOurStocks = await this.getOurStocks()
    loadTbankStocks && loadOurStocks ? this.tbankStock_loaded = true : console.log("Error loading stocks")
    this.tbank_stocks = loadTbankStocks
    this.ourStockList = loadOurStocks
  },
  methods: {
    async createFund() {

      if(this.totalAllocations == 100 && this.fundInfo.fundName != "" && this.fundInfo.fund_investment_amount != 0 && this.fundInterval != 0) {
        // Set the spinner to turn on
        this.isCreatedFund = true
      // Create fund in funds table -> get fund_id
        var fund_id = await this.addNewFund().then((response) => { return response })
        

      // Create new row in users_funds table with fund_id and user_id
      if (fund_id) {
        var userFundInfo = {user_id: this.user_id, fund_id: fund_id}
        var userFund_id = await this.addUserFund(userFundInfo).then((response) => { return response })
      }

      // Create stocks that does not exist in our database in stocks table & allow multiple stocks to be added in one go
      var stockDoesExistInOurDb = this.checkStockDoesntExistInOurDb()
      if (stockDoesExistInOurDb.length > 0) {
        var newStocks = await this.addNewStocks(stockDoesExistInOurDb).then((response) => { return response })
      }

      // Retrieve the stock ID that the user selected -> can use getOurStocks()
      var reloadStocks = await this.getOurStocks()
      if (reloadStocks) {
        // Store the user_id, stock_id, stock_price, volume in users_stocks table
        var stocksToBuythis = this.returnStocksWithStockID(reloadStocks)
        var allocationsStocks = this.returnAllocationswithStockID(stocksToBuythis, this.items)
   
        console.log(stocksToBuythis)



        // Store the fund_id, user_stock_id, allocations in funds_users_stocks table
        if (allocationsStocks && fund_id) {
          var allocateStocks = await this.addNewFundStocks(fund_id, allocationsStocks).then((response) => { return response })
          var placeMarketOrder = await this.placeMarketOrder().then((response) => { return response })


          if(allocateStocks && placeMarketOrder) {
            this.isCreatedFund = false
            Swal.fire({icon: 'success',title: 'Success',text: 'Fund successfully created!'})
            this.items = []
            this.fundInfo = []
            this.fundInterval = 0
            // this.$router.push({name: 'funds'})
          }
        }
      }
    
      } else if (this.totalAllocations < 100 || this.totalAllocations > 100) {
        // this trigger if unmaped stock is selected is less than 100 after minus the mapped stock
        Swal.fire({icon: 'error',title: 'Note',text: 'Stock allocation must equate to 100%'})
      }
    },
    placeMarketOrder() {
      var data = {
        "AdditionalInvest": this.fundInfo.fund_investment_amount,
        "allocations": this.returnAllocationsBasedOnPlaceMarketOrderFormat(),
      }

      return new Promise((resolve, reject) => {
        axios.post("http://localhost:5010/rebalance/" + customer_id, data).then((response) => {
            resolve(response.data.data)
          }).catch(error => {
            reject(error);
        });
      })


    },
    returnAllocationsBasedOnPlaceMarketOrderFormat() {
      var allocations = {}
      this.items.forEach((item) => {
        allocations[item.stock_symbol] = item.stock_allocation
      })
      return allocations
    },
    checkStockDoesntExistInOurDb() {
      return this.items.filter(f => !this.ourStockList.some(d => d.stock_symbol == f.stock_symbol) );
    },
    returnStocksWithStockID(arr1) {
      return arr1.filter(f => this.items.some(d => d.stock_symbol == f.stock_symbol) );
    },
    returnAllocationswithStockID(arr1, arr2) {
      return arr1.map(x => Object.assign(x, arr2.find(y => y.stock_symbol == x.stock_symbol)));
    },
    addNewFundStocks(fund_id,allocatedFunds) {
      // Store the fund_id, user_stock_id, allocations in funds_users_stocks table
      return new Promise((resolve, reject) => {
        var returnList = []

          for (var i = 0; i < allocatedFunds.length; i++) {
            var stock = allocatedFunds[i]
            var stockInfo = {fund_id: fund_id, stock_id: stock.stock_id, allocation: (stock.stock_allocation/100)}
            axios.post('http://localhost:5001/funds_stocks/add', stockInfo).then((response) => {
              returnList.push(response.data.data.stock_id)
              if (returnList.length == allocatedFunds.length) {resolve(returnList)}
            }).catch((error) => {
              reject(error)
            })
          }

          resolve(returnList)
      })
    },
    addNewStocks(stockList) {
      return new Promise((resolve, reject) => {
        var returnList = []

          for (var i = 0; i < stockList.length; i++) {
            var stock = stockList[i]
            var stockInfo = {stock_symbol: stock.stock_symbol, stock_name: stock.company}

            axios.post('http://localhost:5003/stocks/add', stockInfo).then((response) => {
              returnList.push(response.data.data.stock_id)
              if (returnList.length == stockList.length) {resolve(returnList)}
            }).catch((error) => {
              reject(error)
            })
          }

          resolve(returnList)
      })
    },
    addUserFund(userFundInfo) {
      return new Promise((resolve, reject) => {
        axios.post("http://localhost:5006/users_funds/add", userFundInfo).then((response) => {
            resolve(response.data.data)
          }).catch(error => {
            reject(error);
        });
      })
    },
    addNewFund() {
      return new Promise((resolve, reject) => {
        axios.post("http://localhost:5000/funds/add", this.fundInfo).then((response) => {
            resolve(response.data.data.fund_id)
          }).catch(error => {
            reject(error);
        });
      })
    },
    getCustomerStocks(customer_id) {
      return new Promise((resolve, reject) => {
        axios.get("http://localhost:5002/users_stocks/tbank/" + customer_id).then((response) => {
            resolve(response.data.data.user_stocks)
          }).catch(error => {
            reject(error);
        });
      })
    },
    getOurStocks() {
      return new Promise((resolve, reject) => {
        axios.get("http://localhost:5003/stocks-with-price").then((response) => {
            resolve(response.data.data.stocks)
          }).catch(error => {
            reject(error);
        });
      })
    },
    AddItem(symbol, company, price){
        var itemExist = this.items.filter(item => item.stock_symbol === symbol)
        if (itemExist ==  0) {
          this.items.push({stock_symbol: symbol,company: company,current_price: price,stock_allocation: NaN}) 
        } else {
          Swal.fire({icon: 'warning',title: 'Oops...',text: 'Stock is in the funds already!'})
        }
      },
      removeItem(symbol){
        this.items = this.items.filter((item) => item.stock_symbol != symbol);
      },
  },
  computed: {
    totalAllocations() {
      return this.items.reduce((a, c) => {
        return a + Number(c.stock_allocation);
      }, 0)
    },
  },
  template: `
  <!-- Modal -->
  <div class="spinner-border text-dark" role="status" v-if="!tbankStock_loaded" style="position: absolute;top:50%; left: 50%;margin-left: -50px;margin-top: -50px;">
    <span class="visually-hidden">Loading...</span>
  </div>

  <div class="createFundMain" v-else>
  <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="exampleModalLabel">Add new stock</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
              <div class="mb-3 row">
                  <label class="col-sm-4 col-form-label">Stock Symbol</label>
                  <div class="col-sm-8">
                      <select class="form-select" aria-label="Default select example" v-model="stockSelected">
                          <option selected v-for="item in ourStockList" :value="item" :key="item.stock_id">{{item.stock_name}}</option>
                        </select>
                  </div>
                </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="AddItem(this.stockSelected.stock_symbol, this.stockSelected.stock_name, this.stockSelected.stock_price.Price)">Add new stock</button>
          </div>
        </div>
      </div>
    </div>
  
      <h1>Create new fund</h1>
      <form @submit.prevent="createFund" method="POST">
          <div class="mb-3 row">
              <label for="inputFundName" class="col-sm-2 col-form-label">Fund Name</label>
              <div class="col-sm-10">
                <input type="text" class="form-control" v-model="fundInfo.fund_name" placeholder="E.g. my best fund">
              </div>
            </div>
            <div class="mb-3 row">
              <label for="inputInitialValue" class="col-sm-2 col-form-label">Initial Investment Value</label>
              <div class="col-sm-10">
                <input type="text" class="form-control" v-model="fundInfo.fund_investment_amount">
              </div>
            </div>
            <div class="mt-3 mb-3 row">
              <label for="inputInterval" class="col-sm-2 col-form-label">Fund Interval (Days)</label>
              <div class="col-sm-10">
                <input type="text" class="form-control" placeholder="30" max="1080" v-model="fundInterval">
              </div>
            </div>
  
            <div class="mt-3 mb-3 row">
              <h3>TBank Stocks</h3>
              <table class="table table-hover">
                  <thead>
                  <tr>
                      <th>Stock Symbol</th>
                      <th>Company</th>
                      <th>Order Price</th>
                      <th>Map to Fund?</th>
                  </tr>
                  </thead>
                  
                 <tbody>
                      <tr v-if="tbank_stocks.length > 0" v-for="(stock, index) in tbank_stocks[0]" :key="index" v-if="tbankStock_loaded">
                          <td>{{stock.symbol}}</td>
                          <td>{{stock.company}}</td>
                          <td>$ {{stock.price}}</td>
                          <td><button class="btn btn-primary" @click="AddItem(stock.symbol, stock.company, stock.price)">Map</button></td>
                      </tr>
                      
                      </tbody>
              </table>
            </div>
  
            <div class="mb-3 row">
              <h3>New fund stocks</h3>
              <table class="table table-hover">
                  <thead>
                  <tr>
                      <th>Stock Symbol</th>
                      <th>Company</th>
                      <th>Current Price</th>
                      <th>Stock Allocation</th>
                      <th>Actions</th>
                  </tr>
                  </thead>
                 <tbody>
                      <tr v-if="items.length > 0" v-for="(item, index) in items" :key="index">
                          <td>{{item.stock_symbol}}</td>
                          <td>{{item.company}}</td>
                          <td>$ {{item.current_price}}</td>
                          <td><input type="number" v-model="item.stock_allocation"> %</td>
                          <td><button class="btn btn-danger" @click="removeItem(item.stock_symbol)">Unmap</button></td>
                      </tr>
                      
                      </tbody>
              </table>
              <div class="d-flex justify-content-between">
                  <p><span class="fw-bold">Total Stock Allocation:</span> {{totalAllocations}}%</p>   
              </div>
            </div>
            <div class="d-flex justify-content-between">
            <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exampleModal">Add new stock</button>
            <button type="button" class="btn btn-dark" @click="createFund">Create Fund</button>
            </div>
      </form>
      </div>
        `,
});

createFund.mount("#createfunds");
