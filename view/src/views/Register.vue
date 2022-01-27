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
      @submit.prevent="register"
    >
      <field
        label="Register"
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
      </jb-buttons>
    </card-component>
  </full-screen-section>
</template>

<script>
import { post } from '../helpers/api'
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
    }
  }
}
</script>
