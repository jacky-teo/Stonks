const createFund = Vue.createApp({});
// Stocks Component
createFund.component("createfunds", {
  data() {
    return {
        items: [],
        fundInfo: {
            fundName: "",
            fundIvestment: 0,
            fundGoal: 0,
            FundInterval: 0
        },
        stocks: {},
        ourStockList: [],
        tbank_stocks: [],
        stockSelected: [],
        total_allocations: 0,
        tbankStock_loaded: false,
        stockExistInFund: false,
    };
  },
   async mounted() {
    var customer_id = 1;
    var loadTbankStocks = await this.getCustomerStocks(customer_id)
    var loadOurStocks = await this.getOurStocks(customer_id)
    loadTbankStocks && loadOurStocks ? this.tbankStock_loaded = true : console.log("Error loading stocks")
    this.tbank_stocks = loadTbankStocks
    this.ourStockList = loadOurStocks
  },
  methods: {
    createFund() {
      if(this.totalAllocations == 100) {

      // Create fund in funds table -> get fund_id
      var fund_id = new Promise((resolve, reject) => {
        axios.get("http://localhost:5000/funds/add", fundInfo).then((response) => {
            resolve(response.data.data.fund_id)
          }).catch(error => {
            reject(error);
        });
      })

      // Create new row in users_funds table with fund_id and user_id
      if (fund_id) {
        var user_id = 1
        var userFundInfo = {
          user_id: user_id,
          fund_id: fund_id
        }
        axios.get("http://localhost:5006/users_funds/add", userFundInfo).then((response) => {
            console.log(response.data)
          }).catch(error => {
            console.log(error);
        });
      }

      // Create stocks that does not exist in our database in stocks table

      // Retrieve the stock ID that the user selected -> can use getOurStocks()

      // Use Vas helper function (get_ending_shares_no) to get the ending shares no
      // Place Market Order to buy the stock that does not exist in the fund

      // Store the user_id, stock_id, stock_price, volume in users_stocks table

      // Store the fund_id, user_stock_id, allocations in funds_users_stocks table
      } else if (this.totalAllocations > 100) {
        Swal.fire({icon: 'error',title: 'Note',text: 'Stock allocation must equate to 100%'})
      }
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
    getOurStocks(customer_id) {
      return new Promise((resolve, reject) => {
        axios.get("http://localhost:5003/stocks-with-price/" + customer_id).then((response) => {
            resolve(response.data.data.stocks)
          }).catch(error => {
            reject(error);
        });
      })
    },
    AddItem(symbol, company, price){
        var itemExist = this.items.filter(item => item.stock_symbol === symbol)
        if (itemExist ==  0) {
          this.items.push({stock_symbol: symbol,company: company,current_price: price,stock_allocation: 0}) 
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
                <input type="text" class="form-control" id="inputFundName" v-model="fundInfo.fundName" placeholder="E.g. my best fund">
              </div>
            </div>
            <div class="mb-3 row">
              <label for="inputInitialValue" class="col-sm-2 col-form-label">Initial Investment Value</label>
              <div class="col-sm-10">
                <input type="text" class="form-control" id="inputInterval" v-model="fundInfo.fundIvestment">
              </div>
            </div>
            <div class="mb-3 row">
              <label for="inputGoal" class="col-sm-2 col-form-label">Fund Goal</label>
              <div class="col-sm-10">
                <input type="text" class="form-control" id="inputGoal" v-model="fundInfo.fundGoal">
              </div>
            </div>
            <div class="mt-3 mb-3 row">
              <label for="inputInterval" class="col-sm-2 col-form-label">Fund Interval (Days)</label>
              <div class="col-sm-10">
                <input type="text" class="form-control" id="inputInterval" placeholder="30" max="1080" v-model="fundInfo.fundInterval">
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
