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
        @click="getNews"
      />
    </jb-buttons>
  </section>
  <section class="bg-white border-t border-b border-gray-100 p-6 mt-3 dark:bg-gray-900 dark:border-gray-900 dark:text-white">
    <level>
      <h1 @click="$router.push('source-list')" class="text-3xl font-semibold leading-tight cursor-pointer">
        {{ main_title ? main_title : "News sources are empty. Click to add new sources" }}
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
    <div
      v-show="scY > 300"
      id="pagetop"
      class="fixed right-0 bottom-0"
      @click="toTop"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="48"
        height="48"
        viewBox="0 0 24 24"
        fill="none"
        style="cursor: pointer"
        stroke="#4a5568"
        stroke-width="1"
        stroke-linecap="square"
        stroke-linejoin="arcs"
      >
        <path d="M18 15l-6-6-6 6" />
      </svg>
    </div>
  </transition>
</template>

<script>
import { get } from '../helpers/api'
import MainSection from '@/components/MainSection.vue'
import NewsCard from '@/components/NewsCard.vue'
import Level from '@/components/LevelDiv.vue'
import Control from '@/components/Control.vue'
import Field from '@/components/Field.vue'
import JbButton from "@/components/JbButton.vue";
import JbButtons from "@/components/JbButtons.vue";

export default {
  components: {
    MainSection, NewsCard, Level, Control, Field, JbButton, JbButtons
  },
  data () {
    return {
      scTimer: 0,
      scY: 0,
      posts: '',
      main_title: "",
      sources: [],
      selectedSource: "",
      limits: [5, 10, 25, 50],
      limit: 10
    }
  },
  created () {
    this.getUser()
  },
  mounted() {
    window.addEventListener('scroll', this.handleScroll);
  },
  methods: {
    getNews () {
      let _this = this
      get(_this, 'api/news', { params: {
        feed_url: _this.selectedSource.url, limit: _this.limit
        } }, function (response) {
        let json = response.data
        _this.posts = json.result.posts
        _this.main_title = json.result['Blog title']
      }, function () {
        //
      })
    },
    getUser() {
      let _this = this;
      let id = localStorage.getItem('user_id')
      get(_this, 'api/users/' + id, {}, response => {
        if (response.data.result.rssFeeds)
          _this.sources = response.data.result.rssFeeds
        _this.$store.commit('user', {
          name: response.data.result.name,
          email: response.data.result.email,
          id: response.data.result.id,
          password: response.data.result.password,
          rss: response.data.result.rssFeeds
        })
        _this.selectedSource = _this.sources[0]
        _this.getNews()
      }, e => console.log(e))
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
