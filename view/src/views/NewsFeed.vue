<script setup>
import MainSection from '@/components/MainSection.vue'
import NewsCard from '@/components/NewsCard'
</script>

<template>
  <main-section>
    <div v-for="i in 10" :key="i" class="flex justify-center pt-8">
      <news-card
        :img="newsContent.img"
        :content="newsContent.content"
        :hashtags="newsContent.hashtags"
        :title="newsContent.title"
        :img-alt="newsContent.alt"
      ></news-card>
    </div>
  </main-section>
</template>

<script>
export default {
  data () {
    return {
      newsContent: {
        img: 'https://marmotamaps.com/de/fx/wallpaper/download/faszinationen/Marmotamaps_Wallpaper_Berchtesgaden_Desktop_1920x1080.jpg',
        alt: 'No image found',
        title: 'Some news title',
        content: 'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Voluptatibus quia, Nonea! Maiores et perferendis eaque, exercitationem praesentium nihil.',
        hashtags: ['travel', 'mountain', 'sky']
      }
    }
  }
}
</script>
