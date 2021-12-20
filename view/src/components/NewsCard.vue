<template>
  <div class="max-w-3xl rounded overflow-hidden shadow-lg">
    <img class="w-full" :src=img :alt=imgAlt>
    <div class="px-6 py-4">
      <div class="font-bold text-xl mb-2">{{ title }}</div>
      <p class="text-gray-700 text-base">
        {{content}}
      </p>
    </div>
    <div class="px-6 pt-4 pb-2">
      <span v-for="(h, index) in hashtags" :key=index class="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2 mb-2">#{{h}}</span>
    </div>
  </div>
</template>

<script>
export default {
  props: ['img', 'imgAlt', 'title', 'content', 'hashtags']
}
</script>
