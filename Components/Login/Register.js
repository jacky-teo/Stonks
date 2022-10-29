const register = Vue.createApp({
    //resolving
    data() {
        return {
            form:{
                username: "",
                password: "",
                user_acc_id: "",
                user_pin: "",
                settlement_acc: "",
            },
            alert: {
                alertBool: false,
                alertMsg: "",
                successBool: false,
                successMsg: "",
            },
            message: {
                username: "",
                password: "",
                user_acc_id: "",
                user_pin: "",
                settlement_acc: "",
            },
            processing: false,
            userList: [],
        };
    },
    created() {
        this.getAllUsers();
    },
    watch: {
        "form.username"(value){
            if (value && value.trim().length>0){
                if (this.userList.includes(value.trim().toLowerCase())) {
                    this.message.username = "Username already exists";
                } else {
                    this.message.username = "";
                }
            }
            else {
                this.message.username = "Username cannot be empty."
            }
        },
        "form.password"(value){
            if (value && value.trim().length>0){
                this.message.password = ""
            }
            else {
                this.message.password = "Password cannot be empty."
            }
        },
        "form.user_acc_id"(value){
            if (value && value.trim().length>0){
                this.message.user_acc_id = ""
            }
            else {
                this.message.user_acc_id = "tBank User ID cannot be empty."
            }
        },
        "form.user_pin"(value){
            if (value && value.trim().length>0){
                this.message.user_pin = ""
            }
            else {
                this.message.user_pin = "tBank User Pin cannot be empty."
            }
        },
        "form.settlement_acc"(value){
            if (value && value.trim().length>0){
                this.message.settlement_acc = ""
            }
            else {
                this.message = "tBank Settlement Account cannot be empty."
            }
        },
    },
    computed: {
        isFormValid() {
            return (
                !this.form.username.trim() ||
                !this.form.password.trim() ||
                !this.form.user_acc_id.trim() ||
                !this.form.user_pin.trim() ||
                !this.form.settlement_acc.trim() ||
                Object.values(this.message).some((error) => {
                    return error !== "";
                })
            );
        },
     },
    methods: {
        //get all username
        async getAllUsers() {
            try {
               const res = await axios({
                  url: "http://127.0.0.1:5005/users",
               });
   
               data = res.data.data;
               console.log(data)
               this.userList = data.users.map((user) => user.username.toLowerCase());
               console.log(this.userList);
   
            } catch (err) {
               // Handle Error Here
               console.error(err);
            }
         },
        register: function() {
            this.loading = true;
            axios.post("http://127.0.0.1:5005/register", {
                username: this.form.username.trim(),
                password: this.form.password.trim(),
                user_acc_id: this.form.user_acc_id.trim(),
                user_pin: this.form.user_pin.trim(),
                settlement_acc: this.form.settlement_acc.trim(),
            })
            .then(response => {
                if (response.data.status == "success") {
                    this.processing = false;
                    this.$emit("authenticated", true, response.data.data);
                    this.alert.successBool = true;
                    this.alert.sucessMsg = "✔️ Registration Successful!"
                    console.log(response.data)
                    this.getAllSkillNames();
                    //reset form
                    this.form = {
                        username: "",
                        password: "",
                        user_acc_id: "",
                        user_pin: "",
                        settlement_acc: "",
                    };
                } else {
                    console.log(error)
                    this.alert.alertBool = true;
                    this.alert.alertMsg = "❌ Registration Failed, Please try again!";
                }
            })
            .catch(error => {
                console.log(error)
                this.alert.alertMsg = "❌ Registration Failed, Please try again!";
                this.processing = false;
            });
        }
    },
});
 
register.mount("#register");
 