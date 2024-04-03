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
    <div class="relative p-4 w-full max-w-lg max-h-full top-0 right-0 left-0 z-50">
      <div class="relative bg-white rounded-lg shadow dark:bg-gray-700 md:min-w-[600px] w-72">
        <div
          class="flex items-center justify-between p-4 md:p-5 border-b rounded-t dark:border-gray-600"
        >
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Пост</h3>
          <div class="flex">
            <button
              @click="deletePost"
              v-if="
                this.mystore.auth.permissions.some(
                  (obj) => obj.name === 'admin' || obj.name === 'owner'
                ) && !this.creation
              "
              class="mb-2 z-40 mr-4 bg-red-100 p-[4px] px-2 hover:bg-red-200 rounded-lg flex text-red-600"
            >
              <svg
                class="w-6 h-6 text-gray-800 dark:text-white"
                aria-hidden="true"
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                fill="none"
                viewBox="0 0 24 24"
              >
                <path
                  stroke="rgb(220 38 38)"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M5 7h14m-9 3v8m4-8v8M10 3h4a1 1 0 0 1 1 1v3H9V4a1 1 0 0 1 1-1ZM6 7h12v13a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V7Z"
                />
              </svg>
            </button>
            <div>
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
        </div>
        <!-- Modal body -->

        <form :onsubmit="(e) => e.preventDefault()" class="p-4 md:p-5">
          <div class="grid gap-4 mb-4 grid-cols-1">
            <div class="col-span-2 max-w-full">
              <div class="mb-2 focus:outline-0" v-if="this.content.is_approved === 'REJECTED'">
                <div
                  class="bg-red-100 resize-none focus:outline-0 outline-0 focus:shadow-outline border-0 border-gray-200 text-red-600 text-sm rounded-md block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white"
                >
                  {{ content.comment }}
                </div>
              </div>
              <label for="name" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
                >Содержание</label
              >
              <textarea
                v-if="!this.creation"
                :readonly="
                  !mystore.auth.permissions.some(
                    (obj) => obj.name === 'editor' || obj.name === 'admin' || obj.name === 'owner'
                  ) || this.content.is_approved === 'APPROVED'
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
              <textarea
                v-else
                :readonly="
                  !mystore.auth.permissions.some(
                    (obj) => obj.name === 'editor' || obj.name === 'admin' || obj.name === 'owner'
                  ) || this.content.is_approved === 'APPROVED'
                "
                type="text"
                name="name"
                id="name"
                class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500"
                placeholder="Содержание поста"
                required
                v-model="areaContent"
              />
              {{ text }}
            </div>
            <form
              class="flex gap-2"
              :onsubmit="
                (e) => {
                  e.preventDefault()
                  onTagAdd()
                }
              "
            >
              <input
                type="text"
                name="name"
                class="bg-gray-50 flex-1 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500"
                placeholder="Тэг"
                v-model="this.tag"
              />
              <button
                @click="onTagAdd"
                class="flex items-center justify-between text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-2 py-2 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
                type="button"
              >
                <svg
                  class="w-6 h-6 text-gray-800 dark:text-white"
                  aria-hidden="true"
                  xmlns="http://www.w3.org/2000/svg"
                  width="24"
                  height="24"
                  fill="none"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke="#FFF"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M5 12h14m-7 7V5"
                  />
                </svg>
              </button>
            </form>
            <br />
            <div class="flex grid-2 overflow-scroll max-w-full">
              <span
                v-for="tag of this.tags"
                class="inline-flex items-center px-2 py-1 me-2 text-sm font-medium text-blue-800 bg-blue-100 rounded dark:bg-blue-900 dark:text-blue-300"
              >
                {{ tag }}
                <button
                  type="button"
                  class="inline-flex items-center p-1 ms-2 text-sm text-blue-400 bg-transparent rounded-sm hover:bg-blue-200 hover:text-blue-900 dark:hover:bg-blue-800 dark:hover:text-blue-300"
                  data-dismiss-target="#badge-dismiss-default"
                  aria-label="Remove"
                  @click="() => deleteTag(tag)"
                >
                  <svg
                    class="w-2 h-2"
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
                  <span class="sr-only">Remove badge</span>
                </button>
              </span>
            </div>
            <div
              class="col-span-2"
              v-if="
                !this.creation &&
                this.content.is_approved === 'APPROVED' &&
                this.content.sent_status !== 'WAITING'
              "
            >
              <label
                for="name"
                class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
              >
                Запланировать
              </label>
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
                    :disabled="
                      !mystore.auth.permissions.some(
                        (obj) =>
                          obj.name === 'reviewer' || obj.name === 'admin' || obj.name === 'owner'
                      )
                    "
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
                    :disabled="
                      !mystore.auth.permissions.some(
                        (obj) =>
                          obj.name === 'reviewer' || obj.name === 'admin' || obj.name === 'owner'
                      )
                    "
                  />
                </div>
              </div>
            </div>
          </div>
          <div v-if="this.creation">
            <label for="name" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
              >Каналы</label
            >
            <div v-for="channel in channels" :key="channel.id" class="flex items-center mb-4">
              <input
                :id="channel.id"
                type="checkbox"
                :onchange="
                  (e) => {
                    if (e.target.checked) {
                      this.myId = [...this.myId, channel.id]
                    } else {
                      this.myId = this.avId.filter((newId) => newId !== channel?.id)
                    }
                  }
                "
                :checked="false"
                class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600"
              />
              <label
                :for="channel.id"
                class="ms-2 text-sm font-medium text-gray-900 dark:text-gray-300"
              >
                {{ channel.name }}
              </label>
            </div>
          </div>
          <div v-else>
            <label for="name" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">
              Каналы
            </label>
            <div v-for="channel in channels" :key="channel.id" class="flex items-center mb-4">
              <input
                :id="channel"
                type="checkbox"
                :onchange="
                  (e) => {
                    if (e.target.checked) {
                      this.myId = [...this.myId, channel.id]
                    } else {
                      this.myId = this.passId.filter((newId) => newId !== channel?.id)
                    }
                  }
                "
                :disabled="
                  this.content.sent_status === 'WAITING' ||
                  this.content.is_approved === 'WAITING' ||
                  this.content.is_approved === 'APPROVED' ||
                  !this.mystore.auth.permissions.some(
                    (obj) => obj.name === 'admin' || obj.name === 'editor' || obj.name === 'owner'
                  )
                "
                :checked="isChecked2(channel.id)"
                class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600"
              />
              <label
                :for="channel.id"
                class="ms-2 text-sm font-medium text-gray-900 dark:text-gray-300"
              >
                {{ channel.name }}
              </label>
            </div>
          </div>

          <div class="flex justify-between gap-2 flex-wrap">
            <button
              v-if="
                this.content.sent_status !== 'WAITING' &&
                this.content.is_approved !== 'APPROVED' &&
                this.mystore.auth.permissions.some(
                  (obj) => obj.name === 'editor' || obj.name === 'owner' || obj.name === 'admin'
                )
              "
              @click="addPost"
              type="submit"
              class="text-white mr-2 mb-2 inline-flex items-center bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
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
                this.content.sent_status !== 'WAITING' &&
                this.mystore.auth.permissions.some(
                  (obj) => obj.name === 'reviewer' || obj.name === 'admin' || obj.name === 'owner'
                ) &&
                this.channels?.length > 0
              "
              @click="schedulePost"
              type="submit"
              class="text-white inline-flex mb-2 items-center bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
            >
              Запланировать
            </button>
            <button
              @click="sendToReview"
              class="text-white inline-flex mb-2 items-center bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
              v-if="
                !this.creation &&
                this.content.is_approved === 'OPEN' &&
                mystore.auth.permissions.some(
                  (obj) => obj.name === 'editor' || obj.name === 'admin' || obj.name === 'owner'
                )
              "
            >
              Отправить на одобрение
            </button>
            <div
              class="flex md:mt-0 mt-4"
              v-if="
                !this.creation &&
                this.content.is_approved === 'WAITING' &&
                mystore.auth.permissions.some(
                  (obj) => obj.name === 'reviewer' || obj.name === 'admin' || obj.name === 'owner'
                )
              "
            >
              <button
                @click="approvePost"
                class="text-white mr-2 mb-2 inline-flex items-center bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
              >
                Одобрить
              </button>
              <button
                @click="rejectPost"
                class="text-white inline-flex mb-2 items-center bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
              >
                Отклонить
              </button>
            </div>
          </div>
          <div v-if="this.content.is_approved === 'WAITING' && this.showCommentArea">
            <label for="name" class="block my-2 text-sm font-medium text-gray-900 dark:text-white"
              >Оставьте комментарий</label
            >
            <textarea
              :readonly="
                !mystore.auth.permissions.some(
                  (obj) => obj.name === 'reviewer' || obj.name === 'admin' || obj.name === 'owner'
                ) || this.content.is_approved === 'APPROVED'
              "
              type="text"
              name="comment"
              id="comment"
              class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500"
              placeholder="Комментарий проверяющего"
              required
              v-model="newComment"
            />
          </div>
        </form>
      </div>
    </div>
  </div>
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
    post_id: Number,
    channels: Object,
    tags: Array
  },
  data() {
    return {
      text: '',
      areaContent: '',
      commentContent: '',
      time: '',
      date: '',
      mystore: null,
      canEdit: false,
      mychannels: this.$props.channels,
      myId: [],
      passId: [],
      newComment: '',
      showCommentArea: false,
      tag: '',
      tags: JSON.parse(JSON.stringify(this.$props?.tags) || '[]') || [],
      newAddedPostId: ''
    }
  },
  computed: {
    buttonText() {
      if (this.content.is_approved === 'APPROVED') {
        return 'В редактирование'
      }
      return this.creation ? 'Создать пост' : 'Сохранить пост'
    }
  },
  beforeMount() {
    this.text = ''
    this.mystore = store
    this.avId = this.channels.map((el) => el.id)
    this.passId = this.content?.channels?.map((ch) => ch.id)
  },
  methods: {
    isChecked(chid) {
      return this.avId.find((id) => {
        return id !== chid
      })
    },
    onTagAdd() {
      console.log(1)
      if (!this.tag || this.tags.includes(this.tag)) {
        return
      }

      this.tags.push(this.tag)
      this.tag = ''
    },
    deleteTag(tag) {
      this.tags = [...this.tags].filter((targetTag) => tag !== targetTag)
    },
    isChecked2(chid) {
      return this.passId.find((id) => {
        return id === chid
      })
    },
    async addPost() {
      if (this.creation) {
        api
          .addPost(this.id, this.areaContent, { channels: this.myId })
          .then((data) => {
            api.addTagsToPost(this.id, data.post.id, this.tags).then(() => {
              const newPosts = [...store.data.posts]
              const targetIndex = store.data.posts.indexOf(
                ({ post_id }) => post_id === this.post_id
              )

              newPosts[targetIndex] = { ...newPosts[targetIndex], tags: this.tags }
              store.data.posts = newPosts
            }).then(
              api.getPosts(this.id).then((data) => {
              store.data.posts = data
            })
            )
           
            this.closeModal()
            this.myId = []
            this.mychannels = [...this.$props.channels]
          })
          .catch((e) => {
            this.text = e
          })
      } else {
        await api.addTagsToPost(this.id, this.post_id, this.tags).then(() => {
          const newPosts = [...store.data.posts]
          const targetIndex = store.data.posts.indexOf(({ post_id }) => post_id === this.post_id)

          newPosts[targetIndex] = { ...newPosts[targetIndex], tags: this.tags }
          store.data.posts = newPosts
        })
        let content = this.areaContent === '' ? this.content.content : this.areaContent
        api
          .patchPost(this.id, this.post_id, {
            content: content,
            is_approved: this.content.is_approved,
            channels: this.myId
          })
          .then(() => {
            api.getPosts(this.id).then((data) => {
              store.data.posts = data
            })
            this.myId = []
          })
        this.closeModal()
      }
    },
    schedulePost() {
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
    },
    sendToReview() {
      api.patchPost(this.id, this.post_id, { is_approved: 'WAITING' }).then(() => {
        api.getPosts(this.id).then((data) => {
          store.data.posts = data
        })
      })
      this.closeModal()
    },
    approvePost() {
      api
        .patchPost(this.id, this.post_id, {
          is_approved: 'APPROVED',
          comment: this.newComment
        })
        .then(() => {
          api.getPosts(this.id).then((data) => {
            store.data.posts = data
          })
        })
      this.closeModal()
    },
    rejectPost() {
      if (this.showCommentArea) {
        api
          .patchPost(this.id, this.post_id, {
            is_approved: 'REJECTED',
            comment: this.newComment,
            channels: this.myId
          })
          .then(() => {
            api.getPosts(this.id).then((data) => {
              store.data.posts = data
            })
          })
        this.closeModal()
      } else {
        this.showCommentArea = true
      }
    },
    deletePost() {
      api
        .deletePosts(this.id, this.post_id)
        .then(() => {
          api.getPosts(this.id).then((data) => {
            store.data.posts = data
          })
          this.closeModal()
        })
        .catch((e) => {
          api.getPosts(this.id).then((data) => {
            store.data.posts = data
          })
          this.text = e
        })
    }
  }
})
</script>
