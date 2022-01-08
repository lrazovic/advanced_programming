<script setup>
import MainSection from '@/components/MainSection.vue'
import NewsCard from '@/components/NewsCard'
</script>

<template>
  <main-section>
    <div
      v-for="(post, i) in posts"
      :key="i"
      class="flex justify-center pt-8"
    >
      <news-card
        :img="post.img"
        :content="post.summary"
        :hashtags="post.tags"
        :title="post.title"
        :img-alt="img_alt"
        :link="post.link"
      />
    </div>
  </main-section>
</template>

<script>
import { get } from '../../helpers/api'

export default {
  data () {
    return {
      posts: '',
      img_alt: 'No image found'
    }
  },
  methods: {
    getNews () {
      let _this = this
      get(_this, 'dummy/getnews', { params: '' }, function (response) {
        let json = response.data
        _this.posts = json.result.posts
      }, function () {
        //
      })
    }
  },
  created () {
    this.getNews()
  }
}
</script>
