const createFund = Vue.createApp({});
// Stocks Component
createFund.component("createfunds", {
  data() {
    return {
        items: [],
        stocks: {},
        tbank_stocks: [],
        total_allocations: 0,
        tbankStock_loaded: false,
        stockExistInFund: false,
    };
  },
   async mounted() {
    var loadTbankStocks = await this.getStocks()
    console.log(loadTbankStocks)
    loadTbankStocks ? this.tbankStock_loaded = true : console.log("Error loading stocks")
    this.tbank_stocks = loadTbankStocks
  },
  watch: {
    
  },
  methods: {
    getStocks() {
      var customer_id = 1

      return new Promise((resolve, reject) => {
        axios.get("http://localhost:5002/users_stocks/tbank/" + customer_id).then((response) => {
            resolve(response.data.data.user_stocks)
          }).catch(error => {
            reject(error);
        });
      })
     
    },
    currentDate() {
        const current = new Date();
        const date = `${current.getDate()}/${current.getMonth()+1}/${current.getFullYear()}`;
        return date;
      },
    AddItem(symbol, company, price){
        var itemExist = this.items.filter(item => item.stock_symbol === symbol)
        itemExist == 0 ?  this.items.push({stock_symbol: symbol,company: company,current_price: price,stock_allocation: 0}) : this.stockExistInFund=true; // only push non duplicate items
      },
      removeItem(){
        this.items.splice(this.items, 1)
      },
      calculateAllocations(amount, stock) {
        this.stocks[stock] = amount;
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
                      <select class="form-select" aria-label="Default select example">
                          <option selected>Open this select menu</option>
                        </select>
                  </div>
                </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            <button type="button" class="btn btn-primary">Add new stock</button>
          </div>
        </div>
      </div>
    </div>
  
      <h1>Create new fund</h1>
      <form @submit.prevent="createFund" method="POST">
          <div class="mb-3 row">
              <label for="inputFundName" class="col-sm-2 col-form-label">Fund Name</label>
              <div class="col-sm-10">
                <input type="text" class="form-control" id="inputFundName" placeholder="E.g. my best fund">
              </div>
            </div>
            <div class="mb-3 row">
              <label for="inputInitialValue" class="col-sm-2 col-form-label">Initial Investment Value</label>
              <div class="col-sm-10">
                <input type="text" class="form-control" id="inputInterval">
              </div>
            </div>
            <div class="mb-3 row">
              <label for="inputGoal" class="col-sm-2 col-form-label">Fund Goal</label>
              <div class="col-sm-10">
                <input type="text" class="form-control" id="inputGoal">
              </div>
            </div>
            <div class="mt-3 mb-3 row">
              <label for="inputInterval" class="col-sm-2 col-form-label">Fund Interval (Days)</label>
              <div class="col-sm-10">
                <input type="text" class="form-control" id="inputInterval" placeholder="30">
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
                          <td>{{item.current_price}}</td>
                          <td><input type="number" v-model="item.stock_allocation"> %</td>
                          <td><button class="btn btn-danger" @click="removeItem">Unmap</button></td>
                      </tr>
                      
                      </tbody>
              </table>
              <div class="d-flex justify-content-between">
                  <p><span class="fw-bold">Total Stock Allocation:</span> {{totalAllocations}}%</p>   
              </div>
            </div>
            <div class="d-flex justify-content-between">
            <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exampleModal">Add new stock</button>
            <button type="button" class="btn btn-dark">Create Fund</button>
            </div>
      </form>
        `,
});

createFund.mount("#createfunds");
