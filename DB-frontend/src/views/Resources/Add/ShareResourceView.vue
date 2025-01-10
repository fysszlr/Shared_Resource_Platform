<template>
  <v-container>
    <v-col>
      <v-row>
        <v-col>
          <v-text-field
            v-model="title"
            label="标题"
            :rules="[v => !!v || '标题不能为空']"
            aria-required=""
          ></v-text-field>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="6">
          <v-text-field
            v-model="cost"
            label="收费金额"
            :rules="[
              v => v !== null && v !== '' || '费用不能为空',
              v => /^\d+$/.test(v) || '费用必须是非负整数'
            ]"
            required
          ></v-text-field>
        </v-col>
        <v-col cols="6">
          <v-autocomplete
            v-model="tags"
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
                @click:close="remove(data.item)"
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
          <v-text-field
            v-model="link"
            :label="labelText"
            :rules="[rules.required, rules.isValidUrl]"
            aria-required=""
          ></v-text-field>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-textarea
            v-model="content"
            label="描述"
            rows="16"
          ></v-textarea>
        </v-col>
        <v-col>
          <v-md-preview :text="content" default-show-toc="True"></v-md-preview>
        </v-col>
      </v-row>
    </v-col>
    <v-btn
      color="light-blue"
      dark
      @click="publish"
      class="mr-2"
      :disabled="isDisabled"
    >
      <v-icon left>mdi-send</v-icon> 发布
    </v-btn>
    <v-btn
      color="gray"
      dark
      @click="back"
      :disabled="loading"
    >
      <v-icon left>mdi-backspace</v-icon> 取消
    </v-btn>
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
  data: () => ({
    loading: true,
    title: null,
    cost: 0,
    tags: [],
    tags_to_select: [],
    content: "Input your description here. We support **Markdown format**.",
    link: null,
    rules: {
      // 必填校验
      required: v => !!v || '链接不能为空',
      // 链接格式校验
      isValidUrl: v => {
        const urlPattern = new RegExp(
          "^(https?:\\/\\/)?" + // 支持 http 和 https
          "((([a-zA-Z\\d]([a-zA-Z\\d-]*[a-zA-Z\\d])*)\\.)+[a-zA-Z]{2,}|" + // 域名
          "((\\d{1,3}\\.){3}\\d{1,3}))" + // 或 IP 地址
          "(\\:\\d+)?(\\/[-a-zA-Z\\d%_.~+&]*)*" + // 端口和路径
          "(\\?[;&a-zA-Z\\d%_.~+=-]*)?" + // 查询参数
          "(\\#[-a-zA-Z\\d%_.~+=&]*)?$", // 锚点
          "i" // 忽略大小写
        );
        return urlPattern.test(v) || '链接格式不正确';
      },
    },
  }),
  components: {
    VMdPreview
  },
  computed: {
    labelText() {
      // 如果链接格式正确，则显示合法的提示
      if (this.rules.isValidUrl(this.link) === true) {
        return '您上传的链接是合法的';
      }
      return '请上传资源的链接';
    },
    isDisabled() {
      return this.loading ||
        this.title === null ||
        this.cost < 0 ||
        this.content === null ||
        this.link === null ||
        this.rules.isValidUrl(this.link) !== true;
    },
  },
  methods: {
    remove (item) {
      const index = this.tags.indexOf(item.name)
      if (index >= 0) this.tags.splice(index, 1)
    },
    publish() {
      if (this.title === null || this.cost < 0 || this.content === null || this.link === null) {
        this.$store.commit("setAlert", {
          type: "error",
          message: "请填写完整信息！",
        });
        return;
      } else if (this.rules.isValidUrl(this.link) !== true) {
        this.$store.commit("setAlert", {
          type: "error",
          message: "请填写正确的链接！",
        });
        return;
      }
      this.loading = true;
      this.$store.dispatch("createPost", {
        title: this.title,
        cost: this.cost,
        tags: this.tags,
        content: this.content,
        link: this.link,
      })
        .then(() => {
          this.$store.commit("setShares", this.$store.state._shares_ + 1);
          this.$store.commit("setAlert", {
            type: "success",
            message: "发布成功！",
          });
          this.$router.push('/resources');
        })
        .catch((e) => {
          this.$store.commit("setAlert", {
            type: "error",
            message: e,
          });
        })
      this.loading = false;
    },
    back() {
      this.$router.push('/resources');
    }
  },
  mounted() {
    this.$store.dispatch("getTags", {key_word: null})
      .then((res) => {
        this.tags_to_select = res.tags.map((tag) => {
          return {
            name: tag,
          };
        });
      })
      .catch((e) => {
        this.tags_to_select = [];
        this.$store.commit("setAlert", {
          type: "error",
          message: e,
        });
      })
      .finally(() => {
        this.loading = false;
      });
    this.$store.commit("setAppTitle", "分享资源");
  },
}
</script>