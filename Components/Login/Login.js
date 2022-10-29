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
        login: function() {
            this.loading = true;
            axios.post("http://127.0.0.1:5005/login", {
                username: this.username,
                password: this.password
            })
            .then(response => {
                if (response.data.status == "success") {
                    this.processing = false;
                    this.$emit("authenticated", true, response.data.data);
                    window.location.href = 'http://127.0.1:5500/index.html'; // to update this link to dynamic.
                } else {
                    this.message = "Login Failed, Please try again!";
                }
            })
            .catch(error => {
                this.message = "Login Failed, Please try again!";
                this.processing = false;
            });
        }
    },
});
 
login.mount("#login");
 