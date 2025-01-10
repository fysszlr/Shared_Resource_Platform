<template>
  <div>
    <loading v-if="loading" />
    <v-container v-else>
      <!-- 帖子标题部分 -->
      <v-card class="mt-5 pa-5">
        <v-card-title class="d-flex align-center">
          <v-avatar size="40" style="margin-left:-20px;">
              <img :src="post.created_by.avatar" alt="Author" />
          </v-avatar>
          <span class="title font-weight-bold">{{ post.title }}</span>
          <v-chip
            v-for="(tag, index) in post.tags"
            :key="index"
            class="ml-1"
            color="green"
            dark
            small>
            {{ tag }}
          </v-chip>
        </v-card-title>
        <a :href="`/center/${post.created_by.user_id}`" @click.stop class="ml-2" style="font-size: 16px;" target="blank">{{ post.created_by.username }}</a>
        <span class="grey--text text--darken-1" style="font-size:14px;"> 发表于 {{ format(post.created_at, 'yyyy-MM-dd HH:mm:ss') }}</span>
        <v-divider></v-divider>
        <!-- 帖子内容部分 -->
        <v-card-text>
          <v-md-preview :text="post.content == null ? '' : post.content"></v-md-preview>
        </v-card-text>
        <!-- 按钮操作 -->
        <v-card-actions class="d-flex justify-space-between flex-wrap">
          <!-- 点赞、点踩、收藏 -->
          <div class="d-flex">
            <v-btn text @click="toggleLike" :disabled="post.dislike">
              <v-icon :color="post.like ? 'red lighten-1' : 'gray'">mdi-thumb-up</v-icon>
            </v-btn>
            <v-btn text @click="toggleDisLike" :disabled="post.like">
              <v-icon :color="post.dislike ? 'red lighten-1' : 'gray'">mdi-thumb-down</v-icon>
            </v-btn>
            <v-btn text @click="togglefavorite">
              <v-icon :color="post.favorite ? 'red lighten-1' : 'gray'">mdi-heart-box</v-icon>
            </v-btn>
          </div>
          <!-- 操作按钮 -->
          <div class="d-flex" style="gap: 16px;">
            <v-btn
              color="green"
              outlined
              @click="openModifyDialog"
              v-if="$store.state._role_ == 'Administrator' || post.created_by.user_id == $store.state._user_id_"
            >
              编辑
            </v-btn>
            <v-btn color="red" outlined @click="openBhpan">
              下载资源
            </v-btn>
            <v-btn color="blue" outlined @click="toggleFollow">
              {{ followed ? '取消关注' : '关注作者' }}
            </v-btn>
          </div>
        </v-card-actions>
      </v-card>
      <!-- 回答部分 -->
      <v-card class="mt-5 pa-5">
        <v-card-title>{{ comments && comments.length ? comments.length : 0 }} 条评论</v-card-title>
        <v-card flat>
          <!-- 输入框 -->
          <v-card-text class="pa-0">
            <v-textarea
              v-model="newComment"
              outlined
              rows="1"
              label="写下您的评论..."
              color="primary"
              hide-details
            />
            <div class="d-flex justify-end pt-1 pb-1" v-if="newComment != ''">
              <v-btn outlined color="green" @click="submitComment">
                <v-icon left>mdi-send</v-icon>
                提交
              </v-btn>
            </div>
          </v-card-text>
        </v-card>
        <v-divider></v-divider>
        <div v-for="(comment, index) in comments" :key="index">
          <v-card class="pa-2 my-3"  flat>
            <!-- 用户信息 -->
            <v-card-title class="d-flex align-center">
              <v-avatar size="30" class="mr-2">
                <img :src="comment.created_by.avatar" alt="User" />
              </v-avatar>
              <a :href="`/center/${comment.created_by.user_id}`" @click.stop class="mr-2" style="font-size: 16px;" target="blank">{{ comment.created_by.username }}</a>
              <span class="grey--text" style="font-size: 12px;"> 发表于 {{ format(comment.created_at, 'yyyy-MM-dd HH:mm:ss') }} </span>
            </v-card-title>
            <!-- 评论内容 -->
            <v-card-text>
              <p style="font-size: 1rem;">{{ comment.content }}</p>
            </v-card-text>
          </v-card>
        </div>
      </v-card>
    </v-container>
    <v-dialog
      v-model="modifyDialog"
      fullscreen
      hide-overlay
      transition="dialog-bottom-transition"
    >
      <v-card>
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
          <v-toolbar-title>编辑帖子</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-toolbar-items>
            <v-btn
              dark
              text
              @click="savePost"
            >
              保存
            </v-btn>
          </v-toolbar-items>
        </v-toolbar>
        <v-card-text class="mt-4">
          <v-col>
            <v-row>
              <v-col>
                <v-text-field
                  v-model="newPost.title"
                  label="标题"
                  :rules="[v => !!v || '标题不能为空']"
                  aria-required=""
                ></v-text-field>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="6">
                <v-text-field
                  v-model="newPost.cost"
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
                  v-model="newPost.tags"
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
                <v-text-field
                  v-model="newPost.bhpan_url"
                  :label="labelText"
                  :rules="[rules.required, rules.isValidUrl]"
                  aria-required=""
                ></v-text-field>
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-textarea
                  v-model="newPost.content"
                  label="描述"
                  rows="16"
                ></v-textarea>
              </v-col>
              <v-col>
                <v-md-preview :text="newPost.content" default-show-toc="True"></v-md-preview>
              </v-col>
            </v-row>
          </v-col>
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>
<script>
import Loading from '../Loading.vue';
import VMdPreview from '@kangc/v-md-editor/lib/preview';
import '@kangc/v-md-editor/lib/style/preview.css';
import githubTheme from '@kangc/v-md-editor/lib/theme/github.js';
import '@kangc/v-md-editor/lib/theme/style/github.css';
import hljs from 'highlight.js';
import { format } from 'date-fns';
VMdPreview.use(githubTheme, {
  Hljs: hljs,
});
export default {
  name: "PostPage",
  components: {
    VMdPreview,
    format,
    Loading,
  },
  data() {
    return {
      newPost: {
        title: "",
        cost: 0,
        content: "",
        bhpan_url: "",
        tags: [],
      },
      loading: true,
      post: {
        title: "",
        cost: 0,
        content: "",
        bhpan_url: "",
        tags: [],
      },
      followed: false,
      dialog: false, // 控制弹框显示
      newComment: "", // 用户输入的评论
      comments: [],
      modifyDialog: false, // 控制修改弹框显示
      tags_to_select: [],
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
    };
  },
  computed: {
    labelText() {
      // 如果链接格式正确，则显示合法的提示
      if (this.rules.isValidUrl(this.newPost.bhpan_url) === true) {
        return '您上传的链接是合法的';
      }
      return '请上传资源的链接';
    },
    isDisabled() {
      return this.loading ||
        this.title === null ||
        this.cost < 0 ||
        this.content === null ||
        this.newPost.bhpan_url === null ||
        this.rules.isValidUrl(this.newPost.bhpan_url) !== true;
    },
  },
  watch: {
    modifyDialog: {
      handler: function (val) {
        if (val === true && this.tags_to_select.length === 0) {
          this.$store.dispatch("getTags", {key_word: ""})
            .then((res) => {
              this.tags_to_select = res.tags.map((tag) => { return { name: tag }; });
            })
            .catch((err) => { this.$store.commit("setAlert", { "type": "error", "message": err }); })
        }
      },
    },
  },
  methods: {
    format,
    openModifyDialog() {
      this.newPost = JSON.parse(JSON.stringify(this.post));
      this.modifyDialog = true;
    },
    savePost() {
      this.newPost.id = this.$route.params.id;
      this.$store.dispatch("modifyPost", this.newPost)
        .then((res) => {
          this.$store.commit("setAlert", { "type": "success", "message": "帖子已更新。" });
          this.post = JSON.parse(JSON.stringify(this.newPost));
          this.modifyDialog = false;
        })
        .catch((err) => { this.$store.commit("setAlert", { "type": "error", "message": err }); })
    },
    removeTag (item) {
      const index = this.newPost.tags.indexOf(item.name)
      if (index >= 0) this.newPost.tags.splice(index, 1)
    },
    getPost() {
      this.loading = true;
      this.$store.dispatch("getPost", { id: this.$route.params.id })
        .then((res) => {
          this.post = res;
          this.$store.dispatch("getPostComments", { id: this.$route.params.id })
            .then((res) => {
              this.comments = res.comments;
              this.loading = false;
            })
            .catch((err) => { this.$store.commit("setAlert", { "type": "error", "message": err }); })
          this.$store.dispatch("getFollows", { id: this.$store.state._user_id_ })
            .then((res) => {
              if (res.users.map((user) => user.id).includes(this.post.created_by.user_id)) {
                this.followed = true;
              }
            })
            .catch((err) => { this.$store.commit("setAlert", { "type": "error", "message": err }); })
        })
        .catch((err) => { this.$store.commit("setAlert", { "type": "error", "message": err }); })
    },
    openBhpan() {
      window.open(this.post.bhpan_url);
    },
    toggleLike() {
      if (this.post.like == false) {
        this.post.like = true;
        this.$store.dispatch("likePost", {id: this.$route.params.id })
          .then((res) => { this.$store.commit("setAlert", { "type": "success", "message": "已点赞。" }); })
          .catch((err) => { this.$store.commit("setAlert", { "type": "error", "message": err }); })
        if (this.post.dislike == true) {
          this.post.dislike = false;
          this.$store.dispatch("notLikePost", {id: this.$route.params.id })
            .then((res) => {})
            .catch((err) => { this.$store.commit("setAlert", { "type": "error", "message": err }); })
        }
      } else {
        this.post.like = false;
        this.$store.dispatch("notLikePost", {id: this.$route.params.id })
          .then((res) => {})
          .catch((err) => { this.$store.commit("setAlert", { "type": "error", "message": err }); })
      }
    },
    toggleDisLike() {
      if (this.post.dislike == false) {
        this.post.dislike = true;
        this.$store.dispatch("dislikePost", {id: this.$route.params.id })
          .then((res) => { this.$store.commit("setAlert", { "type": "success", "message": "已点踩。" }); })
          .catch((err) => { this.$store.commit("setAlert", { "type": "error", "message": err }); })
        if (this.post.like == true) {
          this.post.like = false;
          this.$store.dispatch("notDislikePost", {id: this.$route.params.id })
            .then((res) => {})
            .catch((err) => { this.$store.commit("setAlert", { "type": "error", "message": err }); })
        }
      } else {
        this.post.dislike = false;
        this.$store.dispatch("notDislikePost", {id: this.$route.params.id })
          .then((res) => {})
          .catch((err) => { this.$store.commit("setAlert", { "type": "error", "message": err }); })
      }
    },
    togglefavorite() {
      if (this.post.favorite == true) {
        this.post.favorite = false;
        this.$store.dispatch("notFavourPost", {id: this.$route.params.id })
          .then((res) => {
            this.$store.commit("setAlert", { "type": "success", "message": "已取消收藏。" });
            this.$store.commit("setFavorites", this.$store.state._favorites_ - 1);
          })
          .catch((err) => { this.$store.commit("setAlert", { "type": "error", "message": err }); })
      } else {
        this.post.favorite = true;
        this.$store.dispatch("favourPost", {id: this.$route.params.id })
          .then((res) => {
            this.$store.commit("setAlert", { "type": "success", "message": "已收藏。" });
            this.$store.commit("setFavorites", this.$store.state._favorites_ + 1);
          })
          .catch((err) => { this.$store.commit("setAlert", { "type": "error", "message": err }); })
      }
    },
    toggleFollow() {
      if (this.followed == false) {
        this.followed = true;
        this.$store.dispatch("followUser", {id: this.post.created_by.user_id })
          .then((res) => {
            this.$store.commit("setAlert", { "type": "success", "message": "已关注。" });
            this.$store.commit("setFollows", this.$store.state._follows_ + 1);
          })
          .catch((err) => { this.$store.commit("setAlert", { "type": "error", "message": err }); })
      } else {
        this.followed = false;
        this.$store.dispatch("notFollowUser", {id: this.post.created_by.user_id })
          .then((res) => {
            this.$store.commit("setAlert", { "type": "success", "message": "已取关。" });
            this.$store.commit("setFollows", this.$store.state._follows_ - 1);
          })
          .catch((err) => { this.$store.commit("setAlert", { "type": "error", "message": err }); })
      }
    },
    openCommentDialog() {
      this.dialog = true;
      this.newComment = ""; // 初始化评论输入框
    },
    submitComment() {
      // 处理评论提交逻辑
      if (this.newComment.trim() !== "") {
        this.dialog = false;
        this.$store.dispatch("createComment", { id: this.$route.params.id, content: this.newComment, parent_id: 0 })
          .then((res) => { 
            this.$store.commit("setAlert", { "type": "success", "message": "评论成功。" }); 
            this.newComment = ""; // 清空评论输入框
            this.getPost();
          })
          .catch((err) => { this.$store.commit("setAlert", { "type": "error", "message": err }); })
        this.$store.dispatch("getPostComments", { id: this.$route.params.id })
          .then((res) => { this.comments = res.comments; })
          .catch((err) => { this.$store.commit("setAlert", { "type": "error", "message": err }); })
      } else {
        this.$store.commit("setAlert", { "type": "error", "message": "评论不可以为空。" });
      }
    },
  },
  mounted() {
    this.getPost();
  },
};
</script>

<style scoped>
  .title {
    font-size: 24px;
    margin-left:10px;
  }
  .v-code {
    font-family: 'Courier New', monospace;
    padding: 10px;
    border-radius: 5px;
    font-size: 14px;
    color: #333;
  }
</style>