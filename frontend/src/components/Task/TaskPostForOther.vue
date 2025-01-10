<template>
  <v-container class="center-container">
    <!-- 任务部分 -->
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card class="pa-5">
          <v-btn
            outlined
            color="primary"
            class="write-answer-button"
            @click="dialog = true"
          >
            <v-icon left>mdi-pencil</v-icon>
            上传资源
          </v-btn>
          <div class="task-header">
            <!-- 标题部分 -->
            <span class="title font-weight-bold">{{ task.title }}</span>
            <!-- 时间和状态部分 -->
            <div class="d-flex align-center mt-1">
              <div class="task-time text-grey text--small">
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
          <v-divider class="my-3"></v-divider>
          <v-md-preview :text="task.content"></v-md-preview>
        </v-card>
      </v-col>
    </v-row>

    <!-- 上传资源弹框 -->
    <v-dialog v-model="dialog" persistent max-width="500px">
      <v-card>
        <v-card-title>上传资源</v-card-title>
        <v-card-text>
          <v-form ref="form" v-model="valid">
            <v-text-field
              v-model="resourceDescription"
              label="资源简介"
              :rules="[rules.required]"
              required
            ></v-text-field>
            <v-text-field
              v-model="resourceUrl"
              label="资源链接"
              :rules="[rules.required, rules.url]"
              required
            ></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-btn text color="primary" @click="dialog = false">取消</v-btn>
          <v-btn
            text
            color="primary"
            :disabled="!valid"
            @click="submitResource"
          >
            提交
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import VMdPreview from '@kangc/v-md-editor/lib/preview';
import '@kangc/v-md-editor/lib/style/preview.css';
import githubTheme from '@kangc/v-md-editor/lib/theme/github.js';
import '@kangc/v-md-editor/lib/theme/style/github.css';
import hljs from 'highlight.js';

VMdPreview.use(githubTheme, {
  Hljs: hljs,
});

export default {
  components: {
    VMdPreview
  },
  props: {
    task: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      dialog: false,
      valid: false,
      resourceDescription: '',
      resourceUrl: '',
      rules: {
        required: (value) => !!value || '必填项',
        url: (value) => {
          const urlPattern = new RegExp(
            "^(https?:\\/\\/)?" + // 支持 http 和 https
            "((([a-zA-Z\\d]([a-zA-Z\\d-]*[a-zA-Z\\d])*)\\.)+[a-zA-Z]{2,}|" + // 域名
            "((\\d{1,3}\\.){3}\\d{1,3}))" + // 或 IP 地址
            "(\\:\\d+)?(\\/[-a-zA-Z\\d%_.~+&]*)*" + // 端口和路径
            "(\\?[;&a-zA-Z\\d%_.~+=-]*)?" + // 查询参数
            "(\\#[-a-zA-Z\\d%_.~+=&]*)?$", // 锚点
            "i" // 忽略大小写
          );
          return urlPattern.test(value) || '链接格式不正确。';
        }
      },
    };
  },

  methods: {
    submitResource() {
      const resource = {
        id: this.task.mission_id,
        profile: this.resourceDescription,
        bhpan_url: this.resourceUrl,
      };
      this.$store.dispatch('submitTask', resource)
        .then(() => {
          this.$store.commit('setAlert', {
            type: 'success',
            message: '资源提交成功！',
          });
          this.dialog = false;
          this.resourceDescription = '';
          this.resourceUrl = '';
        })
        .catch((err) => {
          this.$store.commit('setAlert', {
            type: 'error',
            message: err,
          });
        });
    },
  },
  mounted() {
  },
};
</script>

<style>
.center-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh; /* 占满屏幕高度 */
  padding: 16px; /* 防止卡片紧贴屏幕边缘 */
}

.return-button {
  position: fixed;
  left: 65px;
  top: 80px;
  background-color: #9dedf0;
  color: white;
  border-radius: 50%;
  padding: 10px;
  z-index: 1000;
}

.write-answer-button {
  position: absolute;
  top: 55px;
  right: 30px;
  z-index: 10;
  font-size: 14px;
  font-weight: 500;
  text-transform: none; /* 保持按钮文字原样 */
  border-radius: 8px; /* 圆角效果 */
  padding: 6px 12px; /* 内边距调整 */
  min-width: auto; /* 去掉按钮的最小宽度 */
}

.task-time {
  font-size: 16px; /* 调大时间字体 */
  color: #757575;
  margin-left: 8px;
}

.task-header {
  margin-bottom: 12px;
}

.task-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 12px; /* 增加标签间距 */
}

.title {
  font-size: 28px; /* 增大标题字体 */
  font-weight: bold;
}

.v-card {
  box-shadow: 0 6px 8px rgba(0, 0, 0, 0.1); /* 提升阴影效果 */
  padding: 24px; /* 增加卡片内边距 */
  font-size: 18px; /* 增大卡片内文字大小 */
  line-height: 1.6; /* 提高文字可读性 */
}

.v-chip {
  font-size: 16px; /* 调大标签字体 */
  height: 36px; /* 增加标签高度 */
  border-radius: 18px; /* 更圆润的标签样式 */
}

.v-divider {
  height: 2px; /* 调整分隔线的厚度 */
  background-color: #e0e0e0;
}
</style>