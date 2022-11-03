const UnownedStocks = Vue.createApp({})
// Unowned Stocks Component
UnownedStocks.component('unownedstocks', {
    data() {
        return {
            appName: 'Unowned Stocks',
            stockList: [],
            users_stocks_list: [],
            user_id: 1,
        };
    },
    async created() {
        await this.getUnownedStocks();
        this.user_id = sessionStorage.getItem("user_id");
    },
    computed: {
    },
    methods: {
        getUnownedStocks() {
            axios.get('http://localhost:5002/not_owned_stocks/tbank/' + this.user_id)
                .then(response => {
                    
                    this.stockList = response.data.data.stocks;
                    console.log(this.stockList);
                }
                )
                .catch(error => {
                    console.log(error);
                }
                );
        }
    },
    template: `
    <div>
        <h1 class="text-center">Unowned Stocks</h1>
        <div class="table">
            <table class="table table-striped table-hover">
                <thead>
                    <tr>
                        <th scope="col">Stock Name</th> 
                        <th scope="col">Stock Symbol</th>
                        <th scope="col">Stock Price</th>
                        
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="stock in stockList" v-bind:key="stock">
                        <td>{{stock.stock_name}}</td>
                        <td>{{stock.stock_symbol}}</td>
                        <td>{{stock.stock_price}}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
        `
});
UnownedStocks.mount('#unownedstocks')


