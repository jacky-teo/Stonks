const createFund = Vue.createApp({});


createFund.component("loader", {
  data() {
    return {
        message: 'Welcome to Vue!'
    };
  },
  props: ['loading_message'],
  methods: { },
  template: `
  <div id="mask">
  <div id="popup" class="popup"> 
 <svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
   viewBox="0 0 100 100" style="enable-background:new 0 0 100 100;" xml:space="preserve">
<path class="st0" d="M48.8,83.4L20.2,66.9c-0.4-0.2-0.7-0.7-0.7-1.2v-33c0-0.5,0.3-0.9,0.7-1.2l28.6-16.5c0.4-0.2,1-0.2,1.4,0
  l28.6,16.5c0.4,0.2,0.7,0.7,0.7,1.2v33c0,0.5-0.3,0.9-0.7,1.2L50.2,83.4C49.8,83.7,49.2,83.7,48.8,83.4z"/>
<g>
  <defs>
    <path id="SVGID_1_" d="M48.8,82.3L21.2,66.3c-0.4-0.2-0.7-0.7-0.7-1.2V33.2c0-0.5,0.3-0.9,0.7-1.2l27.6-15.9c0.4-0.2,1-0.2,1.4,0
      l27.6,15.9c0.4,0.2,0.7,0.7,0.7,1.2v31.9c0,0.5-0.3,0.9-0.7,1.2L50.2,82.3C49.8,82.5,49.2,82.5,48.8,82.3z"/>
  </defs>
  <clipPath id="SVGID_2_">
    <use xlink:href="#SVGID_1_"  style="overflow:visible;"/>
  </clipPath>
  <g class="st1">
   <g class="cboard"> 
    <path class="st0" d="M66.3,33.3h9.6c2.1,0,3.8,1.7,3.8,3.8v50.8H34.8V37.1c0-2.1,1.7-3.8,3.8-3.8h8.9"/>
    <path class="st2" d="M65.2,37.2H48.6c-1,0-1.7-0.9-1.5-1.9l1.4-7.5c0.1-0.7,0.8-1.3,1.5-1.3h13.7c0.8,0,1.4,0.5,1.5,1.3l1.4,7.5
      C66.9,36.3,66.1,37.2,65.2,37.2z"/>
    <g>
      <polyline class="st3" points="41.1,46.6 42.6,48.1 46.6,44.1"/>
    </g>
    <g>
      <g>
        <line class="st3" x1="41.3" y1="59.3" x2="45.3" y2="55.4"/>
        <line class="st3" x1="45.3" y1="59.3" x2="41.3" y2="55.4"/>
      </g>
    </g>
    <g>
      <polyline class="st3" points="41.1,69.1 42.6,70.5 46.6,66.6"/>
    </g>
    <g>
      <polyline class="st3" points="41.1,80.3 42.6,81.8 46.6,77.8"/>
    </g>
    <g>
      <rect x="57.7" y="43.6" class="st4" width="17" height="2.2"/>
      <rect x="50" y="43.6" class="st4" width="5.9" height="2.2"/>
      <rect x="50" y="47.1" class="st4" width="9.5" height="2.2"/>
      <rect x="61.3" y="47.1" class="st4" width="10.7" height="2.2"/>
    </g>
    <g>
      <rect x="57.7" y="57.9" class="st4" width="8.5" height="2.2"/>
      <rect x="67.6" y="57.9" class="st4" width="7.7" height="2.2"/>
      <rect x="50" y="57.9" class="st4" width="5.9" height="2.2"/>
      <rect x="50" y="54.3" class="st4" width="9.5" height="2.2"/>
      <rect x="61.3" y="54.3" class="st4" width="10.7" height="2.2"/>
    </g>
    <g>
      <rect x="54.7" y="69.4" class="st4" width="13.5" height="2.2"/>
      <rect x="69.6" y="69.4" class="st4" width="5.7" height="2.2"/>
      <rect x="50" y="69.4" class="st4" width="2.9" height="2.2"/>
      <rect x="50" y="65.8" class="st4" width="15.5" height="2.2"/>
      <rect x="67.3" y="65.8" class="st4" width="4.7" height="2.2"/>
    </g>
    <g>
      <rect x="54.7" y="80.4" class="st4" width="13.5" height="2.2"/>
      <rect x="69.6" y="80.4" class="st4" width="5.7" height="2.2"/>
      <rect x="50" y="80.4" class="st4" width="2.9" height="2.2"/>
      <rect x="50" y="76.8" class="st4" width="15.5" height="2.2"/>
      <rect x="67.3" y="76.8" class="st4" width="4.7" height="2.2"/>
    </g>
    </g>
  </g>
</g>
<g>
  <path class="st5" d="M22.3,76.4l0.1-37.7c0-2.4,2.2-4.4,4.9-4.4c2.7,0,4.9,2,4.9,4.4l-0.1,37.8l-4.7,8.2L22.3,76.4z"/>
  <path class="st2" d="M27.3,79.9l-2.5-5.7l0.1-34.3c0-1.3,1.1-2.4,2.4-2.4h0c1.3,0,2.4,1.1,2.4,2.4l-0.1,34.4L27.3,79.9z"/>
  <path class="st2" d="M25,73.3c0,0,2-1,4.4,0"/>
  <line class="st2" x1="24.9" y1="44.4" x2="29.7" y2="44.4"/>
</g> 
</svg> 
  {{ loading_message }}
</div>  
</div>
        `,
});




