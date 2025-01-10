<template>
  <v-container class="mt-5">
    <!-- 任务部分 -->
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card class="pa-5">
          <div class="task-header">
            <!-- 标题部分 -->
            <span class="title font-weight-bold">{{ task.title }}</span>
            <!-- 时间和状态部分 -->
            <div class="d-flex align-center mt-1">
              <v-avatar size="32">
                <img :src="task.created_by.avatar" alt="avatar">
              </v-avatar>
              <div class="task-time text-grey text--small">
                <a :href="`/center/${task.created_by.user_id}`" @click.stop class="ml-2" style="font-size: 16px;" target="blank">{{ task.created_by.username }}</a>
                发布于：{{ new Date(task.created_at).toLocaleString() }}
              </div>
              <v-chip
                :color="task.open ? 'green' : 'red'"
                class="ml-3"
                outlined
                small
              >
                {{ task.open ? '进行中' : '已关闭' }}
              </v-chip>
            </div>
          </div>
          <v-row align="center">
            <v-col cols="auto">
              <div class="task-tags mt-2">
                <!-- 标签部分 -->
                <v-chip
                  v-for="(tag, index) in task.tags"
                  :key="index"
                  class="ml-1"
                  color="green"
                  dark
                  big
                >
                  {{ tag }}
                </v-chip>
              </div>
            </v-col>
            <v-col cols="auto">
              <v-btn @click="modifyDialog = true">
                <v-icon left>mdi-pencil</v-icon>
                编辑任务
              </v-btn>
            </v-col>
          </v-row>
          <v-divider class="my-3"></v-divider>
          <v-md-preview :text="task.content" />
        </v-card>
      </v-col>
    </v-row>
    <!-- 回答部分 -->
    <v-row justify="center" class="mt-4">
      <v-col cols="12" md="8">
        <v-card v-for="(submit, index) in submits" :key="index" class="mb-3">
          <div class="d-flex align-center">
            <v-avatar size="32">
            <img :src="submit.created_by.avatar" alt="avatar">
            </v-avatar>
              <a :href="`/center/${submit.created_by.user_id}`" @click.stop class="ml-2" style="font-size: 20px;" target="blank">{{ submit.created_by.username }}</a>
            <div class="text-grey ml-auto">{{ formatDate(submit.created_at) }}</div>
          </div>
          <div class="mt-2" style="font-size: 18px;">{{ submit.profile }}</div>
          <div class="mt-3">
            <v-btn @click="openBhpan(submit)" color="primary" outlined class="mr-3">下载资源</v-btn>
            <v-btn v-if="task.open==true" @click="confirmAnswer(submit)">认同答案</v-btn>
          </div>
        </v-card>
      </v-col>
    </v-row>

    <!-- 弹窗 -->
    <v-dialog v-model="dialog" max-width="400">
      <v-card>
        <v-card-title class="headline">确认操作</v-card-title>
        <v-card-text>您确定要认同此答案吗？认同此答案后，全部悬赏菜币将分发给此用户，本任务也将不再接受其他回答。</v-card-text>
        <v-card-actions>
          <v-btn color="blue darken-1" text @click="dialog = false">取消</v-btn>
          <v-btn color="green darken-1" text @click="approveAnswer">确认</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog fullscreen v-model="modifyDialog" hide-overlay transition="dialog-bottom-transition">
      <v-toolbar
        dark
        color="primary"
      >
        <v-btn
          icon
          dark
          @click="modifyDialog = false"
        >
          <v-icon>mdi-close</v-icon>
        </v-btn>
        <v-toolbar-title>编辑任务</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-toolbar-items>
          <v-btn
            dark
            text
            @click="saveTask"
          >
            保存
          </v-btn>
        </v-toolbar-items>
      </v-toolbar>
      <v-card>
        <v-col>
          <v-row>
            <v-col>
              <v-text-field
                v-model="newTask.title"
                label="标题"
                :rules="[v => !!v || '标题不能为空']"
                aria-required=""
              ></v-text-field>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="6">
              <v-text-field
              v-model="newTask.commission"
              label="报酬"
              :rules="[
                v => v !== null && v !== '' || '报酬不能为空',
                v => /^\d+$/.test(v) || '报酬必须是非负整数'
              ]"
              required
              ></v-text-field>
            </v-col>
            <v-col cols="6">
              <v-autocomplete
                v-model="newTask.tags"
                :items="tags_to_select"
                color="blue-grey lighten-2"
                label="标签"
                item-text="name"
                item-value="name"
                multiple
                hide-selected
              >
                <template v-slot:selection="data">
                  <v-chip
                    v-bind="data.attrs"
                    :input-value="data.selected"
                    close
                    @click="data.select"
                    @click:close="removeTag(data.item)"
                  >
                    {{ data.item.name }}
                  </v-chip>
                </template>
                <template v-slot:item="data">
                  <template v-if="typeof data?.item !== 'object'">
                    <v-list-item-content> {{ data.item }} </v-list-item-content>
                  </template>
                  <template v-else>
                    <v-list-item-content>
                    <v-list-item-title>{{ data.item.name }}</v-list-item-title>
                    </v-list-item-content>
                  </template>
                </template>
              </v-autocomplete>
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <v-textarea
                v-model="newTask.content"
                label="描述"
                rows="18"
              ></v-textarea>
            </v-col>
            <v-col>
              <v-md-preview :text="newTask.content" default-show-toc="True"></v-md-preview>
            </v-col>
          </v-row>
        </v-col>
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

