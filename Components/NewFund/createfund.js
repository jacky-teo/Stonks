const createFund = Vue.createApp({});
// Stocks Component
createFund.component("createfunds", {
  data() {
    return {
        items: [
            {
              name: '',
              quantity: 0,
              amount: 0,
              total: 0
            }
          ]
    };
  },
  async created() {
        // await this.getStocks();
  },
  watch: {
    'items': {
      handler (newValue, oldValue) {
        newValue.forEach((item) => {
          item.total = item.quantity * item.amount
        })
      },
      deep: true
    }
  },
  methods: {
    getStocks() {
      var customer_id = 1

      axios.get("http://localhost:5003/users_stocks/tbank/" + customer_id).then((response) => {
            this.stockList = response.data.data.stocks;
          });
    },
    currentDate() {
        const current = new Date();
        const date = `${current.getDate()}/${current.getMonth()+1}/${current.getFullYear()}`;
        return date;
      },
    AddItem(){
        this.items.push({
          name: '',
          quantity: 0,
          amount: 0,
          total: 0
        })
      },
      removeItem(){
        this.items.splice(this.items, 1)
      }
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
      <form>
          <div class="mb-3 row">
              <label for="staticEmail" class="col-sm-2 col-form-label">Fund Name</label>
              <div class="col-sm-10">
                <input type="text" class="form-control" id="staticEmail" placeholder="E.g. my best fund">
              </div>
            </div>
            <div class="mb-3 row">
              <label for="inputInitialValue" class="col-sm-2 col-form-label">Initial Investment Value</label>
              <div class="col-sm-10">
                <input type="text" class="form-control" id="inputInterval">
              </div>
            </div>
            <div class="mb-3 row">
              <label for="inputPassword" class="col-sm-2 col-form-label">Fund Interval (Days)</label>
              <div class="col-sm-10">
                <input type="text" class="form-control" id="inputInterval" placeholder="30">
              </div>
            </div>
  
            <div class="mb-3 row">
              <h3>TBank Stocks</h3>
              <table id="my_table_1" data-toggle="table" data-sort-stable="true">
                  <thead>
                  <tr>
                      <th data-sortable="true">Stock Symbol</th>
                      <th data-sortable="true">Company</th>
                      <th data-sortable="true">Order Price</th>
                      <th data-sortable="false">Map to Fund?</th>
                  </tr>
                  </thead>
                 <tbody>
                      <tr>
                          <td>CC3.SI</td>
                          <td>StarHub</td>
                          <td>$300</td>
                          <td><button class="btn btn-primary">Map</button></td>
                      </tr>
                      
                      </tbody>
              </table>
            </div>
  
            <div class="mb-3 row">
              <h3>New fund stocks</h3>
              <table id="my_table_1" data-toggle="table" data-sort-stable="true">
                  <thead>
                  <tr>
                      <th data-sortable="true">Stock Symbol</th>
                      <th data-sortable="true">Company</th>
                      <th data-sortable="true">Current Price</th>
                      <th data-sortable="false">Stock Allocation</th>
                      <th data-sortable="false">Actions</th>
                  </tr>
                  </thead>
                 <tbody>
                      <tr>
                          <td>DBS</td>
                          <td>DBS</td>
                          <td>$300</td>
                          <td><input type="text"> %</td>
                          <td><button class="btn btn-danger">Unmap</button></td>
                      </tr>
                      
                      </tbody>
              </table>
              <div class="d-flex justify-content-between">
                  <p><span class="fw-bold">Total Stock Allocation:</span> 60%</p>   
              </div>
            </div>
            <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exampleModal">Add new stock</button>
            <button type="button" class="btn btn-dark">Create Fund</button>
      </form>
        `,
});

createFund.mount("#createfunds");
