<template>
  <loading v-if="loading" />
  <v-container style="max-width: 45%; margin-top: 40px;"  v-else>
    <v-card class="card pa-4">
      <v-row>
        <v-col cols="12">
          <h3>用户基本信息</h3>
        </v-col>
        <v-col style="padding: 0;" cols="12">
          <v-divider></v-divider>
        </v-col>
        <v-col cols="8">
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title>
                <v-icon left>mdi-card-account-details</v-icon>
                用户名
              </v-list-item-title>
              <v-list-item-subtitle style="margin-left:9.2%;">
                {{ this.username }}
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title>
                <v-icon left>mdi-google-classroom</v-icon>
                身份
              </v-list-item-title>
              <v-list-item-subtitle style="margin-left:9.2%;">
                {{ this.userrole == 1 ? '管理员' : '普通用户' }}
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title>
                <v-icon left>mdi-email-multiple-outline</v-icon>
                电子邮件地址
              </v-list-item-title>
              <v-list-item-subtitle style="margin-left:9.2%;">{{ email }}</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title>
                <v-icon left>mdi-invoice-text-send-outline</v-icon>
                个性标签
              </v-list-item-title>
              <v-list-item-subtitle style="margin-left:9.2%;">{{ personalityTag }}</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-col>
        <v-col cols="4" style="margin-top: 20px;">
          <div style="text-align: center;">
            <v-avatar
              size="150"
              rounded="true"
            >
              <v-img
                :key="avatarUrl"
                :src="avatarUrl"
              />
            </v-avatar>
            <div class="mt-2">
              <v-btn text color="primary" @click="onSelectNewAvatar" v-if="this.user_id == $store.state._user_id_">
                选择新头像
              </v-btn>
              <!-- 隐藏的文件输入框 -->
              <input
                ref="fileInput"
                type="file"
                accept="image/*"
                style="display: none;"
                @change="onFileSelected"
              />
            </div>
            <div class="mt-2">
              <v-btn text color="error" outlined @click="toggleFollow($route.params.id)" v-if="follow">
                取消关注
              </v-btn>
              <v-btn text color="success" outlined @click="toggleFollow($route.params.id)" v-else>
                关注用户
              </v-btn>
            </div>
          </div>
        </v-col>
        <v-col style="padding: 0;" cols="12" v-if="this.user_id == $store.state._user_id_">
          <v-divider></v-divider>
        </v-col>
        <v-col style="padding: 0.1px;" class="text-right" v-if="this.user_id == $store.state._user_id_">
          <v-btn text color="red" @click="showPasswordDialog">修改密码</v-btn>
          <v-btn text color="red" @click="showEmailDialog">修改电子邮件地址</v-btn>
          <v-btn text color="red" @click="showTagDialog">修改个性标签</v-btn>
          <v-btn text color="red" @click="logout">退出登录</v-btn>
        </v-col>
      </v-row>
    </v-card>
    <v-card class="pa-4">
      <v-row>
        <v-col cols="12">
          <h3>用户数据统计</h3>
        </v-col>
        <v-col style="padding: 0;" cols="12">
          <v-divider></v-divider>
        </v-col>
        <v-col cols="12" class="one_col">
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title>
                <v-icon left>mdi-bootstrap</v-icon>
                菜币数量 &nbsp;&nbsp; {{moneyNumber}}  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                <v-chip color="yellow" label small class="me-1" @click="showGiveMeMoneyDialog = true" v-if="this.user_id == $store.state._user_id_">
                  去充值
                </v-chip>
              </v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-col>
        <!-- 左侧列 -->
        <v-col cols="6">
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title>
                <v-icon left>mdi-thumb-up-outline</v-icon>
                获赞数量
              </v-list-item-title>
              <v-list-item-title style="margin-left:13%;">{{likeNumber}}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title>
                <v-icon left>mdi-human-male-board-poll</v-icon>
                粉丝数量
              </v-list-item-title>
              <v-list-item-title style="margin-left:13%;">{{fansNumber}}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-col>
        <!-- 右侧列 -->
        <v-col cols="6">
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title>
                <v-icon left>mdi-invoice-text-multiple-outline</v-icon>
                分享数量
              </v-list-item-title>
              <v-list-item-title style="margin-left:13%;">{{postNumber}}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title>
                <v-icon left>mdi-google-assistant</v-icon>
                回答数量
              </v-list-item-title>
              <v-list-item-title style="margin-left:13%;">{{answerNumber}}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-col>
      </v-row>
    </v-card>
    <!-- 修改个性标签对话框 -->
    <v-dialog v-model="tagDialog" max-width="500px">
      <v-card>
        <v-card-title>
          <span class="headline">修改个性标签</span>
        </v-card-title>
        <v-card-text>
          <v-text-field v-model="newPersonalityTag" label="个性标签"></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-btn color="green darken-1" text @click="updatePersonalityTag">确认</v-btn>
          <v-btn color="grey" text @click="tagDialog = false">取消</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- 修改密码对话框 -->
    <v-dialog v-model="passwordDialog" max-width="500px">
      <v-card>
        <v-card-title>
          <span class="headline">修改密码</span>
        </v-card-title>
        <v-card-text>
          <v-text-field v-model="newPassword" label="新密码" type="password"></v-text-field>
          <v-text-field v-model="confirmPassword" label="确认密码" type="password"></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-btn color="green darken-1" text @click="updatePassword">确认</v-btn>
          <v-btn color="grey" text @click="passwordDialog = false">取消</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- 修改电子邮件对话框 -->
    <v-dialog v-model="emailDialog" max-width="500px">
      <v-card>
        <v-card-title>
          <span class="headline">修改电子邮件地址</span>
        </v-card-title>
        <v-card-text>
          <v-text-field v-model="newEmail" label="新电子邮件地址"></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-btn color="green darken-1" text @click="updateEmail">确认</v-btn>
          <v-btn color="grey" text @click="emailDialog = false">取消</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="showGiveMeMoneyDialog" max-width="400">
      <v-card>
        <v-card-title>
          <span class="headline">充值提示</span>
        </v-card-title>
        <v-card-text>
          你确定要进行充值吗？
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue" text @click="showGiveMeMoneyDialog = false">取消</v-btn>
          <v-btn color="blue" text @click="confirmRecharge">确认</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import Loading from '../Loading.vue';
