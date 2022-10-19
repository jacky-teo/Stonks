const sidenav = Vue.createApp({});

//navbar vue component
sidenav.component("sidenav", {
    data() {
      return {
        appName: "stonks",
        toggleClick: false,
        modeClick: false,
      };
    },
    computed: {
        links(){
            return{
            dashboardLink: "../dashboard",
            aggregationLink: "../aggregation",
            fundsLink: "../funds",
            notificationsLink: "../notifications",
            logOut: "../login/",
            }
        },

        toggleClass() {
            return this.toggleClick ? 'close' : '';
        },

        modeClass() {
            return this.modeClick ? 'dark' : '';
        },
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
                            <i class='bx bx-home-alt icon' ></i>
                            <span class="text nav-text">Dashboard</span>
                        </a>
                    </li>
                    <li class="nav-link">
                        <a :href=links.aggregationLink>
                            <i class='bx bx-pie-chart-alt icon' ></i>
                            <span class="text nav-text">Aggregation</span>
                        </a>
                    </li>
                    <li class="nav-link">
                        <a :href=links.fundsLink>
                            <i class='bx bx-bar-chart-alt-2 icon' ></i>
                            <span class="text nav-text">Funds</span>
                        </a>
                    </li>
                    <li class="nav-link">
                        <a :href=links.notificationsLink>
                            <i class='bx bx-bell icon'></i>
                            <span class="text nav-text">Notifications</span>
                        </a>
                    </li>
                </ul>
            </div>

            <div class="bottom-content">
                <hr>
                <li class="nav-link">
                    <a :href=links.logOut>
                        <i class='bx bx-log-out icon' ></i>
                        <span class="text nav-text">Logout</span>
                    </a>
                </li>

                <li class="mode">
                    <div class="sun-moon">
                        <i class='bx bx-sun icon sun'></i>
                        <i class='bx bx-moon icon moon'></i>
                    </div>
                    <span class="mode-text text">Mode</span>

                    <div class="toggle-switch" @click="modeClick = !modeClick">
                        <span class="switch"></span>
                    </div>
                </li>
                
            </div>
        </div>
    </nav>`,
    });
sidenav.mount("#sidenav");