<template>
  <v-card flat class="back">
    <v-progress-linear :indeterminate="true" v-show="loading" id="loginPanelProgressBar" color="success" />
    <v-card class="white-card">
      <div class="ma-6">
        <h2 class="mb-4">
          <new-friend v-if="showRegister" />
          <welcome-back v-else />
          <img src="@/assets/images/logo.png" alt="our logo" class="welcome-image" style="float: right">
        </h2>
        <v-subheader id="loginPanelSubheader" style="margin-bottom: 10px">
          <template v-if="loading">
            <span v-if="showRegister">正在联系远程服务器</span>
            <span v-else>正在验证你的身份</span>
          </template>
          <span v-else>
            <span v-if="showRegister">
              填写下列信息，获得属于您的账号。
            </span>
            <span v-else>要继续访问，请使用你的账号登录。</span>
          </span>
        </v-subheader>
        <v-form v-if="showRegister" class="loginPanelForm" @submit.prevent="handleRegister">
          <v-text-field class="dense" outlined label="用户名" :rules="[v => !!v || '必填']" autofocus required
            prepend-inner-icon="mdi-account-box" v-model="username" :disabled="loading" />
          <v-text-field class="dense" outlined label="密码" :rules="[
            v => !!v || '',
            v => v.length > 3 || '至少3字符',
            v => v.length < 21 || '至多20字符',
            v => {
              const pattern = /^.*[0-9].*$/;
              const pattern_w = /^.*[a-zA-Z].*$/;
              return (pattern.test(v) && pattern_w.test(v)) || '必须包含数字和字母';
            }
          ]" type="password" prepend-inner-icon="mdi-fingerprint" required v-model="password" :disabled="loading" />
          <div class="d-flex">
            <v-checkbox class="dense" v-model="robot" label="我是机器人" color="primary" @change="checkIfIsRobot"
              :disabled="loading" />
            <v-spacer />
          </div>
          <v-btn block depressed color="primary" type="submit" :disabled="loading">
            注册
          </v-btn>
        </v-form>
        <v-form v-else class="loginPanelForm" @submit.prevent="handleLogin">
          <v-text-field class="dense" outlined label="用户名" type="text" prepend-inner-icon="mdi-account-box"
            :rules="[v => !!v || '']" v-model="username" required :disabled="loading" />
          <v-text-field class="dense" outlined label="密码" type="password" prepend-inner-icon="mdi-fingerprint"
            :rules="[v => !!v || '']" required v-model="password" :disabled="loading" />
          <div class="d-flex">
            <v-checkbox class="dense" v-model="remember" label="在这台设备上记住我" color="primary"
              @change="warnAboutRememberingLogin" :disabled="loading" />
            <v-spacer />
          </div>
          <v-btn depressed block color="primary" type="submit" :disabled="loading">
            登录
          </v-btn>
        </v-form>
        <v-btn block depressed @click.stop="switchRegisterPage" :disabled="loading" class="mt-2 buttonyt">
          {{ this.showRegister ? '已有账号？登录' : '没有账号？注册' }}
        </v-btn>
      </div>
    </v-card>
  </v-card>
</template>

<script>
import WelcomeBack from "../../components/Auth/WelcomeBack.vue";
import NewFriend from "../../components/Auth/NewFriend.vue";

export default {
  name: "AuthPanel",
  components: { WelcomeBack, NewFriend },
  data() {
    return {
      username: "",
      password: "",
      remember: false,
      showRegister: false,
      loading: false,
      robot: true,
    };
  },
  methods: {
    handleLogin() {
      this.loading = true;
      if (!this.username || !this.password) {
        this.$store.commit("setAlert", {
          type: "error",
          message: "请填写用户名和密码。",
        });
        return;
      }
      this.$store.dispatch("login", {
        username: this.username,
        password: this.password,
        remember: this.remember,
      })
        .then(() => {
          this.$store.commit("getUserName");
          this.$store.commit("setAlert", {
            type: "success",
            message: "欢迎回来，" + this.$store.getters.username + "。",
          });
          this.$router.push("/");
        })
        .catch((e) => {
          this.$store.commit("setAlert", {
            type: "error",
            message: e,
          });
        })
        .finally(() => { this.loading = false; });
    },
    async handleRegister() {
      if (!this.username || !this.password) {
        this.$store.commit("setAlert", {
          type: "error",
          message: "请填写用户名和密码。",
        });
        return;
      }
      if (this.robot) {
        this.$store.commit("setAlert", {
          type: "error",
          message: "拒绝机器人注册，从我做起。",
        });
        return;
      }
      this.loading = true;
      this.$store.dispatch("register", {username: this.username, password: this.password})
        .then(() => {
          this.$store.commit("setAlert", {
            type: "success",
            message: "注册成功，欢迎你！",
          });
          this.username = "";
          this.password = "";
          this.switchRegisterPage();
        })
        .catch((e) => {})
        .finally(() => { this.loading = false; });
    },
    switchRegisterPage() {
      this.showRegister = !this.showRegister;
    },
    warnAboutRememberingLogin() {
      if (this.remember) {
        this.$store.commit("setAlert", {
          type: "warning",
          message: "请不要在公共设备上勾选此选项。",
        });
      }
    },
    checkIfIsRobot() {
      if (!this.robot) {
        this.$store.commit("setAlert", {
          type: "warning",
          message: "你最好不是。",
        });
      }
    },
  },
};
</script>

<style scoped lang="scss">
.back {
  background-image: url('@/assets/images/back.png');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

.dense {
  margin: -5px 0 -10px 0 !important;
}

.topmost {
  z-index: 1001;
}
.v-card {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

#loginPanelProgressBar {
  position: absolute;
  top: -30px;
  margin: 0 0 0 0;
}

.white-card {
  width: 17%; /* 确保与外层卡片同宽 */
  min-width: 300px;
  max-height: fit-content;
  height: 50%;
  min-height: 450px;
  max-width: fit-content;
  position: relative;
  z-index: 2;
  opacity: 0.87; /* 增加透明度 */
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3); /* 增大阴影效果 */
  backdrop-filter: blur(10px);
  border-radius: 12px; /* 增加圆角效果 */
  overflow: hidden; /* 确保内容不溢出 */
}

.loginPanelForm {
  width: 100%;
  z-index: 2;
  position: relative;
}

.buttonyt {
  z-index: 2;
  position: relative;
}

#welcomePanelSubheader {
  clear: both;
  padding-bottom: 20px;
  padding-left: 0;
}

.welcome-image {
  vertical-align: middle;
  width: 70px;
}
</style>
