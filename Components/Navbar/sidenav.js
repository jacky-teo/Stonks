const sidenav = Vue.createApp({});

//navbar vue component
sidenav.component("sidenav", {
    data() {
        return {
            appName: "stonks",
            toggleClick: false,
            modeClick: false,
            authenticated: []
        };
    },
    methods: {
        logout() {
            sessionStorage.clear();
            window.location.replace("login.html");
            axios({
                method: "post",
                url: "http://127.0.0.1:5005/logout",
                // data: getUser.json()
            })
            .then(response => {
                console.log(response);
                // window.location.href = 'http://127.0.1:5500/index.html';
            })
            .catch(error => {
                console.error(error);
                this.message = "Login Failed, Please try again!";
                this.processing = false;
            });
        },
    },
    computed: {
        links(){
            return{
            dashboardLink: "index.html",
            fundsLink: "create-fund.html",
            myStocksLink: "mystocks.html",
            }
        },
        toggleClass() {
            return this.toggleClick ? 'close' : '';
        },
        modeClass() {
            return this.modeClick ? 'dark' : '';
        },
    },
    mounted() {
        let user_id = sessionStorage.getItem('user_id')
        
        if (user_id == "" || user_id == null) {
            window.location.replace("login.html");
        }

    },
    template: `
    <nav class="sidebar" :class="[toggleClass, modeClass]">
        <header>
                <div class="text logo-text">
                    <span class="name">Stonks.</span>
                </div>

            <button class='bx bx-chevron-right toggle' @click="toggleClick = !toggleClick"></button>
        </header>

        <div class="menu-bar">
            <div class="menu">

                <ul class="menu-links">
                    <li class="nav-link">
                        <a :href=links.dashboardLink>
                            <i class='bx bx-home-alt icon'></i>
                            <span class="text nav-text">Dashboard</span>
                        </a>
                    </li>
                    <li class="nav-link">
                        <a :href=links.myStocksLink>
                            <i class='bx bx-wallet icon'></i>
                            <span class="text nav-text">My Stocks</span>
                        </a>
                    </li>
                    <li class="nav-link">
                        <a :href=links.fundsLink>
                            <i class='bx bx-bar-chart-alt-2 icon'></i>
                            <span class="text nav-text">Create Fund</span>
                        </a>
                    </li>
                </ul>
            </div>

            <div class="bottom-content">
                <hr>
                <li class="nav-link">
                    <a href="#" @click=logout>
                        <i class='bx bx-log-out icon'></i>
                        <span class="text nav-text">Logout</span>
                    </a>
                </li>

                <li class="mode">
                    <div class="sun-moon">
                        <i class='bx bx-sun icon sun'></i>
                        <i class='bx bx-moon icon moon'></i>
                    </div>
                    <span class="mode-text text">Mode</span>

                    <div class="toggle-switch" @click="this.modeClick = !modeClick;">
                        <span class="switch"></span>
                    </div>
                </li>
                
            </div>
        </div>
    </nav>`,
    });
sidenav.mount("#sidenav");