const fund = Vue.createApp({})

// Funds Component
fund.component('fundslist', {
    data() {
        return {
            appName: 'Fundslist',
            fundList: [],
            users_funds_list: [],
            user_id: 1
            
            
        };
    },
    async created(){
        await this.getFunds();
        await this.getUsersFunds();
    },
    computed: {
        
    },
    methods: {
        getFunds() {
            axios.get('http://localhost:5000/funds')
                .then(response => {
                    this.fundList = response.data.data.funds;
                    console.log(this.fundList)
                })
                .catch(error => {
                    console.log(error);
                });
        },
        getUsersFunds() {
            axios.get('http://localhost:5006/users_funds/'+ this.user_id)
                .then(response => {
                    this.users_funds_list = response.data.users_funds;
                })
                .catch(error => {
                    console.log(error);
                });
        }
    },
    template: `
    <div>
        <h1 class="text-center">All Funds</h1>
        <div class="row">
            <div class="col-md-4 col-sm-4 d-sm-block align-items-left" v-for="fund in fundList" v-bind:key="fund">
                <div class="card mb-4 shadow-sm">
                    <div class="card-body">
                        <p class="card-text">Fund {{fund.fund_name}}</p>
                        <p class="card-text">Fund {{fund.fund_id}}</p>
                        <p class="card-text">Fund {{fund.fund_goals}}</p>
                        <p class="card-text">Fund {{fund.fund_investment}}</p>
                        <div class="d-flex justify-content-between align-items-center"> 
                            <div class="btn-group">
                                <button type="button" class="btn btn-sm btn-outline-secondary" :id="fund.fund_id" >View</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
        `
});

fund.mount('#fundslist')