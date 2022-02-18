<template>
  <main-section>
    <div class="flex justify-center py-8">
      <draggable
        class="bg-white rounded-lg border border-gray-200 w-96 text-gray-900"
        :list="list"
        @change="log"
      >
        <div
          v-for="element in list"
          :key="element.name"
          class="px-6 py-2 border-b border-gray-200 w-full"
        >
          {{ element.name }}
        </div>
      </draggable>
    </div>
  </main-section>
</template>
<script>
import { defineComponent } from 'vue'
import { VueDraggableNext } from 'vue-draggable-next'
export default defineComponent({
  components: {
    draggable: VueDraggableNext,
  },
  data() {
    return {
      enabled: true,
      list: [
        { name: 'John', id: 1 },
        { name: 'Joao', id: 2 },
        { name: 'Jean', id: 3 },
        { name: 'Gerard', id: 4 },
      ],
      dragging: false,
    }
  },
  methods: {
    log(event) {
      console.log(event)
    },
  },
})
</script>
