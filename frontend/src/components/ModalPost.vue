<template>
  <div
    v-if="isShown"
    @click="closeModal"
    class="top-0 left-0 h-screen w-screen bg-gray-900 fixed opacity-20 z-40"
  ></div>
  <div
    v-if="isShown"
    class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 z-50"
  >
    <div class="relative p-4 w-full max-w-lg max-h-full top-0 right-0 left-0 z-50">
      <div class="relative bg-white rounded-lg shadow dark:bg-gray-700 md:min-w-[600px] w-72">
        <div
          class="flex items-center justify-between p-4 md:p-5 border-b rounded-t dark:border-gray-600"
        >
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Пост</h3>
          <div class="">
            <button
              @click="this.$props.closeModal"
              type="button"
              class="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm w-8 h-8 ms-auto inline-flex justify-center items-center dark:hover:bg-gray-600 dark:hover:text-white"
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
        </div>
        <!-- Modal body -->

        <form :onsubmit="(e) => e.preventDefault()" class="p-4 md:p-5">
          <div class="grid gap-4 mb-4 grid-cols-2">
            <div class="col-span-2">
              <label for="name" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
                >Содержание</label
              >
              <textarea
                :readonly="
                  !mystore.auth.permissions.some(
                    (obj) => obj.name === 'editor' || obj.name === 'admin' || obj.name === 'owner'
                  ) || this.content.is_approved !== 'OPEN' || this.content.is_approved  === undefined
                "
                type="text"
                name="name"
                id="name"
                class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500"
                placeholder="Содержание поста"
                required
                :value="content.content"
                @input="(event) => (areaContent = event.target.value)"
              />
              {{ text }}
            </div>
            <div
              class="col-span-2"
              v-if="
                !this.creation &&
                this.content.is_approved === 'APPROVED' &&
                this.content.sent_status !== 'WAITING'
              "
            >
              <label for="name" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
                >Запланировать</label
              >
              <div class="flex gap-2">
                <div class="relative max-w-sm">
                  <div
                    class="absolute inset-y-0 start-0 flex items-center ps-3.5 pointer-events-none"
                  >
                    <svg
                      class="w-4 h-4 text-gray-500 dark:text-gray-400"
                      aria-hidden="true"
                      xmlns="http://www.w3.org/2000/svg"
                      fill="currentColor"
                      viewBox="0 0 20 20"
                    >
                      <path
                        d="M20 4a2 2 0 0 0-2-2h-2V1a1 1 0 0 0-2 0v1h-3V1a1 1 0 0 0-2 0v1H6V1a1 1 0 0 0-2 0v1H2a2 2 0 0 0-2 2v2h20V4ZM0 18a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V8H0v10Zm5-8h10a1 1 0 0 1 0 2H5a1 1 0 0 1 0-2Z"
                      />
                    </svg>
                  </div>
                  <input
                    datepicker
                    type="date"
                    class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full ps-10 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                    placeholder="Select date"
                    v-model="date"
                  />
                </div>
                <div class="relative">
                  <div
                    class="absolute inset-y-0 end-0 top-0 flex items-center pe-3.5 pointer-events-none"
                  >
                    <svg
                      class="w-4 h-4 text-gray-500 dark:text-gray-400"
                      aria-hidden="true"
                      xmlns="http://www.w3.org/2000/svg"
                      fill="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        fill-rule="evenodd"
                        d="M2 12C2 6.477 6.477 2 12 2s10 4.477 10 10-4.477 10-10 10S2 17.523 2 12Zm11-4a1 1 0 1 0-2 0v4a1 1 0 0 0 .293.707l3 3a1 1 0 0 0 1.414-1.414L13 11.586V8Z"
                        clip-rule="evenodd"
                      />
                    </svg>
                  </div>
                  <input
                    type="time"
                    id="time"
                    class="bg-gray-50 border leading-none border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                    value="00:00"
                    required
                    v-model="time"
                  />
                </div>
              </div>
            </div>
          </div>
          <div class="flex justify-between">
            <button
              v-if="this.content.is_approved !== 'APPROVED'"
              @click="addChannel"
              type="submit"
              class="text-white inline-flex items-center bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
            >
              <svg
                class="me-1 -ms-1 w-5 h-5"
                fill="currentColor"
                viewBox="0 0 20 20"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  fill-rule="evenodd"
                  d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z"
                  clip-rule="evenodd"
                ></path>
              </svg>
              {{ buttonText }}
            </button>
            <button
              v-if="
                !this.creation &&
                this.content.is_approved === 'APPROVED' &&
                this.content.sent_status !== 'WAITING'
              "
              @click="schedulePost"
              type="submit"
              class="text-white inline-flex items-center bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
            >
              Запланировать
            </button>
            <button v-if="!this.creation && this.content.is_approved === 'APPROVED'"></button>
          </div>
        </form>
      </div>
    </div>
  </div>
  {{ post_id }}
</template>
<script>
import { defineComponent } from 'vue'
import { api } from '@/logic/api.js'
import { store } from '@/store/index.js'

export default defineComponent({
  name: 'ModalPost',
  props: {
    isShown: Boolean,
    closeModal: Function,
    content: Object,
    creation: Boolean,
    id: String,
    post_id: Number
  },
  data() {
    return {
      text: '',
      areaContent: '',
      time: '',
      date: '',
      mystore: null
    }
  },
  computed: {
    buttonText() {
      return this.creation ? 'Создать пост' : 'Сохранить пост'
    }
  },
  beforeMount() {
    this.mystore = store
  },
  methods: {
    addChannel() {
      api
        .addPost(this.id, this.areaContent)
        .then(() => {
          api.getPosts(this.id).then((data) => {
            store.data.posts = data
          })
          this.closeModal()
        })
        .catch((e) => {
          this.text = e
        })
    },
    schedulePost() {
      console.log(this.date, this.time)
      api
        .schedulePost(this.id, this.convertToISODateTime(this.date, this.time), this.post_id)
        .then(() => {
          api.getPosts(this.id).then((data) => {
            store.data.posts = data
          })
          this.closeModal()
        })
    },
    convertToISODateTime(dateString, timeString) {
      const combinedDateTimeString = `${dateString}T${timeString}:00`

      const date = new Date(combinedDateTimeString)

      const isoDateTimeString = date.toISOString()

      return isoDateTimeString
    }
  }
})
</script>
