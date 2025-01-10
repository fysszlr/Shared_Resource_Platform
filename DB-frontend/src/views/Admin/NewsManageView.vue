<template>
  <v-container class="spacing-playground pa-16" fluid style="width: 85%;">
    <div>
      <loading v-if="loading"></loading>
      <template v-else>
        <v-row justify="center">
          <v-expansion-panels inset v-model="activePanel">
            <v-expansion-panel
              v-for="(item, i) in news"
              :key="i"
            >
              <v-expansion-panel-header>
                <div style="display: flex; justify-content: space-between; width: 100%;">
                  <div>{{ item.title }}</div>
                  <div style="color: grey; text-align: right; margin-right: 16px;">
                    <span>{{ formatDate(item.notified_at) }}</span>
                  </div>
                </div>
              </v-expansion-panel-header>
              <v-expansion-panel-content>
                <v-md-preview :text="item.content"></v-md-preview>
                <!-- <v-btn block @click="initAnnouncementModifyDialog(item)"> 修改公告 </v-btn> -->

                <v-dialog v-model="dialog_modifyannouncement" width="50%">
                  <v-card>
                    <v-card-title>
                      修改公告
                    </v-card-title>
                    <v-card-text>
                      <v-text-field label="公告标题" filled outlined v-model="announcementTitle"></v-text-field>
                      <v-textarea label="公告内容" filled outlined rows="20" v-model="announcementContent"></v-textarea>
                    </v-card-text>
                    <v-divider></v-divider>
                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn color="primary" text @click="modifyAnnouncement(item)" :disabled="loading"
                        :loading="loading"> 修改
                      </v-btn>
                      <v-btn color="error" text @click="dialog_modifyannouncement = false" :disabled="loading"> 取消
                      </v-btn>
                    </v-card-actions>
                  </v-card>
                </v-dialog>

              </v-expansion-panel-content>
            </v-expansion-panel>
          </v-expansion-panels>
        </v-row>
        <v-banner v-if="news.length === 0">
          好吧，看起来现在还没有公告。
        </v-banner>
      </template>
    </div>
    <v-btn class="fixed-button1" fab dark color="indigo" @click="dialog_openannouncement = true">
      <v-icon dark>
        mdi-invoice-plus
      </v-icon>
    </v-btn>
    <v-dialog v-model="dialog_openannouncement" width="50%">
      <v-card>
        <v-card-title>
          新建公告
        </v-card-title>
        <v-card-text>
          <v-text-field label="公告标题" v-model="announcementTitle"></v-text-field>
          <v-textarea label="公告内容" rows="20" v-model="announcementContent"></v-textarea>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="publishAnnouncement" :disabled="loading" :loading="loading"> 发布 </v-btn>
          <v-btn color="error" text @click="cancelPublishAnnouncement" :disabled="loading"> 取消 </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import { format } from 'date-fns';
import VMdPreview from '@kangc/v-md-editor/lib/preview';
import '@kangc/v-md-editor/lib/style/preview.css';
import githubTheme from '@kangc/v-md-editor/lib/theme/github.js';
import '@kangc/v-md-editor/lib/theme/style/github.css';
import hljs from 'highlight.js';
VMdPreview.use(githubTheme, {
  Hljs: hljs,
});
import Loading from '@/components/Loading.vue';
export default {
  name: "NewsList",
  components: {
    VMdPreview,
    Loading,
  },
  data() {
    return {
      news: [],
      loading: true,
      activePanel: 0, // 默认展开第一个面板，设置为数字

      dialog_openannouncement: false,
      dialog_modifyannouncement: false,

      announcementTitle: "",
      announcementContent: "",
    }
  },
  mounted() {
    this.$store.commit("setAppTitle", "公告管理");
    this.$store.dispatch("getNews", { page: 1 })
      .then(res => {
        this.news = res.messages;
        this.news.sort((a, b) => new Date(b.notified_at) - new Date(a.notified_at));
      })
      .catch(_ => {
        this.news = [];
        this.$store.commit("setAlert", { type: "error", message: "无法获取公告。请检查你的网络设置。" })
      })
      .finally(() => {
        this.loading = false;
      });
  },
  methods: {
    formatDate(dateString) {
      return format(new Date(dateString), 'yyyy-MM-dd HH:mm:ss');
    },
    cancelPublishAnnouncement() {
      this.dialog_openannouncement = false;
    },
    publishAnnouncement() {
      this.loading = true;
      this.$store.dispatch("publishAnnouncement", {
        title: this.announcementTitle,
        content: this.announcementContent,
      })
      .then(_ => {
          this.$store.commit("setAlert", { type: "success", message: "公告发布成功。" });
          this.loading = true;
          this.$store.dispatch("getNews", {page: 1})
            .then(res => {
              this.news = res.messages;
              this.news.sort((a, b) => new Date(b.notified_at) - new Date(a.notified_at));
            })
            .catch(_ => {
              this.news = [];
              this.$store.commit("setAlert", { type: "error", message: "无法获取公告。请检查你的网络设置。" })
            });
        })
        .catch(_ => {
          this.$store.commit("setAlert", { type: "error", message: "无法发布公告。请检查你的网络设置。" });
        })
        .finally(() => {
          this.dialog_openannouncement = false;
          this.loading = false;
        });
    },
    initAnnouncementModifyDialog(item) {
      this.announcementTitle = item.title;
      this.announcementContent = item.content;
      this.dialog_modifyannouncement = true;
    },
    modifyAnnouncement(item) {
      this.loading = true;
      // todo 需要写一下store的action
      this.$store.dispatch("modifyAnnouncement", {
        aid: item.aid,
        title: this.announcementTitle,
        content: this.announcementContent,
      })
        .then(_ => {
          this.$store.commit("setAlert", { type: "success", message: "公告修改成功。" });
          this.loading = true;
          this.$store.dispatch("getNews")
            .then(res => {
              this.news = res.announcements;
            })
            .catch(_ => {
              this.news = [];
              this.$store.commit("setAlert", { type: "error", message: "无法获取公告。请检查你的网络设置。" })
            });
        })
        .catch(_ => {
          this.$store.commit("setAlert", { type: "error", message: "无法修改公告。请检查你的网络设置。" });
        })
        .finally(() => {
          this.dialog_modifyannouncement = false;
          this.loading = false;
        });
    }
  },
  watch: {
    dialog_openannouncement(val) {
      this.announcementContent = "";
      this.announcementTitle = "";
    },
    dialog_modifyannouncement(val) {
      if (!val) {
        this.announcementContent = "";
        this.announcementTitle = "";
      }
    },
  }
}
</script>

<style scoped>
  .v-expansion-panel-header {
    font-size: large;
  }

  .loading-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
  }

  .panel-content {
    margin-top: 30px;
  }

  .fixed-button1 {
    position: fixed;
    right: 4%;
    bottom: 16%;
    z-index: 5;
  }
</style>
