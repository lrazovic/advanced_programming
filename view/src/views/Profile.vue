<script setup>
import { reactive } from 'vue'
import { useStore } from 'vuex'
import { mdiAccount, mdiAccountCircle, mdiLock, mdiMail, mdiAsterisk, mdiFormTextboxPassword } from '@mdi/js'
import MainSection from '@/components/MainSection.vue'
import CardComponent from '@/components/CardComponent.vue'
import Divider from '@/components/DividerBar.vue'
import Field from '@/components/Field.vue'
import Control from '@/components/Control.vue'
import JbButton from '@/components/JbButton.vue'
import JbButtons from '@/components/JbButtons.vue'
import UserCard from '@/components/UserCard.vue'
import ModalBox from '@/components/ModalBox.vue'


const store = useStore()

const profileForm = reactive({
  name: store.state.userName,
  email: store.state.userEmail
})

const passwordForm = reactive({
  password_current: '',
  password: '',
  password_confirmation: ''
})

const submitProfile = () => {
  store.commit('user', profileForm)
}

const submitPass = () => {
  //
}
</script>

<template>
  <user-card />

  <main-section>
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <card-component
        title="Edit Profile"
        :icon="mdiAccountCircle"
        form
        @submit.prevent="submitProfile"
      >
        <!--        <field-->
        <!--          label="Avatar"-->
        <!--          help="Max 500kb"-->
        <!--        >-->
        <!--          <file-picker />-->
        <!--        </field>-->

        <field
          label="Name"
          help="Required. Your name"
        >
          <control
            v-model="profileForm.name"
            :icon="mdiAccount"
            name="username"
            required
            autocomplete="username"
          />
        </field>
        <field
          label="E-mail"
          help="Required. Your e-mail"
        >
          <control
            v-model="profileForm.email"
            :icon="mdiMail"
            type="email"
            name="email"
            required
            autocomplete="email"
          />
        </field>

        <divider />

        <jb-buttons>
          <jb-button
            color="info"
            type="submit"
            label="Submit"
          />
          <!--          <jb-button-->
          <!--            color="info"-->
          <!--            label="Options"-->
          <!--            outline-->
          <!--          />-->
        </jb-buttons>
      </card-component>

      <card-component
        title="Change Password"
        :icon="mdiLock"
        form
        @submit.prevent="submitPass"
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
  >
    <p>Are you sure you want to delete your account?</p>
  </modal-box>
</template>

<script>
export default {
  data () {
    return {
      modalOneActive: false
    }
  }
}
</script>