export default {
  name: "UserCenter",
  components: {
    Loading,
  },
  data() {
    return {
      user_id: this.$route.params.id,
      loading: true,
      tagDialog: false,
      passwordDialog: false,
      emailDialog: false,
      newPersonalityTag: '',
      newPassword: '',
      confirmPassword: '',
      newEmail: '',
      personalityTag: '',
      email: '',
      showGiveMeMoneyDialog: false,
      moneyNumber: 0,
      likeNumber: 0,
      fansNumber: 0,
      postNumber: 0,
      answerNumber: 0,
      username:"",
      userrole: 0,
      avatarUrl: "", // 当前头像路径
      follow: false,
    };
  },
  mounted() {
      this.$store.commit("setAppTitle", "用户信息");
      this.$store.dispatch("getUserProfile", {id: this.$route.params.id})
        .then((res) => {
          this.username = res.username;
          this.userrole = res.role;
          this.personalityTag = res.signature;
          if (!this.personalityTag) this.personalityTag = "这个人很懒，什么也没有写。";
          this.email = res.email;
          if (!this.email) this.email = "未设置";
          this.moneyNumber = res.capital;
          this.likeNumber = res.likes;
          this.fansNumber = res.fans;
          this.postNumber = res.posts;
          this.answerNumber = res.replies;
          this.avatarUrl = res.avatarurl;
          this.loading = false;
        })
        .catch((err) => { this.$store.commit("setAlert", {type: "error", message: err}); });
      this.$store.dispatch("getFollows", { id: this.$store.state._user_id_ })
        .then((res) => {
          if (res.users.find((user) => user.id == this.$route.params.id)) {
            this.follow = true;
          }
        })
        .catch((err) => {
          this.$store.commit("setAlert", {
            type: "error",
            message: err,
          });
        });
  },
  methods: {
    toggleFollow(id) {
      if (this.follow == false) {
        this.follow = true;
        this.$store.dispatch("followUser", {id: id })
          .then((res) => {
            this.$store.commit("setAlert", { "type": "success", "message": "已关注。" });
            this.$store.commit("setFollows", this.$store.state._follows_ + 1);
          })
          .catch((err) => { this.$store.commit("setAlert", { "type": "error", "message": err }); })
      } else {
        this.follow = false;
        this.$store.dispatch("notFollowUser", {id: id })
          .then((res) => {
            this.$store.commit("setAlert", { "type": "success", "message": "已取关。" });
            this.$store.commit("setFollows", this.$store.state._follows_ - 1);
          })
          .catch((err) => { this.$store.commit("setAlert", { "type": "error", "message": err }); })
      }
    },
    showTagDialog() {
      this.newPersonalityTag = this.personalityTag;
      this.tagDialog = true;
    },
    updatePersonalityTag() {
      this.$store.dispatch("modifyUser", {id:this.$store.state._user_id_, password: null, email: null, signature: this.newPersonalityTag})
        .then(() => {
          this.$store.commit("setAlert", {type: "success", message: "签名修改成功。"});
          this.personalityTag = this.newPersonalityTag;
          this.tagDialog = false;
        })
        .catch((err) => { this.$store.commit("setAlert", {type: "error", message: err}); })
    },
    showPasswordDialog() {
      this.newPassword = '';
      this.confirmPassword = '';
      this.passwordDialog = true;
    },
    updatePassword() {
      if (this.newPassword === this.confirmPassword) {
        this.$store.dispatch("modifyUser", {id:this.$store.state._user_id_, password: this.newPassword, email: null, signature: null})
          .then(() => {
            this.newPassword = "";
            this.confirmPassword = "";
            this.$store.commit("setAlert", {type: "success", message: "密码修改成功。"});
          })
          .catch((err) => { this.$store.commit("setAlert", {type: "error", message: err}); })
        this.passwordDialog = false;
      } else {
        this.$store.commit("setAlert", {type: "error", message: "两次输入的密码不一致。"});
      }
    },
    showEmailDialog() {
      this.newEmail = this.email;
      this.emailDialog = true;
    },
    updateEmail() {
      this.$store.dispatch("modifyUser", {id:this.$store.state._user_id_, password: null, email: this.newEmail, signature: null})
        .then(() => {
          this.email = this.newEmail;
          this.$store.commit("setAlert", {type: "success", message: "邮箱修改成功。"});
          this.emailDialog = false;
        })
        .catch((err) => { this.$store.commit("setAlert", {type: "error", message: err}); })
    },
    confirmRecharge() {
      // 在此处添加充值逻辑
      this.showGiveMeMoneyDialog = false;
      alert('警惕虚拟货币的非法交易！！！'); // 弹出提示
      window.location.href = 'https://www.cac.gov.cn/2020-06/07/c_1593081473364231.htm'; // 替换为你的目标网址
    },
    // 点击按钮，触发文件选择器打开
    onSelectNewAvatar() {
      this.$refs.fileInput.click();
    },
    logout() {
      this.$store.commit("clearPersonalInfo");
      this.$router.push("/auth");
    },
    // 文件选择完成后处理
    onFileSelected(event) {
      const file = event.target.files[0];
      if (!file) return;
      if (!file.type.startsWith("image/")) {
        this.$emit("error", "请选择图片文件");
        return;
      }
      this.$store.dispatch("uploadFile", {file: file})
        .then((res) => {
          this.$store.commit("setAlert", {type: "success", message: "头像上传成功。"});
          this.avatarUrl = res.file_url;
          this.$store.commit("setAvatar", res.file_url);
        })
        .catch((err) => { this.$store.commit("setAlert", {type: "error", message: err}); });
    },
  },
};
</script>

<style scoped>
  .card {
    margin-bottom: 35px;
  }
  .one_col {
    padding-bottom: 0%;
    margin-bottom: -1%;
  }
  h3 {
    font-weight: bold;
  }
</style>
