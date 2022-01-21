export default function (Vue) {
    Vue.auth = {

        setToken(token) {
            localStorage.setItem('token', token);
        },

        getToken() {
            let token = localStorage.getItem('token');

            return token;

        },

        destroyToken() {
            localStorage.removeItem('token');
            this.destroyAccountId();
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

    Object.defineProperties(Vue.prototype, {
        $auth: {
            get() {
                return Vue.auth;
            }
        }
    })
}
