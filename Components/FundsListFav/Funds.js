const fundfav = Vue.createApp({});

// Funds Component
fundfav.component('fundfav', {
    data(){
        return {
            appName: 'Funds',
            'Funds':[1,2,3,4]
        };
    },
    created() {

    },
    methods:{
        funds(){
            // Axios Fetch from Databse //
            return this.Funds;
        }
    },
    template:`
    <div>
        <h1 class="text-center">Favorites</h1>
        <div class="row">
            <div class="col-md-4 col-sm-4 d-sm-block align-items-left" v-for="fund in funds" v-bind:key="fund">
                <div class="card mb-4 shadow-sm">
                    <div class="card-body">
                        <p class="card-text">Fund {{fund}}</p>
                        <div class="d-flex justify-content-between align-items-center"> 
                            <div class="btn-group">
                                <button type="button" class="btn btn-sm btn-outline-secondary">View</button>
                                <button type="button" class="btn btn-sm btn-outline-secondary">Delete</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
        `
    });
        
fundfav.mount('#fundfav')