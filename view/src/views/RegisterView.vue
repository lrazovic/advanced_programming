<script setup>
import { mdiAccount, mdiAsterisk, mdiEmailOutline, mdiCheckCircleOutline, mdiAlertCircle } from '@mdi/js'
import FullScreenSection from '@/components/FullScreenSection.vue'
import CardComponent from '@/components/CardComponent.vue'
import Field from '@/components/Field.vue'
import Control from '@/components/Control.vue'
import Divider from '@/components/DividerBar.vue'
import JbButton from '@/components/JbButton.vue'
import JbButtons from '@/components/JbButtons.vue'
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
      title="Register"
      @submit.prevent="register"
    >
      <notification
        v-if="registerSuccess"
        color="success"
        :icon="mdiCheckCircleOutline"
      >
        <b>Registration successful.</b> Click to login
        <template #right>
          <jb-button
            label="Login"
            color="success"
            small
            @click="$router.push('/login')"
          />
        </template>
      </notification>
      <notification
        v-if="registerFailure"
        color="error"
        :icon="mdiAlertCircle"
      >
        <b>Registration unsuccessful.</b>
      </notification>
      <field
        label="Name"
        help="Please enter your name"
      >
        <control
          v-model="form.name"
          :icon="mdiAccount"
          name="login"
          autocomplete="username"
          required=True
        />
      </field>

      <field
        label="Email"
        help="Please enter your email"
      >
        <control
          v-model="form.email"
          :icon="mdiEmailOutline"
          name="email"
          type="email"
          autocomplete="email"
          required=True
        />
      </field>

      <field
        label="Password"
        help="Please enter new password"
      >
        <control
          v-model="form.password"
          :icon="mdiAsterisk"
          type="password"
          name="password"
          autocomplete="current-password"
          required=True
        />
      </field>

      <divider />

      <jb-buttons>
        <jb-button
          type="submit"
          color="info"
          label="Register"
        />
        <jb-button
          to="/login"
          color="info"
          outline
          label="Go to log in"
        />
        <jb-button
          color="warning"
          outline
          label="Sign up with Google"
          @click.prevent="popupGoogle"
        />
      </jb-buttons>
    </card-component>
  </full-screen-section>
</template>

<script>
import { get, post } from '../helpers/api'
export default {
  data () {
    return {
      form: {
        name: '',
        password: '',
        email: ''
      },
      registerSuccess: false,
      registerFailure: false
    }
  },
  methods: {
    register() {
      let _this = this;
      _this.registerSuccess = false
      _this.registerFailure = false
      post(_this, 'auth/register', _this.form, (response) => {
        _this.registerSuccess = response.data.result
        if (!_this.registerSuccess)
          _this.registerFailure = true
        _this.form = {
          name: '',
          password: '',
          email: ''
        }
      }, (e) => {
        console.log(e)
      })
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
          rss: response.data.result.rss
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
  }
}
</script>
