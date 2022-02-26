export default function (app) {
    app.auth = {

        setToken(token, refresh, user_id) {
            localStorage.setItem('jwt', token);
            localStorage.setItem('refresh', refresh);
            localStorage.setItem('user_id', user_id);
        },

        getToken() {
            let token = localStorage.getItem('jwt');

            return token;

        },

        destroyToken() {
            localStorage.removeItem('jwt');
            localStorage.removeItem('refresh');
            localStorage.removeItem('user_id');
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
