<script setup>
// import JbButton from "@/components/JbButton.vue";
// import JbButtons from "@/components/JbButtons.vue";
import ModalBox from '@/components/ModalBox.vue'
import CheckRadioPicker from '@/components/CheckRadioPicker.vue'
</script>
<template>
  <div
    v-if="content"
    class="xl:w-1/2 rounded overflow-hidden shadow-lg bg-white"
  >
    <div class="px-6 py-2">
      <div class="flex items-center justify-end mt-6">
        <check-radio-picker
          v-model="summarise"
          type="switch"
          name="notifications-switch"
          :options="{ outline: 'Summarise' }"
          @change="getSummary"
        />
      </div>
      <div
        class="font-bold text-xl mb-2 cursor-pointer"
        @click="goTo"
      >
        {{ title }}
      </div>
      <p
        class="text-base overflow-hidden cursor-pointer text-lg"
        :class="text_class"
        @click="goTo"
      >
        {{ summarise && summarisedText ? summarisedText : content }}
      </p>
      <div>
        <p
          style="cursor: pointer"
          class="text justify-end font-bold text-sky-600"
          :style="{ display: display_expand }"
          @click="text_class='max-h-full'; display_expand='none'"
        >
          Expand
        </p>
      </div>
    </div>
  </div>
  <modal-box
    v-model="modalOne.active"
    large-title="Something went wrong"
    button="danger"
    shake
  >
    <p>{{ modalOne.error }} ????</p>
  </modal-box>
</template>

<script>
import { get, post } from '../helpers/api'
export default {
  components: {},

  props: ['title', 'link'],
  data () {
    return {
      modalOne: {
        active: false,
        error: ""
      },
      summarise: false,
      content: "",
      id: "",
      text_class: 'max-h-20',
      display_expand: 'flex',
      summarisedText: ''
    }
  },
  created() {
    this.getText();
  },
  methods: {
    goTo () {
      window.open(
        this.link,
        '_blank'
      )
    },
    getSummary() {
      if (!this.summarisedText){
        let _this = this;
        post(_this, 'api/news/articles/summary', { body: _this.content }, response => {
          _this.summarisedText = response.data.result
        }, e => {
          _this.modalOne.error = e;
          _this.modalOne.active = true;
        })
      }
    },
    getText() {
      let _this = this;
      get(_this, 'api/news/articles', { params: { article_url: _this.link } }, response => {
        _this.content = response.data.result
        _this.id = response.data.id
      }, e => {
        _this.modalOne.error = e;
        _this.modalOne.active = true;
      })
    },
  }
}
</script>
