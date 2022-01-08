<template>
  <div class="max-w-3xl rounded overflow-hidden shadow-lg">
    <a :href="link">
      <img class="w-full" :src=img :alt=imgAlt>
    </a>
    <div class="px-6 py-4">
      <div @click="goTo" class="font-bold text-xl mb-2 cursor-pointer">{{ title }}</div>
      <p @click="goTo" class="text-base overflow-hidden cursor-pointer text-lg" :class="text_class">
        {{ content }}
      </p>
      <div><p style="cursor: pointer" class="text justify-end font-bold text-sky-600"
              :style="{ display: display_expand }"
              @click="text_class='max-h-full'; display_expand='none'">Expand</p></div>
    </div>
    <div v-if="hashtags.length>0" class="px-6 pt-4 pb-2">
      <span v-for="(h, index) in hashtags" :key=index class="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2 mb-2">#{{h}}</span>
    </div>
  </div>
<!--  <div class="max-w-3xl rounded overflow-hidden shadow-lg" v-html="content"></div>-->
</template>

<script>
export default {
  props: ['img', 'imgAlt', 'title', 'content', 'hashtags', 'link'],
  data () {
    return {
      text_class: 'max-h-20',
      display_expand: 'flex'
    }
  },
  methods: {
    goTo () {
      window.open(
        this.link,
        '_blank'
      )
    }
  }
}
</script>
