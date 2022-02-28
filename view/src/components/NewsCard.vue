<template>
  <div
    v-if="content"
    class="xl:w-1/2 rounded overflow-hidden shadow-lg bg-white dark:bg-gray-900 dark:border-gray-900"
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
</template>

<script>
import { get, post } from '../helpers/api'

import CheckRadioPicker from '@/components/CheckRadioPicker.vue'
export default {
  components: { CheckRadioPicker },

  props: ['title', 'link'],
  data () {
    return {
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
  watch: {
    link: 'getText'
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
        }, () => {
          _this.toastMessage('error', 'Could not get Summary')
        })
      }
    },
    getText() {
      this.text_class = 'max-h-20'
      this.display_expand = 'flex'
      this.content = ""
      this.summarisedText = ""
      this.summarise = false
      let _this = this;
      get(_this, 'api/news/articles', { params: { article_url: _this.link } }, response => {
        _this.content = response.data.result
        _this.id = response.data.id
      }, () => {

      })
    }
  },
  toastMessage(type, message) {
    this.$snackbar.add({
      type: type,
      text: message
    })
  }
}
</script>
