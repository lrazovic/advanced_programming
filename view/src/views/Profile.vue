<!--<script setup>-->
<!--import { mdiAccount, mdiAccountCircle, mdiLock, mdiMail, mdiAsterisk, mdiFormTextboxPassword } from '@mdi/js'-->
<!--</script>-->

<template>
  <user-card />

  <main-section>
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <card-component
        title="Profile"
        :icon="mdiAccountCircle"
        form
        @submit.prevent=""
      >
        <field
          label="Name"
        >
          <control
            v-model="profileForm.name"
            :icon="mdiAccount"
            name="username"
            required
            disabled
            autocomplete="username"
          />
        </field>
        <field
          label="E-mail"
        >
          <control
            v-model="profileForm.email"
            :icon="mdiMail"
            type="email"
            name="email"
            required
            disabled
            autocomplete="email"
          />
        </field>

      </card-component>

      <card-component
        title="Change Password"
        :icon="mdiLock"
        form
        @submit.prevent=""
      >
        <field
          label="Current password"
          help="Required. Your current password"
        >
          <control
            v-model="passwordForm.password_current"
            :icon="mdiAsterisk"
            name="password_current"
            type="password"
            required
            autocomplete="current-password"
          />
        </field>

        <divider />

        <field
          label="New password"
          help="Required. New password"
        >
          <control
            v-model="passwordForm.password"
            :icon="mdiFormTextboxPassword"
            name="password"
            type="password"
            required
            autocomplete="new-password"
          />
        </field>

        <field
          label="Confirm password"
          help="Required. New password one more time"
        >
          <control
            v-model="passwordForm.password_confirmation"
            :icon="mdiFormTextboxPassword"
            name="password_confirmation"
            type="password"
            required
            autocomplete="new-password"
          />
        </field>

        <divider />

        <jb-buttons>
          <jb-button
            type="submit"
            color="info"
            label="Submit"
            @click="changePass"
          />
        </jb-buttons>
      </card-component>
    </div>
  </main-section>
  <main-section>
    <div class="flex justify-end">
      <jb-buttons>
        <jb-button
          type="submit"
          color="danger"
          label="Delete Account"
          @click="modalOneActive = true"
        />
      </jb-buttons>
    </div>
  </main-section>
  <modal-box
    v-model="modalOneActive"
    title="Please confirm action"
    button-label="Confirm"
    button="danger"
    has-cancel
    @confirm="confirmDelete"
  >
    <p>Are you sure you want to delete your account?</p>
  </modal-box>
</template>

<script>
import {get, del, post} from "../helpers/api";

import MainSection from '@/components/MainSection.vue'
import CardComponent from '@/components/CardComponent.vue'
import Divider from '@/components/DividerBar.vue'
import Field from '@/components/Field.vue'
import Control from '@/components/Control.vue'
import JbButton from '@/components/JbButton.vue'
import JbButtons from '@/components/JbButtons.vue'
import UserCard from '@/components/UserCard.vue'
import ModalBox from '@/components/ModalBox.vue'

export default {
  components: { MainSection, CardComponent, Divider, Field, Control, JbButtons, JbButton, UserCard, ModalBox },
  data () {
    return {
      modalOneActive: false,
      profileForm: {
        name: '',
        email: ''
      },
      passwordForm: {
        password_current: '',
        password: '',
        password_confirmation: ''
      }
    }
  },
  created() {
    this.getUser()
  },
  methods: {
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
        _this.profileForm.name = response.data.result.name
        _this.profileForm.email = response.data.result.email
      }, e => console.log(e))
    },
    confirmDelete(){
      let _this = this;
      let id = localStorage.getItem('user_id')
      del(_this, "api/users/" + id, {}, () => {
        _this.$auth.destroyToken()
        _this.$router.push('/login')
      }, e => {console.log(e)})
    },
    changePass(){
      let _this = this;
      let form = {
        email: this.profileForm.email,
        old_password: this.passwordForm.password_current,
        new_password: this.passwordForm.password_confirmation
      }
      if (this.passwordForm.password === this.passwordForm.password_confirmation) {
        post(_this, 'auth/changepassword', form, (response) => {
          if (response.data.result === "False")
            _this.toastMessage("error", "Failed to change password")
          else{
            _this.toastMessage("success", "Password changed successfully")
            _this.passwordForm = {
              password_current: '',
              password: '',
              password_confirmation: ''
            }
          }
        }, () => {
          _this.toastMessage("error", "Failed to change password")
        })
      }else {
       this.toastMessage("warning", "Passwords do not match")
      }
    },
    toastMessage(type, message) {
      this.$snackbar.add({
        type: type,
        text: message
      })
    }
  }
}
</script>
