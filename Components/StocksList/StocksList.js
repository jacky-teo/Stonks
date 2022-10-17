const stocklist = Vue.createApp({});
// Stocks Component
stocklist.component("stockslist", {
  data() {
    return {
      stockList: [
        {
          Symbol: "TSLA",
          Price: "$388",
          Change: "$122",
          ChangePercent: "30%",
          Volume: "39000000",
        },
      ],
      stockTitle: ["Symbol", "Price", "Change", "Change %", "Volume"],
    };
  },
  computed: {
    stocks() {
      //   let response = axios
      //     .get("http://localhost:8000/api/stocks")
      //     .then((response) => {
      //       this.stockList = response.data;
      //     });

      return this.stockList;
    },
  },
  template: `
    <div>
        <h1 class="text-center">Stocks</h1>
    </div>     
    <h3 class="my-5 mx-auto" v-if="typeof stockList == null">Ooops.. there is no stocks now...</h3>
    <table class="table" v-else>
  <thead>
    <tr v-for="stock of stockTitle">
      <th scope="col">{{stock.title}}</th>
    </tr>
  </thead>
  <tbody>
    <tr v-for="listings of stockList">
      <th scope="row">{{listings.Symbol}}</th>
      <td>{{listings.Price}}</td>
        <td>{{listings.Change}}</td>
        <td>{{listings.ChangePercent}}</td>
        <td>{{listings.Volume}}</td>
    </tr>
  </tbody>
  </table>
        `,
});

stocklist.mount("#stockslist");
