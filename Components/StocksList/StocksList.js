const stocklist = Vue.createApp({});
// Stocks Component
stocklist.component("stockslist", {
  data() {
    return {
      stockList: [],
      stockTitle: ["Symbol", "Name", "Price", "Change %", "Volume"],
    };
  },
  async created() {
        await this.getStocks();
  },
  methods: {
    getStocks() {
      axios.get("http://localhost:5003/stocks").then((response) => {
            this.stockList = response.data.data.stocks;
          });
      console.log(Math.floor(Date.now() / 1000))
    }
  },
  template: `
    <div>
        <h1 class="text-center">Stocks</h1>
    </div>     
    <h3 class="my-5 mx-auto" v-if="stockList.length == 0">Ooops.. there is no stocks now...</h3>
    <table class="table" v-else>
  <thead>
    <tr>
      <th scope="col" v-for="(value, key) in stockTitle" v-bind:key="key">{{value}}</th>
    </tr>
  </thead>
  <tbody>
    <tr v-for="(value, key) in stockList" v-bind:key="key">
      <td>{{value.stock_symbol}}</td>
      <td>{{value.stock_name}}</td>
    </tr>
  </tbody>
  </table>
        `,
});

stocklist.mount("#stockslist");
