// Redirect to login page if user directly access in-app pages without logging in
const path = window.location.pathname;
const currentPage = path.split("/").pop();
const pages = ['index.html', 'create-fund.html', 'mystocks.html'];

if (user_id !== "" || user_id !== null) {
    window.location.replace("login.html");
}


if (currentPage === 'login.html') {
    let user_id = sessionStorage.getItem('user_id')
    if (user_id !== "" || user_id !== null) {
        window.location.replace("index.html");
    }
}