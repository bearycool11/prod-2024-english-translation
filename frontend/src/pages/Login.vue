<script setup>
import { computed, reactive, watch } from 'vue'
import { api } from '@/logic/api.js'
import { store } from '@/store/index.js'
import router from '@/router.js'

const state = reactive({
  isAuthForm: false
})
const enterDate = reactive({
  login: '',
  password: '',
  name: ''
})

const toggleAuth = () => {
  state.isAuthForm = !state.isAuthForm
}

const text = computed(() => {
  if (state.isAuthForm) {
    return {
      header: 'Зайди в акканут',
      link: 'Регистрация',
      button: 'Войти'
    }
  }

  return {
    header: 'Зарегистрироваться',
    link: 'Авторизация',
    button: 'Зарегистрироваться'
  }
})

const onEnterClick = () => {
  store.auth.isLoading = true

  if (!state.isAuthForm) {
    api.register(enterDate).then(() => {
      store.auth.isAuth = true
      store.auth.isLoading = false
      router.push('/')
    })
  } else {
    api.login(enterDate).then(() => {
      store.auth.isAuth = true
      store.auth.isLoading = false
      router.push('/')
    })
  }

  enterDate.login = ''
  enterDate.password = ''
  enterDate.name = ''
}

watch(store.auth, async () => {
  if (store.auth.isAuth && !store.auth.isLoading) {
    await router.push('/')
    window.location.reload()
  }
})
</script>

<template>
  <section class="bg-gray-50 dark:bg-gray-900 h-screen">
    <div
      v-if="store.auth.isLoading"
      role="status"
      class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2"
    >
      <svg
        aria-hidden="true"
        class="w-8 h-8 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600"
        viewBox="0 0 100 101"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
          fill="currentColor"
        />
        <path
          d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
          fill="currentFill"
        />
      </svg>
      <span class="sr-only">Loading...</span>
    </div>
    <div
      v-if="!store.auth.isLoading"
      class="flex flex-col items-center justify-center px-6 py-8 mx-auto md:h-screen lg:py-0"
    >
      <a
        href="#"
        class="flex items-center mb-6 text-2xl font-semibold text-gray-900 dark:text-white"
      >
        <img class="w-18 h-8 mr-2" src="/logo.svg" alt="logo" />
      </a>
      <div
        class="w-full bg-white rounded-lg shadow dark:border md:mt-0 sm:max-w-md xl:p-0 dark:bg-gray-800 dark:border-gray-700"
      >
        <div class="p-6 space-y-4 md:space-y-6 sm:p-8">
          <h1
            class="text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl dark:text-white"
          >
            {{ text.header }}
          </h1>
          <form :onsubmit="(e) => e.preventDefault()" class="space-y-4 md:space-y-6" action="#">
            <div v-if="!state.isAuthForm">
              <label
                for="email"
                class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
              >
                Имя
              </label>
              <input
                type="name"
                name="name"
                id="name"
                class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                placeholder="Имя"
                v-model="enterDate.name"
                required
              />
            </div>
            <div>
              <label
                for="email"
                class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
              >
                Твой email
              </label>
              <input
                type="login"
                name="login"
                id="login"
                class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                placeholder="Твой логин"
                v-model="enterDate.login"
                required
              />
            </div>
            <div>
              <label
                for="password"
                class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
              >
                Пароль
              </label>
              <input
                type="password"
                name="password"
                id="password"
                placeholder="••••••••"
                class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                required
                v-model="enterDate.password"
              />
            </div>
            <button
              @click="onEnterClick"
              type="submit"
              class="w-full text-white bg-primary-600 hover:bg-primary-700 focus:ring-4 focus:outline-none focus:ring-primary-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-primary-600 dark:hover:bg-primary-700 dark:focus:ring-primary-800"
            >
              {{ text.button }}
            </button>
            <div class="pt-1">
              <a
                @click="toggleAuth"
                class="font-medium cursor-pointer text-primary-600 hover:underline dark:text-primary-500"
              >
                {{ text.link }}
              </a>
            </div>
          </form>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped></style>
