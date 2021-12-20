<script setup>
import { computed, ref } from 'vue'
import { useStore } from 'vuex'
import {
  mdiClose,
  mdiDotsVertical,
  mdiAccount,
  mdiCogOutline,
  mdiEmail,
  mdiLogout,
  mdiThemeLightDark
} from '@mdi/js'
import NavBarItem from '@/components/NavBarItem.vue'
import NavBarItemLabel from '@/components/NavBarItemLabel.vue'
import NavBarMenu from '@/components/NavBarMenu.vue'
import NavBarMenuDivider from '@/components/NavBarMenuDivider.vue'
import UserAvatar from '@/components/UserAvatar.vue'
import Icon from '@/components/Icon.vue'

const store = useStore()

const toggleLightDark = () => {
  store.dispatch('darkMode')
}

const isNavBarVisible = computed(() => !store.state.isFullScreen)

const isAsideMobileExpanded = computed(() => store.state.isAsideMobileExpanded)

const userName = computed(() => store.state.userName)

const isMenuNavBarActive = ref(false)

const menuNavBarToggleIcon = computed(() => isMenuNavBarActive.value ? mdiClose : mdiDotsVertical)

const menuNavBarToggle = () => {
  isMenuNavBarActive.value = !isMenuNavBarActive.value
}

</script>

<template>
  <nav
    v-show="isNavBarVisible"
    class="top-0 left-0 right-0 fixed flex bg-white h-14 border-b border-gray-100 z-30 w-screen
    transition-position xl:pl-60 lg:w-auto lg:items-stretch dark:bg-gray-900 dark:border-gray-800"
    :class="{'ml-60 lg:ml-0':isAsideMobileExpanded}"
  >
    <div class="flex-none items-stretch flex h-14 lg:hidden">
      <nav-bar-item @click.prevent="menuNavBarToggle">
        <icon
          :path="menuNavBarToggleIcon"
          size="24"
        />
      </nav-bar-item>
    </div>
    <div
      class="absolute w-screen top-14 left-0 bg-white shadow
        lg:w-auto lg:items-stretch lg:flex lg:grow lg:static lg:border-b-0 lg:overflow-visible lg:shadow-none dark:bg-gray-900"
      :class="[isMenuNavBarActive ? 'block' : 'hidden']"
    >
      <div
        class="max-h-screen-menu overflow-y-auto lg:overflow-visible lg:flex lg:items-stretch lg:justify-end lg:ml-auto"
      >
        <nav-bar-menu has-divider>
          <user-avatar class="w-6 h-6 mr-3 inline-flex" />
          <div>
            <span>{{ userName }}</span>
          </div>

          <template #dropdown>
            <nav-bar-item to="/profile">
              <nav-bar-item-label
                :icon="mdiAccount"
                label="My Profile"
              />
            </nav-bar-item>
            <nav-bar-item>
              <nav-bar-item-label
                :icon="mdiCogOutline"
                label="Settings"
              />
            </nav-bar-item>
            <nav-bar-item>
              <nav-bar-item-label
                :icon="mdiEmail"
                label="Messages"
              />
            </nav-bar-item>
            <nav-bar-menu-divider />
            <nav-bar-item>
              <nav-bar-item-label
                :icon="mdiLogout"
                label="Log Out"
              />
            </nav-bar-item>
          </template>
        </nav-bar-menu>
        <nav-bar-item
          has-divider
          is-desktop-icon-only
          @click.prevent="toggleLightDark"
        >
          <nav-bar-item-label
            :icon="mdiThemeLightDark"
            label="Light/Dark"
            is-desktop-icon-only
          />
        </nav-bar-item>
        <nav-bar-item is-desktop-icon-only>
          <nav-bar-item-label
            :icon="mdiLogout"
            label="Log out"
            is-desktop-icon-only
          />
        </nav-bar-item>
      </div>
    </div>
  </nav>
</template>
