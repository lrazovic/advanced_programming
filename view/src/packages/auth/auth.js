export default function (app) {
    app.auth = {

        setToken(token) {
            localStorage.setItem('token', token);
        },

        getToken() {
            let token = localStorage.getItem('jwt');

            return token;

        },

        destroyToken() {
            localStorage.removeItem('jwt');
            localStorage.removeItem('refresh');
            // this.destroyAccountId();
        },

        isAuthenticated() {
            return !!this.getToken();
        },

        setAccountId(accountId) {
            localStorage.setItem('accountId', accountId);
        },
        getAccountId(){

            let accountId = localStorage.getItem('accountId');

            return accountId ? accountId : null;

        },
        destroyAccountId(){
            localStorage.removeItem('accountId');
        },



    };
    app.config.globalProperties.$auth = app.auth
}
