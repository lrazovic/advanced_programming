<script setup>
// import { reactive } from 'vue'
// import { useRouter } from 'vue-router'
import { mdiAsterisk, mdiEmailOutline, mdiAlertCircle } from "@mdi/js";
import FullScreenSection from "@/components/FullScreenSection.vue";
import CardComponent from "@/components/CardComponent.vue";
import Field from "@/components/Field.vue";
import Control from "@/components/Control.vue";
import Divider from "@/components/DividerBar.vue";
import JbButton from "@/components/JbButton.vue";
import JbButtons from "@/components/JbButtons.vue";
import Notification from '@/components/Notification.vue'
</script>

<template>
  <full-screen-section
    v-slot="{ cardClass, cardRounded }"
    bg="login"
  >
    <card-component
      :class="cardClass"
      :rounded="cardRounded"
      form
      header-icon="."
      title="Log In"
      @submit.prevent="login"
    >
      <notification
        v-if="registerFailure"
        color="danger"
        :icon="mdiAlertCircle"
      >
        <b>Login unsuccessful.</b>
        <template #right>
        </template>
      </notification>
      <field
        label="Email"
        help="Please enter your Email"
      >
        <control
          v-model="form.email"
          :icon="mdiEmailOutline"
          name="email"
          type="email"
          autocomplete="email"
        />
      </field>

      <field
        label="Password"
        help="Please enter your password"
      >
        <control
          v-model="form.password"
          :icon="mdiAsterisk"
          type="password"
          name="password"
          autocomplete="current-password"
        />
      </field>

      <divider />

      <jb-buttons>
        <jb-button
          type="submit"
          color="info"
          label="Log in"
        />
        <jb-button
          to="/register"
          color="info"
          outline
          label="Go to register"
        />
        <jb-button
          color="warning"
          outline
          label="Login with Google"
          @click.prevent="popupGoogle"
        />
      </jb-buttons>
    </card-component>
  </full-screen-section>
</template>

<script>
import { post, get } from "../helpers/api";
export default {
  data() {
    return {
      form: {
        email: "",
        password: "",
      },
      registerFailure: false
    };
  },
  methods: {
    toastMessage(type, message) {
      this.$snackbar.add({
        type: type,
        text: message
      })
    },
    login () {
      let _this = this;
      post(
        _this,
        "auth/loginlocal",
        _this.form,
        (response) => {
          if(response.data.user_id>-1){
          _this.$auth.setToken(response.data.jwt, response.data.refresh,response.data.user_id)
            window.location.replace(window.location.origin)}
          else{_this.toastMessage('error', 'Wrong username or password')}
        },
        () => {
          _this.toastMessage('error', 'Failed to log in')
        }
      );
    },
    getUser(){
      let _this = this;
      let id = localStorage.getItem('user_id')
      get(_this, 'api/users/' + id, {}, response => {
        _this.$store.commit('user', {
          name: response.data.result.name,
          email: response.data.result.email,
          id: response.data.result.id,
          password: response.data.result.password,
          rss: response.data.result.rssFeeds
        })
      }, e => console.log(e))
    },
    popupGoogle () {
      let win = window.open('http://localhost:3000/auth/login', '', 'width=650, height=650');
      let _this = this;
      let timer = setInterval(function() {
        if(win.closed) {
          clearInterval(timer);
          if (_this.$auth.isAuthenticated()) {
            _this.getUser()
            _this.$router.push('/')
          }
        }
      }, 1000);
    }
  },
};
</script>
