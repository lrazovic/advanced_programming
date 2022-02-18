<script setup>
import { mdiAccount, mdiAsterisk } from '@mdi/js'
import FullScreenSection from '@/components/FullScreenSection.vue'
import CardComponent from '@/components/CardComponent.vue'
import Field from '@/components/Field.vue'
import Control from '@/components/Control.vue'
import Divider from '@/components/DividerBar.vue'
import JbButton from '@/components/JbButton.vue'
import JbButtons from '@/components/JbButtons.vue'

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
      <field
        label="Login"
        help="Please enter new login"
      >
        <control
          v-model="form.login"
          :icon="mdiAccount"
          name="login"
          autocomplete="username"
        />
      </field>

      <field
        label="Password"
        help="Please enter new password"
      >
        <control
          v-model="form.pass"
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
          label="Register"
        />
        <jb-button
          to="/login"
          color="info"
          outline
          label="Login"
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
        login: '',
        pass: '',
      }
    }
  },
  methods: {
    register() {
      let _this = this;
      post(_this, '', _this.form, () => {
        this.$router.push('/')
      }, (e) => {
        alert(e)
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
