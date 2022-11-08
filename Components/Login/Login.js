const login = Vue.createApp({
    //resolving
    data() {
        return {
          username: "",
          password: "",
          processing: false,
          message: ""
        };
    },
    mounted() {
        let user_id = sessionStorage.getItem('user_id')
        
        if (user_id !== null) {
            window.location.replace("index.html");
        }
        
    },
    watch: {
        "username"(value){
            if (value && value.trim().length>0){
                this.message = ""
            }
            else {
                this.message = "Username cannot be empty."
            }
        },
        "password"(value){
            if (value && value.trim().length>0){
                this.message = ""
            }
            else {
                this.message = "Password cannot be empty."
            }
        },
    },
    computed: {
        isFormValid() {
            return (
                !this.username.trim() ||
                !this.password.trim() ||
                Object.values(this.message).some((error) => {
                    return error !== "";
                })
            );
        },
     },
    methods: {
        login() {
            this.loading = true;
            axios.post("http://localhost:5005/login", {
                username: this.username,
                password: this.password
            })
            .then(response => {
                if (response.data.status == "success") {
                    this.processing = false;
                    this.$emit("authenticated", true, response.data.data);
                    sessionStorage.setItem("user_id", response.data.data.id );
                    window.location.href = 'index.html';
                    
                } else {
                    this.message = "Login Failed, Please try again!";
                }
            })
            .catch(error => {
                console.error(error)
                this.message = "Login Failed, Please try again!";
                this.processing = false;
            });
        }
    },
});
 
login.mount("#login");
 