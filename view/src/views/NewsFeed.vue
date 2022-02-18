<script setup>
import MainSection from '@/components/MainSection.vue'
import NewsCard from '@/components/NewsCard.vue'
import Level from '@/components/LevelDiv.vue'
import Control from '@/components/Control.vue'
import Field from '@/components/Field.vue'
import JbButton from "@/components/JbButton.vue";
import JbButtons from "@/components/JbButtons.vue";
</script>

<template>
  <section class="bg-white mt-3 border-t border-b border-gray-100 p-6 dark:bg-gray-900 dark:border-gray-900 dark:text-white ">
    <field label="Choose news source">
      <control
          v-model="selectedSource"
          :options="sources"
          help="Select url"
      />
      <control
          v-model="limit"
          :options="limits"
          help="Choose how many posts"
      />
    </field>
    <jb-buttons>
      <jb-button
          type="submit"
          color="info"
          label="Get News"
      />
    </jb-buttons>
  </section>
  <section class="bg-white border-t border-b border-gray-100 p-6 mt-3 dark:bg-gray-900 dark:border-gray-900 dark:text-white">
    <level>
      <h1 class="text-3xl font-semibold leading-tight">
        {{ main_title ? main_title : "News source not selected" }}
      </h1>
    </level>
  </section>
  <main-section style="padding-top: 0">
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
  <transition name="fade">
    <div id="pagetop" class="fixed right-0 bottom-0" v-show="scY > 300" @click="toTop">
      <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none"
           style="cursor: pointer"
           stroke="#4a5568"
           stroke-width="1" stroke-linecap="square" stroke-linejoin="arcs">
        <path d="M18 15l-6-6-6 6"/>
      </svg>
    </div>
  </transition>
</template>

<script>
import { get } from '../helpers/api'

export default {
  data () {
    return {
      scTimer: 0,
      scY: 0,
      posts: '',
      main_title: "",
      sources: [
        {
          label: "Title 1",
          link: "Link 1"
        },
        {
          label: "Title 2",
          link: "Link 2"
        },
        {
          label: "Title 3",
          link: "Link 3"
        }
      ],
      selectedSource: {
        label: "Title 1",
        link: "Link 1"
      },
      limits: [5, 10, 25, 50],
      limit: 10
    }
  },
  created () {
    this.getNews()
  },
  mounted() {
    window.addEventListener('scroll', this.handleScroll);
  },
  methods: {
    getNews () {
      let _this = this
      get(_this, 'api/news', { params: {
        feed_url: 'http://feeds.bbci.co.uk/news/world/rss.xml', limit: _this.limit
        } }, function (response) {
        let json = response.data
        _this.posts = json.result.posts
        _this.main_title = json.result['Blog title']
      }, function () {
        //
      })
    },
    handleScroll: function () {
      if (this.scTimer) return;
      this.scTimer = setTimeout(() => {
        this.scY = window.scrollY;
        clearTimeout(this.scTimer);
        this.scTimer = 0;
      }, 100);
    },
    toTop: function () {
      window.scrollTo({
        top: 0,
        behavior: "smooth"
      });
    },
  }
}
</script>
