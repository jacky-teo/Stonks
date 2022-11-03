const fund = Vue.createApp({})

// Funds Component
fund.component('fundslist', {
    data() {
        return {
            appName: 'Fundslist',
            fundList: [],
            users_funds_list: [],
            user_id: 1,
            mappedList: [],


        };
    },
    async created() {
        await this.getUsersFunds();
        this.user_id = sessionStorage.getItem("user_id");
        console.log(this.user_id);
        
    },
    computed: {
    },
    methods: {
        getUsersFunds() {
            axios.get('http://localhost:5006/funds/user_funds/' + this.user_id)
                .then(response => {
                    
                    this.users_funds_list = response.data.data;
                    console.log(this.users_funds_list)
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
            <div class="col-md-4 col-sm-4 d-sm-block align-items-left" v-for="fund in users_funds_list" v-bind:key="fund">
                <div class="card mb-4 shadow-sm">
                    <div class="card-body">
                        <p class="card-text"><b>Name:</b> {{fund.fund_name}}</p>
                        <p class="card-text"><b>Fund ID: </b> {{fund.fund_id}}</p>
                        <p class="card-text"><b>Initial Investment: </b>\$ {{fund.fund_investment_amount}}</p>
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