// Stocks Component
createFund.component("createfunds", {
  data() {
    return {
        items: [],
        user_id: 2,
        fundInfo: {
            fund_name: "",
            fund_investment_amount: 0,
            fund_interval: 0
        },
        stocks: {},
        ourStockList: [],
        mainStockList: [],
        tbank_stocks: [],
        stockSelected: [],
        total_allocations: 0,
        tbankStock_loaded: false,
        stockExistInFund: false,
        isCreatedFund: false,
        isInProgress: false,
        progressMessage: "loading...",
    };
  },
   async mounted() {
    this.user_id = sessionStorage.getItem("user_id");
    var loadTbankStocks = await this.getCustomerStocks(this.user_id)
    var loadStocksThatIsNotInCustomerStocks = await this.getListStocks(this.user_id)
    var loadMainStockList = await this.getOurStocks()
    console.log(loadMainStockList)
    // var loadCustomerStocksInStonks = await this.updateStonksDb(this.user_id)
    loadTbankStocks && loadStocksThatIsNotInCustomerStocks && loadMainStockList ? this.tbankStock_loaded = true : console.log("Error loading stocks")
    this.tbank_stocks = loadTbankStocks
    this.ourStockList = loadStocksThatIsNotInCustomerStocks
    this.mainStockList = loadMainStockList
  },
  methods: {
    async createFund() {

      if(this.totalAllocations == 100 && this.fundInfo.fundName != "" && this.fundInfo.fund_investment_amount != 0 && this.fundInfo.fund_interval != 0) {
        // Set the spinner to turn on
        this.isCreatedFund = true
        this.isInProgress = true
      // Create fund in funds table -> get fund_id
        var fund_id = await this.addNewFund().then((response) => { return response })
        this.progressMessage = "Creating fund..."
        

      // Create new row in users_funds table with fund_id and user_id
      if (fund_id) {
        var userFundInfo = {user_id: this.user_id, fund_id: fund_id}
        var userFund_id = await this.addUserFund(userFundInfo).then((response) => { return response })
      }
      this.progressMessage = "Linking funds to user..."

      // Create stocks that does not exist in our database in stocks table & allow multiple stocks to be added in one go
      var stockDoesExistInOurDb = this.checkStockDoesntExistInOurDb()
      if (stockDoesExistInOurDb.length > 0) {
        var newStocks = await this.addNewStocks(stockDoesExistInOurDb).then((response) => { return response })
      }
      this.progressMessage = "Adding new stocks to our database..."

      // Retrieve the stock ID that the user selected -> can use getOurStocks()
      var reloadStocks = await this.getOurStocks()
      if (reloadStocks) {
        // Store the user_id, stock_id, stock_price, volume in users_stocks table
        var stocksToBuythis = this.returnStocksWithStockID(reloadStocks)
        var allocationsStocks = this.returnAllocationswithStockID(stocksToBuythis, this.items)
        this.progressMessage = "Get allocations of stocks to purchase..."
        // console.log(stocksToBuythis)

        var userInfo = await this.returnUserInfo().then((response) => { return response })
  

        // Store the fund_id, user_stock_id, allocations in funds_users_stocks table
        if (allocationsStocks && fund_id && userInfo) {
          var allocateStocks = await this.addNewFundStocks(fund_id, allocationsStocks).then((response) => { return response })
          var placeMarketOrder = await this.placeMarketOrder(userInfo.user_acc_id, userInfo.user_pin, userInfo.settlement_acc).then((response) => { return response })
          console.log(placeMarketOrder) 
          // var createTransaction = await this.createTransaction().then((response) => { return response })
          // console.log(placeMarketOrder) 
          this.progressMessage = "Placing market order..."
          this.isInProgress = false

          if(allocateStocks && placeMarketOrder) {
            this.isCreatedFund = false
            var sendSMS = await this.sendConfirmationSMS(userInfo.user_acc_id, userInfo.user_pin)
            Swal.fire({icon: 'success',title: 'Success',text: 'Fund successfully created!'}).then((result) => {
              if (result.isConfirmed) {
                window.location.href = "create-fund.html"
              }
            })
            this.items = []
            this.fundInfo = []
            // this.$router.push({name: 'funds'})
          }
        }
      }
    
      } else if (this.totalAllocations < 100 || this.totalAllocations > 100) {
        // this trigger if unmaped stock is selected is less than 100 after minus the mapped stock
        Swal.fire({icon: 'error',title: 'Note',text: 'Stock allocation must equate to 100%'})
      } else if (this.fundInfo.fundName == "") {
        Swal.fire({icon: 'error',title: 'Note',text: 'Fund name is required'})
      } else if (this.fundInfo.fund_investment_amount == 0) {
        Swal.fire({icon: 'error',title: 'Note',text: 'Fund investment amount is required'})
      } else if (this.fundInfo.fund_interval == 0) {
        Swal.fire({icon: 'error',title: 'Note',text: 'Fund interval is required'})
      } 
    },
    placeMarketOrder(tBankUID, tBankPin, tBankSettlementAccount) {
      return new Promise((resolve, reject) => {
        var data = {
          "userID": tBankUID,
          "PIN": tBankPin, 
          "additionalInvest": this.fundInfo.fund_investment_amount,
          "allocation": JSON.stringify(this.returnAllocationsBasedOnPlaceMarketOrderFormat()).replace(/\\"/g, '"'),
          "settlement_account": tBankSettlementAccount,
        }
        // console.log(data)
        axios.post("http://localhost:5010/rebalance", data).then((response) => {
            resolve(response)
          }).catch(error => {
            reject(error);
        });
      })


    },
    returnUserInfo() {
      return new Promise((resolve, reject) => {
        axios.post("http://localhost:5005/user_info/user/" + this.user_id).then((response) => {
            resolve(response.data.data)
          }).catch(error => {
            reject(error);
        });
      })
    },
    returnAllocationsBasedOnPlaceMarketOrderFormat() {
      var allocations = {}
      this.items.forEach((item) => {
        allocations[item.stock_symbol] = (item.stock_allocation/100)
      })
      return allocations
    },
    checkStockDoesntExistInOurDb() {
      return this.items.filter(f => !this.mainStockList.some(d => d.stock_symbol == f.stock_symbol) );
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
    getListStocks(customer_id) {
      return new Promise((resolve, reject) => {
        axios.get("http://localhost:5002/not_owned_stocks/tbank/" + customer_id).then((response) => {
            resolve(response.data.data.stocks)
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
    // updateStonksDb(customer_id) {
    //   return new Promise((resolve, reject) => {
    //     axios.get("http://localhost:5002/updateStonksDB/"+ customer_id).then((response) => {
    //         resolve(response)
    //       }).catch(error => {
    //         reject(error);
    //     });
    //   })
    // },
    sendConfirmationSMS(userID, PIN) {
      return new Promise((resolve, reject) => {
        data = {
          "message" : 'You made a Fund creation at Stonks at ' + this.getNow() + ' SG Time. If unauthorised, call 24/7 Fraud Hotline.',
          "userID": userID,
          "PIN": PIN.toString(),
        }
        console.log(data)
        axios.post("http://localhost:5004/common/sendSMS", data).then((response) => {
            resolve(response)
          }).catch(error => {
            reject(error);
        });
      })
    },
    getNow() {
      const today = new Date();
      var suffix = today.getHours() >= 12 ? "PM":"AM";
      const month = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
      const date = today.getDate()+'-'+(month[today.getMonth()])+'-'+today.getFullYear();
      var hours = ((today.getHours() + 11) % 12 + 1)
      const time = hours + ":" + today.getMinutes() + suffix;
      const dateTime = time +', '+ date;
      return dateTime;
    },
      AddItem(symbol, company, price){
        var itemExist = this.items.filter(item => item.stock_symbol === symbol)
        // console.log(this.items)
        if (itemExist ==  0) {
          this.items.push({stock_symbol: symbol,company: company,current_price: price,stock_allocation: NaN}) 
        } else {
          Swal.fire({icon: 'warning',title: 'Oops...',text: 'Stock is in the funds already!'})
        } 
      },
      removeItem(symbol){
        this.items = this.items.filter((item) => item.stock_symbol != symbol);
      },
      mappedStocks(mapp) {
        return mapp ? ' btn-secondary' : ' btn-primary';
      },
      mappedStockName(mapp) {
        return mapp ? 'Mapped' : 'Map';
      }
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
  
  
  <loader v-show="isInProgress" :loading_message="progressMessage"></loader>


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
            <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="AddItem(this.stockSelected.stock_symbol, this.stockSelected.stock_name, this.stockSelected.stock_price)">Add new stock</button>
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
                <input type="text" class="form-control" placeholder="30" max="1080" v-model="fundInfo.fund_interval">
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
                          <td><button class="btn" v-bind:class="mappedStocks(stock.mapped)" @click="AddItem(stock.symbol, stock.company, stock.price)" :disabled="stock.mapped == 1">{{ mappedStockName(stock.mapped) }}</button></td>
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
