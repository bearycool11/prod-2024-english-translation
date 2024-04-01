<template>
  <div class="flex justify-evenly mt-10 flex-wrap" v-if="organizations">
    <a
      v-for="(organization, index) in organizations"
      :key="index"
      :href="'/organization/' + organization.id"
      class="block max-w-sm mt-4 p-6 md:w-full w-52 bg-white border border-gray-200 rounded-lg shadow hover:bg-gray-100 dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-gray-700"
    >
      <h5 class="mb-2 text-2xl font-bold truncate tracking-tight text-gray-900 dark:text-white">
        {{ organization.name }}
      </h5>
      <p class="font-normal truncate text-gray-700 dark:text-gray-400">
        {{ organization.description }}
      </p>
    </a>
  </div>
  <div v-else class="flex justify-center mt-10 w-full">
    <p class="flex px-6 py-2 rounded-md bg-neutral-100 w-auto">У вас еще нет организаций</p>
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import { api } from '@/logic/api.js'

export default defineComponent({
  name: 'AllOrganizations',
  async beforeMount() {
    api.getOrganizations().then((organizations) => {
      this.organizations = organizations
    })
  },
  data() {
    return {
      organizations: []
    }
  }
})
</script>
