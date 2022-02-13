<script setup>
import JbButton from "@/components/JbButton.vue";
import JbButtons from "@/components/JbButtons.vue";
import ModalBox from '@/components/ModalBox.vue'
</script>
<template>
  <div class="max-w-3xl rounded overflow-hidden shadow-lg">
    <a :href="link">
      <img
        class="w-full"
        :src="img"
        :alt="imgAlt"
      >
    </a>
    <div class="px-6 py-4">
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
        {{ content }}
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
    <div class="px-6 pt-4 pb-2">
      <span
        v-for="(h, index) in tags"
        :key="index"
        class="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2 mb-2"
      >#{{ h }}</span>
    </div>
    <div class="px-6 pt-4 pb-2">
      <jb-buttons>
        <jb-button
          color="success"
          label="Summarise"
          @click="getSummary"
        />
      </jb-buttons>
    </div>
    <div
      v-if="summarisedText"
      class="px-6 py-4"
    >
      <p
        class="text-base overflow-hidden cursor-pointer text-lg"
      >
        {{ summarisedText }}
      </p>
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
<!--  <div class="max-w-3xl rounded overflow-hidden shadow-lg" v-html="content"></div>-->
</template>

<script>
import { post } from '../helpers/api'
export default {
  components: {},

  props: ['img', 'imgAlt', 'title', 'content', 'hashtags', 'link'],
  data () {
    return {
      modalOne: {
        active: false,
        error: ""
      },
      text_class: 'max-h-20',
      display_expand: 'flex',
      summarisedText: ''
    }
  },
  computed: {
    tags: function () {
      return this.hashtags[0] == 'null' ? [] : this.hashtags
    }
  },
  methods: {
    goTo () {
      window.open(
        this.link,
        '_blank'
      )
    },
    getSummary() {
      let _this = this;
      post(_this, 'api/summary', { body: _this.content }, response => {
        _this.summarisedText = response.data.result
      }, e => {
        _this.modalOne.error = e;
        _this.modalOne.active = true;
      })
    }
  }
}
</script>
