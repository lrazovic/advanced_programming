<script setup>
// import { reactive } from 'vue'
// import { useRouter } from 'vue-router'
import { mdiAccount, mdiAsterisk } from "@mdi/js";
import FullScreenSection from "@/components/FullScreenSection.vue";
import CardComponent from "@/components/CardComponent.vue";
// import CheckRadioPicker from '@/components/CheckRadioPicker.vue'
import Field from "@/components/Field.vue";
import Control from "@/components/Control.vue";
import Divider from "@/components/DividerBar.vue";
import JbButton from "@/components/JbButton.vue";
import JbButtons from "@/components/JbButtons.vue";

// const form = reactive({
//   login: '',
//   pass: '',
//   remember: ['remember']
// })

// const router = useRouter()
//
// const submit = () => {
//
// }
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
      <field
        label="Login"
        help="Please enter your login"
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
        help="Please enter your password"
      >
        <control
          v-model="form.pass"
          :icon="mdiAsterisk"
          type="password"
          name="password"
          autocomplete="current-password"
        />
      </field>

      <!--      <check-radio-picker-->
      <!--        v-model="form.remember"-->
      <!--        name="remember"-->
      <!--        :options="{ remember: 'Remember' }"-->
      <!--      />-->

      <divider />

      <jb-buttons>
        <jb-button
          type="submit"
          color="info"
          label="Login"
        />
        <jb-button
          to="/register"
          color="info"
          outline
          label="Register"
        />
        <jb-button
          color="info"
          outline
          label="Login with Google"
          @click.prevent="popupGoogle"
        />
      </jb-buttons>
    </card-component>
  </full-screen-section>
</template>

<script>
import { post } from "../helpers/api";
export default {
  data() {
    return {
      form: {
        login: "",
        pass: "",
      },
    };
  },
  methods: {
    login () {
      let _this = this;
      post(
        _this,
        "",
        _this.form,
        () => {
          this.$router.push("/");
        },
        (e) => {
          alert(e);
        }
      );
    },
    popupGoogle () {
      window.open('http://localhost:3000/auth/login', '', 'width=650, height=650');
    }
  },
};
</script>
