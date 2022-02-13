<script setup>
import { computed, ref } from 'vue'
import { useStore } from 'vuex'
import { mdiCheckDecagram } from '@mdi/js'
import Level from '@/components/LevelDiv.vue'
import UserAvatar from '@/components/UserAvatar.vue'
import CardComponent from '@/components/CardComponent.vue'
import CheckRadioPicker from '@/components/CheckRadioPicker.vue'
import Pill from '@/components/Pill.vue'


const store = useStore()

const userName = computed(() => store.state.userName)

const userSwitchVal = ref([])
</script>

<template>
  <card-component rounded="">
    <level type="justify-around lg:justify-center">
      <div class="space-y-3 text-center md:text-left lg:mx-12">
        <h1 class="text-2xl">
          Howdy, <b>{{ userName }}</b>!
        </h1>
      </div>
    </level>
  </card-component>
</template>
