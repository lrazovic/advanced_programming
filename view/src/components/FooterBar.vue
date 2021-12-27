<script setup>
import { computed } from 'vue'
import { useStore } from 'vuex'
import Level from '@/components/LevelDiv.vue'

const store = useStore()

const year = computed(() => new Date().getFullYear())

const isFooterBarVisible = computed(() => !store.state.isFullScreen)
</script>

<template>
  <footer
    v-show="isFooterBarVisible"
    class="bg-white py-2 px-6 dark:bg-gray-900"
  >
    <level>
      <div class="text-center md:text-left">
        <b>&copy; {{ year }}, <a
          href="https://github.com/lrazovic/advanced_programming"
          target="_blank"
        >Laboratory of advanced programming group</a>.</b>
      </div>
    </level>
  </footer>
</template>
