<script setup>
import MainSection from '@/components/MainSection.vue'
import NewsCard from '@/components/NewsCard.vue'
</script>

<template>
  <main-section>
    <div
      v-for="(post, i) in posts"
      :key="i"
      class="flex justify-center pt-8"
    >
      <news-card
        :title="post.title"
        :link="post.link"
      />
    </div>
  </main-section>
</template>

<script>
import { get } from '../helpers/api'

export default {
  data () {
    return {
      posts: '',
      img_alt: 'No image found'
    }
  },
  created () {
    this.getNews()
  },
  methods: {
    getNews () {
      let _this = this
      get(_this, 'api/news', { params: {
        feed_url: 'http://feeds.bbci.co.uk/news/world/rss.xml', limit: 10
        } }, function (response) {
        let json = response.data
        _this.posts = json.result.posts
      }, function () {
        //
      })
    }
  }
}
</script>
