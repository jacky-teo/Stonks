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
      var serviceName = "getStockPrice"
      var userID = "B930284"
      var PIN = "828676"
      var OTP = "999999"
      var symbol = "IBM"

      axios.get("http://localhost:5003/stocks").then((response) => {
            this.stockList = response.data.data.stocks;
          });

      // set request parameters
      var userID = "";
      var PIN = "";
      var serviceName = "getStockPrice";
      var OTP = ""
      var symbol = "IBM"

      var headerObj = {
        Header: {
            serviceName: serviceName,
            userID: userID,
            PIN: PIN,
            OTP: OTP
        }
    };
    
    var contentObj = {
        Content: {
            symbol: symbol,
        }
    };
        
    var header = JSON.stringify(headerObj);
    var content = JSON.stringify(contentObj);

    // setup http request
    var xmlHttp = new XMLHttpRequest();
    if (xmlHttp === null){
        alert("Browser does not support HTTP request.");
        return;
    }
    xmlHttp.open("POST", "http://tbankonline.com/SMUtBank_API/Gateway"+"?Header="+header+"&Content="+content, true);
    xmlHttp.timeout = 5000;

    // setup http event handlers
    xmlHttp.onreadystatechange = function() {
        if (xmlHttp.readyState === 4 && xmlHttp.status === 200) {
            responseObj = JSON.parse(xmlHttp.responseText);
            serviceRespHeader = responseObj.Content.ServiceResponse.ServiceRespHeader;
            globalErrorID = serviceRespHeader.GlobalErrorID;
            if (globalErrorID === "010041"){
                showOTPModal(1);
                return;
            }
            else if (globalErrorID !== "010000"){
                showErrorModal(serviceRespHeader.ErrorDetails);
                return;
            }
            
            // get data
            stockDetails = responseObj.Content.ServiceResponse.Stock_Details;
            volume = stockDetails.volume;
            symbol2 = stockDetails.symbol;
            price = stockDetails.price;
            percentageChange = stockDetails.percentageChange;
            tradingDate = stockDetails.tradingDate;
            change = stockDetails.change;
            company = stockDetails.company;
            prevClose = stockDetails.prevClose;

            // display data
            console.log(price)
            
        }
    };
    xmlHttp.ontimeout = function (e) {
        showErrorModal("Timeout invoking API.");
        return;
    };					

    // send the http request
    xmlHttp.send();


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