export default {
  name: 'TaskPost',
  components: {
    VMdPreview,
    format
  },
  props: {
    task: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      newTask: {
        title: "",
        content: "",
        tags: [],
        commission: 0,
      },
      tags_to_select: [],
      modifyDialog: false,
      dialog: false,
      selectedSubmit: null,
      submits: [],
    };
  },
  watch: {
    modifyDialog: {
      handler(newVal) {
        if (newVal) {
          this.newTask = JSON.parse(JSON.stringify(this.task));
          if (this.tags_to_select.length === 0) {
            this.$store.dispatch("getTags", {key_word: ""})
              .then((res) => {
                this.tags_to_select = res.tags.map((tag) => {
                  return {
                    name: tag,
                  };
                });
              })
              .catch((err) => {
                this.$store.commit("setAlert", {
                  type: "error",
                  message: err,
                });
              });
          }
        }
      },
    },
  },
  methods: {
    formatDate(date) {
      return format(new Date(date), 'yyyy-MM-dd HH:mm:ss');
    },
    saveTask() {
      this.$store.dispatch("modifyTask", {
        id: this.task.mission_id,
        title: this.newTask.title,
        commission: this.newTask.commission,
        tags: this.newTask.tags,
        content: this.newTask.content,
      })
        .then(() => {
          this.$store.commit("setAlert", {
            type: "success",
            message: "任务修改成功。",
          });
          this.modifyDialog = false;
          this.task = JSON.parse(JSON.stringify(this.newTask));
        })
        .catch((err) => {
          this.$store.commit("setAlert", {
            type: "error",
            message: err,
          });
        });
    },
    openBhpan(submit) {
      window.open(submit.bhpan_url);
    },
    confirmAnswer(submit) {
      this.selectedSubmit = submit;
      this.dialog = true;
    },
    approveAnswer() {
      this.$store.dispatch("confirmTask", {task_id: this.task.mission_id, submit_id: this.selectedSubmit.submit_id})
        .then(() => {
          this.$store.commit("setAlert", {
            type: "success",
            message: "任务已关闭，悬赏菜币已分发。",
          });
          this.dialog = false;
          this.$router.push({ name: "/tasks" });
        })
        .catch((err) => {
          this.$store.commit("setAlert", {
            type: "error",
            message: err,
          });
        });
    },
    removeTag(item) {
      const index = this.newTask.tags.indexOf(item.name);
      if (index >= 0) this.newTask.tags.splice(index, 1);
    },
  },
  mounted() {
    this.$store.dispatch("getTaskSubmits", { id: this.task.mission_id })
      .then((res) => {
        this.submits = res.submits;
      })
      .catch((err) => {
        this.$store.commit("setAlert", {
          type: "error",
          message: err,
        });
      });
  }
};
</script>

<style>
.task-time {
  font-size: 14px;
  color: #757575;
  margin-left: 8px;
}

.return-button {
  position: fixed;
  left: 65px;
  top: 80px;
  background-color: #9dedf0;
  color: white;
  border-radius: 50%;
  padding: 8px;
  z-index: 1000;
}

.task-header {
  margin-bottom: 8px;
}

.task-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.title {
  font-size: 24px;
}

.v-container {
  max-width: 960px;
  margin: 0 auto;
}

.v-card {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.answer-actions {
  display: flex;
  gap: 12px;
  margin-top: -20px;
  margin-left: 7px;
}

.answer-actions button {
  padding: 7px 12px;
  border: none;
  background-color: #007bff;
  color: #fff;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.answer-actions button:hover {
  background-color: #0056b3;
}
</style>