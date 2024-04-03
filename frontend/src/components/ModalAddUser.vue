<template>
  <div
    v-if="isShown"
    @click="closeModal"
    class="top-0 left-0 h-screen w-screen bg-gray-900 fixed opacity-20 z-40"
  ></div>
  <div
    v-if="isShown"
    class="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 z-50"
  >
    <div class="relative p-4 w-full max-w-md max-h-full top-0 right-0 left-0 z-50">
      <div class="relative bg-white rounded-lg shadow dark:bg-gray-700 min-w-80">
        <div
          class="flex items-center justify-between p-4 md:p-5 border-b rounded-t dark:border-gray-600"
        >
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
            {{
              !this.$props.initialUser.user?.name
                ? 'Добавить пользователя'
                : 'Редактировать пользоваетля'
            }}
          </h3>
          <button
            @click="closeModal"
            type="button"
            class="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm w-8 h-8 ms-auto inline-flex justify-center items-center dark:hover:bg-gray-600 dark:hover:text-white"
            data-modal-toggle="crud-modal"
          >
            <svg
              class="w-3 h-3"
              aria-hidden="true"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 14 14"
            >
              <path
                stroke="currentColor"
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"
              />
            </svg>
            <span class="sr-only">Close modal</span>
          </button>
        </div>
        <!-- Modal body -->
        <form :onsubmit="(e) => e.preventDefault()" class="p-4 md:p-5">
          <div class="grid gap-4 mb-4 grid-cols-2">
            <div class="col-span-2">
              <label for="name" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
                >Логин</label
              >
              <input
                :disabled="this.$props.initialUser?.user?.name"
                type="text"
                name="name"
                id="name"
                v-model="login"
                class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500"
                placeholder="Логин пользователя"
                required
              />
            </div>
          </div>

          <div v-for="right in rights" :key="right" class="flex items-center mb-4">
            <input
              :id="right"
              type="checkbox"
              :onchange="
                (e) => {
                  if (e.target.checked) {
                    this.permissions = [...permissions, right]
                  } else {
                    this.permissions = permissions
                      .map((right) => right?.name || right)
                      .filter((newRight) => newRight !== right)
                  }
                }
              "
              :disabled="right === 'viewer'"
              :checked="isChecked(right)"
              class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600"
            />
            <label :for="right" class="ms-2 text-sm font-medium text-gray-900 dark:text-gray-300">
              {{ convertMyPerm(right) }}
            </label>
          </div>
          <button
            @click="addUser"
            :disabled="!login"
            class="text-white inline-flex items-center bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
          >
            {{
              !this.$props.initialUser.user?.name
                ? 'Добавить пользователя'
                : 'Редактировать пользоваетля'
            }}
          </button>
          <button
            @click="deleteUser"
            v-if="!!this.$props.initialUser.user?.name"
            class="text-white inline-flex items-center bg-red-500 hover:bg-red-800 focus:ring-4 focus:outline-none focus:ring-red-300 font-medium rounded-lg text-sm px-5 mt-2 py-2.5"
          >
            Выгони пользователя
          </button>
        </form>
      </div>
    </div>
  </div>
</template>
<script>
import { defineComponent } from 'vue'
import { api } from '@/logic/api.js'
import { store } from '@/store/index.js'
import convertPermissions  from '../logic/converter.js'

export default defineComponent({
  name: 'ModalAddUser',
  props: {
    isShown: Boolean,
    closeModal: Function,
    id: String,
    initialUser: Object
  },
  data() {
    return {
      permissions: this.$props.initialUser?.rights || ['viewer'],
      login: this.$props.initialUser?.user?.login,
      rights: ['viewer', 'editor', 'reviewer'],
      mystore: null
    }
  },
  beforeMount() {
    this.mystore = store
  },
  mounted() {

    if (this.mystore.auth.permissions.some((obj) => obj.name === 'owner')) {
      this.rights.push('admin')
    }
  },
  methods: {
    convertMyPerm(permission) {
    return convertPermissions(permission)
  },
    isChecked(right) {
      return this.permissions.find((permission) => {
        return permission === right || permission.name === right
      })
    },
    async deleteUser() {
      api
        .deleteUser(this.id, this.login)
        .then(() => {
          store.data.users = [...store.data.users].filter(({ user }) => user.login !== this.login)
        })
        .finally(() => {
          this.closeModal()
        })
    },
    async addUser() {
      if (!!this.$props.initialUser?.user?.login) {
       
        await api
          .updateUser(this.id, {
            login: this.login,
            permissions: this.permissions.map((right) => right?.name || right)
          })
          .then((user) => {
            const newUsers = [...store.data.users]
            const index = newUsers.findIndex(({ user }) => user.login === this.login)
            newUsers[index] = { ...user, rights: this.permissions }

            store.data.users = newUsers
          })
          .finally(() => {
            this.closeModal()
          })
        return
      }

      api
        .inviteUser(this.id, {
          login: this.login,
          permissions: this.permissions.map((right) => right?.name || right)
        })
        .then((user) => {
          store.data.users = [
            ...store.data.users,
            {
              ...user,
              rights: this.permissions.map((right) => right?.name || right)
            }
          ]
        })
        .finally(() => {
          this.closeModal()
        })
    }
  }
})
</script>
