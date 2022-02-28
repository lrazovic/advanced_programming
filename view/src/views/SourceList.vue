<script setup>
import { mdiTrashCan } from '@mdi/js'

import Field from '@/components/Field.vue'
import Control from '@/components/Control.vue'
import JbButton from "@/components/JbButton.vue";
import JbButtons from "@/components/JbButtons.vue";
import CardComponent from '@/components/CardComponent.vue'
import MainSection from '@/components/MainSection.vue'
</script>
<template>
  <section class="bg-white mt-3 border-t border-b border-gray-100 p-6 dark:bg-gray-900 dark:border-gray-900 dark:text-white ">
    <form @submit="addToList">
      <field
        label="Add RSS link"
        help="Place your desired news rss link"
      >
        <control
          v-model="rssLink.url"
          placeholder="Place rss link here"
          type=“url”
          @keyup.enter="addToList"
          required
        />
      </field>
      <jb-buttons>
        <jb-button
          type="submit"
          color="info"
          label="Add"
        />
      </jb-buttons>
    </form>
  </section>
  <main-section>
    <card-component
      class="mb-6"
      title="Manage RSS links list"
      has-table
    >
      <div class="flex justify-center py-8">
        <draggable
          class="bg-white rounded-lg border border-gray-200 xl:w-1/2 text-gray-900 dark:bg-gray-900 dark:border-gray-900"
          :list="list"
          @change="addLink"
        >
          <div
            v-for="(element, index) in list"
            :key="index"
            class="px-6 py-2 border-b border-gray-200 w-full flex justify-between "
          >
            <div class="overflow-x-auto ">
              <p class="dark:bg-gray-800 dark:text-gray-100">
                {{ element.url }}
              </p>
            </div>
            <div>
              <jb-buttons
                type="justify-start lg:justify-end"
                no-wrap
              >
                <jb-button
                  color="danger"
                  :icon="mdiTrashCan"
                  small
                  @click="deleteItem(index)"
                />
              </jb-buttons>
            </div>
          </div>
        </draggable>
      </div>
    </card-component>
  </main-section>
</template>
<script>
import {get, put} from '../helpers/api'
import { defineComponent } from 'vue'
import { VueDraggableNext } from 'vue-draggable-next'
export default defineComponent({
  components: {
    draggable: VueDraggableNext,
  },
  data() {
    return {
      rssLink: {
        url: ""
      },
      enabled: true,
      list: [],
      dragging: false,
    }
  },
  methods: {
    addLink() {
      let id = localStorage.getItem('user_id')
      let payloadList = this.list.map( (v,i) => {
        return {
          url: v.url,
          rank: i+1
        }
      })
      let _this = this
      put(_this, 'api/users/' + id + '/rss-feeds', {
        rssFeeds: payloadList
      }, () => {}, () => {})
    },
    addToList() {
      if (this.rssLink){
        let t = this.rssLink
        this.list.push(t)
        this.rssLink = { url: ""}
        this.addLink()
      }
    },
    getUser() {
      let _this = this;
      let id = localStorage.getItem('user_id')
      get(_this, 'api/users/' + id, {}, response => {
        if (response.data.result.rssFeeds)
          _this.list = response.data.result.rssFeeds
        _this.$store.commit('user', {
          name: response.data.result.name,
          email: response.data.result.email,
          id: response.data.result.id,
          password: response.data.result.password,
          rss: response.data.result.rssFeeds
        })
      }, e => console.log(e))
    },
    deleteItem(i) {
      this.list.splice(i, 1);
      this.addLink()
    }
  },
  created() {
    this.getUser()
  }
})
</script>
